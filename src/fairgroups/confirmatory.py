"""ชุดวิเคราะห์ยืนยันต่อรัฐ-ปี (แผนวิเคราะห์ §2.4, §3, §5.1): ไม่มี group-DRO

อินพุตเป็นอาร์เรย์ล้วน (ไม่ผูกกับ run.py) เพื่อให้ทดสอบด้วยข้อมูลสังเคราะห์ได้:
  shared   : ชุดแบ่งคงที่ต่อรัฐ-ปี (split_seed คงที่) -> val_inter, test_inter, test_race, test_lei, y_val, y_test, val_ids, และ
             (ถ้าต้องการเพดานการกู้คืน) xt, xv, xx, train_inter
  seeds    : list ของ dict ต่อ seed ของโครงข่าย: seed, labels_val/labels_test (dict ชื่อวิธี -> ป้ายกลุ่ม), p_val, p_test
             (ความน่าจะเป็นของ ERM-LightGBM ที่เกณฑ์ 0.5 เป็นฐานของการปรับเกณฑ์)
ชื่อวิธีของกลุ่มที่ค้นพบ: 'raw|k', 'scarf|k', 'GEORGE|k', 'HBAC', 'geoproxy'

bootstrap: น้ำหนักจำนวนเต็มต่อใบคำขอชุดเดียวกันในทุกวิธี (paired); ในแต่ละรอบเฉลี่ยข้าม seed ก่อน (แผน §3.1)
ทำสองแบบ: ระดับใบคำขอ (หลักตามแผน) และ cluster ตามผู้ให้กู้ lei (เข้มกว่า); ข้อสรุป 'conservative' ต้องผ่านทั้งสองแบบ
"""
import json
import time
from contextlib import contextmanager
from pathlib import Path
import numpy as np
import pandas as pd
from . import stats, controls

UNKNOWN = controls.UNKNOWN
USES_DEMOGRAPHICS = ["oracle ceiling (ceil_a, ceil_b)", "mixed oracle-random groups (H4a)"]


class SectionTimer:
    def __init__(self):
        self.rows = []

    @contextmanager
    def section(self, name, **extra):
        start = time.perf_counter()
        try:
            yield
        finally:
            self.rows.append({"component": name, **extra, "wall_seconds": time.perf_counter() - start})


def _pred_gap_setup(test_race, min_group):
    races, codes = np.unique(np.asarray(test_race).astype(str), return_inverse=True)
    counts = np.bincount(codes, minlength=len(races))
    eligible = (counts >= min_group) & (races != UNKNOWN)       # ตัดสินจากชุดทดสอบเต็มก่อน bootstrap แล้วคงที่ (§2.6)
    onehot = np.zeros((len(codes), len(races)))
    onehot[np.arange(len(codes)), codes] = 1.
    return onehot[:, eligible], races[eligible]


