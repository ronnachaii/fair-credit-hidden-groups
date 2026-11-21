"""วัดว่า GPU เร็วกว่า CPU ที่ n_train เท่าไรสำหรับส่วนที่ใช้ torch: ERM-MLP, SCARF, DRO fine-tune

ใช้ข้อมูลจอร์เจียปี 2566 (ชุดพัฒนา) ตัดแถวเป็นหลายขนาด ฝึกด้วย config เต็ม (hidden 128, epochs 40, SCARF 30) 1 seed
ไม่แตะ test: ฝึกและทำนาย validation เท่านั้น ผลลัพธ์เขียน CSV ลง --out
  python tools/bench_device.py --sizes 9000 24000 48000 84000 --out <โฟลเดอร์>
"""
import argparse
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("MLFLOW_DISABLE_AGENT_HINT", "1")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import torch
from threadpoolctl import threadpool_limits

from config import make_config
from fairgroups.hmda import load_hmda, split_hmda, LeakageGuard, HMDAPreprocessor
from fairgroups.models import set_seed, train_mlp
from fairgroups.representations import train_scarf


def main(args):
    config = make_config(quick=False)
    frame, y, s, _ = load_hmda(ROOT / "data", "GA")
    rows = []
    seed = 17
    with threadpool_limits(limits=config.threads):
        for n_train in args.sizes:
            max_rows = int(n_train / 0.6)
            splits = split_hmda(frame, y, s, seed, max_rows if max_rows < len(y) else 0)
            train, val = splits["train"], splits["val"]
            guard = LeakageGuard().fit(train["frame"], train["y"])
            for part in splits.values():
                part["x"] = guard.transform(part["frame"])
            processor = HMDAPreprocessor(config.min_category_frequency, config.lei_top_n).fit(train["x"])
            xt, xv = processor.transform(train["x"]), processor.transform(val["x"])
            vg = val["s"].intersection.to_numpy()
            groups = np.random.default_rng(seed).integers(8, size=len(xt)) + 8 * train["y"]
            for device in args.devices:
                config.device = device
                if device == "cuda":
                    set_seed(seed, config.threads, "cuda")
                    torch.randn(64, 64, device="cuda").sum().item()  # warm-up context
                def timed(name, fn):
                    if device == "cuda":
                        torch.cuda.synchronize()
                    t = time.perf_counter()
                    result = fn()
                    if device == "cuda":
                        torch.cuda.synchronize()
                    rows.append({"n_train": len(xt), "device": device, "component": name,
                                 "wall_seconds": time.perf_counter() - t})
                    print(rows[-1], flush=True)
                    return result
                cp = timed("ERM-MLP_40ep", lambda: train_mlp(xt, train["y"], xv, val["y"], vg, config, seed))
                erm = cp[0]["average"][0]
                profile = {}
                timed("SCARF_30ep_total", lambda: train_scarf(train["x"], processor, config, seed, profile))
                rows.append({"n_train": len(xt), "device": device, "component": "SCARF_cpu_prep_part",
                             "wall_seconds": profile["cpu_prep_seconds"]})
                rows.append({"n_train": len(xt), "device": device, "component": "SCARF_network_part",
                             "wall_seconds": profile["network_seconds"]})
                timed("DRO_finetune_5ep_8x2groups", lambda: train_mlp(
                    xt, train["y"], xv, val["y"], vg, config, seed, groups=groups, initial_model=erm, epochs=5,
                    inferred_val_groups=vg))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / "bench_device_GA.csv", index=False)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sizes", type=int, nargs="+", default=[9000, 24000, 48000, 84000])
    p.add_argument("--devices", nargs="+", default=["cpu", "cuda"])
    p.add_argument("--out", required=True)
    main(p.parse_args())
