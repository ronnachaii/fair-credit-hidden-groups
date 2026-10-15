"""ตรวจการรวมกลุ่ม การถ่วง loss และคำอธิบายที่มีผลต่อข้อสรุปรอบ 3"""
import copy
import json
import numpy as np
import pandas as pd
import torch
from config import Config
from fairgroups.dro import merge_small_groups, group_dro_loss
from fairgroups.explanations import fit_surrogate, feature_differences, card_text, choose_surrogate
from fairgroups.models import train_mlp, predict_mlp, cross_labels, selection_rank, worst_accuracy
from fairgroups.run import choose_dro


def test_merge_chooses_nearest_center_only_within_class():
    x=np.r_[np.full(2,1.),np.zeros(8),np.full(8,10.),np.ones(8)][:,None]
    y=np.r_[np.zeros(18),np.ones(8)].astype(int)
    clusters=np.r_[np.zeros(2),np.ones(8),np.full(8,2),np.full(8,3)].astype(int)
    groups, details=merge_small_groups(x,y,clusters,min_size=5)
    assert np.all(groups[:2]==groups[2])
    assert groups[0]!=groups[-1] and groups[0]!=groups[10]
    assert details['n_groups_before']==4 and details['n_groups_after']==3
    assert min(details['group_sizes'])>=5
    for group in np.unique(groups):
        assert len(np.unique(y[groups==group]))==1


def test_merge_small_groups_together_and_report_undersized_class():
    x=np.arange(9,dtype=float)[:,None];y=np.r_[np.zeros(6),np.ones(3)]
    groups, details=merge_small_groups(x,y,np.arange(9),min_size=5)
    assert sorted(details['group_sizes'])==[3,6]
    assert details['undersized_remaining']==1
    np.testing.assert_array_equal(groups,merge_small_groups(x,y,np.arange(9),5)[0])


def test_adjustment_uses_full_train_counts_and_excludes_absent_batch_group():
    losses=torch.ones(3,requires_grad=True);log_weights=torch.zeros(3)
    value=group_dro_loss(losses,torch.tensor([0,0,1]),log_weights,eta=1,
                         group_counts=torch.tensor([100.,4.,1.]),adjustment=1)
    expected=torch.log_softmax(torch.tensor([1.1,1.5,0.]),dim=0)
    torch.testing.assert_close(log_weights,expected)
    value.backward()
    w=torch.softmax(torch.tensor([1.1,1.5]),dim=0)
    torch.testing.assert_close(losses.grad,torch.tensor([w[0]/2,w[0]/2,w[1]]))


def test_small_separable_surrogate_predicts_both_sides_on_holdout():
    train=np.r_[np.zeros(990),np.ones(10)][:,None]
    target=np.r_[np.zeros(990),np.ones(10)].astype(int)
    tree=fit_surrogate(train,target,17)
    holdout=np.r_[np.zeros(200),np.ones(10)][:,None]
    truth=np.r_[np.zeros(200),np.ones(10)].astype(int)
    np.testing.assert_array_equal(tree.predict(holdout),truth)
    assert tree.get_depth()<=3 and tree.class_weight=='balanced'


def test_fallback_effect_sizes_and_low_fidelity_card():
    frame=pd.DataFrame({'loan_amount':[0.,2.,2.,4.],'loan_type':['a','a','b','b']})
    differences=feature_differences(frame,np.array([True,True,False,False]))
    numeric=next(d for d in differences if d['feature']=='loan_amount')
    np.testing.assert_allclose(numeric['value'],-np.sqrt(2))
    category=next(d for d in differences if d['feature']=='loan_type')
    assert abs(category['value'])==1
    row={'population':'{}','method':'test','seed':17,'group':0,'rules':'[]',
         'n_train':10,'n_val':2,'n_test':2,'coverage':.1,'fidelity_f1':.2,
         'fidelity_precision':.25,'fidelity_recall':.5,'rule_length':3,'max_conditions_per_path':3,
         'approval_rate':.5,'erm_error':.5,'fpr':0.,'fnr':1.,
         'fallback_features':json.dumps(differences)}
    card=card_text(row)
    assert 'กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี' in card
    assert 'loan_amount' in card and 'loan_type' in card and 'train เท่านั้น' in card
    assert 'precision 0.2500' in card and 'recall 0.5000' in card


