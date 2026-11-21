"""วัดเวลา T0-T3 (แผนวิเคราะห์ §6.4) ของ pipeline ลดขอบเขต: ไม่มี DRO / JTT / คำอธิบายกลุ่ม

ใช้ฟังก์ชันของ src/fairgroups ชุดเดียวกับ run.py แต่ครอบด้วย ComponentTimer และไม่เขียนทับ results/ เดิม
ผลทั้งหมดเขียนลงโฟลเดอร์ --out เท่านั้น (ไม่แตะ results/ และ mlflow.db)

ตัวอย่าง (ตั้ง PYTHONUTF8=1 ก่อนรัน):
  python tools/time_t0t3.py --state GA  --quick --device cpu  --out <โฟลเดอร์>   # เทียบ device บนชุดนำร่อง
  python tools/time_t0t3.py --state ID  --device cuda --seeds 17 29 --out <โฟลเดอร์>  # config เต็ม (--full)

ข้อกำหนดความปลอดภัยรอบนี้: อนุญาตเฉพาะ GA / ID / NM (ปี 2566); CA / OH / FL ถูกปฏิเสธ
ส่วนที่ยังไม่มีในโค้ด (ตัวจำแนกเพดาน, กลุ่มผสม H4a, bootstrap) ไม่ได้ถูกวัด และระบุไว้ในผลลัพธ์
"""
import argparse
import json
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
from lightgbm import LGBMClassifier
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

from config import make_config
from fairgroups.hmda import load_hmda, split_hmda, LeakageGuard, HMDAPreprocessor
from fairgroups.hmda_groups import ClassClusters, GlobalClusters, GeoGroups, hidden, fit_hbac, group_scores
from fairgroups.models import set_seed, train_mlp, predict_mlp, validation_scores
from fairgroups.representations import train_scarf, encode_scarf
from fairgroups.metrics import evaluate
from fairgroups.postprocess import XRandomGroups, fit_candidates, evaluate_candidates
from fairgroups.run import oof_errors
from fairgroups.timing import ComponentTimer

ALLOWED_STATES = {"GA", "ID", "NM"}
NOT_MEASURED = ["ceiling_classifier", "mixed_groups_H4a", "bootstrap"]  # ยังไม่มีโค้ด (รอบถัดไป)


