"""จุดเริ่มต้นสำหรับ command line และ notebook"""
import argparse
import sys
import os
from pathlib import Path

if sys.platform == "darwin":
    os.environ["OMP_NUM_THREADS"] = "1"
os.environ.setdefault("MLFLOW_DISABLE_AGENT_HINT", "1")

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from config import make_config
from fairgroups.run import run_experiment
from threadpoolctl import threadpool_limits


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HMDA hidden-group fairness pilot (CPU)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true", help="3 seeds, full labels, 20,000 rows")
    mode.add_argument("--full", action="store_true", help="5 seeds, full labels, all rows")
    parser.add_argument("--dataset", choices=["hmda", "acs"], default="hmda")
    parser.add_argument("--state", default="GA")
    args = parser.parse_args()
    config = make_config(quick=not args.full)
    config.dataset, config.state = args.dataset, args.state.upper()
    if args.dataset == "acs":
        from fairgroups.acs_run import run_experiment
    with threadpool_limits(limits=config.threads):
        run_experiment(config, ROOT)