def test_dro_grid_selection_invariant_to_validation_demographics_and_preserves_erm():
    rng=np.random.default_rng(7);x=rng.normal(size=(120,3)).astype(np.float32)
    y=(x[:,0]>0).astype(int);cfg=Config(epochs=2,dro_epoch_grid=(2,),hidden=8,batch_size=32)
    cp,_=train_mlp(x[:80],y[:80],x[80:],y[80:],np.zeros(40),cfg,17)
    erm=cp['average'][0];saved=copy.deepcopy(erm.state_dict())
    a, selected, history=choose_dro(x[:80],y[:80],x[80:],y[80:],np.zeros(40),y[:80],erm,cfg,17,'test',inferred_val_groups=cross_labels((x[80:,1]>0).astype(int),y[80:]))
    b, other, _=choose_dro(x[:80],y[:80],x[80:],y[80:],np.arange(40)%4,y[:80],erm,cfg,17,'test',inferred_val_groups=cross_labels((x[80:,1]>0).astype(int),y[80:]))
    assert len(history)==24 and sum(r['selected'] for r in history)==3
    primary=[r for r in history if r['selection']=='inferred_worst_group']
    def rank(r):
        return selection_rank('inferred_worst_group',{'average':r['validation_accuracy'],
            'inferred_worst_group':r['validation_selection_score']},r['accuracy_floor'])
    assert selected==max(primary,key=rank)
    assert selected['parameter_l2_from_erm']>0
    assert all(r['final_group_weight_max']>r['final_group_weight_min'] for r in history)
    assert {k:v for k,v in selected.items() if k!='validation_true_worst_group'}=={k:v for k,v in other.items() if k!='validation_true_worst_group'}
    np.testing.assert_array_equal(predict_mlp(a['inferred_worst_group'][0],x[80:]),predict_mlp(b['inferred_worst_group'][0],x[80:]))
    for key, value in saved.items():
        torch.testing.assert_close(erm.state_dict()[key],value)


def test_guard_prefers_eligible_and_falls_back_to_closest_average():
    def rank(average,worst):
        return selection_rank('inferred_worst_group',{'average':average,'inferred_worst_group':worst},.88)
    assert rank(.88,.5)>rank(.879,.99)
    assert rank(.90,.7)>rank(.92,.6)
    assert rank(.87,.1)>rank(.86,.9)
    assert rank(.90,.7)>rank(.89,.7)


def test_validation_groups_cross_cluster_and_label_without_dro_merge():
    groups=cross_labels(np.array([0,0,1,1]),np.array([0,1,0,1]))
    assert len(np.unique(groups))==4
    correct=np.array([True,True,False,True])
    assert worst_accuracy(correct,groups)==0
    assert worst_accuracy(correct,np.array(['a','a','Unknown','b']))==1


def test_surrogate_selects_better_validation_f1_from_both_candidates():
    rng=np.random.default_rng(9)
    x=rng.normal(size=(500,3)); target=(x[:,0]+x[:,1]>2).astype(int)
    xv=rng.normal(size=(200,3)); truth=(xv[:,0]+xv[:,1]>2).astype(int)
    tree,meta=choose_surrogate(x,target,xv,truth,17)
    from sklearn.metrics import f1_score
    selected=f1_score(truth,tree.predict(xv),zero_division=0)
    assert selected==max(meta['fidelity_f1_balanced'],meta['fidelity_f1_unbalanced'])
    assert tree.get_depth()<=3 and meta['surrogate_selection_split']=='validation'


def test_oracle_sanity_reports_failure_and_success_without_hiding_it():
    from fairgroups.hmda_reporting import oracle_sanity
    rows=[]
    for seed in [17,29]:
        rows.extend([{'seed':seed,'method':'ERM-MLP','selection':'average','worst_group_accuracy':.8},
                     {'seed':seed,'method':'GDRO-oracle','selection':'inferred_worst_group','worst_group_accuracy':.7}])
    frame=pd.DataFrame(rows);_,passed,gain=oracle_sanity(frame)
    assert not passed['cy'] and gain['cy']<0
    frame.loc[frame.method.eq('GDRO-oracle'),'worst_group_accuracy']=.81
    _,passed,gain=oracle_sanity(frame)
    assert passed['cy'] and gain['cy']>0
