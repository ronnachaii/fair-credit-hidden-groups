"""Design B (transfer 2023 -> 2024): synthetic data only. No real HMDA file, no 2024 data, no network."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from config import make_v1_config
from fairgroups.access_guard import AccessDenied
from fairgroups.design_b import (SchemaMismatch, fit_source, apply_source, run_design_b_arrays, run_design_b)
from fairgroups.hmda import split_hmda, demographics

ROOT = Path(__file__).resolve().parents[1]


def _part(n, seed, shift=0.0, start=0):
    """Synthetic HMDA-like rows; `shift` moves the income distribution (a stand-in for year-to-year drift)."""
    rng = np.random.default_rng(seed)
    race = rng.choice(["White", "Black or African American", "Asian", "Other"], n, p=[.55, .2, .15, .1])
    eth = np.where(rng.random(n) < .12, "Hispanic or Latino", "Not Hispanic or Latino")
    sex = rng.choice(["Male", "Female", "Joint"], n)
    frame = pd.DataFrame({
        "loan_amount": rng.lognormal(12, .4, n), "income": rng.lognormal(4.5 + shift, .5, n),
        "loan_to_value_ratio": rng.normal(80, 10, n), "loan_term": rng.choice([180, 240, 360], n),
        "loan_type": rng.choice(["1", "2", "3"], n), "lei": rng.choice([f"L{i}" for i in range(12)], n),
        "tract_minority_population_percent": rng.uniform(0, 100, n),
        "derived_race": race, "derived_ethnicity": eth, "derived_sex": sex,
        "applicant_age": rng.choice(["25-34", "35-44", "45-54", "55-64"], n)},
        index=np.arange(start, start + n))
    s = demographics(frame)
    frame = frame.drop(columns=["derived_race", "derived_ethnicity", "derived_sex", "applicant_age"])
    p = 1 / (1 + np.exp(-(0.8 * (np.log(frame.income) - 4.5) + 0.5 * (s.race_eth == "NH White").to_numpy() - 0.2)))
    y = (rng.random(n) < p).astype(int)
    return frame, y, s


def _config():
    cfg = make_v1_config(quick=True)
    cfg.seeds, cfg.cheap_seeds = (17,), (17,)
    cfg.scarf_epochs, cfg.trees, cfg.ceiling_trees, cfg.mixed_reps = 1, 10, 8, 1
    cfg.bootstrap_rounds, cfg.threads, cfg.max_rows = 20, 2, 0
    return cfg


@pytest.fixture(scope="module")
def world():
    frame, y, s = _part(6000, 1)
    source = split_hmda(frame, y, s, 17)
    tf, ty, ts = _part(1600, 2, shift=0.3, start=100000)
    target = {"frame": tf, "y": ty, "s": ts, "ids": tf.index.to_numpy()}
    return source, target


def test_fit_uses_source_train_only_and_apply_does_not_change_models(world):
    source, target = world
    cfg = _config()
    m = fit_source(source["train"], source["val"], cfg, 17)
    train_ids = set(source["train"]["ids"])
    for stage, ids in m.fit_log:
        assert set(ids) == train_ids, stage
        assert set(ids).isdisjoint(source["val"]["ids"]) and set(ids).isdisjoint(source["test"]["ids"]), stage
    centers = {key: c.centers_.copy() for key, c in m.clusters.items()}
    edges, median, iteration = m.geo.edges_.copy(), m.geo.median_, m.lgb_iteration
    apply_source(m, target["frame"], cfg.ks)
    apply_source(m, target["frame"].assign(income=1e7), cfg.ks)       # extreme target values must not leak back
    for key, c in m.clusters.items():
        np.testing.assert_array_equal(c.centers_, centers[key])
    np.testing.assert_array_equal(m.geo.edges_, edges)
    assert m.geo.median_ == median and m.lgb_iteration == iteration


def test_apply_on_source_train_reproduces_fitted_labels(world):
    source, _ = world
    cfg = _config()
    m = fit_source(source["train"], source["val"], cfg, 17)
    _, _, labels = apply_source(m, source["train"]["frame"], cfg.ks)
    for (rep, k), c in m.clusters.items():
        np.testing.assert_array_equal(labels[f"{rep}|{k}"], c.labels_)


def test_schema_mismatch_is_reported(world):
    source, target = world
    cfg = _config()
    m = fit_source(source["train"], source["val"], cfg, 17)
    with pytest.raises(SchemaMismatch, match="income"):
        apply_source(m, target["frame"].drop(columns=["income"]), cfg.ks)
    with pytest.raises(SchemaMismatch, match="tract_minority"):
        apply_source(m, target["frame"].drop(columns=["tract_minority_population_percent"]), cfg.ks)


def test_design_b_end_to_end_synthetic(world, tmp_path):
    source, target = world
    cfg = _config()
    res = run_design_b_arrays(source, target, cfg, tmp_path, state="SYN", rounds=20)
    out = tmp_path / "design_B"
    for name in ["confirm_alignment_seed.csv", "confirm_h3b_seed.csv", "confirm_ceiling_seed.csv", "confirm_h4a_points.csv",
                 "confirm_bootstrap_summary_row.csv", "confirm_bootstrap_summary_lei.csv", "confirm_hypotheses.csv",
                 "confirm_meta.json"]:
        assert (out / "confirm" / name).exists(), name
    audit = json.loads((out / "design_b_audit.json").read_text(encoding="utf-8"))
    assert audit["design"] == "B_transfer" and audit["target_used_in_fit"] is False
    assert audit["n_target"] == len(target["ids"]) and audit["n_source_train"] == len(source["train"]["ids"])
    assert not (tmp_path / "confirm").exists()                      # nothing written outside design_B/
    meta = json.loads((out / "confirm" / "confirm_meta.json").read_text(encoding="utf-8"))
    assert meta["n_test"] == len(target["ids"])
    p = res["point"]
    assert {"N|scarf|8", "N|raw|8", "N_geo", "N_rand", "B_rand", "dAcc_method", "C_a"} <= set(p)
    hyp = pd.read_csv(out / "confirm" / "confirm_hypotheses.csv")
    assert hyp[hyp.hypothesis.isin(["H1a", "H1b", "H3b", "H4a"])].p_state.between(0, 1).all()


def test_design_b_base_gap_uses_source_model_on_target(world, tmp_path):
    source, target = world
    cfg = _config()
    res = run_design_b_arrays(source, target, cfg, tmp_path, state="SYN", rounds=10)
    m = fit_source(source["train"], source["val"], cfg, 17)           # same seed, same data -> same model
    _, pt, _ = apply_source(m, target["frame"], cfg.ks)
    pred = (pt >= .5).astype(int)
    race = target["s"].race_eth.to_numpy()
    rates = [pred[race == r].mean() for r in np.unique(race) if (race == r).sum() >= cfg.min_fair_group and r != "Unknown"]
    assert res["point"]["Gap_base"] == pytest.approx(max(rates) - min(rates), abs=1e-9)


def test_run_design_b_refuses_2024_without_unlock_before_any_file_access(tmp_path):
    cfg = _config()
    cfg.state = "GA"
    with pytest.raises(AccessDenied):
        run_design_b(cfg, tmp_path, tmp_path / "out")
    assert not (tmp_path / "data").exists() and not (tmp_path / "out").exists()
    with pytest.raises(ValueError):
        run_design_b(cfg, tmp_path, None)
    cfg.split_seed = None
    with pytest.raises(ValueError):
        run_design_b(cfg, tmp_path, tmp_path / "out")


def test_rounds_option_reaches_analyze_and_default_is_2000(world, tmp_path, monkeypatch):
    from fairgroups import confirmatory
    from fairgroups.design_b import __main__ as cli
    import fairgroups.design_b.core as core
    seen = {}
    monkeypatch.setattr(confirmatory, "analyze", lambda shared, seeds, config, out, state="XX", rounds=None, **kw:
                        seen.update(rounds=rounds, effective=rounds or config.bootstrap_rounds) or {})
    monkeypatch.setattr(core, "fit_source", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("stop")))
    # CLI -> run_design_b: capture the rounds argument
    got = {}
    monkeypatch.setattr(cli, "run_design_b", lambda cfg, root, out, target_rows="test", rounds=None: got.update(rounds=rounds))
    cli.main(["--state", "GA", "--output-dir", str(tmp_path), "--v1", "--rounds", "20"])
    assert got["rounds"] == 20
    cli.main(["--state", "GA", "--output-dir", str(tmp_path), "--v1", "--full"])
    assert got["rounds"] is None                        # None -> analyze uses config.bootstrap_rounds, same call as design A
    assert make_v1_config(quick=False).bootstrap_rounds == 2000
    # core -> analyze: forward the value unchanged
    monkeypatch.undo()
    source, target = world
    cfg = _config()
    captured = {}
    monkeypatch.setattr(confirmatory, "analyze", lambda shared, seeds, config, out, state="XX", rounds=None, **kw:
                        captured.update(rounds=rounds) or {})
    core.run_design_b_arrays(source, target, cfg, tmp_path, state="SYN", rounds=20)
    assert captured["rounds"] == 20
