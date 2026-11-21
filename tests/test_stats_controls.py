"""ทดสอบ bootstrap/ตัวชี้วัดถ่วงน้ำหนัก, IUT+Holm, ตัวเทียบสุ่มจับคู่ขนาด, เกณฑ์เดียว k=1, เพดานการกู้คืน, กลุ่มผสม H4a"""
import numpy as np
import pytest
from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score, normalized_mutual_info_score
from fairgroups import stats, controls
from fairgroups.metrics import evaluate


def _labels(n=600, seed=0):
    rng = np.random.default_rng(seed)
    a = rng.integers(0, 5, n)
    b = np.where(rng.random(n) < .4, a % 3, rng.integers(0, 4, n))
    return a, b


def test_nmi_ari_ami_match_sklearn_unweighted():
    a, b = _labels()
    ca, na = stats.encode(a)
    cb, nb = stats.encode(b)
    c = stats.contingency(ca, na, cb, nb)
    assert stats.nmi(c) == pytest.approx(normalized_mutual_info_score(a, b, average_method="arithmetic"), abs=1e-12)
    assert stats.ari(c) == pytest.approx(adjusted_rand_score(a, b), abs=1e-12)
    assert stats.ami(c) == pytest.approx(adjusted_mutual_info_score(a, b, average_method="arithmetic"), abs=1e-9)


def test_integer_weights_equal_repeated_rows():
    a, b = _labels(300, 1)
    w = np.random.default_rng(2).integers(0, 4, len(a)).astype(float)
    ca, na = stats.encode(a)
    cb, nb = stats.encode(b)
    c = stats.contingency(ca, na, cb, nb, w)
    ra, rb = np.repeat(a, w.astype(int)), np.repeat(b, w.astype(int))
    assert stats.nmi(c) == pytest.approx(normalized_mutual_info_score(ra, rb, average_method="arithmetic"), abs=1e-12)
    assert stats.ari(c) == pytest.approx(adjusted_rand_score(ra, rb), abs=1e-12)
    assert stats.ami(c) == pytest.approx(adjusted_mutual_info_score(ra, rb, average_method="arithmetic"), abs=1e-9)


def test_weighted_gap_matches_evaluate_and_group_eligibility_is_fixed():
    rng = np.random.default_rng(3)
    n = 900
    race = rng.choice(["NH White", "NH Black", "Hispanic", "Unknown"], n, p=[.5, .2, .2, .1])
    sex = rng.choice(["Male", "Female"], n)
    y = rng.integers(0, 2, n)
    prob = np.clip(.5 + .2 * (race == "NH White") + rng.normal(0, .2, n), 0, 1)
    s = {"race_eth": race, "sex": sex, "age": np.full(n, "35-44"),
         "intersection": np.where(race == "Unknown", "Unknown", race + " × " + sex)}
    import pandas as pd
    m = evaluate(y, prob, pd.DataFrame(s), 30)
    races, codes = np.unique(race, return_inverse=True)
    elig = stats.eligible_groups(codes, len(races), 30, exclude=[list(races).index("Unknown")])
    assert stats.weighted_gap((prob >= .5).astype(int), codes, elig) == pytest.approx(m["approval_rate_gap_race_eth"])


def test_bootstrap_is_paired_reproducible_and_cluster_weights_are_blockwise():
    w = list(stats.bootstrap_weights(100, 3, 7))
    w2 = list(stats.bootstrap_weights(100, 3, 7))
    for x, y in zip(w, w2):
        np.testing.assert_array_equal(x, y)
        assert x.sum() == 100
    clusters = np.repeat(np.arange(10), 10)
    for x in stats.bootstrap_weights(100, 5, 1, clusters):
        assert x.sum() == 100
        for c in range(10):                      # ทุกใบของผู้ให้กู้เดียวกันได้น้ำหนักเท่ากัน
            assert len(set(x[clusters == c])) == 1
    draws = stats.run_bootstrap(lambda w: [w.mean(), (w ** 2).mean()], 100, 50, 3)
    assert draws.shape == (50, 2) and np.allclose(draws[:, 0], 1.)


def test_ci_and_pvalues():
    d = np.linspace(0.02, 0.05, 1000)
    assert stats.percentile_ci(d, .95, "lower") > 0.02
    assert stats.p_greater(d, 0.0) == pytest.approx(1 / 1001)
    assert stats.p_greater(d, 0.06) == pytest.approx(1.0)
    assert stats.p_less(d, 0.10) == pytest.approx(1 / 1001)


def test_iut_is_max_and_holm_four_tests():
    assert stats.iut_p([0.01, 0.04, 0.02]) == 0.04
    adj = stats.holm({"H1a": 0.01, "H1b": 0.02, "H3b": 0.03, "H4a": 0.04})
    assert adj["H1a"] == pytest.approx(0.04) and adj["H1b"] == pytest.approx(0.06)
    assert adj["H3b"] == pytest.approx(0.06) and adj["H4a"] == pytest.approx(0.06)     # monotone step-down
    assert stats.holm([0.5, 0.5, 0.5, 0.5]) == [1.0] * 4
    combo = stats.combine_states({"CA": {"H1a": .01, "H1b": .02, "H3b": .5, "H4a": .01},
                                  "OH": {"H1a": .03, "H1b": .01, "H3b": .2, "H4a": .02}})
    assert combo["p_iut"]["H1a"] == .03 and combo["p_iut"]["H3b"] == .5
    assert combo["p_holm"]["H1a"] == pytest.approx(.08) and combo["p_holm"]["H3b"] == pytest.approx(.5)


