"""ตัวควบคุมและตัวเทียบที่ตรึงในแผนวิเคราะห์ §2.4 และ §3.6

ทุกตัวในไฟล์นี้ที่ใช้ข้อมูลประชากรในการสร้างหรือฝึก (เพดานการกู้คืน, กลุ่มผสม oracle–สุ่ม) เป็น
"ตัวควบคุมแบบ oracle ไม่ใช่วิธีที่เสนอ": ผลของมันต้องติดป้าย 'uses_demographics' ในทุกตาราง (แผน §4.1)
ตัวที่ไม่ใช้ประชากรเลย: กลุ่มสุ่มจับคู่ขนาด, เกณฑ์เดียว k = 1
"""
import numpy as np
from sklearn.cluster import KMeans
from .postprocess import ValidationThresholds
from . import stats

UNKNOWN = "Unknown"


# ---------------------------------------------------------------- 1. กลุ่มสุ่มจับคู่ขนาด (§2.4 แถว 2 และ 3)
def permuted_label_sets(labels, n_sets, seed):
    """สลับป้ายกลุ่ม (permutation) ระหว่างแถว: ขนาดทุกกลุ่มเท่ากับ labels ทุกประการ ไม่อ่าน y/ประชากร/ตัวแปร
    ใช้ได้ทั้งเป็นตัวเทียบ NMI โดยบังเอิญ (ชุดทดสอบ) และเป็นกลุ่มสุ่มสำหรับปรับเกณฑ์ (ชุดตรวจสอบ/ทดสอบ)"""
    labels = np.asarray(labels)
    rng = np.random.default_rng(seed)
    return [labels[rng.permutation(len(labels))] for _ in range(n_sets)]


def size_matched_random_nmi(true_labels, labels, n_sets=30, seed=42, unknown=UNKNOWN):
    """NMI ของกลุ่มสุ่มจับคู่ขนาด n_sets ชุด คืนอาร์เรย์ความยาว n_sets (คำนวณเฉพาะแถวที่ทราบประชากร)"""
    true_labels = np.asarray(true_labels)
    known = true_labels != unknown
    t, nt = stats.encode(true_labels[known])
    out = []
    for perm in permuted_label_sets(labels, n_sets, seed):
        l, nl = stats.encode(perm[known])
        out.append(stats.nmi(stats.contingency(t, nt, l, nl)))
    return np.array(out)


# ---------------------------------------------------------------- 2. เกณฑ์เดียว k = 1 (§2.4 แถว 4)
def match_rate_threshold(p_val, target_rate):
    """หาเกณฑ์เดียวบนชุดตรวจสอบที่ให้อัตราทำนายอนุมัติรวมใกล้ target_rate ที่สุด
    (target_rate = อัตราทำนายอนุมัติรวมบน validation ของวิธีที่เทียบ ไม่ดู test)"""
    p = np.sort(np.asarray(p_val, dtype=float))
    n = len(p)
    candidates = np.unique(np.r_[p, np.nextafter(p.max(), np.inf)])
    rates = (n - np.searchsorted(p, candidates, side="left")) / n   # อัตรา (p >= c) ที่แท้จริง รวมกรณีค่าซ้ำ
    best = np.argmin(np.abs(rates - target_rate))
    return float(candidates[best]), float(rates[best])


def single_threshold_predict(p_val, p_test, target_rate):
    """ปรับเกณฑ์ทั่วไปเกณฑ์เดียวให้อัตราอนุมัติรวมบน validation เท่ากับวิธีที่เทียบ แล้วใช้กับ test"""
    tau, achieved = match_rate_threshold(p_val, target_rate)
    return (np.asarray(p_test) >= tau).astype(int), {"threshold": tau, "validation_rate": achieved}


# ---------------------------------------------------------------- ปรับเกณฑ์รายกลุ่ม (ขั้นตอนเดียวกับ H3b / H4a)
def fit_group_thresholds(p_val, y_val, val_groups, val_ids, p_test, test_groups, min_group=200, tolerance=0.02,
                         objective="parity", min_class=30):
    """ขั้นตอนเดียวกับ postprocess.ValidationThresholds (เกณฑ์หาจาก validation เท่านั้น); คืน (pred_test, model)"""
    model = ValidationThresholds(objective, min_group, tolerance, min_class).fit(p_val, y_val, val_groups, val_ids)
    return model.predict(p_test, test_groups), model


# ---------------------------------------------------------------- 3. เพดานการกู้คืนประชากร (§2.4 แถว 8)  [oracle]
def recoverability_ceiling(xt, train_groups, xv, xx, k, seed, trees=300, threads=2, unknown=UNKNOWN,
                           lgbm_params=None):
    """(ก) LightGBM ทำนายเชื้อชาติ × เพศจากตัวแปรชุดเดียวกัน (ฝึกบนแถวฝึกที่ทราบประชากรเท่านั้น) -> ป้ายที่ทำนายบน test
       (ข) k-means (k เดียวกัน) บนเวกเตอร์ความน่าจะเป็นที่ทำนาย: fit บน validation (นอกตัวอย่างของตัวจำแนก) แล้วทำนาย test
    ใช้ข้อมูลประชากรฝึกตัวจำแนก จึงเป็นตัวควบคุมแบบ oracle ไม่ใช่วิธีที่เสนอ
    คืน dict: pred_class_test (ป้ายกลุ่มจริงที่ทำนาย), kmeans_test, classes"""
    from lightgbm import LGBMClassifier
    train_groups = np.asarray(train_groups).astype(str)
    known = train_groups != unknown
    classes, y = np.unique(train_groups[known], return_inverse=True)
    params = dict(n_estimators=trees, num_leaves=15, max_depth=5, learning_rate=.05, verbosity=-1,
                  n_jobs=threads, random_state=seed, deterministic=True, force_col_wise=True,
                  subsample=0.8, subsample_freq=1, colsample_bytree=0.8)  # สุ่มย่อยเพื่อให้ seed มีผลจริง
    params.update(lgbm_params or {})
    clf = LGBMClassifier(**params).fit(xt[known], y)
    prob_test = clf.predict_proba(xx)
    km = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(clf.predict_proba(xv))
    return {"pred_class_test": classes[prob_test.argmax(1)], "kmeans_test": km.predict(prob_test).astype(int),
            "classes": classes.tolist(), "uses_demographics": True}


# ---------------------------------------------------------------- 4. กลุ่มผสม oracle–สุ่ม (§3.6)  [oracle]
def mixed_groups(true_labels, p, rng):
    """แต่ละใบ: ด้วยความน่าจะเป็น p ได้กลุ่มจริง; ด้วย 1 − p ได้กลุ่มที่สุ่มจากการแจกแจงเดิมของชุดเดียวกัน
    (คงขนาดกลุ่มโดยเฉลี่ย) p = 1 -> oracle เต็ม, p = 0 -> สุ่มล้วน"""
    true_labels = np.asarray(true_labels)
    if not 0. <= p <= 1.:
        raise ValueError("p ต้องอยู่ในช่วง [0, 1]")
    take_true = rng.random(len(true_labels)) < p
    random_part = true_labels[rng.integers(len(true_labels), size=len(true_labels))]
    return np.where(take_true, true_labels, random_part)
