"""ตรวจผล HMDA, MLflow SQLite, Gradio, notebook และ fallback ในโฟลเดอร์ว่าง"""
import hashlib
import os
import json
import subprocess
import sys
import tempfile
from pathlib import Path
if sys.platform == "darwin":
    os.environ["OMP_NUM_THREADS"]="1"
os.environ["MLFLOW_DISABLE_AGENT_HINT"]="1"
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'tools')]
from build_notebook import validate
from fairgroups.tracking import setup_tracking
import mlflow


def check_postprocess(results, env):
    """ตรวจเกณฑ์/การเลือกซ้ำจาก validation และจับคู่ฐานทุก seed"""
    from fairgroups.postprocess import selection_key
    from fairgroups.postprocess_reporting import sanity_table, METRICS
    pp=pd.read_csv(results/'postprocess_results.csv')
    thresholds=pd.read_csv(results/'postprocess_thresholds.csv')
    assert len(pp)==54*len(env['seeds'])==env['postprocess_rows']
    assert not pp.duplicated(['base','seed','method','objective']).any()
    assert np.isfinite(pp[METRICS].to_numpy()).all()
    candidates=pp[~pp.objective.eq('baseline')]
    assert candidates.accuracy_guard_passed.all()
    assert (candidates.validation_accuracy>=candidates.validation_accuracy_floor-1e-12).all()
    assert candidates.group_definition.eq('c').all()
    assert thresholds[thresholds.frozen_small_group].threshold.eq(.5).all()
    assert thresholds.fit_split.eq('validation').all()
    assert thresholds.unseen_group_threshold.eq(.5).all()
    for (base,seed),part in pp.groupby(['base','seed']):
        assert part.auroc.nunique()==1
        for flag,reps in [('proposed_selected',['raw','scarf']),
                          ('selected_without_demographics',['raw','scarf','GEORGE','HBAC','geoproxy'])]:
            chosen=part[part[flag]]
            assert len(chosen)==1
            best=min(part[part.representation.isin(reps)].to_dict('records'),key=selection_key)
            assert chosen.iloc[0]['method']==best['method'] and chosen.iloc[0]['objective']==best['objective']
        for row in part[~part.objective.eq('baseline')].itertuples():
            group=thresholds[(thresholds.base==base)&(thresholds.seed==seed)&
                (thresholds.method==row.method)&(thresholds.objective==row.objective)]
            assert len(group)==row.n_validation_groups
        old=pd.read_csv(results/'hmda_pilot_results.csv')
        ref=old[(old.method==base)&(old.seed==seed)&old.selection.eq('average')].iloc[0]
        pp_base=part[part.objective.eq('baseline')].iloc[0]
        np.testing.assert_allclose(ref[METRICS].to_numpy(dtype=float),pp_base[METRICS].to_numpy(dtype=float))
    audit=json.loads((results/'postprocess_audit.json').read_text())
    original=json.loads((results/'leakage_audit.json').read_text())['seeds']
    for entry in audit:
        split=next(a for a in original if a['seed']==entry['seed'])
        assert set(entry['threshold_fit_ids'])==set(split['val_ids'])
        assert set(entry['threshold_fit_ids']).isdisjoint(split['train_ids']+split['test_ids'])
        assert not entry['selection_uses_demographics'] and entry['oracle_excluded_from_selection']
    pd.testing.assert_frame_equal(sanity_table(pp),pd.read_csv(results/'postprocess_sanity.csv'))
    oracle=sanity_table(pp).query("representation == 'oracle'").groupby('base').race_gap_reduction.mean()
    assert oracle.gt(0).all(), 'oracle parity ไม่ลด race gap ต้องตรวจบั๊กก่อนส่งงาน'
    assert (results/'figures/postprocess_tradeoff.png').stat().st_size>10000
    for row in pp.to_dict('records'):
        run=mlflow.tracking.MlflowClient().get_run(row['mlflow_run_id'])
        assert run.info.status=='FINISHED' and run.data.params['base']==row['base']
        assert not mlflow.tracking.MlflowClient().list_artifacts(row['mlflow_run_id'])
    snapshot=results/'round5/snapshot_sha256.json'
    if snapshot.exists():
        for relative,checksum in json.loads(snapshot.read_text()).items():
            assert hashlib.sha256((snapshot.parent/relative).read_bytes()).hexdigest()==checksum
        old=pd.read_csv(snapshot.parent/'hmda_pilot_results.csv')
        current=pd.read_csv(results/'hmda_pilot_results.csv')
        keys=['seed','method','selection','dro_variant']
        pd.testing.assert_frame_equal(old.sort_values(keys)[keys+METRICS].reset_index(drop=True),
            current.sort_values(keys)[keys+METRICS].reset_index(drop=True))
    return {'rows':len(pp),'threshold_rows':len(thresholds),
        'all_validation_guards_passed':True,'oracle_race_gap_reduction':oracle.to_dict(),
        'selection_recomputed_without_demographics':True,'threshold_validation_ids_checked':len(audit),
        'round5_snapshot_and_predictive_metrics_preserved':snapshot.exists()}


