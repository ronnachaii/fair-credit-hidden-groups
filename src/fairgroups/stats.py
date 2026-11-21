"""ตัวชี้วัดถ่วงน้ำหนัก + bootstrap + การทดสอบ (แผนวิเคราะห์ §3.1, §3.2, §3.5)

หลักการ: bootstrap ทำเป็นน้ำหนักจำนวนเต็มต่อใบคำขอ (จำนวนครั้งที่ถูกสุ่มได้) แล้วคำนวณตัวชี้วัดจากตารางไขว้ถ่วงน้ำหนัก
จึงไม่ต้องสร้างข้อมูลซ้ำทุกรอบ ผลของ NMI/ARI/AMI ถ่วงน้ำหนักจำนวนเต็มเท่ากับตัวชี้วัดของ sklearn บนข้อมูลที่ซ้ำแถวตามน้ำหนัก
(ตรวจในเทสต์) และทุกวิธีใช้น้ำหนักชุดเดียวกันในแต่ละรอบ (paired)
"""
import numpy as np


# ------------------------------ ตัวชี้วัดจากตารางไขว้ ------------------------------
def encode(labels):
    """คืน (รหัส 0..L-1, L)"""
    values, codes = np.unique(np.asarray(labels).astype(str), return_inverse=True)
    return codes.astype(np.int64), len(values)


def contingency(a, na, b, nb, w=None):
    return np.bincount(a * nb + b, weights=w, minlength=na * nb).reshape(na, nb).astype(np.float64)


def _entropy(counts):
    counts = counts[counts > 0]
    total = counts.sum()
    return float(-(counts / total * np.log(counts / total)).sum()) if total > 0 else 0.


def mutual_info(c):
    n = c.sum()
    if n <= 0:
        return 0.
    pa, pb = c.sum(1), c.sum(0)
    nz = c > 0
    i, j = np.nonzero(nz)
    return float((c[nz] / n * (np.log(c[nz] * n) - np.log(pa[i]) - np.log(pb[j]))).sum())


def nmi(c):
    """normalized mutual information, average_method='arithmetic' (ตรงกับ sklearn)"""
    if c.sum() <= 0:
        return np.nan
    ha, hb = _entropy(c.sum(1)), _entropy(c.sum(0))
    if (c.sum(1) > 0).sum() == 1 and (c.sum(0) > 0).sum() == 1:
        return 1.0
    mi = mutual_info(c)
    return float(mi / max((ha + hb) / 2, np.finfo(float).eps))


def ari(c):
    """adjusted Rand index จากตารางไขว้ (น้ำหนักต้องเป็นจำนวนเต็ม)"""
    n = c.sum()
    comb = lambda x: x * (x - 1) / 2.
    sum_c, sum_a, sum_b = comb(c).sum(), comb(c.sum(1)).sum(), comb(c.sum(0)).sum()
    total = comb(n)
    if total == 0:
        return 1.0
    expected = sum_a * sum_b / total
    maximum = (sum_a + sum_b) / 2
    if maximum == expected:
        return 1.0
    return float((sum_c - expected) / (maximum - expected))


def ami(c):
    """adjusted MI (arithmetic) ใช้ฟังก์ชัน expected MI ของ sklearn; น้ำหนักต้องเป็นจำนวนเต็ม"""
    from sklearn.metrics.cluster._expected_mutual_info_fast import expected_mutual_information
    c = c[c.sum(1) > 0][:, c.sum(0) > 0]
    n = int(round(c.sum()))
    if c.shape[0] == 1 and c.shape[1] == 1:
        return 1.0
    mi = mutual_info(c)
    emi = expected_mutual_information(c, n)
    h = (_entropy(c.sum(1)) + _entropy(c.sum(0))) / 2
    denom = h - emi
    denom = min(denom, -np.finfo('float64').eps) if denom < 0 else max(denom, np.finfo('float64').eps)
    return float((mi - emi) / denom)


def weighted_alignment(true_codes, n_true, label_codes, n_labels, w=None, known=None):
    """NMI ระหว่างกลุ่มจริงกับกลุ่มที่ค้นพบ เฉพาะแถวที่ทราบประชากร (known)"""
    if known is not None:
        true_codes, label_codes = true_codes[known], label_codes[known]
        w = None if w is None else w[known]
    return nmi(contingency(true_codes, n_true, label_codes, n_labels, w))


