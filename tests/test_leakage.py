"""ตรวจการรั่วจากเลขแถวจริงและจากข้อมูลจำลองที่มีค่า holdout แปลกออกไป"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from config import Config
from fairgroups.data import (TrainPreprocessor, FEATURES, NUMERIC, SENSITIVE,
                             split_data, labeled_indices)
from fairgroups.representations import crossfit_error, train_scarf
from fairgroups.clustering import discover


def sample_data():
    rng = np.random.default_rng(12)
    n = 160
    x = pd.DataFrame({c: rng.integers(1, 6, n).astype(float) for c in FEATURES},
                     index=np.arange(1000, 1000+n))
    y = np.tile([0, 1], n // 2)
    s = pd.DataFrame({"SEX": np.tile([1, 1, 2, 2], n//4),
                      "RAC1P": np.tile([1, 1, 1, 1, 2, 2, 2, 2], n//8)}, index=x.index)
    return x, y, s


def test_train_only_scaler_encoder_scarf_kmeans():
    x, y, s = sample_data()
    split = split_data(x, y, s, seed=17)
    train, test = split["train"], split["test"]
    processor = TrainPreprocessor(2).fit(train["x"])
    test_changed = test["x"].copy()
    test_changed.loc[:, "AGEP"] = 99999
    processor.transform(test_changed)
    assert not SENSITIVE.intersection(processor.feature_names_in_)
    assert set(processor.fit_ids_).isdisjoint(test["ids"])
    expected_mean = train["x"][NUMERIC].mean().to_numpy()
    np.testing.assert_allclose(processor.encoder.named_transformers_["numeric"].mean_, expected_mean)
    config = Config(scarf_epochs=1, hidden=8, embedding=4, batch_size=32)
    scarf = train_scarf(train["x"], processor, config, 17)
    _, _, km = discover(processor.transform(train["x"]), train["ids"], train["s"], 2, 17)
    for estimator in [processor, scarf, km]:
        assert set(estimator.fit_ids_) == set(train["ids"])
        assert set(estimator.fit_ids_).isdisjoint(test["ids"])
        assert set(estimator.fit_ids_).isdisjoint(split["val"]["ids"])


def test_sensitive_features_are_rejected():
    x, _, _ = sample_data()
    for sensitive in SENSITIVE:
        with pytest.raises(AssertionError):
            TrainPreprocessor().fit(x.assign(**{sensitive: 1}))


def test_oof_exactly_once_within_label_budget():
    x, y, s = sample_data()
    part = split_data(x, y, s, seed=17)["train"]
    labeled = labeled_indices(part["y"], 0.5, 17)
    processor = TrainPreprocessor(2).fit(part["x"])
    ids = part["ids"][labeled]
    rep, audit = crossfit_error(processor.transform(part["x"])[labeled], part["y"][labeled],
                               ids, Config(trees=3), 17)
    assert rep.shape == (len(labeled), 3)
    held = []
    for fold in audit["folds"]:
        assert set(fold["fit_ids"]).isdisjoint(fold["heldout_ids"])
        assert set(fold["fit_ids"]) | set(fold["heldout_ids"]) == set(ids)
        held.extend(fold["heldout_ids"])
    assert sorted(held) == sorted(ids)
    assert len(ids) == len(part["y"]) // 2


def test_recorded_experiment_has_no_holdout_in_fit():
    path = Path(__file__).resolve().parents[1] / "results/acs_round1/leakage_audit.json"
    if not path.exists():
        pytest.skip("ยังไม่ได้รันชุดจริง; หลัง --quick จะตรวจหลักฐานนี้อีกครั้ง")
    for audit in json.loads(path.read_text()):
        train, val, test = (set(audit[f"{name}_ids"]) for name in ["train", "val", "test"])
        assert train.isdisjoint(val) and train.isdisjoint(test) and val.isdisjoint(test)
        assert not SENSITIVE.intersection(audit["features"])
        for fit in audit["fits"]:
            assert set(fit["fit_ids"]).issubset(train)
            assert set(fit["fit_ids"]).isdisjoint(test | val)
        for error in audit["error_crossfits"]:
            labeled = set(error["fit_ids"])
            assert len(labeled) == int(len(train) * error["label_fraction"])
            held = []
            for fold in error["folds"]:
                assert set(fold["fit_ids"]).isdisjoint(fold["heldout_ids"])
                assert set(fold["fit_ids"]) | set(fold["heldout_ids"]) == labeled
                held.extend(fold["heldout_ids"])
            assert len(held) == len(set(held)) == len(labeled)
