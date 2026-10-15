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