def weighted_gap(pred, group_codes, eligible, w=None, n_groups=None):
    """Gap = max − min ของอัตราทำนายอนุมัติข้ามกลุ่มที่ 'เข้าเกณฑ์' (เกณฑ์ตัดสินครั้งเดียวก่อน bootstrap แล้วคงที่)
    pred เป็น 1 มิติหรือเมทริกซ์ (S × n) คืนอาร์เรย์ความยาว S (หรือ scalar)"""
    pred = np.atleast_2d(np.asarray(pred, dtype=np.float64))
    n_groups = int(group_codes.max()) + 1 if n_groups is None else n_groups
    onehot = np.zeros((len(group_codes), n_groups))
    onehot[np.arange(len(group_codes)), group_codes] = 1.
    onehot = onehot[:, eligible]
    weight = np.ones(len(group_codes)) if w is None else np.asarray(w, dtype=np.float64)
    den = weight @ onehot
    rates = ((pred * weight) @ onehot) / den
    gap = rates.max(axis=1) - rates.min(axis=1)
    return gap if gap.size > 1 else float(gap[0])


def eligible_groups(group_codes, n_groups, min_size=30, exclude=()):
    """กลุ่มที่มี ≥ min_size ใบ (นับจากชุดทดสอบเต็มก่อน bootstrap) และไม่อยู่ใน exclude (เช่น Unknown)"""
    counts = np.bincount(group_codes, minlength=n_groups)
    ok = counts >= min_size
    ok[list(exclude)] = False
    return ok


# ------------------------------ bootstrap ------------------------------
def bootstrap_weights(n, rounds, seed, cluster_codes=None):
    """generator ของน้ำหนักจำนวนเต็ม (ความยาว n) ต่อรอบ
    cluster_codes=None: bootstrap ระดับใบคำขอ; ไม่เช่นนั้น cluster bootstrap (สุ่มกลุ่มซ้ำ เช่น ผู้ให้กู้ lei)"""
    rng = np.random.default_rng(seed)
    if cluster_codes is None:
        probs = np.full(n, 1. / n)
        for _ in range(rounds):
            yield rng.multinomial(n, probs).astype(np.float64)
    else:
        cluster_codes = np.asarray(cluster_codes)
        m = int(cluster_codes.max()) + 1
        probs = np.full(m, 1. / m)
        for _ in range(rounds):
            yield rng.multinomial(m, probs).astype(np.float64)[cluster_codes]


def run_bootstrap(stat_fn, n, rounds, seed, cluster_codes=None):
    """stat_fn(w) -> 1D array; คืน draws (rounds × n_stats). ทุกสถิติในรอบเดียวกันใช้ w ชุดเดียวกัน"""
    out = [np.asarray(stat_fn(w), dtype=np.float64) for w in bootstrap_weights(n, rounds, seed, cluster_codes)]
    return np.vstack(out)


def percentile_ci(draws, level=0.95, side="two"):
    """side: 'two' = ช่วงสองด้าน, 'lower' = ขอบล่างด้านเดียว, 'upper' = ขอบบนด้านเดียว (percentile)"""
    draws = np.asarray(draws, dtype=np.float64)
    if side == "two":
        a = (1 - level) / 2
        return np.nanquantile(draws, a, axis=0), np.nanquantile(draws, 1 - a, axis=0)
    if side == "lower":
        return np.nanquantile(draws, 1 - level, axis=0)
    if side == "upper":
        return np.nanquantile(draws, level, axis=0)
    raise ValueError(side)


def p_greater(draws, threshold):
    """p ด้านเดียวของ H1: ค่า > threshold   p = (1 + #{draw <= threshold}) / (B + 1)"""
    draws = np.asarray(draws)
    return float((1 + (draws <= threshold).sum()) / (len(draws) + 1))


def p_less(draws, threshold):
    """p ด้านเดียวของ H1: ค่า < threshold   p = (1 + #{draw >= threshold}) / (B + 1)"""
    draws = np.asarray(draws)
    return float((1 + (draws >= threshold).sum()) / (len(draws) + 1))


