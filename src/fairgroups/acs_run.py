"""รัน pilot ทุกวิธีและเก็บหลักฐานแยกข้อมูลฝึก/ทดสอบ"""
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.preprocessing import StandardScaler
from .data import (load_data, split_data, labeled_indices, TrainPreprocessor,
                   reference_groups, categorical_frames)
from .models import set_seed, train_mlp, predict_mlp, validation_scores
from .representations import train_scarf, encode_scarf, crossfit_error
from .clustering import discover, cross_label_groups
from .efficiency import ResourceMonitor, network_cost, inference_seconds, environment
from .metrics import evaluate
from .tracking import setup_tracking, log_row
from .reporting import generate_reports


def save_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def record_decision(rows, model, predict, selected, base, test, config, env, output):
    """test ใช้วัดผลเมื่อเลือก checkpoint ด้วย validation เสร็จแล้ว"""
    selection, epoch, score = selected
    row = dict(base, selection=selection, selected_epoch=epoch, validation_selection_score=score)
    row.update(evaluate(test["y"], predict(test["x"]), test["s"], config.min_fair_group))
    row["inference_seconds_per_1000"] = inference_seconds(predict, test["x"])
    if base["method"] == "ERM-LGBM":
        trees = model.booster_.dump_model(num_iteration=epoch)["tree_info"]
        row.update(parameters=np.nan, flops_per_row=np.nan,
                   tree_count=len(trees), leaf_count=sum(t["num_leaves"] for t in trees))
    else:
        row.update(network_cost(model), tree_count=np.nan, leaf_count=np.nan)
    row["mlflow_run_id"] = log_row(row, env["libraries"], config)
    rows.append(row)
    pd.DataFrame(rows).to_csv(output / "pilot_results.csv", index=False)


