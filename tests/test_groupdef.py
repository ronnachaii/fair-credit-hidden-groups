"""ตรวจนิยามกลุ่มและสูตร class balance ที่มีผลต่อ ablation รอบ 5"""
import inspect
import numpy as np
import torch
import pytest
from fairgroups.dro import balanced_cluster_weights, make_dro_groups, validation_groups, group_dro_loss
from fairgroups.hmda_groups import GlobalClusters


def test_balanced_weights_equal_class_mass_within_each_cluster():
    c=np.array([0]*10+[1]*8+[2]*3)
    y=np.array([0]*2+[1]*8+[0]*6+[1]*2+[1]*3)
    weights=balanced_cluster_weights(c,y)
    for cluster in np.unique(c):
        mask=c==cluster
        np.testing.assert_allclose(weights[mask].mean(),1.)
        totals=[weights[mask & (y==label)].sum() for label in np.unique(y[mask])]
        np.testing.assert_allclose(totals,totals[0])
    np.testing.assert_array_equal(weights[c==2],np.ones(3))


def test_c_clustering_merging_and_validation_do_not_use_y():
    rng=np.random.default_rng(3);x=rng.normal(size=(80,3)).astype(np.float32)
    model=GlobalClusters().fit(x,np.arange(80),4,17)
    assert 'y' not in inspect.signature(GlobalClusters.fit).parameters
    base=model.labels_.copy()
    groups,audit=make_dro_groups(x,base,20,'c')
    changed,other=make_dro_groups(x,base,20,'c',y=rng.integers(2,size=80))
    np.testing.assert_array_equal(groups,changed);assert audit==other
    assert all('y' not in row for row in audit['mapping'])
    a=validation_groups(base,np.zeros(80),'c');b=validation_groups(base,np.ones(80),'c')
    np.testing.assert_array_equal(a,b)
    before=model.centers_.copy();model.predict(x*100)
    np.testing.assert_array_equal(model.centers_,before)
    assert set(model.fit_ids_)==set(range(80))


def test_cy_requires_y_and_crosses_oracle_intersections():
    c=np.array(['A','A','B','Unknown']);y=np.array([0,1,0,1])
    assert validation_groups(c,y,'cy').tolist()==['A|y=0','A|y=1','B|y=0','Unknown']
    assert validation_groups(c,y,'c').tolist()==c.tolist()
    with pytest.raises(ValueError): validation_groups(c,definition='cy')
    with pytest.raises(ValueError): make_dro_groups(np.zeros((4,1)),np.arange(4),definition='cy')


def test_balanced_c_loss_and_gradients_use_train_weights():
    c=np.zeros(4,dtype=int);y=np.array([0,1,1,1])
    weights=torch.tensor(balanced_cluster_weights(c,y))
    losses=torch.tensor([6.,3.,3.,3.],requires_grad=True)
    loss=group_dro_loss(losses*weights,torch.tensor(c),torch.zeros(1),0.)
    torch.testing.assert_close(loss,torch.tensor(4.5))
    loss.backward();torch.testing.assert_close(losses.grad,torch.tensor([.5,1/6,1/6,1/6]))


def test_cy_balanced_scales_pure_label_dro_losses_in_mixed_parent_cluster():
    y=np.array([0,1,1,1]);weights=torch.tensor(balanced_cluster_weights(np.zeros(4),y))
    losses=torch.ones(4,requires_grad=True)
    loss=group_dro_loss(losses*weights,torch.tensor(y),torch.zeros(2),0.)
    # เฉลี่ยกลุ่มย่อยหลังถ่วง (2 + 2/3)/2; หาร sum(w) ในกลุ่มจะทำให้เหลือ 1 ผิดนิยาม
    torch.testing.assert_close(loss,torch.tensor(4/3))
    loss.backward();torch.testing.assert_close(losses.grad,torch.tensor([1.,1/9,1/9,1/9]))


def test_single_class_parent_cluster_balance_is_explicit_noop():
    y=np.array([0,0,1,1,1])
    np.testing.assert_array_equal(balanced_cluster_weights(np.array([0,0,1,1,1]),y),np.ones(5))


def test_oracle_sanity_keeps_four_independent_variant_outcomes():
    import pandas as pd
    from fairgroups.hmda_reporting import oracle_sanity
    rows=[]
    for seed in [17,29]:
        rows.append({'seed':seed,'method':'ERM-MLP','selection':'average','dro_variant':'none','worst_group_accuracy':.8})
        for variant,value in [('cy',.7),('cy_bal',.75),('c',.82),('c_bal',.79)]:
            rows.append({'seed':seed,'method':'GDRO-oracle','selection':'inferred_worst_group',
                         'dro_variant':variant,'worst_group_accuracy':value})
    sanity,status,gains=oracle_sanity(pd.DataFrame(rows))
    assert len(sanity)==8 and status=={'cy':False,'cy_bal':False,'c':True,'c_bal':False}
    assert gains['c']>0 and gains['c_bal']<0
