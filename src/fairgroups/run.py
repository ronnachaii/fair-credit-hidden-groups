"""HMDA pilot ต่อยอดโมดูลเดิม: train-only discovery และ full labels เท่านั้น"""
import json
import time
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from lightgbm import LGBMClassifier
from .hmda import load_hmda, split_hmda, LeakageGuard, HMDAPreprocessor, write_profile
from .hmda_groups import ClassClusters, GeoGroups, hidden, fit_hbac, group_scores
from .models import set_seed, train_mlp, predict_mlp, validation_scores
from .representations import train_scarf, encode_scarf
from .efficiency import ResourceMonitor, network_cost, inference_seconds, environment
from .metrics import evaluate
from .tracking import setup_tracking, log_row
from .explanations import describe_groups, export_explanations


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


def choose_jtt(xt,train,xv,val,vg,config,seed):
    """กริดเล็ก เลือกด้วย average accuracy; รายงาน collapse ทุก candidate"""
    _, identification=train_mlp(xt,train['y'],xv,val['y'],vg,config,seed,epochs=config.jtt_identification_epochs)
    mistakes=(predict_mlp(identification,xt)>=.5)!=train['y']
    candidates=[]; history=[]
    for weight in config.jtt_grid:
        checkpoints,_=train_mlp(xt,train['y'],xv,val['y'],vg,config,seed,
                                sample_weights=np.where(mistakes,weight,1.))
        p=predict_mlp(checkpoints['average'][0],xv); rate=float((p>=.5).mean())
        collapsed=rate<=.005 or rate>=.995
        history.append({'seed':seed,'upweight':weight,'validation_accuracy':checkpoints['average'][2],
                        'positive_rate':rate,'collapsed':collapsed,'n_mistakes':int(mistakes.sum())})
        candidates.append((checkpoints['average'][2],weight,checkpoints))
    # ใช้ accuracy เป็นกติกาหลักตรงกันทุกวิธี ไม่เลือกจาก fairness หรือ test
    score,weight,chosen=max(candidates,key=lambda t:t[0])
    selected=next(h for h in history if h['upweight']==weight)
    if selected['collapsed']: warnings.warn('JTT validation ทายข้างเดียว อ่าน accuracy และ rate ควบคู่')
    return chosen,weight,history