# ------------------------------ IUT + Holm ------------------------------
def iut_p(pvalues):
    """intersection–union test: p ของข้อกล่าวอ้าง 'ผ่านครบทุกรายการ' = ค่ามากสุด (แผน §3.2)"""
    values = [p for p in pvalues]
    if not values or any(np.isnan(values)):
        return np.nan
    return float(max(values))


def holm(pvalues):
    """Holm step-down ปรับ p; รับ dict หรือ list คืนชนิดเดียวกัน (ชุดยืนยันคือ H1a,H1b,H3b,H4a = 4 การทดสอบ)"""
    keys = list(pvalues.keys()) if isinstance(pvalues, dict) else list(range(len(pvalues)))
    p = np.array([pvalues[k] for k in keys], dtype=np.float64)
    m = len(p)
    order = np.argsort(p)
    adjusted = np.empty(m)
    running = 0.
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * p[idx])
        adjusted[idx] = min(1., running)
    return dict(zip(keys, adjusted)) if isinstance(pvalues, dict) else adjusted.tolist()


# รัฐที่เข้า IUT ข้ามรัฐ (แผน §3.4); FL เป็นรัฐเสริม รายงานแยก ไม่เข้า IUT (ผู้ใช้ยืนยัน 2026-11-20)
IUT_STATES = ("GA", "CA", "OH")


def combine_states(per_state_p, family=("H1a", "H1b", "H3b", "H4a"), allowed_states=IUT_STATES):
    """per_state_p: {state: {hypothesis: p ที่ผ่าน IUT ภายในรัฐแล้ว}}
    ขั้น 1: IUT ข้ามรัฐ (ผ่านครบทุกรัฐ) = max p ข้ามรัฐ; ขั้น 2: Holm ข้ามสมมติฐานทั้ง 4
    ปฏิเสธรัฐที่ไม่อยู่ใน IUT_STATES (เช่น FL) เพื่อไม่ให้รัฐเสริมเข้ามาในการตัดสินหลักโดยไม่ตั้งใจ"""
    extra = sorted(set(per_state_p) - set(allowed_states))
    if extra:
        raise ValueError(f"รัฐ {extra} ไม่อยู่ใน IUT_STATES {tuple(allowed_states)} (รายงานแยก ไม่เข้า IUT)")
    raw = {h: iut_p([per_state_p[s][h] for s in per_state_p]) for h in family}
    return {"p_iut": raw, "p_holm": holm(raw)}


# ------------------------------ H4b: Spearman + permutation แบบแบ่งชั้นตามรัฐ ------------------------------
def _rank(x):
    from scipy.stats import rankdata
    return rankdata(x)


def stratified_spearman_permutation(x_by_state, y_by_state, n_perm=10000, seed=0):
    """สถิติ = ค่าเฉลี่ยของ Spearman ρ รายรัฐ; สลับ y ภายในรัฐ n_perm ครั้ง; p สองด้าน (แผน §3.5 ข้อ 2)
    รายงานว่าสมมติให้จุดสลับกันได้ ซึ่งไม่ตรงกับความจริงที่วิธีเดียวกันต่าง k ใช้ตัวแทนร่วมกัน"""
    rng = np.random.default_rng(seed)
    xs = [_rank(np.asarray(x_by_state[s], dtype=float)) for s in x_by_state]
    ys = [_rank(np.asarray(y_by_state[s], dtype=float)) for s in x_by_state]

    def rho(a, b):
        a, b = a - a.mean(), b - b.mean()
        d = np.sqrt((a * a).sum() * (b * b).sum())
        return float((a * b).sum() / d) if d > 0 else 0.

    observed = float(np.mean([rho(a, b) for a, b in zip(xs, ys)]))
    exceed = 0
    for _ in range(n_perm):
        stat = np.mean([rho(a, rng.permutation(b)) for a, b in zip(xs, ys)])
        exceed += abs(stat) >= abs(observed) - 1e-12
    return {"rho_mean": observed, "p_two_sided": (1 + exceed) / (n_perm + 1),
            "rho_by_state": {s: rho(a, b) for s, a, b in zip(x_by_state, xs, ys)}}
