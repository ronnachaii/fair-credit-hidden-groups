"""SQLite ต้องอ่านผลกลับได้ และไม่มี artifact รายรัน"""
import mlflow
from fairgroups.tracking import setup_tracking, log_row
from config import Config


def test_sqlite_tracking_has_no_per_run_artifacts(tmp_path):
    setup_tracking(tmp_path)
    run_id=log_row({'seed':17,'representation':'raw','method':'test','accuracy':.75},{},Config())
    fetched=mlflow.get_run(run_id)
    assert fetched.data.metrics['accuracy']==.75
    assert fetched.data.params['seed']=='17'
    assert fetched.info.status=='FINISHED'
    assert mlflow.get_tracking_uri().startswith('sqlite:///')
    assert not mlflow.tracking.MlflowClient().list_artifacts(run_id)
    assert len([p for p in tmp_path.rglob('*') if p.is_file() and not p.name.startswith('._')])<=3
