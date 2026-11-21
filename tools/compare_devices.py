"""เทียบผล CPU กับ CUDA จากไฟล์ที่ time_t0t3.py เขียนไว้ (metrics_*.csv, arrays_*.npz) แล้วสรุปเป็น Markdown
  python tools/compare_devices.py --dir <โฟลเดอร์> --prefix GA_quick
ต้องมีไฟล์ของ <prefix>_cpu, <prefix>_cpu_rep2, <prefix>_cuda, <prefix>_cuda_rep2 (รันซ้ำ seed เดียวกันเพื่อตรวจ determinism)
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score


def load(d, tag):
    return pd.read_csv(d / f"metrics_{tag}.csv"), np.load(d / f"arrays_{tag}.npz")


def main(a):
    d = Path(a.dir)
    tags = {k: f"{a.prefix}_{k}" for k in ["cpu", "cpu_rep2", "cuda", "cuda_rep2"]}
    data = {k: load(d, t) for k, t in tags.items() if (d / f"metrics_{t}.csv").exists()}
    lines = [f"# เทียบ CPU กับ CUDA: {a.prefix}", ""]

    # 1) determinism: รันซ้ำบน device เดิม seed เดิม ต้องได้ความน่าจะเป็นเหมือนกันทุกบิตหรือไม่
    lines += ["## 1. ทำซ้ำได้บน device เดียวกันหรือไม่ (ความน่าจะเป็น ERM-MLP บน test)", "",
              "| คู่เทียบ | seed | เหมือนกันทุกบิต | max abs diff | จำนวนแถวที่ label ต่างที่เกณฑ์ 0.5 |", "|---|---|---|---|---|"]
    seeds = sorted({int(k.split("|")[1]) for k in data["cpu"][1].files if k.startswith("erm_mlp_test_prob")})
    for x, y in [("cpu", "cpu_rep2"), ("cuda", "cuda_rep2"), ("cpu", "cuda")]:
        if x not in data or y not in data:
            continue
        for sd in seeds:
            p, q = data[x][1][f"erm_mlp_test_prob|{sd}"], data[y][1][f"erm_mlp_test_prob|{sd}"]
            lines.append(f"| {x} vs {y} | {sd} | {'ใช่' if np.array_equal(p, q) else 'ไม่'} | {np.abs(p - q).max():.2e} | "
                         f"{int(((p >= .5) != (q >= .5)).sum())} / {len(p)} |")

    # 2) ตัวชี้วัดตัดสินใจ
    lines += ["", "## 2. ตัวชี้วัด ERM-MLP / ERM-LGBM (test)", "",
              "| method | seed | acc CPU | acc CUDA | ต่าง | AUROC CPU | AUROC CUDA | epoch CPU | epoch CUDA |", "|---|---|---|---|---|---|---|---|---|"]
    mc, mg = data["cpu"][0], data["cuda"][0]
    for method in ["ERM-MLP", "ERM-LGBM"]:
        for sd in seeds:
            c = mc[(mc.kind == "base") & (mc.method == method) & (mc.seed == sd)].iloc[0]
            g = mg[(mg.kind == "base") & (mg.method == method) & (mg.seed == sd)].iloc[0]
            lines.append(f"| {method} | {sd} | {c.accuracy:.4f} | {g.accuracy:.4f} | {g.accuracy - c.accuracy:+.4f} | "
                         f"{c.auroc:.4f} | {g.auroc:.4f} | {int(c.selected_epoch)} | {int(g.selected_epoch)} |")

    # 3) กลุ่มที่ค้นพบ
    key = ["seed", "definition", "representation", "k"]
    dc = mc[mc.kind == "discovery"].set_index(key)
    dg = mg[mg.kind == "discovery"].set_index(key)
    cols = [c for c in dc.columns if c.startswith(("nmi_", "ari_"))] + ["silhouette_train"]
    diff = (dg[cols] - dc[cols]).abs()
    lines += ["", "## 3. กลุ่มที่ค้นพบ: ความต่างสัมบูรณ์ของ NMI / ARI / Silhouette (CUDA เทียบ CPU)", "",
              "| representation | จำนวนเซลล์ | max NMI(intersection) diff | max ARI(intersection) diff | max Silhouette diff |", "|---|---|---|---|---|"]
    for rep, g in diff.groupby(level="representation"):
        lines.append(f"| {rep} | {len(g)} | {g['nmi_intersection'].max():.4f} | {g['ari_intersection'].max():.4f} | {g['silhouette_train'].max():.4f} |")
    lines += ["", "ความสอดคล้องของป้ายกลุ่มบน test ระหว่างสองอุปกรณ์ (ARI ระหว่าง labels CPU กับ CUDA; 1.0 = เหมือนกันทั้งหมด)", "",
              "| representation | ค่า ARI ต่ำสุดข้ามเซลล์ | จำนวนเซลล์ที่ = 1.0 |", "|---|---|---|"]
    agree = {}
    for k in data["cpu"][1].files:
        if k.startswith("labels_test"):
            rep = k.split("|")[3]
            agree.setdefault(rep, []).append(adjusted_rand_score(data["cpu"][1][k], data["cuda"][1][k]))
    for rep, v in agree.items():
        lines.append(f"| {rep} | {min(v):.4f} | {sum(np.isclose(v, 1.0))} / {len(v)} |")
    (d / f"สรุปเทียบ_{a.prefix}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dir", required=True)
    p.add_argument("--prefix", required=True)
    main(p.parse_args())