def run_experiment(config, root="."):
    """ต้นทางทั้งหมดเป็น relative path จึงใช้เหมือนกันใน Colab"""
    root = Path(root).resolve()
    output = root / "results" / "acs_optional"
    output.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    set_seed(config.seeds[0], config.threads)
    env = environment(config)
    save_json(output / "environment.json", env)
    setup_tracking(root)
    with ResourceMonitor() as overall:
        x, y, sensitive = load_data(root / "data")
        env["eligible_source_rows"] = len(y)
        rows, cluster_rows, resource_rows, audits = [], [], [], []
        for seed in config.seeds:
            print(f"seed={seed}: split / preprocess / SCARF", flush=True)
            set_seed(seed, config.threads)
            splits = split_data(x, y, sensitive, seed, config.max_rows)
            train, val, test = (splits[name] for name in ["train", "val", "test"])
            audit = {"seed": seed, "train_ids": train["ids"].tolist(),
                     "val_ids": val["ids"].tolist(), "test_ids": test["ids"].tolist(),
                     "features": list(train["x"].columns), "fits": [], "error_crossfits": []}
            def add_fit(stage, ids, **extra):
                assert set(ids).issubset(set(train["ids"]))
                assert set(ids).isdisjoint(test["ids"])
                audit["fits"].append({"stage": stage, "fit_ids": np.asarray(ids).tolist(), **extra})
            with ResourceMonitor() as pre_resource:
                processor = TrainPreprocessor(config.min_category_frequency).fit(train["x"])
                transformed = {name: processor.transform(part["x"]) for name, part in splits.items()}
                categorical = categorical_frames(splits)
            add_fit("onehot_scaler", processor.fit_ids_)
            add_fit("lgbm_categories", train["ids"])
            with ResourceMonitor() as scarf_resource:
                scarf = train_scarf(train["x"], processor, config, seed)
                scaler = StandardScaler()
                reps = {"raw": transformed["train"],
                        "scarf": scaler.fit_transform(encode_scarf(scarf, transformed["train"])).astype(np.float32)}
                # val/test ไม่เคยเข้า fit แม้ในการเรียนแบบไม่มีป้ายกำกับ
                scarf_holdout = {name: scaler.transform(encode_scarf(scarf, transformed[name]))
                                 for name in ["val", "test"]}
            add_fit("scarf", scarf.fit_ids_)
            add_fit("scarf_scaler", train["ids"])
            encoder_cost = network_cost(scarf.encoder)
            pretraining_cost = network_cost(scarf)
            resource_rows.append(dict(representation="scarf", discovery_label_fraction=0, seed=seed,
                discovery_train_seconds=scarf_resource.seconds, peak_memory_mb=scarf_resource.peak_mb,
                inference_seconds_per_1000=inference_seconds(lambda xx: encode_scarf(scarf, xx), transformed["test"]),
                **encoder_cost, pretraining_parameters=pretraining_cost["parameters"],
                pretraining_flops_per_row=pretraining_cost["flops_per_row"]))
            resource_rows.append(dict(representation="raw", discovery_label_fraction=0, seed=seed,
                discovery_train_seconds=pre_resource.seconds, peak_memory_mb=pre_resource.peak_mb,
                inference_seconds_per_1000=inference_seconds(processor.transform, test["x"]),
                parameters=0, flops_per_row=0, pretraining_parameters=0, pretraining_flops_per_row=0))
            discoveries = {}
            for rep_name, rep in reps.items():
                for k in config.ks:
                    with ResourceMonitor() as cluster_resource:
                        clusters, scores, km = discover(rep, train["ids"], train["s"], k, seed)
                        # ใช้เพียง transform/predict บน holdout เพื่อยืนยันขั้นนำไปใช้
                        for name in ["val", "test"]:
                            km.predict(transformed[name] if rep_name == "raw" else scarf_holdout[name])
                    add_fit(f"kmeans_{rep_name}_{k}", km.fit_ids_)
                    discovery_seconds = cluster_resource.seconds + (scarf_resource.seconds if rep_name == "scarf" else 0)
                    discovery_peak = max(cluster_resource.peak_mb, scarf_resource.peak_mb if rep_name == "scarf" else pre_resource.peak_mb)
                    discoveries[(rep_name, k)] = (clusters, scores, discovery_seconds, discovery_peak)
                    cluster_row = dict(representation=rep_name, k=k, seed=seed,
                        discovery_label_fraction=0, n_discovery=len(train["y"]), **scores,
                        discovery_train_seconds=discovery_seconds, peak_memory_mb=discovery_peak)
                    cluster_row["mlflow_run_id"] = log_row(cluster_row, env["libraries"], config, "clustering")
                    cluster_rows.append(cluster_row)
            vg = reference_groups(val["s"])["intersection"]
            for fraction in config.label_fractions:
                labeled = labeled_indices(train["y"], fraction, seed)
                xl, yl = transformed["train"][labeled], train["y"][labeled]
                ids = train["ids"][labeled]
                print(f"seed={seed}, labels={fraction:g}, n={len(yl)}: OOF + 16 methods", flush=True)
                with ResourceMonitor() as error_resource:
                    error_rep, error_audit = crossfit_error(xl, yl, ids, config, seed)
                error_audit["label_fraction"] = fraction
                audit["error_crossfits"].append(error_audit)
                add_fit(f"error_oof_and_scaler_{fraction}", ids)
                resource_rows.append(dict(representation="error", discovery_label_fraction=fraction, seed=seed,
                    discovery_train_seconds=error_resource.seconds, peak_memory_mb=error_resource.peak_mb,
                    inference_seconds_per_1000=np.nan,
                    parameters=np.nan, flops_per_row=np.nan, pretraining_parameters=np.nan,
                    pretraining_flops_per_row=np.nan))
                current_discoveries = dict(discoveries)
                for k in config.ks:
                    with ResourceMonitor() as er_cluster:
                        clusters, scores, km = discover(error_rep, ids, train["s"].iloc[labeled], k, seed)
                    add_fit(f"kmeans_error_{k}_{fraction}", km.fit_ids_)
                    seconds = error_resource.seconds + er_cluster.seconds
                    peak = max(error_resource.peak_mb, er_cluster.peak_mb)
                    current_discoveries[("error", k)] = (clusters, scores, seconds, peak)
                    cluster_row = dict(representation="error", k=k, seed=seed,
                        discovery_label_fraction=fraction, n_discovery=len(yl), **scores,
                        discovery_train_seconds=seconds, peak_memory_mb=peak)
                    cluster_row["mlflow_run_id"] = log_row(cluster_row, env["libraries"], config, "clustering")
                    cluster_rows.append(cluster_row)
                common = dict(seed=seed, label_fraction=fraction, n_labeled=len(yl), n_train=len(train["y"]),
                              n_val=len(val["y"]), n_test=len(test["y"]), input_dimension=xl.shape[1],
                              preprocessing_seconds=pre_resource.seconds,
                              threshold=0.5, label_budget_includes_discovery=True)
                # LightGBM ใช้ categorical โดยตรง เลือกจำนวนต้นไม้จากกริดบน validation
                with ResourceMonitor() as lgb_resource:
                    lgb = LGBMClassifier(n_estimators=config.trees, num_leaves=15, max_depth=5,
                        learning_rate=0.05, verbosity=-1, n_jobs=config.threads, random_state=seed,
                        deterministic=True, force_col_wise=True)
                    lgb.fit(categorical["train"].iloc[labeled], yl)
                    candidates = sorted(set([10, 25, 50, config.trees]))
                    scores_by_tree = {t: validation_scores(val["y"],
                        lgb.predict_proba(categorical["val"], num_iteration=t)[:, 1], vg) for t in candidates}
                base = dict(common, method="ERM-LGBM", representation="none", k=0,
                            decision_train_seconds=lgb_resource.seconds, discovery_train_seconds=0,
                            train_seconds=pre_resource.seconds + lgb_resource.seconds,
                            peak_memory_mb=max(pre_resource.peak_mb, lgb_resource.peak_mb))
                for selection in ["average", "worst_group"]:
                    epoch = max(candidates, key=lambda t: scores_by_tree[t][selection])
                    predict = lambda xx, epoch=epoch: lgb.predict_proba(xx, num_iteration=epoch)[:, 1]
                    record_decision(rows, lgb, predict, (selection, epoch, scores_by_tree[epoch][selection]),
                        base, dict(test, x=categorical["test"]), config, env, output)
                # JTT รอบระบุตัวอย่างยากมีจำนวน epoch คงที่ ไม่ใช้กลุ่มจริงเลือก
                with ResourceMonitor() as jtt_resource:
                    _, identification = train_mlp(xl, yl, transformed["val"], val["y"], vg,
                        config, seed, epochs=config.jtt_identification_epochs)
                    mistakes = (predict_mlp(identification, xl) >= 0.5) != yl
                    jtt_weights = np.where(mistakes, config.jtt_upweight, 1.0)
                methods = [("ERM-MLP", "none", 0, None, None, {}, 0, 0),
                           ("JTT", "none", 0, None, jtt_weights, {}, jtt_resource.seconds, jtt_resource.peak_mb)]
                for k in config.ks:
                    # ใช้ random k แต่ละค่าเพื่อให้จำนวนกลุ่มตรงกับ ablation ทุก k
                    random_clusters = np.random.default_rng(seed + k).integers(k, size=len(yl))
                    methods.append((f"GDRO-random-k{k}", "random", k,
                                    cross_label_groups(random_clusters, yl), None, {}, 0, 0))
                for (rep_name, k), (clusters, scores, seconds, peak) in current_discoveries.items():
                    selected_clusters = clusters if rep_name == "error" else clusters[labeled]
                    methods.append((f"GDRO-{rep_name}-k{k}", rep_name, k,
                        cross_label_groups(selected_clusters, yl), None, scores, seconds, peak))
                _, oracle_groups = np.unique(reference_groups(train["s"].iloc[labeled])["intersection"], return_inverse=True)
                methods.append(("GDRO-oracle", "oracle", 4, oracle_groups, None, {}, 0, 0))
                for method, rep_name, k, groups, weights, alignment, discovery_seconds, discovery_peak in methods:
                    with ResourceMonitor() as fit_resource:
                        checkpoints, _ = train_mlp(xl, yl, transformed["val"], val["y"], vg,
                                                   config, seed, groups=groups, sample_weights=weights)
                    decision_seconds = fit_resource.seconds + (jtt_resource.seconds if method == "JTT" else 0)
                    # JTT รอบแรกนับใน decision time แล้ว ไม่บวกซ้ำใน discovery
                    actual_discovery = 0 if method == "JTT" else discovery_seconds
                    base = dict(common, method=method, representation=rep_name, k=k, **alignment,
                        decision_train_seconds=decision_seconds, discovery_train_seconds=actual_discovery,
                        train_seconds=pre_resource.seconds + actual_discovery + decision_seconds,
                        peak_memory_mb=max(pre_resource.peak_mb, fit_resource.peak_mb, discovery_peak),
                        n_dro_groups=0 if groups is None else len(np.unique(groups)))
                    for selection, (model, epoch, score) in checkpoints.items():
                        record_decision(rows, model, lambda xx, model=model: predict_mlp(model, xx),
                            (selection, epoch, score), base, dict(test, x=transformed["test"]), config, env, output)
                pd.DataFrame(cluster_rows).to_csv(output / "clustering_results.csv", index=False)
                pd.DataFrame(resource_rows).to_csv(output / "representation_resources.csv", index=False)
            audits.append(audit)
            save_json(output / "leakage_audit.json", audits)
            for resource in resource_rows:
                if resource["seed"] == seed:
                    resource["mlflow_run_id"] = log_row(resource, env["libraries"], config, "representation")
            pd.DataFrame(resource_rows).to_csv(output / "representation_resources.csv", index=False)
        generate_reports(output)
    env.update(wall_seconds=time.perf_counter() - start, peak_process_rss_mb=overall.peak_mb,
               decision_rows=len(rows), clustering_rows=len(cluster_rows),
               completed=True, colab_runtime_verified=False)
    save_json(output / "environment.json", env)
    print(f"DONE: {len(rows)} decision rows, {len(cluster_rows)} clustering rows, {env['wall_seconds']:.2f} seconds", flush=True)
    return env