def analyze(shared, seeds, config, output_dir, state="XX", timer=None, rounds=None, kinds=("row", "lei")):
    """คืน dict ผลหลัก และเขียน CSV/JSON ลง output_dir/confirm/"""
    timer = timer or SectionTimer()
    out = Path(output_dir) / "confirm"
    out.mkdir(parents=True, exist_ok=True)
    rounds = rounds or config.bootstrap_rounds
    k_main = config.k_main
    test_inter = np.asarray(shared["test_inter"]).astype(str)
    n = len(test_inter)
    known = test_inter != UNKNOWN
    t_codes, nt = stats.encode(test_inter[known])
    y_val, y_test = np.asarray(shared["y_val"]), np.asarray(shared["y_test"])
    OH, eligible_races = _pred_gap_setup(shared["test_race"], config.min_fair_group)
    if len(eligible_races) < 3:
        raise ValueError("กลุ่มเชื้อชาติที่เข้าเกณฑ์ < 3 กลุ่ม: Gap คำนวณไม่ได้ (แผน §2.6)")
    seed_ids = [s["seed"] for s in seeds]
    methods = list(seeds[0]["labels_test"])
    main_scarf, main_raw = f"scarf|{k_main}", f"raw|{k_main}"
    for key in (main_scarf, main_raw):
        if key not in methods:
            raise KeyError(f"ไม่มีกลุ่มค้นพบ {key} (k หลัก = {k_main})")

    nmi_items, nmi_index = [], {}          # (codes, n_levels) ต่อรายการ; index: ชื่อกลุ่มรายการ -> list ตำแหน่ง

    def add_nmi(group, labels):
        l, nl = stats.encode(np.asarray(labels)[known])
        nmi_items.append((l, nl))
        nmi_index.setdefault(group, []).append(len(nmi_items) - 1)

    preds, pred_index = [], {}

    def add_pred(group, pred):
        preds.append(np.asarray(pred, dtype=np.float32))
        pred_index.setdefault(group, []).append(len(preds) - 1)

    # ---- 1. กลุ่มที่ค้นพบ (M1) --------------------------------------------------------------
    for art in seeds:
        for method in methods:
            add_nmi(method, art["labels_test"][method])

    # ---- 2. กลุ่มสุ่มจับคู่ขนาด สำหรับ H1a (NMI) และสำหรับปรับเกณฑ์ (H3b) --------------------------
    seed_rows_h3b = []
    with timer.section("random_control_and_threshold_fit", sets=config.random_sets, seeds=len(seeds)):
        for art in seeds:
            seed = art["seed"]
            pv, pt = np.asarray(art["p_val"]), np.asarray(art["p_test"])
            base_pred = (pt >= .5).astype(int)
            add_pred("base", base_pred)
            lv, lt = np.asarray(art["labels_val"][main_scarf]), np.asarray(art["labels_test"][main_scarf])
            method_pred, model = controls.fit_group_thresholds(pv, y_val, lv, shared["val_ids"], pt, lt,
                                                               config.min_threshold_group, config.selection_accuracy_tolerance,
                                                               min_class=config.min_threshold_class)
            add_pred("method", method_pred)
            val_rate = float(model.predict(pv, lv).mean())
            single_pred, single_info = controls.single_threshold_predict(pv, pt, val_rate)
            add_pred("single", single_pred)
            val_perms = controls.permuted_label_sets(lv, config.random_sets, config.control_seed + 7919 * seed)
            test_perms = controls.permuted_label_sets(lt, config.random_sets, config.control_seed + 104729 * seed)
            for vperm, tperm in zip(val_perms, test_perms):
                add_nmi("rand_nmi", tperm)
                p_rand, _ = controls.fit_group_thresholds(pv, y_val, vperm, shared["val_ids"], pt, tperm,
                                                          config.min_threshold_group, config.selection_accuracy_tolerance,
                                                               min_class=config.min_threshold_class)
                add_pred("rand", p_rand)
            seed_rows_h3b.append({"seed": seed, "single_threshold": single_info["threshold"],
                                  "single_validation_rate": single_info["validation_rate"],
                                  "method_validation_rate": val_rate, "method_validation_accuracy": model.validation_["accuracy"],
                                  "erm_validation_accuracy": model.baseline_accuracy_})

    # ---- 3. เพดานการกู้คืนประชากร (oracle) ------------------------------------------------------
    ceiling_rows = []
    if all(key in shared for key in ("xt", "xv", "xx", "train_inter")):
        with timer.section("ceiling_classifier", seeds=len(config.cheap_seeds), k=k_main):
            for seed in config.cheap_seeds:
                c = controls.recoverability_ceiling(shared["xt"], shared["train_inter"], shared["xv"], shared["xx"],
                                                    k_main, seed, config.ceiling_trees, config.threads)
                add_nmi("ceil_a", c["pred_class_test"])
                add_nmi("ceil_b", c["kmeans_test"])
                ceiling_rows.append({"seed": seed, "uses_demographics": True})

    # ---- 4. กลุ่มผสม oracle–สุ่ม สำหรับ H4a (oracle) -------------------------------------------------
    mix_points = []
    with timer.section("mixed_groups_H4a", p_grid=len(config.mixed_p), reps=config.mixed_reps, seeds=len(seeds)):
        for art in seeds:
            seed = art["seed"]
            pv, pt = np.asarray(art["p_val"]), np.asarray(art["p_test"])
            val_true = np.asarray(shared["val_inter"]).astype(str)
            for pi, p in enumerate(config.mixed_p):
                for rep in range(config.mixed_reps):
                    rng_v = np.random.default_rng([config.control_seed, seed, pi, rep, 0])
                    rng_t = np.random.default_rng([config.control_seed, seed, pi, rep, 1])
                    gv, gt = controls.mixed_groups(val_true, p, rng_v), controls.mixed_groups(test_inter, p, rng_t)
                    mix_pred, _ = controls.fit_group_thresholds(pv, y_val, gv, shared["val_ids"], pt, gt,
                                                                config.min_threshold_group, config.selection_accuracy_tolerance,
                                                               min_class=config.min_threshold_class)
                    add_nmi(f"mix|{pi}|{rep}", gt)
                    add_pred(f"mix|{pi}|{rep}", mix_pred)
                    mix_points.append((pi, rep, seed))

    # ---- 5. ตัวประเมินต่อรอบ bootstrap ---------------------------------------------------------------
    P = np.vstack(preds)
    Cm = (P == y_test[None, :]).astype(np.float32)
    n_nmi = len(nmi_items)

    def stat_fn(w):
        wk = w[known]
        values = [stats.nmi(stats.contingency(t_codes, nt, l, nl, wk)) for l, nl in nmi_items]
        woh = (w[:, None] * OH)
        rates = (P @ woh.astype(np.float32)) / (w @ OH)[None, :]
        gap = rates.max(1) - rates.min(1)
        acc = (Cm @ w.astype(np.float32)) / w.sum()
        return np.concatenate([values, gap, acc])

    def derive(vec):
        """vec: (R × stats) -> dict ชื่อปริมาณ -> (R,) เฉลี่ยข้าม seed ภายในรอบ ตามแผน §3.1"""
        vec = np.atleast_2d(vec)
        nm, gp, ac = vec[:, :n_nmi], vec[:, n_nmi:n_nmi + len(preds)], vec[:, n_nmi + len(preds):]
        mean = lambda block, group: block[:, pred_index[group] if block is not nm else nmi_index[group]].mean(1)
        d = {}
        for method in methods:
            d[f"N|{method}"] = mean(nm, method)
        d["N_rand"] = mean(nm, "rand_nmi")
        d["dN_raw"] = d[f"N|{main_scarf}"] - d[f"N|{main_raw}"]
        d["dN_rand"] = d[f"N|{main_scarf}"] - d["N_rand"]
        d["N_geo"] = d["N|geoproxy"] if "geoproxy" in methods else np.full(len(vec), np.nan)
        if "ceil_a" in nmi_index:
            d["C_a"], d["C_b"] = mean(nm, "ceil_a"), mean(nm, "ceil_b")
            d["N_over_C_a"] = d[f"N|{main_scarf}"] / d["C_a"]
            d["N_over_C_b"] = d[f"N|{main_scarf}"] / d["C_b"]
        base_gap, base_acc = mean(gp, "base"), mean(ac, "base")
        gap_of = lambda g: mean(gp, g)
        acc_of = lambda g: mean(ac, g)
        d["Gap_base"], d["Gap_method"] = base_gap, gap_of("method")
        d["dGap_method"] = base_gap - gap_of("method")
        d["dGap_single"] = base_gap - gap_of("single")
        d["dGap_rand"] = base_gap - gap_of("rand")
        d["B_rand"] = d["dGap_method"] - d["dGap_rand"]
        d["B_single"] = d["dGap_method"] - d["dGap_single"]
        d["dAcc_method"] = acc_of("method") - base_acc
        d["dAcc_single"] = acc_of("single") - base_acc
        d["dAcc_rand"] = acc_of("rand") - base_acc
        # H4a: จุด (p, rep) เฉลี่ยข้าม seed แล้วประมาณความชัน OLS ของ dGap ต่อ NMI
        xs, ys = [], []
        for pi in range(len(config.mixed_p)):
            for rep in range(config.mixed_reps):
                g = f"mix|{pi}|{rep}"
                xs.append(mean(nm, g))
                ys.append(base_gap - mean(gp, g))
        xs, ys = np.array(xs), np.array(ys)                     # (points × R)
        xc, yc = xs - xs.mean(0), ys - ys.mean(0)
        den = (xc ** 2).sum(0)
        d["H4a_slope"] = np.where(den > 0, (xc * yc).sum(0) / np.where(den > 0, den, 1), np.nan)
        d["H4a_intercept"] = ys.mean(0) - d["H4a_slope"] * xs.mean(0)
        d["H4a_predicted_dGap_at_scarf_NMI"] = d["H4a_intercept"] + d["H4a_slope"] * d[f"N|{main_scarf}"]
        d["H4a_residual_observed_minus_predicted"] = d["dGap_method"] - d["H4a_predicted_dGap_at_scarf_NMI"]
        return d, xs, ys

    point_vec = stat_fn(np.ones(n))[None, :]
    point, xs_pt, ys_pt = derive(point_vec)

    # ---- 6. ตารางจุดประมาณราย seed -----------------------------------------------------------------
    seed_rows = []
    for art_i, art in enumerate(seeds):
        for method in methods:
            idx = nmi_index[method][art_i]
            l, nl = nmi_items[idx]
            c = stats.contingency(t_codes, nt, l, nl)
            seed_rows.append({"seed": art["seed"], "method": method, "nmi": stats.nmi(c), "ari": stats.ari(c),
                              "ami": stats.ami(c), "n_known": int(known.sum())})
    seed_table = pd.DataFrame(seed_rows)
    seed_table.to_csv(out / "confirm_alignment_seed.csv", index=False)
    pd.DataFrame(seed_rows_h3b).to_csv(out / "confirm_h3b_seed.csv", index=False)
    if ceiling_rows:
        def seed_nmi(group, i):
            l, nl = nmi_items[nmi_index[group][i]]
            return stats.nmi(stats.contingency(t_codes, nt, l, nl))
        pd.DataFrame([{**r, "nmi_ceil_a": seed_nmi("ceil_a", i), "nmi_ceil_b": seed_nmi("ceil_b", i)}
                      for i, r in enumerate(ceiling_rows)]).to_csv(out / "confirm_ceiling_seed.csv", index=False)
    pts = pd.DataFrame([{"p": config.mixed_p[pi], "rep": rep, "nmi_mean_over_seeds": xs_pt[pi * config.mixed_reps + rep, 0],
                         "dGap_mean_over_seeds": ys_pt[pi * config.mixed_reps + rep, 0], "uses_demographics": True}
                        for pi in range(len(config.mixed_p)) for rep in range(config.mixed_reps)])
    pts.to_csv(out / "confirm_h4a_points.csv", index=False)

    # ---- 7. bootstrap ------------------------------------------------------------------------------
    results = {"point": {k: float(v[0]) for k, v in point.items()}, "kinds": {}}
    if "lei" in kinds and "test_lei" not in shared:
        raise KeyError("ต้องมี test_lei สำหรับ cluster bootstrap ตามผู้ให้กู้")
    for kind in kinds:
        cluster = None if kind == "row" else stats.encode(np.asarray(shared["test_lei"]))[0]
        with timer.section(f"bootstrap_{kind}", rounds=rounds, stats=n_nmi + 2 * len(preds), n_test=n):
            draws = stats.run_bootstrap(stat_fn, n, rounds, config.bootstrap_seed, cluster)
        derived, _, _ = derive(draws)
        summary = _summarize(derived, point, kind, config)
        summary.to_csv(out / f"confirm_bootstrap_summary_{kind}.csv", index=False)
        results["kinds"][kind] = {"derived": derived, "summary": summary, "hypotheses": _hypotheses(derived, point, config)}
    hyp_rows = []
    for kind, r in results["kinds"].items():
        for h, v in r["hypotheses"].items():
            hyp_rows.append({"bootstrap": kind, "hypothesis": h, **v})
    hyp = pd.DataFrame(hyp_rows)
    if len(results["kinds"]) == 2:       # ข้อสรุปเข้มกว่า: ผ่านต่อเมื่อทั้งสองแบบผ่าน; p = ค่ามากกว่า
        extra = []
        for h, part in hyp.groupby("hypothesis", sort=False):
            extra.append({"bootstrap": "conservative(max)", "hypothesis": h, "p_state": part.p_state.max(),
                          "passes_state": bool(part.passes_state.all())})
        hyp = pd.concat([hyp, pd.DataFrame(extra)], ignore_index=True)
    hyp.to_csv(out / "confirm_hypotheses.csv", index=False)
    results["hypotheses_table"] = hyp
    timing = pd.DataFrame(timer.rows)
    timing.to_csv(out / "confirm_timing.csv", index=False)
    (out / "confirm_meta.json").write_text(json.dumps({
        "state": state, "n_test": n, "n_test_known_demographics": int(known.sum()), "k_main": k_main,
        "bootstrap_rounds": rounds, "bootstrap_kinds": list(kinds), "network_seeds": seed_ids,
        "cheap_seeds": list(config.cheap_seeds) if ceiling_rows else [], "random_sets": config.random_sets,
        "mixed_p": list(config.mixed_p), "mixed_reps": config.mixed_reps,
        "thresholds": {"delta_min": config.delta_min, "theta_neg": config.theta_neg, "m": config.m_benefit,
                       "delta_acc_min": config.delta_acc_min},
        "eligible_race_groups": eligible_races.tolist(),
        "uses_demographics_labels": USES_DEMOGRAPHICS,
        "group_dro": "not part of the confirmatory pipeline (context_dro mode, GA only)",
        "group_definition_for_discovered_groups": "c (k-means without y)"}, indent=2, ensure_ascii=False), encoding="utf-8")
    results["timing"] = timing
    return results


