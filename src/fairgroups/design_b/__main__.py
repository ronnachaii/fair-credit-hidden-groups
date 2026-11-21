"""python -m fairgroups.design_b --state GA --output-dir DIR --v1 --full --unlock-R H --unlock-C H --plan-file PLAN
Needs the 2024 data, which stay locked until the v2.0 freeze (see access_guard). Do not run before that."""
import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("MLFLOW_DISABLE_AGENT_HINT", "1")
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from config import make_config, make_v1_config
from fairgroups.design_b import run_design_b
from threadpoolctl import threadpool_limits


def build_parser():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--state", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--v1", action="store_true")
    ap.add_argument("--target-rows", choices=["test", "all"], default="test")
    ap.add_argument("--unlock-R", default=None)
    ap.add_argument("--unlock-C", default=None)
    ap.add_argument("--plan-file", default=None)
    ap.add_argument("--rounds", type=int, default=None,
                    help="bootstrap rounds for row and lei (default: config.bootstrap_rounds = 2000, as design A)")
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    if a.rounds is not None and a.rounds < 1:
        raise SystemExit("--rounds must be >= 1")
    cfg = make_v1_config(quick=not a.full) if a.v1 else make_config(quick=not a.full)
    cfg.state = a.state.upper()
    cfg.unlock_R, cfg.unlock_C, cfg.plan_file = a.unlock_R, a.unlock_C, a.plan_file
    if cfg.split_seed is None:
        cfg.split_seed = 17
    with threadpool_limits(limits=cfg.threads):
        run_design_b(cfg, ROOT, a.output_dir, target_rows=a.target_rows, rounds=a.rounds)


if __name__ == "__main__":
    main()