def run(args):
    state = args.state.upper()
    if state not in ALLOWED_STATES:
        raise SystemExit(f"รอบนี้อนุญาตเฉพาะ {sorted(ALLOWED_STATES)}; ไม่รันรัฐ {state}")
    config = make_config(quick=args.quick)
    config.state, config.device = state, args.device
    if args.seeds:
        config.seeds = tuple(args.seeds)
    if args.threads:
        config.threads = args.threads
    if args.max_rows is not None:
        config.max_rows = args.max_rows
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    tag = f"{state}_{'quick' if args.quick else 'full'}_{args.device}{args.suffix}"
    meta = {"state": state, "device": args.device, "config_mode": "quick" if args.quick else "full",
            "threads": config.threads}
    timer = ComponentTimer(args.device, **{k: v for k, v in meta.items() if k != "device"})

    # ดาวน์โหลดครั้งแรก (ถ้าไฟล์ยังไม่อยู่ในแคช) ไม่นับเป็นเวลา T0
    path = ROOT / "data" / "hmda" / f"hmda_2023_{state}.csv"
    if not path.exists():
        t = time.perf_counter()
        load_hmda(ROOT / "data", state)
        print(f"ดาวน์โหลด {state}: {time.perf_counter() - t:.1f} s (ไม่นับใน T0)", flush=True)

    metrics, arrays = [], {}
    if args.device == "cuda":
        # สร้าง CUDA context + cuBLAS handle ก่อนเริ่มจับเวลาส่วนประกอบ (ค่าเริ่มต้นครั้งเดียวต่อโปรเซส ~ หลายวินาที)
        set_seed(config.seeds[0], config.threads, "cuda")
        with timer.section("cuda_warmup"):
            w = torch.randn(256, 256, device="cuda")
            (w @ w).sum().item()
    wall_start = time.perf_counter()
    with threadpool_limits(limits=config.threads):
        with timer.section("load_filter"):
            frame, y, s, stages = load_hmda(ROOT / "data", state)
        meta.update(source_rows=int(stages.iloc[0]["n"]), eligible_rows=len(y))
        for seed in config.seeds:
            print(f"[{tag}] seed={seed}", flush=True)
            seed_start = time.perf_counter()
            tm = lambda name, **kw: timer.section(name, seed=seed, **kw)
            with tm("split"):
                splits = split_hmda(frame, y, s, seed, config.max_rows)
            train, val, test = (splits[n] for n in ["train", "val", "test"])
            with tm("transform"):
                guard = LeakageGuard().fit(train["frame"], train["y"])
                for part in splits.values():
                    part["x"] = guard.transform(part["frame"])
                processor = HMDAPreprocessor(config.min_category_frequency, config.lei_top_n).fit(train["x"])
                transformed = {n: processor.transform(p["x"]) for n, p in splits.items()}
            xt, xv, xx = (transformed[n] for n in ["train", "val", "test"])
            n_train = len(xt)
            vg = val["s"].intersection.to_numpy()

            with tm("ERM-MLP", n_train=n_train):
                erm_cp, _ = train_mlp(xt, train["y"], xv, val["y"], vg, config, seed)
            erm, erm_epoch, _ = erm_cp["average"]
            with tm("ERM-LGBM", n_train=n_train):
                lgb = LGBMClassifier(n_estimators=config.trees, num_leaves=15, max_depth=5, learning_rate=.05,
                                     verbosity=-1, n_jobs=config.threads, random_state=seed,
                                     deterministic=True, force_col_wise=True)
                lgb.fit(xt, train["y"])
                choices = {t: validation_scores(val["y"], lgb.predict_proba(xv, num_iteration=t)[:, 1], vg)
                           for t in sorted({10, 25, 50, config.trees})}
                lgb_iter = max(choices, key=lambda t: choices[t]["average"])
            profile = {}
            with tm("SCARF_train", n_train=n_train) as _:
                scarf = train_scarf(train["x"], processor, config, seed, profile)
            timer.rows[-1].update(scarf_cpu_prep_seconds=profile.get("cpu_prep_seconds"),
                                  scarf_network_seconds=profile.get("network_seconds"))
            with tm("SCARF_encode"):
                scarf_scaler = StandardScaler().fit(encode_scarf(scarf, xt))
                reps = {"raw": transformed,
                        "scarf": {n: scarf_scaler.transform(encode_scarf(scarf, x)).astype(np.float32)
                                  for n, x in transformed.items()}}
            with tm("GEORGE_hidden"):
                george_scaler = StandardScaler().fit(hidden(erm, xt))
                reps["GEORGE"] = {n: george_scaler.transform(hidden(erm, x)).astype(np.float32)
                                  for n, x in transformed.items()}

            discoveries, selected = {}, {}
            for definition in ["cy", "c"]:
                for rep_name, rep in reps.items():
                    for k in config.ks:
                        with tm("kmeans", definition=definition, representation=rep_name, k=k):
                            km = (ClassClusters().fit(rep["train"], train["y"], train["ids"], k, seed)
                                  if definition == "cy" else GlobalClusters().fit(rep["train"], train["ids"], k, seed))
                            labels = {"train": km.labels_, **{n: km.predict(rep[n]) for n in ["val", "test"]}}
                        with tm("group_scores", definition=definition, representation=rep_name, k=k):
                            scores = group_scores(rep["train"], labels["train"], train["s"], seed)
                            alignment = group_scores(rep["test"], labels["test"], test["s"], seed)
                        discoveries[(definition, rep_name, k)] = (km, labels, scores["silhouette"])
                        metrics.append({"seed": seed, "kind": "discovery", "definition": definition,
                                        "representation": rep_name, "k": k, "silhouette_train": scores["silhouette"],
                                        **{a: b for a, b in alignment.items() if a.startswith(("ari_", "nmi_"))}})
                        arrays[f"labels_test|{seed}|{definition}|{rep_name}|{k}"] = labels["test"].astype(np.int16)
                    selected[(definition, rep_name)] = max(config.ks, key=lambda k: discoveries[(definition, rep_name, k)][2])
            with tm("HBAC_oof", n_train=n_train):
                error, _ = oof_errors(train, config, seed)
            with tm("HBAC_fit", n_train=n_train):
                hbac = fit_hbac(xt, error, train["ids"], seed, k=4)
                hlabels = {"train": hbac.labels_, **{n: hbac.predict(transformed[n]) for n in ["val", "test"]}}
            with tm("HBAC_scores"):
                hscore = group_scores(xt, hlabels["train"], train["s"], seed)
                halign = group_scores(xx, hlabels["test"], test["s"], seed)
            metrics.append({"seed": seed, "kind": "discovery", "definition": "shared", "representation": "HBAC",
                            "k": hbac.n_clusters_, "silhouette_train": hscore["silhouette"],
                            **{a: b for a, b in halign.items() if a.startswith(("ari_", "nmi_"))}})
            arrays[f"labels_test|{seed}|shared|HBAC|{hbac.n_clusters_}"] = hlabels["test"].astype(np.int16)
            with tm("geoproxy"):
                geo_values = {n: pd.to_numeric(p["frame"].tract_minority_population_percent, errors="coerce").to_numpy()
                              for n, p in splits.items()}
                geo = GeoGroups().fit(geo_values["train"], train["ids"])
                geo_labels = {n: geo.predict(v) for n, v in geo_values.items()}

            # ตัวควบคุมสุ่ม (hash ของ x) แยกเวลาออกจากการหาเกณฑ์
            pp_methods = []
            for (definition, rep, k), (km, labels, _) in discoveries.items():
                if definition != "c" or (rep == "GEORGE" and k != selected[("c", rep)]):
                    continue
                pp_methods.append((f"PP-{rep}-k{k}" if rep in ["raw", "scarf"] else "PP-GEORGE", rep, k, labels))
            with tm("random_control"):
                for k in config.ks:
                    rm = XRandomGroups().fit(xt, train["ids"], k, seed)
                    pp_methods.append((f"PP-random-k{k}", "random", k, {n: rm.predict(x) for n, x in transformed.items()}))
            pp_methods.extend([("PP-HBAC", "HBAC", hbac.n_clusters_, hlabels),
                               ("PP-geoproxy", "geoproxy", len(np.unique(geo_labels["train"])), geo_labels),
                               ("PP-oracle", "oracle", train["s"].intersection.nunique(),
                                {n: p["s"].intersection.to_numpy() for n, p in splits.items()})])
            for base in ["ERM-LGBM", "ERM-MLP"]:
                vp = lgb.predict_proba(xv, num_iteration=lgb_iter)[:, 1] if base == "ERM-LGBM" else predict_mlp(erm, xv)
                tp = lgb.predict_proba(xx, num_iteration=lgb_iter)[:, 1] if base == "ERM-LGBM" else predict_mlp(erm, xx)
                with tm("threshold_fit", base=base, candidates=len(pp_methods) * 2):
                    candidates = fit_candidates(base, vp, val, pp_methods, config, seed)
                with tm("threshold_eval", base=base):
                    evaluated, _ = evaluate_candidates(candidates, tp, test, config.min_fair_group)
                with tm("evaluate_base", base=base):
                    base_eval = evaluate(test["y"], tp, test["s"], config.min_fair_group)
                row = {"seed": seed, "kind": "base", "method": base,
                       **{k: base_eval[k] for k in ["accuracy", "auroc", "positive_rate", "eo_gap", "dp_difference"]}}
                if base == "ERM-MLP":
                    row["selected_epoch"] = erm_epoch
                    arrays[f"erm_mlp_test_prob|{seed}"] = tp.astype(np.float64)
                    arrays[f"erm_mlp_val_prob|{seed}"] = vp.astype(np.float64)
                else:
                    row["selected_epoch"] = lgb_iter
                metrics.append(row)
                for r in evaluated:
                    if r["proposed_selected"] or r["method"] in ("PP-oracle", "PP-geoproxy", "PP-HBAC"):
                        metrics.append({"seed": seed, "kind": "postprocess", "base": base, "method": r["method"],
                                        "objective": r["objective"], "proposed_selected": r["proposed_selected"],
                                        **{k: r[k] for k in ["accuracy", "eo_gap", "dp_difference"]}})
            timer.rows.append({**meta, "component": "SEED_TOTAL", "seed": seed, "n_train": n_train,
                               "wall_seconds": time.perf_counter() - seed_start})
    total = time.perf_counter() - wall_start
    timer.rows.append({**meta, "component": "RUN_TOTAL", "wall_seconds": total})
    env = {"torch": torch.__version__, "cuda_available": torch.cuda.is_available(),
           "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
           "device_requested": args.device, "config": config.to_dict(), **meta,
           "n_train_last_seed": int(n_train), "not_measured": NOT_MEASURED, "run_total_seconds": total,
           "cpu_count_logical": os.cpu_count(), "uses_test_eval": True,
           "determinism": {"use_deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
                           "CUBLAS_WORKSPACE_CONFIG": os.environ.get("CUBLAS_WORKSPACE_CONFIG")}}
    pd.DataFrame(timer.rows).to_csv(out / f"timing_{tag}.csv", index=False)
    pd.DataFrame(metrics).to_csv(out / f"metrics_{tag}.csv", index=False)
    np.savez_compressed(out / f"arrays_{tag}.npz", **arrays)
    (out / f"env_{tag}.json").write_text(json.dumps(env, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[{tag}] DONE total {total:.1f} s -> {out}", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--state", required=True)
    p.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    p.add_argument("--quick", action="store_true", help="config QUICK (20,000 แถว, 3 seed, epochs 10); ไม่ใส่ = config เต็ม")
    p.add_argument("--seeds", type=int, nargs="*")
    p.add_argument("--threads", type=int, help="ค่าเริ่มต้นของ config (Windows = 2)")
    p.add_argument("--max-rows", type=int, default=None)
    p.add_argument("--suffix", default="")
    p.add_argument("--out", required=True)
    run(p.parse_args())
