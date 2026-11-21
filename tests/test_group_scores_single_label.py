"""group_scores must not raise when the 1,000-row silhouette sample contains a single label (returns NaN)."""
import numpy as np
from fairgroups.hmda_groups import group_scores


def _s(n):
    return {'race_eth': np.array(['NH White', 'NH Black'] * (n // 2)), 'sex': np.array(['Male', 'Female'] * (n // 2)),
            'age': np.array(['25-34'] * n), 'intersection': np.array(['a'] * n)}


def test_single_label_in_sample_returns_nan_instead_of_raising():
    # find a one-row cluster that the real 1,000-row sample (seed 17) misses -> sklearn raises ValueError for real
    import pandas as pd
    n = 5000
    rng = np.random.default_rng(0)
    x = rng.normal(size=(n, 3))
    from sklearn.metrics import silhouette_score
    labels = np.zeros(n, dtype=int)
    for i in range(n):
        labels[:] = 0; labels[i] = 1
        try:
            silhouette_score(x, labels, sample_size=1000, random_state=17)
        except ValueError:
            break
    else:
        raise AssertionError('no one-row cluster missed by the sample')
    out = group_scores(x, labels, pd.DataFrame(_s(n)), seed=17)
    assert out['n_clusters'] == 2
    assert np.isnan(out['silhouette'])


def test_normal_case_unchanged():
    import pandas as pd
    n = 2000
    rng = np.random.default_rng(1)
    labels = np.r_[np.zeros(n // 2, dtype=int), np.ones(n // 2, dtype=int)]
    x = rng.normal(size=(n, 3)) + labels[:, None] * 3
    out = group_scores(x, labels, pd.DataFrame(_s(n)), seed=17)
    assert out['silhouette'] > 0.3
