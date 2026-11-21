"""Design B (transfer): everything that is *learned* is fitted on the source state-year (2023) only.

Learned on source (train / validation of 2023):
  - leakage guard (column selection), imputer/scaler/category/top-lender preprocessor
  - SCARF encoder + scaler, global k-means (definition 'c', no y) on raw and SCARF representations, k in config.ks
  - geoproxy quantile edges, ERM-LightGBM (+ number of trees chosen on 2023 validation)
  - per-group thresholds (fitted inside confirmatory.analyze from 2023 validation probabilities and labels)
Applied (inference only) to the target (2024 test rows): preprocessing, encoders, cluster assignment, probabilities.
Nothing in the target is used to fit, select k, choose trees or tune thresholds.

The statistics (NMI, Gap, controls, bootstrap, hypotheses) reuse confirmatory.analyze unchanged: its "val" arrays
come from the source year and its "test" arrays from the target year.

Not included (descriptive only, no hypothesis uses them): GEORGE and HBAC groups.
"""
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from lightgbm import LGBMClassifier
from ..hmda import load_hmda, split_hmda, LeakageGuard, HMDAPreprocessor
from ..hmda_groups import GlobalClusters, GeoGroups
from ..models import set_seed, validation_scores
from ..representations import train_scarf, encode_scarf
from ..access_guard import require_access, C_YEAR
from .. import confirmatory

SOURCE_YEAR = 2023
GEO_COLUMN = "tract_minority_population_percent"


class SchemaMismatch(ValueError):
    """The target frame lacks columns the source models were fitted on."""


@dataclass
class SourceModel:
    seed: int
    guard: object
    processor: object
    scarf: object
    scarf_scaler: object
    clusters: dict                       # (rep, k) -> GlobalClusters
    geo: object
    lgb: object
    lgb_iteration: int
    train_ids: np.ndarray
    fit_log: list = field(default_factory=list)   # (stage, ids) pairs, for the audit file


def fit_source(train, val, config, seed):
    """train / val: dicts with frame, y, s, ids (as returned by split_hmda). Only these two parts are ever touched."""
    guard = LeakageGuard().fit(train["frame"], train["y"])
    x_train = guard.transform(train["frame"])
    processor = HMDAPreprocessor(config.min_category_frequency, config.lei_top_n).fit(x_train)
    xt = processor.transform(x_train)
    xv = processor.transform(guard.transform(val["frame"]))
    scarf = train_scarf(x_train, processor, config, seed)
    scarf_scaler = StandardScaler().fit(encode_scarf(scarf, xt))
    reps_train = {"raw": xt,
                  "scarf": scarf_scaler.transform(encode_scarf(scarf, xt)).astype(np.float32)}
    clusters, log = {}, [("leakage_guard", guard.fit_ids_), ("preprocessor", processor.fit_ids_),
                         ("scarf", scarf.fit_ids_)]
    for rep, x in reps_train.items():
        for k in config.ks:
            clusters[(rep, k)] = GlobalClusters().fit(x, train["ids"], k, seed)
            log.append((f"kmeans_{rep}_{k}", clusters[(rep, k)].fit_ids_))
    geo = GeoGroups().fit(pd.to_numeric(train["frame"][GEO_COLUMN], errors="coerce").to_numpy(), train["ids"])
    log.append(("geoproxy", geo.fit_ids_))
    lgb = LGBMClassifier(n_estimators=config.trees, num_leaves=15, max_depth=5, learning_rate=.05, verbosity=-1,
                         n_jobs=config.threads, random_state=seed, deterministic=True, force_col_wise=True)
    lgb.fit(xt, train["y"])
    vg = val["s"].intersection.to_numpy()
    choices = {t: validation_scores(val["y"], lgb.predict_proba(xv, num_iteration=t)[:, 1], vg)["average"]
               for t in sorted({10, 25, 50, config.trees})}
    iteration = max(choices, key=choices.get)            # same rule as run.py (average accuracy on validation)
    log.append(("erm_lgbm", train["ids"]))
    return SourceModel(seed, guard, processor, scarf, scarf_scaler, clusters, geo, lgb, iteration,
                       np.asarray(train["ids"]).copy(), log)


def _check_schema(model, frame):
    need = list(model.guard.features_) + [GEO_COLUMN]
    absent = [c for c in need if c not in frame.columns]
    if absent:
        raise SchemaMismatch(f"target frame lacks {len(absent)} source column(s): {absent[:10]}")


def apply_source(model, frame, ks):
    """Inference only. Returns (x, probability, labels) where labels maps method name -> group labels.
    No fit_*, no state change on the model (guaranteed by tests)."""
    _check_schema(model, frame)
    x = model.processor.transform(model.guard.transform(frame))
    p = model.lgb.predict_proba(x, num_iteration=model.lgb_iteration)[:, 1]
    reps = {"raw": x, "scarf": model.scarf_scaler.transform(encode_scarf(model.scarf, x)).astype(np.float32)}
    labels = {f"{rep}|{k}": model.clusters[(rep, k)].predict(reps[rep]) for rep in reps for k in ks}
    geo_values = pd.to_numeric(frame[GEO_COLUMN], errors="coerce").to_numpy()
    labels["geoproxy"] = model.geo.predict(geo_values)
    return x, p, labels


