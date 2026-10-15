"""ทดสอบเส้นทางรั่วและพฤติกรรม HMDA ที่มีผลต่อข้อสรุป"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from config import Config
from fairgroups.hmda import (LeakageGuard,HMDAPreprocessor,POST,FEATURES,prohibited,
                             demographics,split_hmda,dti_numeric)
from fairgroups.hmda_groups import ClassClusters,fit_hbac
from fairgroups.run import choose_jtt,oof_errors
from fairgroups.models import predict_mlp
from fairgroups.metrics import evaluate

ROOT=Path(__file__).resolve().parents[1]


def test_all_post_decision_and_sensitive_features_rejected():
    y=np.tile([0,1],40)
    cols=FEATURES+list(POST)+['denial_reason-1','tract_minority_population_percent',
        'applicant_race-1','co-applicant_ethnicity-1','applicant_sex_observed',
        'applicant_age_above_62','derived_race','derived_ethnicity','derived_sex']
    x=pd.DataFrame({c:np.ones(80) for c in cols})
    guard=LeakageGuard().fit(x,y)
    assert set(guard.features_)==set(FEATURES)
    assert all(not prohibited(c) for c in guard.features_)
    for c in cols:
        if prohibited(c):
            with pytest.raises(AssertionError): HMDAPreprocessor().fit(pd.DataFrame({c:np.ones(80)}))


def test_missing_gap_train_only_and_dti_order():
    y=np.tile([0,1],40)
    x=pd.DataFrame({'loan_amount':np.arange(80,dtype=float),'income':np.where(y==0,'Exempt','40')})
    guard=LeakageGuard().fit(x,y)
    assert guard.features_==['loan_amount']
    assert next(r for r in guard.audit_ if r['column']=='income')['missing_gap']==1
    before=guard.features_.copy();guard.transform(x.assign(income='99',loan_amount=np.nan))
    assert guard.features_==before
    np.testing.assert_array_equal(dti_numeric(pd.Series(['<20%','20%-<30%','30%-<36%','36','50%-60%','>60%'])),[10,25,33,36,55,65])


def test_unknown_retained_but_excluded_from_fairness():
    frame=pd.DataFrame({'derived_race':['White','Race Not Available','Race Not Available','Black or African American'],
                         'derived_ethnicity':['Not Hispanic or Latino','Hispanic or Latino','Ethnicity Not Available','Not Hispanic or Latino'],
                         'derived_sex':['Male','Female','Sex Not Available','Joint'],'applicant_age':['35-44','<25','8888','>74']})
    s=demographics(frame)
    assert s.race_eth.tolist()==['NH White','Hispanic','Unknown','NH Black']
    assert len(s)==4
    m=evaluate(np.array([1,0,0,1]),np.array([.9,.1,.8,.8]),s,min_detail=1)
    assert m['excluded_unknown_race_eth']==1 and m['excluded_unknown_sex']==1
    assert 'Unknown' not in json.loads(m['group_accuracy_intersection'])


def test_hmda_unsupervised_fits_never_include_holdout():
    rng=np.random.default_rng(17);n=160
    frame=pd.DataFrame({'loan_amount':rng.normal(size=n),'income':rng.normal(size=n),'lei':np.tile(['a','b','c','d'],40)},index=np.arange(500,500+n))
    y=np.tile([0,1],80)
    s=pd.DataFrame({'race_eth':np.tile(['NH White','NH Black'],80),'sex':'Male','age':'35-44','intersection':np.tile(['a','b'],80)},index=frame.index)
    splits=split_hmda(frame,y,s,17)
    tr=splits['train'];guard=LeakageGuard().fit(tr['frame'],tr['y']);tr['x']=guard.transform(tr['frame'])
    pre=HMDAPreprocessor(2,lei_top_n=1).fit(tr['x']);x=pre.transform(tr['x'])
    km=ClassClusters().fit(x,tr['y'],tr['ids'],2,17)
    saved=km.centers_.copy();pre.transform(guard.transform(splits['test']['frame'].assign(income=99999)))
    km.predict(x*100);np.testing.assert_array_equal(km.centers_,saved)
    for obj in [guard,pre,km]:
        assert set(obj.fit_ids_)==set(tr['ids'])
        assert set(obj.fit_ids_).isdisjoint(np.r_[splits['test']['ids'],splits['val']['ids']])
    error,audit=oof_errors(tr,Config(oof_folds=2,trees=3),17)
    held=[]
    for f in audit['folds']:
        assert set(f['fit_ids']).isdisjoint(f['heldout_ids'])
        assert set(f['guard_fit_ids'])==set(f['preprocessor_fit_ids'])==set(f['fit_ids'])
        held.extend(f['heldout_ids'])
    assert sorted(held)==sorted(tr['ids']) and np.isfinite(error).all()


def test_hbac_package_assigns_new_rows_without_bias_metric():
    rng=np.random.default_rng(2);x=np.r_[rng.normal(-3,.1,(40,3)),rng.normal(3,.1,(40,3))].astype(np.float32)
    m=fit_hbac(x,np.r_[np.zeros(40),np.ones(40)],np.arange(80),17,k=2)
    assert m.n_clusters_==2
    np.testing.assert_array_equal(m.predict(x),m.labels_)


def test_jtt_validation_grid_does_not_collapse_on_separable_data():
    rng=np.random.default_rng(7);x=rng.normal(size=(400,4)).astype(np.float32);y=(x[:,0]>0).astype(int)
    cfg=Config(epochs=12,jtt_identification_epochs=3,hidden=16,batch_size=32)
    cp,weight,history=choose_jtt(x[:300],{'y':y[:300]},x[300:],{'y':y[300:]},np.zeros(100),cfg,17)
    p=predict_mlp(cp['average'][0],x[300:]);assert .05<(p>=.5).mean()<.95
    assert weight==max(history,key=lambda r:r['validation_accuracy'])['upweight']


def test_hmda_recorded_audit_and_jtt():
    path=ROOT/'results/leakage_audit.json'
    if not path.exists(): pytest.skip('ยังไม่มีผล HMDA จริง')
    audits=json.loads(path.read_text())['seeds']
    for a in audits:
        train,val,test=(set(a[f'{n}_ids']) for n in ['train','val','test'])
        assert train.isdisjoint(val|test) and val.isdisjoint(test)
        assert all(not prohibited(c) for c in a['features'])
        for f in a['fits']:
            assert set(f['fit_ids']).issubset(train) and set(f['fit_ids']).isdisjoint(val|test)
        for oof in a['error_crossfits']:
            held=[]
            for f in oof['folds']:
                assert set(f['fit_ids']).isdisjoint(f['heldout_ids'])
                assert set(f['fit_ids'])|set(f['heldout_ids'])==train
                assert set(f['guard_fit_ids'])==set(f['preprocessor_fit_ids'])==set(f['fit_ids'])
                held.extend(f['heldout_ids'])
            assert sorted(held)==sorted(train)
        for r in a['column_audit']:
            if not r['dropped']: assert r['missing_gap']<=.10
    results=pd.read_csv(ROOT/'results/hmda_pilot_results.csv')
    jtt=results[(results.method=='JTT') & (results.selection=='average')]
    # ถ้าโมเดลยุบเป็นคลาสเดียว งานจริงต้อง fail ให้แก้หรือรายงาน ไม่ซ่อนด้วย EO
    assert jtt.positive_rate.between(.005,.995,inclusive='neither').all()


def test_demo_build_and_prediction():
    if not (ROOT/'results/demo_bundle.joblib').exists(): pytest.skip('ยังไม่มี bundle จาก pilot')
    from fairgroups.demo import load_bundle,predict_application,build_interface
    b=load_bundle(ROOT/'results');values=[b['defaults'][c] for c in b['inputs']]
    result,card=predict_application(b,*values)
    assert 0<=result['โอกาสอนุมัติ ERM']<=1
    assert 0<=result['โอกาสอนุมัติหลังฝึก DRO']<=1
    assert 'วิจัย' in card and str(result['กลุ่ม']) in card
    assert len(b['inputs'])==8
    demo=build_interface(ROOT/'results');assert callable(demo.fn)
    second=demo.fn(*values);assert second[0]==result
