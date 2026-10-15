"""HMDA pilot ต่อยอดโมดูลเดิม: train-only discovery และ full labels เท่านั้น"""
import json
import time
import warnings
from dataclasses import replace
from itertools import product
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from lightgbm import LGBMClassifier
from .hmda import load_hmda, split_hmda, LeakageGuard, HMDAPreprocessor, write_profile
from .hmda_groups import ClassClusters, GlobalClusters, GeoGroups, hidden, fit_hbac, group_scores
from .models import set_seed, train_mlp, predict_mlp, validation_scores, cross_labels, selection_rank
from .representations import train_scarf, encode_scarf
from .efficiency import ResourceMonitor, network_cost, inference_seconds, environment
from .metrics import evaluate
from .tracking import setup_tracking, log_row
from .explanations import describe_groups, export_explanations
from .dro import make_dro_groups, balanced_cluster_weights, validation_groups
from .postprocess import XRandomGroups, fit_candidates, evaluate_candidates


def save_json(path,value):
    Path(path).write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8')


def oof_errors(train,config,seed):
    """แต่ละ fold มี imputer/encoder ของตัวเอง แถว held ไม่เข้า fit แม้ขั้นแปลง"""
    y=train['y']; p=np.full(len(y),np.nan); folds=[]
    for fit,held in StratifiedKFold(config.oof_folds,shuffle=True,random_state=seed).split(train['x'],y):
        # ตัวกรอง missing gap อาศัย y จึงต้อง fit ใหม่ภายใน fold ด้วย
        fold_guard=LeakageGuard().fit(train['frame'].iloc[fit],y[fit])
        fold_train=fold_guard.transform(train['frame'].iloc[fit])
        fold_held=fold_guard.transform(train['frame'].iloc[held])
        pre=HMDAPreprocessor(config.min_category_frequency,config.lei_top_n).fit(fold_train)
        model=LGBMClassifier(n_estimators=config.trees,num_leaves=15,max_depth=5,verbosity=-1,
                             n_jobs=config.threads,random_state=seed,deterministic=True,force_col_wise=True)
        model.fit(pre.transform(fold_train),y[fit])
        p[held]=model.predict_proba(pre.transform(fold_held))[:,1]
        folds.append({'fit_ids':train['ids'][fit].tolist(),'heldout_ids':train['ids'][held].tolist(),
                      'guard_fit_ids':fold_guard.fit_ids_.tolist(),'preprocessor_fit_ids':pre.fit_ids_.tolist(),
                      'features':fold_guard.features_})
    assert np.isfinite(p).all()
    return ((p>=.5)!=y).astype(float),{'fit_ids':train['ids'].tolist(),'folds':folds}


def choose_jtt(xt,train,xv,val,vg,config,seed,erm_accuracy=0.0):
    """JTT มีกลุ่มผิด/ถูกจากโมเดลรอบสั้น × y; เลือกแยกทั้งสามเกณฑ์"""
    _, identification=train_mlp(xt,train['y'],xv,val['y'],vg,config,seed,epochs=config.jtt_identification_epochs)
    mistakes=(predict_mlp(identification,xt)>=.5)!=train['y']
    val_mistakes=(predict_mlp(identification,xv)>=.5)!=val['y']
    inferred=cross_labels(val_mistakes.astype(int),val['y'])
    floor=erm_accuracy-config.selection_accuracy_tolerance
    chosen={}; best_ranks={}; history=[]
    for weight in config.jtt_grid:
        checkpoints,_=train_mlp(xt,train['y'],xv,val['y'],vg,config,seed,
            sample_weights=np.where(mistakes,weight,1.),inferred_val_groups=inferred,accuracy_floor=floor)
        for selection,cp in checkpoints.items():
            model,epoch,score=cp; meta=model.selection_metadata_
            rate=float((predict_mlp(model,xv)>=.5).mean())
            row={'seed':seed,'selection':selection,'upweight':weight,
                 'validation_accuracy':meta['average'],'validation_selection_score':score,
                 'selected_epoch':epoch,'positive_rate':rate,'collapsed':rate<=.005 or rate>=.995,
                 'n_mistakes':int(mistakes.sum()),'accuracy_guard_passed':meta['accuracy_guard_passed'],
                 'accuracy_floor':floor,'selected':False}
            history.append(row)
            rank=selection_rank(selection,meta,floor)
            if selection not in best_ranks or rank>best_ranks[selection]:
                chosen[selection]=cp;best_ranks[selection]=rank
                model.selection_metadata_={**meta,'jtt_upweight':weight}
                chosen[selection][0].grid_index_=len(history)-1
    for selection,cp in chosen.items():
        row=history[cp[0].grid_index_];row['selected']=True
        if row['collapsed']:
            warnings.warn(f'JTT {selection} validation ทายข้างเดียว อ่าน accuracy และ rate ควบคู่')
    return chosen,chosen['average'][0].selection_metadata_['jtt_upweight'],history


