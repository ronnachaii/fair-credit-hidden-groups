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


def main():
    results=ROOT/'results';env=json.loads((results/'environment.json').read_text())
    df=pd.read_csv(results/'hmda_pilot_results.csv');clusters=pd.read_csv(results/'clustering_results.csv')
    assert len(df)==16*2*len(env['seeds'])==env['decision_rows']
    assert not df.duplicated(['method','seed','selection']).any()
    required=['accuracy','precision','recall','f1','auroc','eo_gap','dp_difference','worst_group_accuracy',
              'approval_rate_gap_race_eth','approval_rate_gap_sex','train_seconds','inference_seconds_per_1000','peak_memory_mb']
    assert np.isfinite(df[required].to_numpy()).all()
    assert df.label_fraction.eq(1.).all()
    assert len(clusters)==11*len(env['seeds'])
    setup_tracking(ROOT);client=mlflow.tracking.MlflowClient()
    for row in df.to_dict('records'):
        run=client.get_run(row['mlflow_run_id'])
        assert run.info.status=='FINISHED' and int(run.data.params['seed'])==row['seed']
        assert not client.list_artifacts(row['mlflow_run_id'])
    from fairgroups.hmda_reporting import generate_reports
    before=(results/'hmda_pilot_summary.md').read_bytes();generate_reports(results)
    assert before==(results/'hmda_pilot_summary.md').read_bytes()
    from fairgroups.demo import load_bundle,predict_application,build_interface
    print('checking demo build and prediction',flush=True)
    bundle=load_bundle(results);prediction=predict_application(bundle,*[bundle['defaults'][c] for c in bundle['inputs']])
    assert prediction[0]['กลุ่ม'] in bundle['cards']
    interface=build_interface(results);assert callable(interface.fn)
    validation={'decision_rows':len(df),'clustering_rows':len(clusters),'finished_mlflow_runs_checked':len(df),
                'per_run_artifacts':0,'summary_rebuilt_identically_from_csv':True,
                'notebook':validate(ROOT/'notebooks/pilot_colab.ipynb'),'demo_prediction':prediction[0],
                'gradio_interface_built':True,'colab_live_test':False}
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
            assert fallback_env['completed'] and fallback_env['decision_rows']==96
            repeated=pd.read_csv(Path(folder)/'results'/'hmda_pilot_results.csv')
            keys=['seed','method','selection']
            metrics=['accuracy','eo_gap','worst_group_accuracy','selected_epoch','positive_rate','jtt_upweight']
            pd.testing.assert_frame_equal(df.sort_values(keys)[keys+metrics].reset_index(drop=True),
                                          repeated.sort_values(keys)[keys+metrics].reset_index(drop=True))
            validation['fallback_predictive_metrics_match_main_run']=True
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
