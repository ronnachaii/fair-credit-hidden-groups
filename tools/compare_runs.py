"""เทียบผลสองโฟลเดอร์ (เช่น results/ เดิม กับรันใหม่) ทีละไฟล์ CSV: จำนวนแถวที่จับคู่ได้, คอลัมน์ที่ต่าง, ค่าต่างสูงสุด

  python tools/compare_runs.py <โฟลเดอร์เดิม> <โฟลเดอร์ใหม่> [--tol 1e-9]
คอลัมน์เวลา/หน่วยความจำ/MLflow id และคอลัมน์ใหม่ที่มีด้านเดียวถูกข้าม (รายงานแยก)
"""
import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd

KEYS = {
    "hmda_pilot_results.csv": ["seed", "method", "representation", "k", "selection", "dro_variant", "group_definition"],
    "clustering_results.csv": ["seed", "representation", "k", "group_definition"],
    "postprocess_results.csv": ["seed", "base", "method", "objective"],
}
SKIP = ("seconds", "peak_", "mlflow", "memory", "analysis_role", "process_threads")


def compare(old_dir, new_dir, tol):
    for name, keys in KEYS.items():
        a_path, b_path = Path(old_dir) / name, Path(new_dir) / name
        if not (a_path.exists() and b_path.exists()):
            print(f"{name}: ไม่มีไฟล์ในฝั่งใดฝั่งหนึ่ง"); continue
        a, b = pd.read_csv(a_path), pd.read_csv(b_path)
        keys = [k for k in keys if k in a and k in b]
        for f in (a, b):
            f[keys] = f[keys].astype(str)
        a, b = a.drop_duplicates(keys).set_index(keys), b.drop_duplicates(keys).set_index(keys)
        common_rows = a.index.intersection(b.index)
        only_a, only_b = len(a.index.difference(b.index)), len(b.index.difference(a.index))
        cols = [c for c in a.columns if c in b.columns and not any(s in c for s in SKIP)]
        num = [c for c in cols if pd.api.types.is_numeric_dtype(a[c]) and pd.api.types.is_numeric_dtype(b[c])]
        other = [c for c in cols if c not in num]
        diffs = {}
        for c in num:
            x, y = a.loc[common_rows, c].astype(float), b.loc[common_rows, c].astype(float)
            d = (x - y).abs()
            d[x.isna() & y.isna()] = 0.
            diffs[c] = float(d.max()) if len(d) else 0.
        text_diff = [c for c in other if not a.loc[common_rows, c].astype(str).equals(b.loc[common_rows, c].astype(str))]
        differing = {c: v for c, v in diffs.items() if not (v <= tol)}
        print(f"\n== {name}: แถวจับคู่ {len(common_rows)} | เฉพาะเดิม {only_a} | เฉพาะใหม่ {only_b} | "
              f"คอลัมน์ตัวเลขที่เทียบ {len(num)} | ต่างเกิน tol {len(differing)} | ข้อความต่าง {text_diff}")
        print("   คอลัมน์ใหม่ (เฉพาะฝั่งใหม่):", sorted(set(b.columns) - set(a.columns))[:12])
        for c, v in sorted(differing.items(), key=lambda kv: -kv[1])[:12]:
            print(f"   {c:45s} max|diff| = {v:.6g}")
        yield name, len(common_rows), len(num), differing


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("old"); ap.add_argument("new")
    ap.add_argument("--tol", type=float, default=1e-9)
    args = ap.parse_args()
    list(compare(args.old, args.new, args.tol))