def main():
    results=ROOT/'results';env=json.loads((results/'environment.json').read_text())
    df=pd.read_csv(results/'hmda_pilot_results.csv');clusters=pd.read_csv(results/'clustering_results.csv')
    setup_tracking(ROOT)
    pp_validation=check_postprocess(results,env)
    assert len(df)==163*len(env['seeds'])==env['decision_rows']
    assert not df.duplicated(['method','seed','selection','dro_variant']).any()
    required=['accuracy','precision','recall','f1','auroc','eo_gap','dp_difference','worst_group_accuracy',
              'approval_rate_gap_race_eth','approval_rate_gap_sex','train_seconds','inference_seconds_per_1000','peak_memory_mb']
    assert np.isfinite(df[required].to_numpy()).all()
    assert df.label_fraction.eq(1.).all()
    assert len(clusters)==20*len(env['seeds'])
    grid=pd.read_csv(results/'dro_grid.csv')
    from fairgroups.models import selection_rank
    from fairgroups.hmda_reporting import main_rows,oracle_sanity
    cfg=env['config']
    n_candidates=np.prod([len(cfg[key]) for key in ['dro_eta_grid','dro_adjustment_grid','dro_learning_rate_grid','dro_epoch_grid']])
    assert len(grid)==13*4*n_candidates*3*len(env['seeds'])
    assert set(grid.selection)=={'average','worst_group','inferred_worst_group'}
    assert grid.selection.eq(grid.selection_metric).all()
    assert grid.final_group_weight_min.gt(0).all()
    assert grid.final_group_weight_max.ge(grid.final_group_weight_min).all()
    assert grid.final_group_weight_max.le(1).all()
    assert grid.final_parameter_l2_from_erm.gt(0).all() and grid.parameter_l2_from_erm.gt(0).all()
    assert set(grid.dro_variant)==set(cfg['dro_variants'])
    for (seed,method,selection,variant),part in grid.groupby(['seed','method','selection','dro_variant']):
        assert len(part)==n_candidates and part.selected.sum()==1
        def rank(r):
            return selection_rank(selection,{'average':r.validation_accuracy,
                'worst_group':r.validation_true_worst_group,
                'inferred_worst_group':r.validation_inferred_worst_group},r.accuracy_floor)
        chosen=part[part.selected].iloc[0]
        assert rank(chosen)==max(rank(r) for r in part.itertuples())
        if selection=='inferred_worst_group':
            assert bool(chosen.accuracy_guard_passed)==bool(part.accuracy_guard_passed.any())
        row=df[(df.seed==seed)&(df.method==method)&(df.selection==selection)&df.dro_variant.eq(variant)].iloc[0]
        assert row.dro_eta==chosen.dro_eta and row.dro_adjustment==chosen.C
        assert row.dro_learning_rate==chosen.learning_rate and row.dro_finetune_epochs==chosen.finetune_epochs
        assert row.selected_epoch==chosen.selected_epoch
        assert np.isclose(row.validation_selection_score,chosen.validation_selection_score)
        assert np.isclose(row.validation_average_accuracy,chosen.validation_accuracy)
        assert bool(row.accuracy_guard_passed)==bool(chosen.accuracy_guard_passed)
        assert np.isclose(chosen.accuracy_floor,chosen.erm_validation_accuracy-cfg['selection_accuracy_tolerance'])
        assert chosen.validation_group_source==('true intersection' if method=='GDRO-oracle' else 'inferred cluster') + (' x y' if variant.startswith('cy') else '')
    main=main_rows(df)
    # เลือก variant ซ้ำจาก validation เท่านั้น แล้วเทียบ flag ที่ pipeline บันทึก
    def vrank(r):
        return selection_rank('inferred_worst_group',{'average':r.validation_average_accuracy,
            'inferred_worst_group':r.validation_selection_score},r.validation_accuracy_floor)
    for seed,part in main[main.proposed_selected].groupby('seed'):
        assert len(part)==4 and part.dro_variant.nunique()==4
        best=max(part.itertuples(),key=vrank)
        marked=part[part.proposed_variant_selected]
        assert len(marked)==1 and marked.iloc[0].dro_variant==best.dro_variant
        # ยืนยันว่า representation/k ใช้เฉพาะ silhouette train ในแต่ละนิยาม
        for r in part.itertuples():
            subset=clusters[(clusters.seed==seed)&clusters.group_definition.eq(r.group_definition)&
                            clusters.representation.isin(['raw','scarf'])]
            winner=subset.loc[subset.silhouette.idxmax()]
            assert r.representation==winner.representation and r.k==winner.k
    for (seed,method),part in main[~main.representation.isin(['none','oracle'])].groupby(['seed','method']):
        assert len(part)==4
        best=max(part.itertuples(),key=vrank)
        marked=part[part.variant_selected_without_demographics]
        assert len(marked)==1 and marked.iloc[0].dro_variant==best.dro_variant
    assert len(main)==55*len(env['seeds'])
    assert main[main.method.str.startswith('ERM-')].selection.eq('average').all()
    jtt=pd.read_csv(results/'jtt_validation_grid.csv')
    for (seed,selection),part in jtt.groupby(['seed','selection']):
        assert len(part)==len(cfg['jtt_grid']) and part.selected.sum()==1
        chosen=part[part.selected].iloc[0]
        def jrank(r):
            return selection_rank(selection,{'average':r.validation_accuracy,selection:r.validation_selection_score},r.accuracy_floor)
        assert jrank(chosen)==max(jrank(r) for r in part.itertuples())
        row=df[(df.seed==seed)&df.method.eq('JTT')&df.selection.eq(selection)].iloc[0]
        assert row.jtt_upweight==chosen.upweight and row.selected_epoch==chosen.selected_epoch
    sanity,oracle_passed,oracle_gain=oracle_sanity(df)
    pd.testing.assert_frame_equal(sanity,pd.read_csv(results/'oracle_sanity.csv'))
    print(f'oracle sanity per variant: {oracle_passed}; mean gains {oracle_gain}',flush=True)
    # ไม่ซ่อน sanity ที่ล้มเหลว: ตรวจรายงานให้ตรงผลจริง แล้วบันทึกสถานะแยกจาก delivery
    summary=(results/'hmda_pilot_summary.md').read_text()
    for variant,passed in oracle_passed.items():
        assert f"- {variant}: {'ผ่าน' if passed else 'ไม่ผ่าน'};" in summary
    cards=pd.read_csv(results/'group_explanations.csv')
    assert cards[['fidelity_f1','fidelity_precision','fidelity_recall']].ge(0).all().all()
    assert cards[['fidelity_f1','fidelity_precision','fidelity_recall']].le(1).all().all()
    np.testing.assert_allclose(cards.fidelity_f1,cards[['fidelity_f1_balanced','fidelity_f1_unbalanced']].max(axis=1))
    assert cards.surrogate_selection_split.eq('validation').all()
    assert cards.surrogate_class_weight.eq(np.where(cards.fidelity_f1_balanced>=cards.fidelity_f1_unbalanced,'balanced','unbalanced')).all()
    assert cards.fallback_split.eq('train').all() and cards.max_conditions_per_path.le(3).all()
    for row in cards[cards.fidelity_f1<.5].to_dict('records'):
        from fairgroups.explanations import card_text
        assert 'กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี' in card_text(row)
        assert 3<=len(json.loads(row['fallback_features']))<=5
    audit=json.loads((results/'leakage_audit.json').read_text())
    for seed in audit['seeds']:
        assert len(seed['dro_merges'])==52
        for merge in seed['dro_merges']:
            assert merge['fit_split']=='train'
            if merge['group_definition']=='cy':
                for group in {r['dro_group'] for r in merge['mapping']}:
                    assert len({r['y'] for r in merge['mapping'] if r['dro_group']==group})==1
            else:
                assert all('y' not in r for r in merge['mapping'])
            assert merge['undersized_remaining']==0
    setup_tracking(ROOT);client=mlflow.tracking.MlflowClient()
    for row in df.to_dict('records'):
        run=client.get_run(row['mlflow_run_id'])
        assert run.info.status=='FINISHED' and int(run.data.params['seed'])==row['seed']
        assert run.data.params['dro_variant']==row['dro_variant']
        assert not client.list_artifacts(row['mlflow_run_id'])
    from fairgroups.hmda_reporting import generate_reports
    before=(results/'hmda_pilot_summary.md').read_bytes();generate_reports(results)
    assert before==(results/'hmda_pilot_summary.md').read_bytes()
    from fairgroups.demo import load_bundle,predict_application,build_interface
    print('checking demo build and prediction',flush=True)
    bundle=load_bundle(results);prediction=predict_application(bundle,*[bundle['defaults'][c] for c in bundle['inputs']])
    assert bundle['selection']=='inferred_worst_group'
    selected_demo=main[(main.seed==env['seeds'][0])&main.proposed_variant_selected].iloc[0]
    assert bundle['dro_variant']==selected_demo.dro_variant and bundle['method']==selected_demo.method
    assert (results/'figures/dro_variants.png').stat().st_size>10000

    assert prediction[0]['กลุ่ม'] in bundle['cards']
    assert 'เกณฑ์รายกลุ่ม' in prediction[0] and bundle['postprocess']['base']=='ERM-LGBM'
    interface=build_interface(results);assert callable(interface.fn)
    validation={'decision_rows':len(df),'clustering_rows':len(clusters),'finished_mlflow_runs_checked':len(df),
                'per_run_artifacts':0,'summary_rebuilt_identically_from_csv':True,
                'notebook':validate(ROOT/'notebooks/pilot_colab.ipynb'),'demo_prediction':prediction[0],
                'gradio_interface_built':True,'colab_live_test':False}
    validation['postprocess']=pp_validation
    validation.update(oracle_sanity_passed=oracle_passed,oracle_mean_worst_group_gain=oracle_gain,
                      primary_guard_failures=main[main.selection.eq('inferred_worst_group')].accuracy_guard_passed.eq(False).sum().item(),
                      dro_grid_candidates_checked=int(len(grid)//3),dro_grid_selection_rows_checked=len(grid),low_fidelity_cards_with_fallback=int(cards.fidelity_f1.lt(.5).sum()),
                      dro_merge_audits_checked=sum(len(a['dro_merges']) for a in audit['seeds']))
    notebook=json.loads((ROOT/'notebooks/pilot_colab.ipynb').read_text())
    with tempfile.TemporaryDirectory(prefix='.fallback-check-',dir=ROOT) as folder:
        for item in notebook['cells']:
            source=''.join(item['source'])
            if source.startswith('%%writefile '):
                header,body=source.split('\n',1);path=Path(folder)/header.removeprefix('%%writefile ')
                path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)
        help_result=subprocess.run([sys.executable,'run_pilot.py','--help'],cwd=folder,capture_output=True,text=True,check=True)
        print('checking notebook fallback tests',flush=True)
        test_result=subprocess.run([sys.executable,'-m','pytest','tests','-q'],cwd=folder,capture_output=True,text=True,check=True)
        validation.update(fallback_cli_help_passed='--quick' in help_result.stdout,fallback_tests=test_result.stdout.strip())
        # โฟลเดอร์เริ่มว่าง มีเพียงไฟล์ฝัง notebook; ใช้แคชเดียวกันเพื่อไม่ดาวน์โหลดใน sandbox
        cached=ROOT/'data'/'hmda'/'hmda_2023_GA.csv'
        if cached.exists():
            cache_dest=Path(folder)/'data'/'hmda';cache_dest.mkdir(parents=True,exist_ok=True)
            (cache_dest/cached.name).symlink_to(cached)
            print('checking notebook fallback full QUICK with local cache',flush=True)
            pilot=subprocess.run([sys.executable,'run_pilot.py','--quick'],cwd=folder,capture_output=True,text=True,check=True)
            (results/'fallback_pilot.log').write_text(pilot.stdout+pilot.stderr)
            fallback_env=json.loads((Path(folder)/'results'/'environment.json').read_text())
            assert fallback_env['completed'] and fallback_env['decision_rows']==163*len(env['seeds'])
            repeated=pd.read_csv(Path(folder)/'results'/'hmda_pilot_results.csv')
            fallback_pp=pd.read_csv(Path(folder)/'results'/'postprocess_results.csv')
            main_pp=pd.read_csv(results/'postprocess_results.csv')
            pp_keys=['base','seed','method','objective']
            pp_columns=pp_keys+['accuracy','f1','auroc','positive_rate','approval_rate_gap_race_eth',
                'approval_rate_gap_sex','eo_gap','worst_group_accuracy','validation_accuracy',
                'validation_approval_gap','validation_eo_gap','accuracy_guard_passed',
                'proposed_selected','selected_without_demographics']
            pd.testing.assert_frame_equal(main_pp.sort_values(pp_keys)[pp_columns].reset_index(drop=True),
                fallback_pp.sort_values(pp_keys)[pp_columns].reset_index(drop=True))
            pd.testing.assert_frame_equal(pd.read_csv(results/'postprocess_thresholds.csv'),
                pd.read_csv(Path(folder)/'results'/'postprocess_thresholds.csv'))
            validation['fallback_postprocess_metrics_and_thresholds_match']=True
            keys=['seed','method','selection','dro_variant']
            metrics=['accuracy','eo_gap','worst_group_accuracy','selected_epoch','positive_rate','jtt_upweight',
                     'dro_eta','dro_adjustment','dro_learning_rate','dro_finetune_epochs','n_dro_groups',
                     'validation_selection_score','validation_average_accuracy','accuracy_guard_passed','parameter_l2_from_erm',
                     'class_weight_min','class_weight_max','proposed_selected','proposed_variant_selected','variant_selected_without_demographics']
            pd.testing.assert_frame_equal(df.sort_values(keys)[keys+metrics].reset_index(drop=True),
                                          repeated.sort_values(keys)[keys+metrics].reset_index(drop=True))
            validation['fallback_predictive_metrics_match_main_run']=True
            pd.testing.assert_frame_equal(cards,pd.read_csv(Path(folder)/'results'/'group_explanations.csv'))
            pd.testing.assert_frame_equal(grid,pd.read_csv(Path(folder)/'results'/'dro_grid.csv'))
            validation.update(fallback_explanations_match_main_run=True,fallback_dro_grid_matches_main_run=True)
            validation.update(fallback_quick_pipeline_completed=True,fallback_quick_seconds=fallback_env['wall_seconds'],
                              fallback_data_source='existing HMDA cache symlink; no network/download/install tested')
            post=subprocess.run([sys.executable,'-m','pytest','tests','-q'],cwd=folder,capture_output=True,text=True,check=True)
            validation['fallback_post_pilot_tests']=post.stdout.strip()
            (results/'fallback_post_pilot_tests.log').write_text(post.stdout+post.stderr)
        (results/'fallback_tests.log').write_text(test_result.stdout+test_result.stderr)
    paths=[ROOT/'config.py',ROOT/'requirements.txt',ROOT/'run_pilot.py']+[p for p in (ROOT/'src').rglob('*.py') if not p.name.startswith('._')]
    validation['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    # นับรวม AppleDouble ทุกไฟล์ และแยกไฟล์จริงให้ตรวจ exFAT ได้
    files=[p for p in ROOT.rglob('*') if p.is_file()]
    validation.update(total_files_including_appledouble=len(files),content_files=sum(not p.name.startswith('._') for p in files),
                      pilot_new_files=env['new_files'],pilot_new_files_within_limit=env['new_files']<=200)
    assert validation['pilot_new_files_within_limit']
    (results/'validation.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False))
    print(json.dumps({k:v for k,v in validation.items() if k!='source_sha256'},indent=2,ensure_ascii=False))


if __name__=='__main__':
    from threadpoolctl import threadpool_limits
    with threadpool_limits(limits=1): main()
