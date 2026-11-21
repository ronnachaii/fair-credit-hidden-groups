"""ทดสอบชุดวิเคราะห์ยืนยันด้วยข้อมูลสังเคราะห์ที่รู้คำตอบ + smoke test ของโหมด confirm / context_dro"""
import json
from dataclasses import replace
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from config import make_v1_config, Config
from fairgroups import confirmatory
from fairgroups.metrics import evaluate
from fairgroups.run import run_experiment

ROOT = Path(__file__).resolve().parents[1]


def _synthetic(n_val=6000, n_test=1600, seeds=(17, 29), informative=True):
    rng = np.random.default_rng(11)
    def split(n):
        race = rng.choice(["NH White", "NH Black", "Hispanic", "NH Asian", "Unknown"], n, p=[.5, .2, .15, .1, .05])
        sex = rng.choice(["Male", "Female"], n)
        inter = np.where(race == "Unknown", "Unknown", race + " × " + sex)
        y = (rng.random(n) < np.where(race == "NH White", .85, .72)).astype(int)
        return race, inter, y
    vr, vi, vy = split(n_val)
    tr, ti, ty = split(n_test)
    lei = rng.integers(0, 40, n_test).astype(str)
    shared = {"val_inter": vi, "test_inter": ti, "test_race": tr, "test_lei": lei, "y_val": vy, "y_test": ty,
              "val_ids": np.arange(n_val)}
    arts = []
    for seed in seeds:
        r = np.random.default_rng(seed)
        def labels(inter, race, informative_flag):
            truth_code = np.unique(inter, return_inverse=True)[1]
            noisy = np.where(r.random(len(inter)) < .6, truth_code, r.integers(0, 8, len(inter))) % 8
            return noisy if informative_flag else r.integers(0, 8, len(inter))
        lv, lt, = {}, {}
        for rep, good in [("raw", False), ("scarf", informative), ("GEORGE", False)]:
            for k in (2, 4, 8):
                lv[f"{rep}|{k}"] = labels(vi, vr, good) % k
                lt[f"{rep}|{k}"] = labels(ti, tr, good) % k
        lv["HBAC"], lt["HBAC"] = r.integers(0, 4, n_val), r.integers(0, 4, n_test)
        lv["geoproxy"], lt["geoproxy"] = r.integers(0, 4, n_val), r.integers(0, 4, n_test)
        p = lambda race: np.clip(.45 + .45 * (race == "NH White") + r.normal(0, .15, len(race)), 0, 1)
        arts.append({"seed": seed, "labels_val": lv, "labels_test": lt, "p_val": p(vr), "p_test": p(tr)})
    return shared, arts


def _small_config():
    cfg = make_v1_config(quick=True)
    cfg.cheap_seeds, cfg.ceiling_trees, cfg.mixed_reps, cfg.threads = (17, 29), 8, 2, 1
    cfg.bootstrap_rounds = 40
    return cfg


def test_analyze_end_to_end_synthetic(tmp_path):
    shared, arts = _synthetic()
    n_val, n_test, d = 6000, 1600, 5
    rng = np.random.default_rng(3)
    inter_all = np.r_[rng.choice(["a", "b", "c"], 900), shared["val_inter"], shared["test_inter"]]
    x_all = rng.normal(size=(len(inter_all), d))
    shared.update(xt=x_all[:900], xv=x_all[900:900 + n_val], xx=x_all[900 + n_val:],
                  train_inter=inter_all[:900])
    cfg = _small_config()
    res = confirmatory.analyze(shared, arts, cfg, tmp_path, state="SYN", rounds=40)
    out = tmp_path / "confirm"
    for name in ["confirm_alignment_seed.csv", "confirm_h3b_seed.csv", "confirm_ceiling_seed.csv", "confirm_h4a_points.csv",
                 "confirm_bootstrap_summary_row.csv", "confirm_bootstrap_summary_lei.csv", "confirm_hypotheses.csv",
                 "confirm_timing.csv", "confirm_meta.json"]:
        assert (out / name).exists(), name
    meta = json.loads((out / "confirm_meta.json").read_text(encoding="utf-8"))
    assert meta["k_main"] == 8 and "group_dro" in meta and meta["uses_demographics_labels"]
    p = res["point"]
    assert p["N|scarf|8"] > p["N|raw|8"] + 0.02                         # กลุ่ม scarf ที่ออกแบบให้ตรงมีค่า NMI สูงกว่า
    assert abs(p["N_rand"]) < 0.02                                       # ตัวเทียบสุ่มจับคู่ขนาด ≈ 0
    assert "C_a" in p and p["C_a"] < 0.2                                 # ข้อมูล x สังเคราะห์ไม่มีสัญญาณประชากร -> เพดานต่ำ
    # ธง H4a: NMI ที่ p=1 คือ 1.0 และ NMI เพิ่มตาม p
    pts = pd.read_csv(out / "confirm_h4a_points.csv")
    by_p = pts.groupby("p").nmi_mean_over_seeds.mean()
    assert by_p.loc[1.0] == pytest.approx(1.0) and by_p.is_monotonic_increasing and pts.uses_demographics.all()
    # Gap ฐานตรงกับ metrics.evaluate (นิยามเดียวกันกับตาราง M2 ของ pipeline)
    s = pd.DataFrame({"race_eth": shared["test_race"], "sex": "Male", "age": "35-44", "intersection": shared["test_inter"]})
    base_gaps = [evaluate(shared["y_test"], a["p_test"], s, cfg.min_fair_group)["approval_rate_gap_race_eth"] for a in arts]
    assert p["Gap_base"] == pytest.approx(np.mean(base_gaps))
    hyp = pd.read_csv(out / "confirm_hypotheses.csv")
    assert {"row", "lei", "conservative(max)"} <= set(hyp.bootstrap)
    assert hyp[hyp.hypothesis.isin(["H1a", "H1b", "H3b", "H4a"])].p_state.between(0, 1).all()
    assert hyp[(hyp.bootstrap == "row") & (hyp.hypothesis == "H4a")].passes_state.iloc[0]
    assert not hyp[(hyp.bootstrap == "row") & (hyp.hypothesis == "H1b")].passes_state.iloc[0]   # NMI scarf > theta_neg ไม่ได้ต่ำ
    comps = set(res["timing"].component)
    assert {"ceiling_classifier", "mixed_groups_H4a", "bootstrap_row", "bootstrap_lei"} <= comps


