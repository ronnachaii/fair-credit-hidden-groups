"""กฎจากตัวแปรเดิม และทดสอบความต่างบน test ที่ไม่ใช้สร้างกลุ่ม"""
import json
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, chi2_contingency
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.metrics import f1_score
from .hmda import HMDAPreprocessor, NUMERIC, reference_groups


def rules(tree, names):
    """แสดงเฉพาะเส้นทางใบที่ทายว่าอยู่กลุ่มนี้ แต่ละเส้นทางไม่เกิน 3 เงื่อนไข"""
    found=[]
    def visit(node, conditions):
        if tree.tree_.feature[node] == _tree.TREE_UNDEFINED:
            if tree.classes_[np.argmax(tree.tree_.value[node][0])] == 1:
                found.append(('IF ' + ' AND '.join(conditions) if conditions else 'IF TRUE') + ' THEN อยู่กลุ่มนี้')
            return
        feature=names[tree.tree_.feature[node]].replace('numeric__','').replace('category__','')
        threshold=tree.tree_.threshold[node]
        visit(tree.tree_.children_left[node], conditions+[f'{feature} ≤ {threshold:.4g}'])
        visit(tree.tree_.children_right[node], conditions+[f'{feature} > {threshold:.4g}'])
    visit(0,[])
    return found or ['ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)']


def describe_groups(method, k, seed, train, val, test, labels, erm_probability, config):
    processor=HMDAPreprocessor(config.min_category_frequency,config.lei_top_n,scale=False).fit(train['x'])
    xtr,xv = processor.transform(train['x']),processor.transform(val['x'])
    rows, tests=[] , []
    for group in np.unique(labels['train']):
        target=(labels['train']==group).astype(int)
        tree=DecisionTreeClassifier(max_depth=3,min_samples_leaf=max(20,len(target)//100),random_state=seed)
        tree.fit(xtr,target)
        vp=tree.predict(xv); vt=(labels['val']==group).astype(int)
        mask=labels['test']==group; yy=test['y'][mask]; pp=(erm_probability[mask]>=.5).astype(int)
        n=int(mask.sum()); positive=yy==1; negative=yy==0
        population={}
        for dimension, values in reference_groups(test['s']).items():
            if dimension=='intersection': continue
            population[dimension]={str(v):{'group':float((values[mask]==v).mean()) if n else None,
                                          'overall':float((values==v).mean())} for v in np.unique(values)}
        paths=rules(tree,processor.names())
        positive_leaves=[]
        def lengths(node,depth=0):
            if tree.tree_.feature[node]==_tree.TREE_UNDEFINED:
                if tree.classes_[np.argmax(tree.tree_.value[node][0])]==1: positive_leaves.append(depth)
            else:
                lengths(tree.tree_.children_left[node],depth+1); lengths(tree.tree_.children_right[node],depth+1)
        lengths(0)
        row={'seed':seed,'method':method,'k':k,'group':int(group),'n_train':int(target.sum()),'n_val':int(vt.sum()),'n_test':n,
             'fidelity_f1':float(f1_score(vt,vp,zero_division=0)), 'rule_length':sum(positive_leaves),
             'max_conditions_per_path':max(positive_leaves,default=0),'n_rules':len(positive_leaves),
             'coverage':float(vp.mean()),'actual_coverage_test':float(mask.mean()),
             'approval_rate':float(yy.mean()) if n else np.nan,'erm_error':float((yy!=pp).mean()) if n else np.nan,
             'fpr':float(pp[negative].mean()) if negative.any() else np.nan,
             'fnr':float((1-pp[positive]).mean()) if positive.any() else np.nan,
             'rules':json.dumps(paths,ensure_ascii=False),'population':json.dumps(population,ensure_ascii=False),
             'rule_fit_split':'train','fidelity_split':'validation','statistical_test_split':'test'}
        rows.append(row)
        for c in test['x']:
            a,b=test['x'].loc[mask,c],test['x'].loc[~mask,c]
            p=np.nan
            if c in NUMERIC:
                a,b=a.dropna(),b.dropna()
                if len(a)>1 and len(b)>1 and (a.var()>0 or b.var()>0):
                    p=float(ttest_ind(a,b,equal_var=False).pvalue)
                test_name='Welch t-test'
            else:
                table=pd.crosstab(pd.Series(mask,index=test['x'].index),test['x'][c])
                if table.shape[0]==2 and table.shape[1]>1:
                    p=float(chi2_contingency(table,correction=False)[1])
                test_name='chi-square'
            tests.append({'seed':seed,'method':method,'k':k,'group':int(group),'feature':c,'test':test_name,'p_value':p})
    return rows,tests,processor.fit_ids_


def card_text(row):
    r=row
    def fmt(v): return f'{v:.4f}' if pd.notna(v) else 'N/A'
    pop=json.loads(r['population']); composition=[]
    for dim, vals in pop.items():
        composition.append(dim+': '+', '.join(f"{v} {d['group']:.1%} (ทั้งชุด {d['overall']:.1%})" for v,d in vals.items() if d['group'] is not None))
    return '\n'.join([f"### {r['method']} · seed {r['seed']} · กลุ่ม {r['group']}",
        *['- '+v for v in json.loads(r['rules'])],
        f"- ขนาด train/validation/test: {r['n_train']}/{r['n_val']}/{r['n_test']} · coverage กฎบน validation {fmt(r['coverage'])}",
        f"- Fidelity F1 {fmt(r['fidelity_f1'])} · เงื่อนไขรวม {r['rule_length']} · สูงสุดต่อเส้นทาง {r['max_conditions_per_path']}",
        f"- อนุมัติจริง {fmt(r['approval_rate'])} · ERM error {fmt(r['erm_error'])} · FPR {fmt(r['fpr'])} · FNR {fmt(r['fnr'])}",
        '- ตัวแปรต่างชัดหลัง Bonferroni: '+r.get('significant_features',''),
        *['- องค์ประกอบ '+v for v in composition],
        '- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation', ''])


def export_explanations(output, rows, tests):
    tests=pd.DataFrame(tests)
    # ปรับทั้ง family ของการทดสอบทุก seed/วิธี/กลุ่ม/ตัวแปรที่ส่งออก
    tests['p_bonferroni']=(tests.p_value*tests.p_value.notna().sum()).clip(upper=1)
    tests['significant']=tests.p_bonferroni<.05
    tests.to_csv(output/'group_feature_tests.csv',index=False)
    for row in rows:
        matching=tests[(tests.seed==row['seed']) & (tests.method==row['method']) & (tests.group==row['group']) & tests.significant]
        row['significant_features']=', '.join(f"{r.feature} (p_adj={r.p_bonferroni:.2g})" for r in matching.itertuples()) or 'ไม่พบ'
    frame=pd.DataFrame(rows);frame.to_csv(output/'group_explanations.csv',index=False)
    (output/'group_cards.md').write_text('# การ์ดอธิบายกลุ่ม HMDA\n\nกฎ one-hot ที่ ≤ 0.5 หมายถึงไม่มีค่านั้น; สถิติต่างกลุ่มเป็นเชิงสำรวจ ไม่ใช่เหตุและผล\n\n'+'\n'.join(card_text(r) for r in rows),encoding='utf-8')
    return rows