def build_transfer_inputs(source, target, models, config):
    """source: dict of split parts (needs train, val); target: one part dict (frame, y, s, ids).
    Returns (shared, seeds) in the format confirmatory.analyze expects."""
    train, val = source["train"], source["val"]
    seeds, first = [], models[0]
    xv0 = first.processor.transform(first.guard.transform(val["frame"]))
    xt0 = first.processor.transform(first.guard.transform(train["frame"]))
    xx0 = None
    for m in models:
        _, pv, lv = apply_source(m, val["frame"], config.ks)
        xx, pt, lt = apply_source(m, target["frame"], config.ks)
        seeds.append({"seed": m.seed, "labels_val": lv, "labels_test": lt, "p_val": pv, "p_test": pt})
        if xx0 is None:
            xx0 = xx
    shared = {"train_inter": train["s"].intersection.to_numpy(), "val_inter": val["s"].intersection.to_numpy(),
              "test_inter": target["s"].intersection.to_numpy(), "test_race": target["s"].race_eth.to_numpy(),
              "test_lei": target["frame"].lei.astype(str).to_numpy(), "y_val": val["y"], "y_test": target["y"],
              "val_ids": val["ids"], "test_ids": target["ids"], "xt": xt0, "xv": xv0, "xx": xx0}
    return shared, seeds


def run_design_b_arrays(source, target, config, output_dir, state="XX", target_rows="test", rounds=None):
    """Fit on source, apply to target, run the shared analysis; writes output_dir/design_B/confirm/* and
    output_dir/design_B/design_b_audit.json. source/target are already-loaded split parts (no file or network access)."""
    out = Path(output_dir) / "design_B"
    out.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    models = []
    for seed in config.seeds:
        print(f"design B seed={seed}: fit on source", flush=True)
        set_seed(seed, config.threads, config.device)
        m = fit_source(source["train"], source["val"], config, seed)
        for stage, ids in m.fit_log:                       # every fit used source-train rows only
            assert set(ids) == set(source["train"]["ids"]), stage
        models.append(m)
    shared, seeds = build_transfer_inputs(source, target, models, config)
    results = confirmatory.analyze(shared, seeds, config, out, state=state, rounds=rounds)
    audit = {"design": "B_transfer", "role": "secondary (plan 4.5)", "state": state, "source_year": SOURCE_YEAR,
             "target_year": C_YEAR, "target_used_in_fit": False, "target_rows": target_rows,
             "n_source_train": int(len(source["train"]["ids"])), "n_source_val": int(len(source["val"]["ids"])),
             "n_target": int(len(target["ids"])), "network_seeds": [m.seed for m in models],
             "lgb_iteration": {str(m.seed): m.lgb_iteration for m in models},
             "thresholds_fitted_on": "source validation (inside confirmatory.analyze)",
             "not_included": ["GEORGE", "HBAC"], "wall_seconds": time.perf_counter() - start}
    (out / "design_b_audit.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    return results


def run_design_b(config, root, output_dir, target_rows="test", rounds=None):
    """Load source (2023) and target (2024) through the access guard, then run design B.
    The target year is always the confirmatory year (needs the v2.0 unlock); output_dir is mandatory."""
    if not output_dir:
        raise ValueError("design B needs an explicit output_dir (never writes into results/)")
    if config.split_seed is None:
        raise ValueError("design B needs config.split_seed (one fixed split per state-year, plan 2.1)")
    if target_rows not in ("test", "all"):
        raise ValueError("target_rows must be 'test' or 'all'")
    access = dict(unlock_R=config.unlock_R, unlock_C=config.unlock_C, plan_file=config.plan_file)
    require_access(config.state, SOURCE_YEAR, log=False, **access)
    require_access(config.state, C_YEAR, log=False, **access)       # fail before touching any file
    data = Path(root).resolve() / "data"
    frame, y, s, _ = load_hmda(data, config.state, SOURCE_YEAR, access)
    source = split_hmda(frame, y, s, config.split_seed, config.max_rows)
    frame_t, y_t, s_t, _ = load_hmda(data, config.state, C_YEAR, access)
    if target_rows == "test":                                        # same split rule as design A -> comparable rows
        target = split_hmda(frame_t, y_t, s_t, config.split_seed, config.max_rows)["test"]
    else:
        target = {"frame": frame_t, "y": y_t, "s": s_t, "ids": frame_t.index.to_numpy()}
    return run_design_b_arrays(source, target, config, output_dir, state=config.state,
                               target_rows=target_rows, rounds=rounds)
