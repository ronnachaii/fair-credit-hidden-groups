"""SQLite เก็บ params/metrics/tags โดยไม่มี artifact รายรัน"""
from pathlib import Path
import numpy as np
import mlflow


def setup_tracking(root):
    import os
    os.environ.setdefault('MLFLOW_ENABLE_TELEMETRY', 'false')
    root = Path(root).resolve()
    mlflow.set_tracking_uri('sqlite:///' + str(root / 'mlflow.db'))
    client = mlflow.tracking.MlflowClient()
    name = 'hmda-hidden-groups-pilot'
    exp = client.get_experiment_by_name(name)
    if exp is None:
        exp_id = client.create_experiment(name, artifact_location=(root/'results'/'no_run_artifacts').as_uri())
    else:
        exp_id = exp.experiment_id
    mlflow.set_experiment(experiment_id=exp_id)


def log_row(row, versions, config, kind='decision'):
    keys = ['method','representation','k','label_fraction','seed','selection','selected_epoch','n_train','n_test',
            'dro_variant','group_definition','class_balanced','base','objective','fit_split']
    with mlflow.start_run(run_name=f"{kind}-{row.get('method', row.get('representation','none'))}-{row['seed']}") as run:
        mlflow.set_tags({'kind':kind,'dataset':config.dataset,'state':config.state,'artifact_policy':'none'})
        mlflow.log_params({k:row[k] for k in keys if k in row})
        mlflow.log_params({f'version_{k}':v for k,v in versions.items()})
        mlflow.log_params({f'config_{k}':str(v) for k,v in config.to_dict().items()})
        mlflow.log_metrics({k:float(v) for k,v in row.items() if isinstance(v,(int,float,np.number)) and np.isfinite(v)})
        return run.info.run_id
