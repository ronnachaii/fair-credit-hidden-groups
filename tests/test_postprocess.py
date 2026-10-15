"""ตรวจ validation-only, การอนุมานจาก x และ guard ด้วยข้อมูลที่ไม่สมดุล"""
import inspect
import itertools
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from config import Config
from fairgroups.postprocess import ValidationThresholds, XRandomGroups, fit_candidates, selection_key
from fairgroups.hmda_groups import GlobalClusters
from fairgroups.metrics import evaluate


def sample():
    rng=np.random.default_rng(19)
    groups=np.repeat([0,1,2], [100,100,12])
    y=(rng.random(len(groups))<np.where(groups==0,.95,.7)).astype(int)
    p=np.clip(.3+.5*y+rng.normal(0,.2,len(y)),.01,.99)
    return p,y,groups,np.arange(1000,1000+len(y))


@pytest.mark.parametrize('objective',['parity','eo'])
def test_validation_only_fit_and_frozen_small_unseen_groups(objective):
    p,y,g,ids=sample()
    with pytest.raises(ValueError,match='validation'):
        ValidationThresholds().fit(p,y,g,ids,split='test')
    model=ValidationThresholds(objective).fit(p,y,g,ids)
    assert model.fit_split_=='validation' and set(model.fit_ids_)==set(ids)
    assert model.thresholds_[2]==.5
    np.testing.assert_array_equal(model.predict([.49,.51],[999,999]),[0,1])
    assert model.validation_['accuracy']>=model.baseline_accuracy_-.02-1e-12
    frozen=model.thresholds_.copy()
    model.predict(np.array([.01,.99]),np.array([0,1]))
    assert frozen==model.thresholds_  # test prediction เปลี่ยนค่า fit ไม่ได้
    assert 'test' not in inspect.signature(fit_candidates).parameters


def test_parity_matches_bruteforce_grid_optimum_and_eo_improves_its_target():
    p,y,g,ids=sample()
    parity=ValidationThresholds().fit(p,y,g,ids)
    best=1.
    # ชุดนี้มี 2 กลุ่มที่ขยับได้ ใช้ brute force ยืนยันตัวค้นช่วง
    for i,j in itertools.product(range(len(parity.tables_[0]['threshold'])),range(len(parity.tables_[1]['threshold']))):
        s=parity._stats([i,j,0])
        if s['accuracy']>=parity.accuracy_floor_-1e-12:
            best=min(best,s['approval_gap'])
    assert parity.validation_['approval_gap']<=best+1e-6
    eo=ValidationThresholds('eo').fit(p,y,g,ids)
    assert eo.validation_['eo_gap']<=parity.validation_['eo_gap']+1e-12
    assert eo.validation_['eo_gap']<=eo._stats(np.zeros(3,dtype=int))['eo_gap']+1e-12


def test_proposed_and_random_assignment_are_x_only_stable_per_row():
    rng=np.random.default_rng(7);x=rng.normal(size=(80,3)).astype(np.float32)
    cluster=GlobalClusters().fit(x,np.arange(80),4,17)
    random=XRandomGroups().fit(x,np.arange(80),4,17)
    for model in [cluster,random]:
        assert set(inspect.signature(model.predict).parameters)=={'x'}
        before=model.predict(x)
        np.testing.assert_array_equal(model.predict(x[::-1])[::-1],before)
        np.testing.assert_array_equal(model.predict(x[:1]),before[:1])


def test_selection_ignores_true_group_and_test_metrics_and_auroc_uses_scores():
    p,y,g,ids=sample();val={'y':y,'ids':ids}
    methods=[('PP-raw-k2','raw',2,{'val':g}),('PP-oracle','oracle',3,{'val':g}),
             ('PP-random-k2','random',2,{'val':g})]
    candidates=fit_candidates('ERM-MLP',p,val,methods,Config(),17)
    selected=[r for r,_,_ in candidates if r['proposed_selected']]
    assert len(selected)==1 and selected[0]['representation']=='raw'
    row=selected[0]
    assert selection_key(row)==selection_key({**row,'test_accuracy':0,'approval_rate_gap_race_eth':999})
    sensitive=pd.DataFrame({'race_eth':np.where(g==0,'White','Non-white'),
        'sex':np.where(np.arange(len(y))%2,'Male','Female'),'age':np.repeat('25-44',len(y))})
    sensitive['intersection']=sensitive.race_eth+'|'+sensitive.sex
    baseline=evaluate(y,p,sensitive,1)
    changed=evaluate(y,p,sensitive,1,prediction=np.zeros(len(y),dtype=int))
    assert baseline['auroc']==changed['auroc'] and changed['positive_rate']==0


def test_completed_pp_audit_and_small_group_thresholds():
    output=Path(__file__).resolve().parents[1]/'results'
    if not (output/'postprocess_audit.json').exists():
        pytest.skip('ยังไม่มีผลรอบ 6')
    for audit in json.loads((output/'postprocess_audit.json').read_text()):
        assert audit['fit_split']=='validation'
        assert set(audit['threshold_fit_ids']).isdisjoint(audit['test_ids'])
        assert audit['candidate_count']==26
    thresholds=pd.read_csv(output/'postprocess_thresholds.csv')
    assert thresholds[thresholds.frozen_small_group].threshold.eq(.5).all()
    results=pd.read_csv(output/'postprocess_results.csv')
    for _,part in results.groupby(['base','seed']):
        assert part.proposed_selected.sum()==part.selected_without_demographics.sum()==1
        assert part[part.proposed_selected].representation.isin(['raw','scarf']).all()
        assert part.auroc.nunique()==1
