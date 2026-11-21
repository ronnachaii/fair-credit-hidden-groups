"""ค่าทดลองชุดเดียวกันสำหรับเครื่องส่วนตัวและ Colab CPU"""
from dataclasses import asdict, dataclass
import sys


@dataclass
class Config:
    quick: bool = True
    dataset: str = "hmda"
    state: str = "GA"
    lei_top_n: int = 30
    jtt_grid: tuple = (1.0, 2.0, 4.0)
    seeds: tuple = (17, 29, 43)
    label_fractions: tuple = (1.0,)
    ks: tuple = (2, 4, 8)
    max_rows: int = 20000
    epochs: int = 10
    scarf_epochs: int = 8
    batch_size: int = 256
    hidden: int = 64
    embedding: int = 32
    learning_rate: float = 0.002
    weight_decay: float = 0.001
    dro_eta: float = 0.05
    dro_adjustment: float = 0.0
    dro_eta_grid: tuple = (0.01, 0.1)
    dro_adjustment_grid: tuple = (0.0, 1.0)
    min_dro_group: int = 50
    # แผน §2.6: เกณฑ์รายกลุ่ม ต้อง validation >= 200 ใบ และแต่ละคลาส >= 30 ใบ (ไม่ใช่ min_dro_group)
    min_threshold_group: int = 200
    min_threshold_class: int = 30
    dro_finetune_epochs: int = 5
    # งบ 5 epoch ครอบคลุม checkpoint 1–5 อยู่แล้ว ไม่ฝึกงบ 3 ซ้ำ
    dro_epoch_grid: tuple = (5,)
    dro_variants: tuple = ('cy', 'cy_bal', 'c', 'c_bal')
    selection_accuracy_tolerance: float = 0.02
    dro_learning_rate_grid: tuple = (0.0002, 0.001)
    jtt_upweight: float = 10.0
    jtt_identification_epochs: int = 3
    corruption_rate: float = 0.6
    temperature: float = 0.5
    oof_folds: int = 5
    trees: int = 100
    min_category_frequency: int = 20
    min_fair_group: int = 30
    # macOS env นี้มี libomp หลายชุด ใช้หนึ่งเธรดเพื่อเลี่ยงการชนกัน
    threads: int = 1 if sys.platform == "darwin" else 2
    # torch device: 'cpu' (default, reproduces the earlier results) or 'cuda'
    device: str = "cpu"
    # --- analysis plan v1 additions (แผนวิเคราะห์ §2-§4, §8) ---
    # mode: 'confirm' = confirmatory pipeline (NO group-DRO / JTT); 'context_dro' = old full pipeline incl. DRO,
    # GA 2023 only, results are context only and never enter the confirmatory tables / multiplicity family
    mode: str = "confirm"
    year: int = 2023
    # None = split changes with each algorithm seed (legacy pilot); int = one fixed split per state-year (plan §2.1)
    split_seed: int = None
    # unlock flags for restricted data (value = SHA-256 of the frozen plan file); see fairgroups/access_guard.py
    unlock_R: str = None
    unlock_C: str = None
    plan_file: str = None
    k_main: int = 8
    delta_min: float = 0.01
    theta_neg: float = 0.10
    m_benefit: float = 0.01
    delta_acc_min: float = -0.02
    bootstrap_rounds: int = 2000
    bootstrap_seed: int = 20261120
    control_seed: int = 42
    random_sets: int = 30
    # seeds for the cheap, network-free parts (ceiling classifier) -- plan §3.3
    cheap_seeds: tuple = (17, 29, 43, 59, 71, 83, 97, 101, 113, 127)
    mixed_p: tuple = (0.0, 0.1, 0.25, 0.5, 0.75, 1.0)
    mixed_reps: int = 5
    ceiling_trees: int = 300

    def to_dict(self):
        return asdict(self)


def make_config(quick=True):
    """โหมดเต็มใช้ข้อมูลทั้งหมดและเพิ่มจำนวนรอบฝึก"""
    cfg = Config(quick=quick)
    if not quick:
        cfg.seeds = (17, 29, 43, 59, 71)
        cfg.label_fractions = (1.0,)
        cfg.max_rows = 0
        cfg.epochs = 40
        cfg.scarf_epochs = 30
        cfg.hidden = 128
        cfg.trees = 300
    return cfg


# ---------------------------------------------------------------------------
# v1.0 frozen values (แผนวิเคราะห์ §2.5, §3.3, §4.3, §8). Single place to read them.
# Changing anything here changes the SHA-256 printed by tools/freeze_v1.py and invalidates a written
# freeze manifest, which in turn makes the restricted-data guard refuse to open R / C.
# ---------------------------------------------------------------------------
V1_FROZEN = {
    "k_main": 8,                      # plan §2.2 / §8.3: primary k fixed in advance
    "ks_secondary": (2, 4, 8),        # secondary results (Silhouette-selected k stays secondary)
    "delta_min": 0.01,                # min meaningful NMI difference (H1a)
    "theta_neg": 0.10,                # ceiling for "low alignment" (H1b)
    "m_benefit": 0.01,                # min benefit of discovered groups vs random in Gap (H3b)
    "delta_acc_min": -0.02,
    "threads": 2,
    "device": "cpu",
    "network_seeds": (17, 29, 43, 59, 71),                                # SCARF / MLP: 5 seeds
    "cheap_seeds": (17, 29, 43, 59, 71, 83, 97, 101, 113, 127),          # cheap parts: 10 seeds
    "split_seed": 17,
    "bootstrap_rounds": 2000,
    "bootstrap_seed": 20261120,
    "control_seed": 42,
    "random_sets": 30,
    "mixed_p": (0.0, 0.1, 0.25, 0.5, 0.75, 1.0),
    "mixed_reps": 5,
    "min_fair_group": 30,
    "min_dro_group": 50,
    "min_threshold_group": 200,       # plan §2.6: per-group threshold needs val >= 200 rows ...
    "min_threshold_class": 30,        # ... and >= 30 in each class; else pooled default threshold 0.5
    "no_training_set_cap": True,      # user decision: no 40,000-row cap
    "holm_family": ("H1a", "H1b", "H3b", "H4a"),
}


def make_v1_config(quick=False):
    """Config used for the confirmatory pipeline. quick=True only shrinks data/epochs for smoke tests and is NOT v1.0."""
    cfg = make_config(quick=quick)
    cfg.mode = "confirm"
    cfg.threads, cfg.device = V1_FROZEN["threads"], V1_FROZEN["device"]
    cfg.split_seed = V1_FROZEN["split_seed"]
    cfg.ks = V1_FROZEN["ks_secondary"]
    for key in ("k_main", "delta_min", "theta_neg", "m_benefit", "delta_acc_min", "bootstrap_rounds",
                "bootstrap_seed", "control_seed", "random_sets", "cheap_seeds", "mixed_p", "mixed_reps",
                "min_fair_group", "min_dro_group", "min_threshold_group", "min_threshold_class"):
        setattr(cfg, key, V1_FROZEN[key])
    if not quick:
        cfg.seeds = V1_FROZEN["network_seeds"]
    return cfg