def test_bootstrap_ci_covers_point_and_is_paired(tmp_path):
    shared, arts = _synthetic(seeds=(17,))
    cfg = _small_config()
    res = confirmatory.analyze(shared, arts, cfg, tmp_path, state="SYN", rounds=60, kinds=("row",))
    summary = res["kinds"]["row"]["summary"].set_index("quantity")
    for q in ["N|scarf|8", "dN_raw", "Gap_base", "B_rand"]:
        r = summary.loc[q]
        assert r.ci95_two_low <= r.point <= r.ci95_two_high or abs(r.point - r.boot_mean) < 3 * r.boot_sd
    # ผลต่าง paired มี SD ต่ำกว่าสองค่าแยกกันถ้าสัมพันธ์กัน: อย่างน้อยต้องคำนวณได้และไม่เป็น NaN
    assert np.isfinite(summary.loc["dN_raw"].boot_sd)


def test_analyze_requires_three_eligible_race_groups(tmp_path):
    shared, arts = _synthetic()
    shared["test_race"] = np.where(np.arange(len(shared["test_race"])) % 2 == 0, "NH White", "NH Black")
    with pytest.raises(ValueError, match="< 3"):
        confirmatory.analyze(shared, arts, _small_config(), tmp_path, rounds=2, kinds=("row",))


# ----------------------------------------------------------------------------------- run_experiment smoke
@pytest.mark.skipif(not (ROOT / "data" / "hmda" / "hmda_2023_ID.csv").exists(), reason="ไม่มีไฟล์ ID 2566 ในแคช")
def test_confirm_mode_runs_on_small_state_without_dro(tmp_path):
    cfg = make_v1_config(quick=True)
    cfg.state, cfg.seeds, cfg.max_rows = "ID", (17,), 14000
    cfg.epochs, cfg.scarf_epochs, cfg.trees, cfg.ceiling_trees = 2, 1, 10, 10
    cfg.cheap_seeds, cfg.mixed_reps, cfg.bootstrap_rounds, cfg.threads = (17,), 1, 15, 2
    run_experiment(cfg, ROOT, output_dir=tmp_path / "out")
    out = tmp_path / "out"
    assert (out / "confirm" / "confirm_hypotheses.csv").exists()
    results = pd.read_csv(out / "hmda_pilot_results.csv")
    assert set(results.method) == {"ERM-MLP", "ERM-LGBM"}                  # ไม่มี DRO / JTT ใน pipeline ยืนยัน
    assert not (out / "dro_grid.csv").exists() and not (out / "jtt_validation_grid.csv").exists()
    assert not (out / "CONTEXT_ONLY_NOT_CONFIRMATORY.txt").exists()
    assert (out / "postprocess_results.csv").exists() and "ami_race_eth" in pd.read_csv(out / "clustering_results.csv")


def test_context_dro_is_ga_only_and_never_writes_into_results(tmp_path):
    for state in ["ID", "NM"]:
        with pytest.raises(ValueError, match="GA"):
            run_experiment(Config(mode="context_dro", state=state), ROOT, output_dir=tmp_path / "x")
    with pytest.raises(ValueError, match="output_dir"):
        run_experiment(Config(mode="context_dro", state="GA"), ROOT)
    with pytest.raises(ValueError, match="output_dir"):
        run_experiment(Config(mode="context_dro", state="GA"), ROOT, output_dir=ROOT / "results")
    with pytest.raises(ValueError, match="split_seed"):
        run_experiment(Config(mode="confirm", state="GA", split_seed=None), ROOT, output_dir=tmp_path / "y")
    with pytest.raises(ValueError, match="mode"):
        run_experiment(Config(mode="dro", state="GA"), ROOT, output_dir=tmp_path / "z")