def choose_dro(xt, y, xv, yv, vg, groups, erm, config, seed, method,
               inferred_val_groups=None, inferred_min_size=1, variant="cy", sample_weights=None):
    """ค้นกริดและ checkpoint แยกแต่ละเกณฑ์; primary ใช้ inferred groups พร้อม guard"""
    if inferred_val_groups is None:
        raise ValueError('ต้องระบุกลุ่ม validation ของวิธีนี้ ห้ามใช้ประชากรแทนโดยปริยาย')
    erm_accuracy=float(((predict_mlp(erm,xv)>=.5)==yv).mean())
    floor=erm_accuracy-config.selection_accuracy_tolerance
    chosen={};best_ranks={};best_indices={};history=[]
    for eta, adjustment, learning_rate, epochs in product(config.dro_eta_grid, config.dro_adjustment_grid,
                                                         config.dro_learning_rate_grid, config.dro_epoch_grid):
        candidate=replace(config,dro_eta=eta,dro_adjustment=adjustment)
        checkpoints,final=train_mlp(xt,y,xv,yv,vg,candidate,seed,groups=groups,
            initial_model=erm,epochs=epochs,learning_rate=learning_rate,
            inferred_val_groups=inferred_val_groups,accuracy_floor=floor,inferred_min_size=inferred_min_size, sample_weights=sample_weights)
        for selection,cp in checkpoints.items():
            model,epoch,score=cp;meta=model.selection_metadata_
            settings={'dro_variant':variant,'dro_eta':eta,'dro_adjustment':adjustment,'dro_learning_rate':learning_rate,
                      'dro_finetune_epochs':epochs}
            model.selection_metadata_={**meta,**settings}
            row={'seed':seed,'method':method,'dro_variant':variant,'selection':selection,'dro_eta':eta,'C':adjustment,
                 'validation_accuracy':meta['average'],'validation_selection_score':score,
                 'validation_inferred_worst_group':meta['inferred_worst_group'],
                 'validation_true_worst_group':meta['worst_group'],'selected_epoch':epoch,
                 'selection_metric':selection,'warm_start':'ERM-MLP average checkpoint',
                 'finetune_epochs':epochs,'learning_rate':learning_rate,
                 'n_dro_groups':len(np.unique(groups)),'n_validation_groups':len(np.unique(inferred_val_groups)),
                 'validation_group_source':('true intersection' if method=='GDRO-oracle' else 'inferred cluster') + (' x y' if variant.startswith('cy') else ''),
                 'inferred_min_size':inferred_min_size,'erm_validation_accuracy':erm_accuracy,
                 'accuracy_floor':floor,'accuracy_guard_passed':meta['accuracy_guard_passed'],
                 'parameter_l2_from_erm':meta['parameter_l2_from_erm'],
                 'group_weight_min':meta['group_weight_min'],'group_weight_max':meta['group_weight_max'],
                 **final.training_diagnostics_,'selected':False}
            history.append(row);rank=selection_rank(selection,meta,floor)
            if selection not in best_ranks or rank>best_ranks[selection]:
                best_ranks[selection]=rank;chosen[selection]=cp;best_indices[selection]=len(history)-1
    for index in best_indices.values(): history[index]['selected']=True
    return chosen,history[best_indices['inferred_worst_group']],history