def run_experiment(config,root='.'):
    root=Path(root).resolve(); output=root/'results';output.mkdir(exist_ok=True)
    start=time.perf_counter(); set_seed(config.seeds[0],config.threads)
    before={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    prior_env=json.loads((output/'environment.json').read_text()) if (output/'environment.json').exists() else {}
    env=environment(config); setup_tracking(root)
    rows=[];clusters=[];resources=[];audits=[];explanations=[];feature_tests=[];jtt_history=[];demo_bundle=None
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
            # กลุ่มจริงใช้เลือกเฉพาะผล worst_group ที่รายงานแยก; average ไม่แตะข้อมูลนี้
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
            for rep_name,rep in reps.items():
                for k in config.ks:
                    with ResourceMonitor() as cr:
                        km=ClassClusters().fit(rep['train'],train['y'],train['ids'],k,seed)
                        labels={'train':km.labels_,**{n:km.predict(rep[n]) for n in ['val','test']}}
                        # k เลือกจาก train เท่านั้น; ARI/NMI test เก็บภายหลังเพื่อประเมิน
                        scores=group_scores(rep['train'],labels['train'],train['s'],seed)
                        alignment=group_scores(rep['test'],labels['test'],test['s'],seed)
                    add_fit(f'class_kmeans_{rep_name}_{k}',km.fit_ids_)
                    seconds=cr.seconds+(sr.seconds if rep_name=='scarf' else er.seconds+gr.seconds if rep_name=='GEORGE' else 0)
                    rec={'seed':seed,'representation':rep_name,'k':k,'silhouette':scores['silhouette'],
                         'davies_bouldin':scores['davies_bouldin'],'n_clusters':scores['n_clusters'],
                         **{key:value for key,value in alignment.items() if key.startswith(('ari_','nmi_','alignment_'))},
                         'discovery_train_seconds':seconds,'assignment':'nearest center across classes without y'}
                    clusters.append(rec);discoveries[(rep_name,k)]=(km,labels,rec,seconds)
                selected[rep_name]=max(config.ks,key=lambda k:discoveries[(rep_name,k)][2]['silhouette'])
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
            clusters.append(hrec);discoveries[('HBAC',hbac.n_clusters_)]=(hbac,labels,hrec,hr.seconds)
            selected['HBAC']=hbac.n_clusters_
            resources.append({'seed':seed,'representation':'HBAC','discovery_train_seconds':hr.seconds,
                              'peak_memory_mb':hr.peak_mb,'parameters':np.nan,'flops_per_row':np.nan})
            with ResourceMonitor() as geo_r:
                geo_values={n:pd.to_numeric(p['frame'].tract_minority_population_percent,errors='coerce').to_numpy() for n,p in splits.items()}
                geo=GeoGroups().fit(geo_values['train'],train['ids'])
                geo_labels={n:geo.predict(v) for n,v in geo_values.items()}
                geo_score=group_scores(xx,geo_labels['test'],test['s'],seed)
            add_fit('geoproxy_quantiles',geo.fit_ids_)
            clusters.append({'seed':seed,'representation':'geoproxy','k':4,**geo_score,'discovery_train_seconds':geo_r.seconds})
            # อธิบายเฉพาะ k ที่เลือกไว้ โดย test ไม่เคยถูกใช้เลือก
            for rep_name,k in selected.items():
                _,labels,_,_=discoveries[(rep_name,k)]
                method=f'GDRO-{rep_name}-k{k}' if rep_name in ['raw','scarf'] else rep_name
                cards,tests,fit_ids=describe_groups(method,k,seed,train,val,test,labels,predict_mlp(erm,xx),config)
                explanations.extend(cards);feature_tests.extend(tests);add_fit(f'explanation_{rep_name}',fit_ids)
            main_rep,main_k=max([(r,selected[r]) for r in ['raw','scarf']],key=lambda pair:discoveries[pair][2]['silhouette'])
            def record(method,rep,k,checkpoints,seconds,peak,alignment=None,discovery_seconds=0,extra=None):
                for selection,(model,epoch,score) in checkpoints.items():
                    predict=(lambda a,model=model:predict_mlp(model,a)) if method!='ERM-LGBM' else (lambda a,epoch=epoch:model.predict_proba(a,num_iteration=epoch)[:,1])
                    row={'seed':seed,'method':method,'representation':rep,'k':k,'label_fraction':1.,'selection':selection,
                         'selected_epoch':epoch,'validation_selection_score':score,'n_train':len(xt),'n_val':len(xv),'n_test':len(xx),
                         'input_dimension':xt.shape[1],'threshold':.5,'train_seconds':pr.seconds+seconds+discovery_seconds,
                         'decision_train_seconds':seconds,'discovery_train_seconds':discovery_seconds,'peak_memory_mb':max(peak,pr.peak_mb),
                         'selected_without_demographics':(rep in selected and k==selected[rep]) or rep=='geoproxy',
                         'proposed_selected':rep==main_rep and k==main_k,**(alignment or {}),**(extra or {})}
                    row.update(evaluate(test['y'],predict(xx),test['s'],config.min_fair_group))
                    row['inference_seconds_per_1000']=inference_seconds(predict,xx)
                    if method=='ERM-LGBM':
                        trees=model.booster_.dump_model(num_iteration=epoch)['tree_info']
                        row.update(parameters=np.nan,flops_per_row=np.nan,tree_count=len(trees),leaf_count=sum(t['num_leaves'] for t in trees))
                    else: row.update(network_cost(model))
                    row['mlflow_run_id']=log_row(row,env['libraries'],config);rows.append(row)
            record('ERM-MLP','none',0,erm_checkpoints,er.seconds,er.peak_mb)
            with ResourceMonitor() as lr:
                lgb=LGBMClassifier(n_estimators=config.trees,num_leaves=15,max_depth=5,learning_rate=.05,verbosity=-1,
                    n_jobs=config.threads,random_state=seed,deterministic=True,force_col_wise=True)
                lgb.fit(xt,train['y'])
                choices={t:validation_scores(val['y'],lgb.predict_proba(xv,num_iteration=t)[:,1],vg) for t in sorted(set([10,25,50,config.trees]))}
                lc={sel:(lgb,t,choices[t][sel]) for sel in ['average','worst_group'] for t in [max(choices,key=lambda t:choices[t][sel])]}
            record('ERM-LGBM','none',0,lc,lr.seconds,lr.peak_mb)
            with ResourceMonitor() as jr:
                jc,jw,jhistory=choose_jtt(xt,train,xv,val,vg,config,seed)
            jtt_history.extend(jhistory);record('JTT','none',0,jc,jr.seconds,jr.peak_mb,extra={'jtt_upweight':jw})
            methods=[]
            for k in config.ks:
                # ควบคุมจำนวนกลุ่มและการใช้ y ให้เท่ากับวิธีที่จัด k กลุ่มต่อคลาส
                random=train['y']*k+np.random.default_rng(seed+k).integers(k,size=len(xt))
                methods.append((f'GDRO-random-k{k}','random',k,random,{},0))
            for (rep,k),(_,labels,rec,seconds) in discoveries.items():
                if rep=='GEORGE' and k!=selected[rep]: continue
                name=f'GDRO-{rep}-k{k}' if rep in ['raw','scarf'] else rep
                methods.append((name,rep,k,labels['train'],rec,seconds))
            methods.append(('GDRO-geoproxy','geoproxy',4,geo_labels['train'],geo_score,geo_r.seconds))
            _,oracle=np.unique(train['s'].intersection.to_numpy(),return_inverse=True)
            # Unknown ไม่ตีความเป็นประชากรที่ยืนยัน; ใช้เป็นกลุ่มฝึกแยกเพื่อไม่ทิ้งแถว
            methods.append(('GDRO-oracle','oracle',len(np.unique(oracle)),oracle,{},0))
            for method,rep,k,groups,alignment,seconds in methods:
                print(f'  {seed}: {method}',flush=True)
                with ResourceMonitor() as mr:
                    checkpoints,_=train_mlp(xt,train['y'],xv,val['y'],vg,config,seed,groups=groups)
                metrics={a:b for a,b in alignment.items() if a.startswith(('ari_','nmi_','silhouette','davies_bouldin','n_clusters'))}
                record(method,rep,k,checkpoints,mr.seconds,mr.peak_mb,metrics,seconds,extra={'n_dro_groups':len(np.unique(groups))})
                if seed==config.seeds[0] and rep==main_rep and k==main_k:
                    demo_bundle={'guard':guard,'processor':processor,'erm':erm,'fair':checkpoints['average'][0],
                        'representation':rep,'scarf':scarf,'scarf_scaler':scarf_scaler,'clusterer':discoveries[(rep,k)][0],
                        'defaults':{c:float(train['x'][c].median()) if pd.api.types.is_numeric_dtype(train['x'][c]) else train['x'][c].mode().iloc[0] for c in train['x']},
                        'method':method,'seed':seed}
            audits.append(audit)
            pd.DataFrame(rows).to_csv(output/'hmda_pilot_results.csv',index=False)
            pd.DataFrame(clusters).to_csv(output/'clustering_results.csv',index=False)
            save_json(output/'leakage_audit.json',{'scope':'train-only per seed','seeds':audits})
        export_explanations(output,explanations,feature_tests)
        pd.DataFrame(resources).to_csv(output/'representation_resources.csv',index=False)
        pd.DataFrame(jtt_history).to_csv(output/'jtt_validation_grid.csv',index=False)
        from .demo import save_bundle
        save_bundle(output,demo_bundle)
        from .hmda_reporting import generate_reports
        generate_reports(output)
    env.update(wall_seconds=time.perf_counter()-start,peak_process_rss_mb=overall.peak_mb,decision_rows=len(rows),
               clustering_rows=len(clusters),completed=True,colab_runtime_verified=False,hbac_backend='unsupervised-bias-detection 0.2.6')
    after={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    env.update(new_files=len(after-before),total_files=len(after),new_file_limit=200,
               max_new_files_completed_runs=max(prior_env.get('max_new_files_completed_runs',prior_env.get('new_files',0)),len(after-before)))
    pd.DataFrame([{k:env[k] for k in ['wall_seconds','peak_process_rss_mb','decision_rows','clustering_rows','new_files','total_files','max_new_files_completed_runs']}]).to_csv(output/'runtime_summary.csv',index=False)
    assert env['new_files']<=200,env['new_files']
    save_json(output/'environment.json',env)
    print(f"DONE: {len(rows)} decision rows; {env['wall_seconds']:.2f} s; peak RSS {overall.peak_mb:.1f} MiB; new files {env['new_files']}",flush=True)
    return env