def test_combine_states_rejects_states_outside_iut_set():
    row = {"H1a": .01, "H1b": .02, "H3b": .5, "H4a": .01}
    assert stats.IUT_STATES == ("GA", "CA", "OH")
    assert stats.combine_states({"GA": row, "CA": row, "OH": row})["p_iut"]["H1a"] == .01
    with pytest.raises(ValueError, match="FL"):
        stats.combine_states({"GA": row, "CA": row, "OH": row, "FL": row})


def test_stratified_spearman_permutation_detects_monotone_relation():
    x = {"A": np.arange(11.), "B": np.arange(11.)}
    y = {"A": np.arange(11.) ** 2, "B": np.arange(11.) * 3}
    r = stats.stratified_spearman_permutation(x, y, n_perm=300, seed=1)
    assert r["rho_mean"] == pytest.approx(1.0) and r["p_two_sided"] < .02


# --------------------------------------------------------------------------- ตัวควบคุม
def test_size_matched_random_nmi_keeps_sizes_and_is_near_zero_for_unrelated_labels():
    rng = np.random.default_rng(0)
    true = rng.choice(["a", "b", "c"], 3000)
    labels = (np.array(["a", "b", "c"]).searchsorted(true) % 3)          # ตรงกับกลุ่มจริง 100%
    assert stats.nmi(stats.contingency(*stats.encode(true)[:1], 3, *stats.encode(labels)[:1], 3)) == pytest.approx(1.0)
    perms = controls.permuted_label_sets(labels, 30, 5)
    assert len(perms) == 30
    for p in perms:
        np.testing.assert_array_equal(np.sort(p), np.sort(labels))      # ขนาดกลุ่มเท่ากันทุกประการ
    nmis = controls.size_matched_random_nmi(true, labels, 30, 5)
    assert len(nmis) == 30 and nmis.max() < 0.02
    np.testing.assert_array_equal(nmis, controls.size_matched_random_nmi(true, labels, 30, 5))   # ซ้ำได้


def test_size_matched_random_ignores_unknown_rows():
    true = np.array(["a", "b"] * 50 + ["Unknown"] * 20)
    labels = np.array([0, 1] * 50 + [0] * 20)
    n_known = controls.size_matched_random_nmi(true, labels, 5, 1)
    assert np.isfinite(n_known).all()


def test_single_threshold_matches_target_rate_without_seeing_test():
    rng = np.random.default_rng(4)
    pv, pt = rng.random(5000), rng.random(5000)
    pred, info = controls.single_threshold_predict(pv, pt, 0.30)
    assert abs(info["validation_rate"] - 0.30) < 2e-4
    assert abs((pv >= info["threshold"]).mean() - info["validation_rate"]) < 1e-12
    assert abs(pred.mean() - 0.30) < 0.03
    tau0, _ = controls.match_rate_threshold(pv, 1.0)
    assert (pv >= tau0).all()


def test_recoverability_ceiling_high_when_features_encode_group_and_low_when_not():
    rng = np.random.default_rng(5)
    n = 900
    groups = rng.choice(["g1", "g2", "g3"], n)
    informative = np.c_[(groups == "g1") * 2. + rng.normal(0, .3, n), (groups == "g2") * 2. + rng.normal(0, .3, n),
                        rng.normal(size=n)]
    noise = rng.normal(size=(n, 3))
    tr, va, te = slice(0, 500), slice(500, 700), slice(700, 900)
    from fairgroups.stats import nmi, contingency, encode
    def ceiling_nmi(x):
        out = controls.recoverability_ceiling(x[tr], groups[tr], x[va], x[te], 3, 17, trees=40, threads=1)
        t, nt = encode(groups[te])
        a, na = encode(out["pred_class_test"])
        b, nb = encode(out["kmeans_test"])
        assert out["uses_demographics"] is True
        return nmi(contingency(t, nt, a, na)), nmi(contingency(t, nt, b, nb))
    hi, lo = ceiling_nmi(informative), ceiling_nmi(noise)
    assert hi[0] > 0.5 and hi[1] > 0.3
    assert lo[0] < 0.1 and lo[1] < 0.1


def test_ceiling_trains_on_known_rows_only():
    rng = np.random.default_rng(6)
    n = 300
    groups = np.array(["g1", "g2", "Unknown"])[rng.integers(0, 3, n)]
    x = rng.normal(size=(n, 3))
    out = controls.recoverability_ceiling(x, groups, x, x, 2, 1, trees=5, threads=1)
    assert "Unknown" not in out["classes"] and "Unknown" not in set(out["pred_class_test"])


def test_mixed_groups_endpoints_and_monotone_alignment():
    rng = np.random.default_rng(7)
    true = rng.choice(["a", "b", "c", "d"], 4000)
    t, nt = stats.encode(true)
    def nmi_at(p):
        g = controls.mixed_groups(true, p, np.random.default_rng(1))
        l, nl = stats.encode(g)
        return stats.nmi(stats.contingency(t, nt, l, nl)), g
    values = [nmi_at(p)[0] for p in [0, .1, .25, .5, .75, 1]]
    assert values[-1] == pytest.approx(1.0) and values[0] < 0.01
    assert all(a < b for a, b in zip(values, values[1:]))                # NMI เพิ่มตาม p
    g0 = nmi_at(0)[1]
    for c in ["a", "b", "c", "d"]:                                       # คงขนาดกลุ่มโดยเฉลี่ย
        assert abs((g0 == c).mean() - (true == c).mean()) < 0.03
    with pytest.raises(ValueError):
        controls.mixed_groups(true, 1.2, np.random.default_rng(1))
