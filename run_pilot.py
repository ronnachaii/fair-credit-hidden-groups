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
from config import make_config, make_v1_config
from fairgroups.run import run_experiment
from threadpoolctl import threadpool_limits


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HMDA hidden-group fairness pilot (CPU)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true", help="3 seeds, full labels, 20,000 rows")
    mode.add_argument("--full", action="store_true", help="5 seeds, full labels, all rows")
    parser.add_argument("--dataset", choices=["hmda", "acs"], default="hmda")
    parser.add_argument("--state", default="GA")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu",
                        help="torch device (default cpu keeps earlier results reproducible)")
    parser.add_argument("--output-dir", default=None,
                        help="write results here instead of ./results (HMDA only; avoids overwriting earlier results)")
    parser.add_argument("--mode", choices=["confirm", "context_dro"], default="confirm",
                        help="confirm = pipeline ยืนยัน (ไม่มี group-DRO/JTT); context_dro = รัน DRO เชิงบริบท GA 2566 เท่านั้น")
    parser.add_argument("--year", type=int, default=2023, help="ปีข้อมูล HMDA (2024 ถูกล็อกจนกว่าจะตรึง v2.0)")
    parser.add_argument("--v1", action="store_true", help="ใช้ค่าตรึง v1.0 จาก config.make_v1_config (ใช้ร่วมกับ --full)")
    parser.add_argument("--unlock-R", default=None, help="SHA-256 ของไฟล์แผนที่ตรึง v1.0 (ปลดล็อก CA/OH/FL 2566)")
    parser.add_argument("--unlock-C", default=None, help="SHA-256 ของไฟล์แผนที่ตรึง v2.0 (ปลดล็อกปี 2567)")
    parser.add_argument("--plan-file", default=None, help="ไฟล์แผนที่ใช้ตรวจ SHA-256 ของ --unlock-R/--unlock-C")
    parser.add_argument("--split-seed", type=int, default=None, help="ชุดแบ่งเดียวต่อรัฐ-ปี (ค่าเริ่มต้น: ตาม seed แบบนำร่อง)")
    args = parser.parse_args()
    config = make_v1_config(quick=not args.full) if args.v1 else make_config(quick=not args.full)
    config.dataset, config.state, config.device = args.dataset, args.state.upper(), args.device
    config.mode, config.year = args.mode, args.year
    config.unlock_R, config.unlock_C, config.plan_file = args.unlock_R, args.unlock_C, args.plan_file
    if args.split_seed is not None:
        config.split_seed = args.split_seed
    if args.mode == "confirm" and config.split_seed is None:
        config.split_seed = 17   # confirm ต้องมีชุดแบ่งคงที่ (v1.0 = 17)
    if args.dataset == "acs":
        from fairgroups.acs_run import run_experiment
    with threadpool_limits(limits=config.threads):
        if args.output_dir and args.dataset == "hmda":
            run_experiment(config, ROOT, output_dir=args.output_dir)
        else:
            run_experiment(config, ROOT)