def run_experiment(config,root='.'):
    root=Path(root).resolve(); output=root/'results';output.mkdir(exist_ok=True)
    start=time.perf_counter(); set_seed(config.seeds[0],config.threads)
    before={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    prior_env=json.loads((output/'environment.json').read_text()) if (output/'environment.json').exists() else {}
    env=environment(config); setup_tracking(root)
    rows=[];clusters=[];resources=[];audits=[];explanations=[];feature_tests=[];jtt_history=[];dro_history=[];demo_bundle=None
    pp_rows=[];pp_thresholds=[];pp_audits=[];pp_demo=None
    with ResourceMonitor() as overall:
        frame,y,s,stages=load_hmda(root/'data',config.state)
        write_profile(output,stages,y,s)
        env.update(eligible_source_rows=len(y),source_rows=int(stages.iloc[0]['n']))
        for seed in config.seeds:
            print(f'seed={seed}: HMDA split / audit / representation',flush=True)
            splits=split_hmda(frame,y,s,seed,config.max_rows)
            train,val,test=(splits[n] for n in ['train','val','test'])
            audit={'seed':seed,**{f'{n}_ids':p['ids'].tolist() for n,p in splits.items()},'fits':[]}
            def add_fit(stage,ids):
                assert set(ids).issubset(train['ids']) and set(ids).isdisjoint(np.r_[val['ids'],test['ids']])
                audit['fits'].append({'stage':stage,'fit_ids':np.asarray(ids).tolist()})
            with ResourceMonitor() as pr:
                guard=LeakageGuard().fit(train['frame'],train['y'])
                for part in splits.values(): part['x']=guard.transform(part['frame'])
                processor=HMDAPreprocessor(config.min_category_frequency,config.lei_top_n).fit(train['x'])
                transformed={n:processor.transform(p['x']) for n,p in splits.items()}
            xt,xv,xx=(transformed[n] for n in ['train','val','test'])
            add_fit('leakage_guard',guard.fit_ids_);add_fit('imputer_scaler_categories_top_lei',processor.fit_ids_)
            audit.update(features=guard.features_,column_audit=guard.audit_)
            # กลุ่มจริงใช้เลือก oracle และผลเสริม worst_group เท่านั้น
            vg=val['s'].intersection.to_numpy()
            with ResourceMonitor() as er:
                erm_checkpoints,_=train_mlp(xt,train['y'],xv,val['y'],vg,config,seed)
            erm=erm_checkpoints['average'][0]
            with ResourceMonitor() as sr:
                scarf=train_scarf(train['x'],processor,config,seed)
                scarf_scaler=StandardScaler().fit(encode_scarf(scarf,xt))
                reps={'raw':transformed,'scarf':{n:scarf_scaler.transform(encode_scarf(scarf,x)).astype(np.float32) for n,x in transformed.items()}}
            add_fit('scarf',scarf.fit_ids_);add_fit('scarf_scaler',train['ids'])
            with ResourceMonitor() as gr:
                george_scaler=StandardScaler().fit(hidden(erm,xt))
                reps['GEORGE']={n:george_scaler.transform(hidden(erm,x)).astype(np.float32) for n,x in transformed.items()}
            add_fit('GEORGE_erm_hidden_scaler',train['ids'])
            for name,seconds,model in [('raw',pr.seconds,None),('scarf',sr.seconds,scarf.encoder),('GEORGE',er.seconds+gr.seconds,erm)]:
                resources.append({'seed':seed,'representation':name,'discovery_train_seconds':seconds,
                                  'peak_memory_mb':overall.process.memory_info().rss/1024**2,
                                  **(network_cost(model) if model is not None else {'parameters':0,'flops_per_row':0})})
            discoveries={}; selected={}
            for definition in ['cy','c']:
                for rep_name,rep in reps.items():
                    for k in config.ks:
                        with ResourceMonitor() as cr:
                            km=(ClassClusters().fit(rep['train'],train['y'],train['ids'],k,seed)
                                if definition=='cy' else GlobalClusters().fit(rep['train'],train['ids'],k,seed))
                            labels={'train':km.labels_,**{n:km.predict(rep[n]) for n in ['val','test']}}
                            scores=group_scores(rep['train'],labels['train'],train['s'],seed)
                            alignment=group_scores(rep['test'],labels['test'],test['s'],seed)
                        add_fit(f'{definition}_kmeans_{rep_name}_{k}',km.fit_ids_)
                        seconds=cr.seconds+(sr.seconds if rep_name=='scarf' else er.seconds+gr.seconds if rep_name=='GEORGE' else 0)
                        rec={'seed':seed,'representation':rep_name,'k':k,'group_definition':definition,
                             'silhouette':scores['silhouette'],'davies_bouldin':scores['davies_bouldin'],
                             'n_clusters':scores['n_clusters'],
                             **{key:value for key,value in alignment.items() if key.startswith(('ari_','nmi_','alignment_'))},
                             'discovery_train_seconds':seconds,
                             'assignment':'nearest center without y', 'cluster_fit_uses_y':definition=='cy'}
                        clusters.append(rec);discoveries[(definition,rep_name,k)]=(km,labels,rec,seconds)
                    selected[(definition,rep_name)]=max(config.ks,key=lambda k:discoveries[(definition,rep_name,k)][2]['silhouette'])
            # HBAC ใช้ OOF error ของ ERM-LGBM บน train ไม่ใช้ demographic
            with ResourceMonitor() as hr:
                error,oof=oof_errors(train,config,seed)
                hbac=fit_hbac(xt,error,train['ids'],seed,k=4)
                labels={'train':hbac.labels_,**{n:hbac.predict(transformed[n]) for n in ['val','test']}}
                hscore=group_scores(xt,labels['train'],train['s'],seed)
                alignment=group_scores(xx,labels['test'],test['s'],seed)
            audit['error_crossfits']=[oof];add_fit('HBAC_OOF',train['ids']);add_fit('HBAC',hbac.fit_ids_)
            hrec={'seed':seed,'representation':'HBAC','k':hbac.n_clusters_,'silhouette':hscore['silhouette'],
                  'davies_bouldin':hscore['davies_bouldin'],'n_clusters':hbac.n_clusters_,
                  **{a:b for a,b in alignment.items() if a.startswith(('ari_','nmi_','alignment_'))},'discovery_train_seconds':hr.seconds}
            hlabels=labels
            clusters.append({**hrec,'group_definition':'shared'})
            resources.append({'seed':seed,'representation':'HBAC','discovery_train_seconds':hr.seconds,
                              'peak_memory_mb':hr.peak_mb,'parameters':np.nan,'flops_per_row':np.nan})
            with ResourceMonitor() as geo_r:
                geo_values={n:pd.to_numeric(p['frame'].tract_minority_population_percent,errors='coerce').to_numpy() for n,p in splits.items()}
                geo=GeoGroups().fit(geo_values['train'],train['ids'])
                geo_labels={n:geo.predict(v) for n,v in geo_values.items()}
                geo_score=group_scores(xx,geo_labels['test'],test['s'],seed)
            add_fit('geoproxy_quantiles',geo.fit_ids_)
            clusters.append({'seed':seed,'representation':'geoproxy','k':4,**geo_score,'discovery_train_seconds':geo_r.seconds})
            # ใช้ Silhouette train เลือก representation/k แยก c และ cy ก่อนเลือก variant ด้วย validation
            main_pairs={d:max([(r,selected[(d,r)]) for r in ['raw','scarf']],
                             key=lambda pair:discoveries[(d,*pair)][2]['silhouette']) for d in ['cy','c']}
            for (definition,rep_name),k in selected.items():
                _,labels,_,_=discoveries[(definition,rep_name,k)]
                method=f'GDRO-{rep_name}-k{k}' if rep_name in ['raw','scarf'] else rep_name
                cards,tests,fit_ids=describe_groups(method,k,seed,train,val,test,labels,predict_mlp(erm,xx),config)
                for row in cards+tests: row['group_definition']=definition
                explanations.extend(cards);feature_tests.extend(tests);add_fit(f'explanation_{definition}_{rep_name}',fit_ids)
            cards,tests,fit_ids=describe_groups('HBAC',hbac.n_clusters_,seed,train,val,test,hlabels,predict_mlp(erm,xx),config)
            for definition in ['cy','c']:
                explanations.extend([{**r,'group_definition':definition} for r in cards])
                feature_tests.extend([{**r,'group_definition':definition} for r in tests])
            add_fit('explanation_HBAC',fit_ids)
            def record(method,rep,k,checkpoints,seconds,peak,alignment=None,discovery_seconds=0,extra=None):
                for selection,(model,epoch,score) in checkpoints.items():
                    predict=(lambda a,model=model:predict_mlp(model,a)) if method!='ERM-LGBM' else (lambda a,epoch=epoch:model.predict_proba(a,num_iteration=epoch)[:,1])
                    row={'seed':seed,'method':method,'representation':rep,'k':k,'label_fraction':1.,'selection':selection,
                         'selected_epoch':epoch,'validation_selection_score':score,'n_train':len(xt),'n_val':len(xv),'n_test':len(xx),
                         'input_dimension':xt.shape[1],'threshold':.5,'train_seconds':pr.seconds+seconds+discovery_seconds,
                         'decision_train_seconds':seconds,'discovery_train_seconds':discovery_seconds,'peak_memory_mb':max(peak,pr.peak_mb),
                         'dro_variant':'none','group_definition':'none',
                         'selected_without_demographics':False,'proposed_selected':False,
                         'variant_selected_without_demographics':False,'proposed_variant_selected':False,**(alignment or {}),**(extra or {})}
                    if hasattr(model,'selection_metadata_'):
                        meta=model.selection_metadata_
                        row.update({key:value for key,value in meta.items() if key.startswith(('dro_','jtt_'))})
                        row.update(validation_average_accuracy=meta['average'],accuracy_guard_passed=meta['accuracy_guard_passed'],
                                   validation_accuracy_floor=meta['accuracy_floor'],parameter_l2_from_erm=meta['parameter_l2_from_erm'])
                    row.update(evaluate(test['y'],predict(xx),test['s'],config.min_fair_group))
                    row['inference_seconds_per_1000']=inference_seconds(predict,xx)
                    if method=='ERM-LGBM':
                        trees=model.booster_.dump_model(num_iteration=epoch)['tree_info']
                        row.update(parameters=np.nan,flops_per_row=np.nan,tree_count=len(trees),leaf_count=sum(t['num_leaves'] for t in trees))
                    else: row.update(network_cost(model))
                    rows.append(row)
            record('ERM-MLP','none',0,erm_checkpoints,er.seconds,er.peak_mb)
            with ResourceMonitor() as lr:
                lgb=LGBMClassifier(n_estimators=config.trees,num_leaves=15,max_depth=5,learning_rate=.05,verbosity=-1,
                    n_jobs=config.threads,random_state=seed,deterministic=True,force_col_wise=True)
                lgb.fit(xt,train['y'])
                choices={t:validation_scores(val['y'],lgb.predict_proba(xv,num_iteration=t)[:,1],vg) for t in sorted(set([10,25,50,config.trees]))}
                lc={sel:(lgb,t,choices[t][sel]) for sel in ['average','worst_group'] for t in [max(choices,key=lambda t:choices[t][sel])]}
            record('ERM-LGBM','none',0,lc,lr.seconds,lr.peak_mb)
            # PP ใช้ c เท่านั้น; เลือก GEORGE k ด้วย silhouette train เดิม
            pp_methods=[]
            for (definition,rep,k),(km,labels,rec,seconds) in discoveries.items():
                if definition!='c' or (rep=='GEORGE' and k!=selected[('c',rep)]): continue
                name=f'PP-{rep}-k{k}' if rep in ['raw','scarf'] else 'PP-GEORGE'
                pp_methods.append((name,rep,k,labels))
            for k in config.ks:
                random_model=XRandomGroups().fit(xt,train['ids'],k,seed)
                random_labels={n:random_model.predict(x) for n,x in transformed.items()}
                add_fit(f'PP_random_xhash_{k}',random_model.fit_ids_)
                pp_methods.append((f'PP-random-k{k}','random',k,random_labels))
            pp_methods.extend([('PP-HBAC','HBAC',hbac.n_clusters_,hlabels),
                ('PP-geoproxy','geoproxy',len(np.unique(geo_labels['train'])),geo_labels),
                ('PP-oracle','oracle',train['s'].intersection.nunique(),
                 {n:p['s'].intersection.to_numpy() for n,p in splits.items()})])
            for base in ['ERM-LGBM','ERM-MLP']:
                print(f'  {seed}: postprocess {base}',flush=True)
                if base=='ERM-LGBM':
                    iteration=lc['average'][1]
                    vp=lgb.predict_proba(xv,num_iteration=iteration)[:,1]
                else:
                    vp=predict_mlp(erm,xv)
                # ตัวหาเกณฑ์ไม่รับ test แม้แต่คะแนน เพื่อป้องกันเลือกจาก holdout
                candidates=fit_candidates(base,vp,val,pp_methods,config,seed)
                for meta,model,_ in candidates:
                    assert set(model.fit_ids_)==set(val['ids'])
                    assert set(model.fit_ids_).isdisjoint(test['ids'])
                pp_audits.append({'seed':seed,'base':base,'fit_split':'validation',
                    'threshold_fit_ids':val['ids'].tolist(),'test_ids':test['ids'].tolist(),
                    'candidate_count':len(candidates),'selection_uses_demographics':False,
                    'oracle_excluded_from_selection':True})
                tp=lgb.predict_proba(xx,num_iteration=iteration)[:,1] if base=='ERM-LGBM' else predict_mlp(erm,xx)
                pp_rows.append({'seed':seed,'base':base,'method':base,'representation':'none','k':0,
                    'objective':'baseline','fit_split':'none','proposed_selected':False,
                    'selected_without_demographics':False,'threshold_fit_seconds':0.,
                    **evaluate(test['y'],tp,test['s'],config.min_fair_group)})
                evaluated,thresholds=evaluate_candidates(candidates,tp,test,config.min_fair_group)
                pp_rows.extend(evaluated);pp_thresholds.extend(thresholds)
                for meta,model,labels in candidates:
                    if seed==config.seeds[0] and base=='ERM-LGBM' and meta['proposed_selected']:
                        rep,k=meta['representation'],meta['k']
                        pp_demo={'base':base,'base_model':lgb,'iteration':lc['average'][1],
                            'threshold_model':model,'method':meta['method'],'objective':meta['objective'],
                            'representation':rep,'clusterer':discoveries[('c',rep,k)][0]}
            pd.DataFrame(pp_rows).to_csv(output/'postprocess_results.csv',index=False)
            pd.DataFrame(pp_thresholds).to_csv(output/'postprocess_thresholds.csv',index=False)
            save_json(output/'postprocess_audit.json',pp_audits)
            with ResourceMonitor() as jr:
                jc,jw,jhistory=choose_jtt(xt,train,xv,val,vg,config,seed,erm_checkpoints['average'][2])
            jtt_history.extend(jhistory);record('JTT','none',0,jc,jr.seconds,jr.peak_mb,extra={'jtt_upweight':jw})
            methods=[]
            for variant in config.dro_variants:
                definition='cy' if variant.startswith('cy') else 'c'
                for k in config.ks:
                    # cy คงกลุ่มสุ่มต่อคลาสเดิม; c สุ่มโดยไม่รับ y
                    random=np.random.default_rng(seed+k).integers(k,size=len(xt))
                    random_val=np.random.default_rng(seed+k+10000).integers(k,size=len(xv))
                    if definition=='cy':
                        random=train['y']*k+random
                        random_val=val['y']*k+random_val
                    methods.append((variant,f'GDRO-random-k{k}','random',k,random,random_val,{},0))
                for (d,rep,k),(_,labels,rec,seconds) in discoveries.items():
                    if d!=definition or (rep=='GEORGE' and k!=selected[(d,rep)]): continue
                    name=f'GDRO-{rep}-k{k}' if rep in ['raw','scarf'] else rep
                    methods.append((variant,name,rep,k,labels['train'],labels['val'],rec,seconds))
                methods.append((variant,'HBAC','HBAC',hbac.n_clusters_,hlabels['train'],hlabels['val'],hrec,hr.seconds))
                methods.append((variant,'GDRO-geoproxy','geoproxy',4,geo_labels['train'],geo_labels['val'],geo_score,geo_r.seconds))
                _,oracle=np.unique(train['s'].intersection.to_numpy(),return_inverse=True)
                methods.append((variant,'GDRO-oracle','oracle',len(np.unique(oracle)),oracle,vg,{},0))
            audit['dro_merges']=[];variant_candidates={};demo_candidates={}
            for variant,method,rep,k,base_groups,val_clusters,alignment,seconds in methods:
                definition='cy' if variant.startswith('cy') else 'c'
                print(f'  {seed}: {method} / {variant}',flush=True)
                with ResourceMonitor() as mr:
                    merge_space=reps[rep]['train'] if rep in reps else xt
                    groups,merge=make_dro_groups(merge_space,base_groups,config.min_dro_group,definition,
                                                 train['y'] if definition=='cy' else None)
                    weights=balanced_cluster_weights(base_groups if definition=='cy' else groups,train['y']) if variant.endswith('_bal') else None
                    inferred_val=validation_groups(val_clusters,val['y'],definition)
                    audit['dro_merges'].append({'method':method,'dro_variant':variant,**merge,
                        'class_weight_split':'train' if weights is not None else 'none',
                        'validation_group_counts':{str(g):int((inferred_val==g).sum()) for g in np.unique(inferred_val)}})
                    add_fit(f'dro_merge_{method}_{variant}',train['ids'])
                    checkpoints,chosen,history=choose_dro(xt,train['y'],xv,val['y'],vg,groups,erm,config,seed,method,
                        inferred_val_groups=inferred_val,inferred_min_size=config.min_fair_group if rep=='oracle' else 1,
                        variant=variant,sample_weights=weights)
                dro_history.extend(history)
                metrics={a:b for a,b in alignment.items() if a.startswith(('ari_','nmi_','silhouette','davies_bouldin','n_clusters'))}
                is_proposed=rep in ['raw','scarf'] and (rep,k)==main_pairs[definition]
                record(method,rep,k,checkpoints,mr.seconds+er.seconds,mr.peak_mb,metrics,seconds,
                    extra={'n_dro_groups':len(np.unique(groups)),'n_dro_groups_before_merge':merge['n_groups_before'],
                           'dro_warm_start':True,'min_dro_group':config.min_dro_group,'dro_variant':variant,
                           'group_definition':definition,'class_balanced':weights is not None,
                           'class_weight_min':float(weights.min()) if weights is not None else 1.,
                           'class_weight_max':float(weights.max()) if weights is not None else 1.,
                           'selected_without_demographics':selected.get((definition,rep))==k or rep in ['HBAC','geoproxy'],
                           'proposed_selected':is_proposed})
                cp=checkpoints['inferred_worst_group'][0]
                variant_candidates[(method,variant)]=cp.selection_metadata_
                if seed==config.seeds[0] and is_proposed:
                    demo_candidates[variant]={'guard':guard,'processor':processor,'erm':erm,'fair':cp,
                        'selection':'inferred_worst_group','dro_variant':variant,'group_definition':definition,
                        'representation':rep,'scarf':scarf,'scarf_scaler':scarf_scaler,'clusterer':discoveries[(definition,rep,k)][0],
                        'defaults':{c:float(train['x'][c].median()) if pd.api.types.is_numeric_dtype(train['x'][c]) else train['x'][c].mode().iloc[0] for c in train['x']},
                        'method':method,'seed':seed}
            # การเปรียบเทียบนี้อ่านเฉพาะ validation metadata ไม่อ่านตัวชี้วัด test ที่ record แล้ว
            def variant_rank(key):
                meta=variant_candidates[key]
                return selection_rank('inferred_worst_group',meta,meta['accuracy_floor'])
            best_variants={method:max([key for key in variant_candidates if key[0]==method],key=variant_rank)[1]
                           for method,_ in variant_candidates}
            proposed_keys=[(f'GDRO-{main_pairs["cy" if v.startswith("cy") else "c"][0]}-k{main_pairs["cy" if v.startswith("cy") else "c"][1]}',v)
                           for v in config.dro_variants]
            best_proposed=max(proposed_keys,key=variant_rank)
            for row in rows:
                if row['seed']!=seed or row['dro_variant']=='none': continue
                row['variant_selected_without_demographics']=row['representation']!='oracle' and row['dro_variant']==best_variants[row['method']]
                row['proposed_variant_selected']=(row['method'],row['dro_variant'])==best_proposed
            if seed==config.seeds[0]: demo_bundle=demo_candidates[best_proposed[1]]
            for row in rows:
                if row['seed']==seed: row['mlflow_run_id']=log_row(row,env['libraries'],config)
            for row in pp_rows:
                if row['seed']==seed: row['mlflow_run_id']=log_row(row,env['libraries'],config,kind='postprocess')
            pd.DataFrame(pp_rows).to_csv(output/'postprocess_results.csv',index=False)
            audits.append(audit)
            pd.DataFrame(rows).to_csv(output/'hmda_pilot_results.csv',index=False)
            pd.DataFrame(clusters).to_csv(output/'clustering_results.csv',index=False)
            pd.DataFrame(dro_history).to_csv(output/'dro_grid.csv',index=False)
            save_json(output/'leakage_audit.json',{'scope':'train-only per seed','seeds':audits})
        export_explanations(output,explanations,feature_tests)
        pd.DataFrame(resources).to_csv(output/'representation_resources.csv',index=False)
        pd.DataFrame(jtt_history).to_csv(output/'jtt_validation_grid.csv',index=False)
        from .demo import save_bundle
        demo_bundle['postprocess']=pp_demo
        save_bundle(output,demo_bundle)
        from .hmda_reporting import generate_reports
        generate_reports(output)
    env.update(wall_seconds=time.perf_counter()-start,peak_process_rss_mb=overall.peak_mb,decision_rows=len(rows),
               clustering_rows=len(clusters),completed=True,colab_runtime_verified=False,hbac_backend='unsupervised-bias-detection 0.2.6')
    env.update(postprocess_rows=len(pp_rows),postprocess_fit_seconds=sum(r['threshold_fit_seconds'] for r in pp_rows),
               postprocess_accuracy_tolerance=config.selection_accuracy_tolerance,
               postprocess_search='parity interval bisection 20 steps; EO coordinate descent 10 sweeps, two starts')
    after={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    env.update(new_files=len(after-before),total_files=len(after),new_file_limit=200,
               max_new_files_completed_runs=max(prior_env.get('max_new_files_completed_runs',prior_env.get('new_files',0)),len(after-before)))
    pd.DataFrame([{k:env[k] for k in ['wall_seconds','peak_process_rss_mb','decision_rows','clustering_rows','new_files','total_files','max_new_files_completed_runs']}]).to_csv(output/'runtime_summary.csv',index=False)
    assert env['new_files']<=200,env['new_files']
    save_json(output/'environment.json',env)
    print(f"DONE: {len(rows)} decision rows; {env['wall_seconds']:.2f} s; peak RSS {overall.peak_mb:.1f} MiB; new files {env['new_files']}",flush=True)
    return env