def _summarize(derived, point, kind, config):
    rows = []
    for name, draws in derived.items():
        lo2, hi2 = stats.percentile_ci(draws, 0.95, "two")
        rows.append({"bootstrap": kind, "quantity": name, "point": float(point[name][0]),
                     "boot_mean": float(np.nanmean(draws)), "boot_sd": float(np.nanstd(draws, ddof=1)),
                     "ci95_two_low": float(lo2), "ci95_two_high": float(hi2),
                     "ci95_one_lower": float(stats.percentile_ci(draws, 0.95, "lower")),
                     "ci95_one_upper": float(stats.percentile_ci(draws, 0.95, "upper"))})
    return pd.DataFrame(rows)


def _hypotheses(D, point, config):
    """p ด้านเดียวต่อรัฐ (IUT ภายในรัฐ) และธงตามเกณฑ์ §2.5 / §5.2; ข้ามรัฐใช้ stats.combine_states"""
    lower = lambda x: float(stats.percentile_ci(x, 0.95, "lower"))
    upper = lambda x: float(stats.percentile_ci(x, 0.95, "upper"))
    d, m, th, da = config.delta_min, config.m_benefit, config.theta_neg, config.delta_acc_min
    main = f"N|scarf|{config.k_main}"
    out = {}
    p1 = [stats.p_greater(D["dN_raw"], d), stats.p_greater(D["dN_rand"], d)]
    out["H1a"] = {"p_state": stats.iut_p(p1), "passes_state": bool(lower(D["dN_raw"]) > d and lower(D["dN_rand"]) > d),
                  "detail": f"lower95 dN_raw={lower(D['dN_raw']):.4f}, dN_rand={lower(D['dN_rand']):.4f}, delta_min={d}"}
    out["H1b"] = {"p_state": stats.p_less(D[main], th), "passes_state": bool(upper(D[main]) < th),
                  "detail": f"upper95 N_scarf={upper(D[main]):.4f}, theta_neg={th}"}
    p3 = [stats.p_greater(D["B_rand"], m), stats.p_greater(D["B_single"], m), stats.p_greater(D["dAcc_method"], da)]
    out["H3b"] = {"p_state": stats.iut_p(p3),
                  "passes_state": bool(lower(D["B_rand"]) > m and lower(D["B_single"]) > m and lower(D["dAcc_method"]) > da),
                  "detail": f"lower95 B_rand={lower(D['B_rand']):.4f}, B_single={lower(D['B_single']):.4f}, dAcc={lower(D['dAcc_method']):.4f}"}
    out["H4a"] = {"p_state": stats.p_greater(D["H4a_slope"], 0.), "passes_state": bool(lower(D["H4a_slope"]) > 0),
                  "detail": f"lower95 slope={lower(D['H4a_slope']):.4f}"}
    # ธงของตารางตัดสินเรื่องเล่า §5.2 (ต่อรัฐ; การรวมข้ามรัฐทำที่ขั้นตัดสิน v2.0)
    out["flag_alignment_low"] = {"p_state": np.nan, "passes_state": bool(upper(D[main]) < th), "detail": "upper95 N_s < theta_neg"}
    out["flag_alignment_high"] = {"p_state": np.nan, "passes_state": bool(
        point[main][0] >= point["N_geo"][0] and lower(D["dN_raw"]) > d and lower(D["dN_rand"]) > d),
        "detail": "N_s >= N_geo (point) and lower95 dN_raw, dN_rand > delta_min"}
    out["flag_benefit_appears"] = {"p_state": np.nan, "passes_state": bool(lower(D["B_rand"]) > m and point["dAcc_method"][0] >= da),
                                   "detail": "lower95 B_s > m and dAcc >= -0.02 (point)"}
    out["flag_benefit_absent"] = {"p_state": np.nan, "passes_state": bool(upper(D["B_rand"]) < m), "detail": "upper95 B_s < m"}
    return out
