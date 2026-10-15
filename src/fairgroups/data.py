"""โหลด ACS และแยกข้อมูลประชากรออกก่อนแปลงตัวแปร"""
from pathlib import Path
import numpy as np
import pandas as pd
from folktables import ACSDataSource, ACSIncome
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SENSITIVE = {"SEX", "RAC1P"}
CATEGORICAL = ["COW", "SCHL", "MAR", "OCCP", "POBP", "RELP"]
NUMERIC = ["AGEP", "WKHP"]
FEATURES = NUMERIC + CATEGORICAL


def load_data(root="data"):
    """ใช้แคชเดิมก่อน ถ้าไม่มีจึงให้ folktables ดาวน์โหลด"""
    cache = Path(root) / "2018/1-Year/psam_p06.csv"
    source = ACSDataSource(survey_year="2018", horizon="1-Year",
                           survey="person", root_dir=str(root))
    frame = source.get_data(states=["CA"], download=not cache.exists())
    # ใช้กติกาคัดคนของ ACSIncome โดยเก็บเลขแถวต้นฉบับไว้ตรวจข้อมูลรั่ว
    filtered = ACSIncome._preprocess(frame)
    x = filtered[FEATURES].fillna(-1).copy()
    y = (filtered["PINCP"].to_numpy() > 50000).astype(np.int64)
    sensitive = filtered[["SEX", "RAC1P"]].astype(int).copy()
    del frame, filtered
    return x, y, sensitive


def reference_groups(sensitive):
    """กลุ่มหลักใช้ White/Non-white เพื่อลดปัญหากลุ่มเล็ก"""
    sex = sensitive.SEX.to_numpy().astype(str)
    race = np.where(sensitive.RAC1P.to_numpy() == 1, "White", "Non-white")
    return {"sex": sex, "race": race,
            "intersection": np.char.add(np.char.add(sex, "_"), race),
            "race_detail": sensitive.RAC1P.to_numpy().astype(str)}


def split_data(x, y, sensitive, seed, max_rows=0):
    """สุ่มนำร่องและแบ่ง 60/20/20 ด้วย y ร่วมกับเพศและเชื้อชาติแบบสองกลุ่ม"""
    positions = np.arange(len(y))
    strata = np.char.add(reference_groups(sensitive)["intersection"], y.astype(str))
    if max_rows and len(y) > max_rows:
        positions, _ = train_test_split(positions, train_size=max_rows,
                                       stratify=strata, random_state=seed)
    train, holdout = train_test_split(positions, test_size=0.4,
                                     stratify=strata[positions], random_state=seed)
    val, test = train_test_split(holdout, test_size=0.5,
                                stratify=strata[holdout], random_state=seed)
    return {name: {"x": x.iloc[pos].copy(), "y": y[pos],
                   "s": sensitive.iloc[pos].copy(), "ids": x.index.to_numpy()[pos]}
            for name, pos in [("train", train), ("val", val), ("test", test)]}


def labeled_indices(y, fraction, seed):
    """เลือกป้ายกำกับด้วย y เท่านั้น ไม่ต้องรู้ข้อมูลประชากร"""
    ids = np.arange(len(y))
    if fraction == 1:
        return ids
    chosen, _ = train_test_split(ids, train_size=fraction, stratify=y,
                                random_state=seed)
    return np.sort(chosen)


class TrainPreprocessor:
    """รวมค่าหายากและ one-hot โดยเรียนรู้จาก train เท่านั้น"""
    def __init__(self, min_frequency=20):
        self.encoder = ColumnTransformer([
            ("numeric", StandardScaler(), NUMERIC),
            ("category", OneHotEncoder(handle_unknown="infrequent_if_exist",
             min_frequency=min_frequency, sparse_output=False, dtype=np.float32),
             CATEGORICAL)], sparse_threshold=0)

    def fit(self, frame):
        """เก็บเลขแถวและชื่อตัวแปรไว้เป็นหลักฐาน"""
        assert not SENSITIVE.intersection(frame.columns)
        self.feature_names_in_ = list(frame.columns)
        self.fit_ids_ = frame.index.to_numpy().copy()
        self.encoder.fit(frame)
        return self

    def transform(self, frame):
        return self.encoder.transform(frame).astype(np.float32)


def categorical_frames(splits):
    """LightGBM ใช้หมวดหมู่จาก train และให้ค่าใหม่เป็น missing"""
    categories = {c: sorted(splits["train"]["x"][c].unique()) for c in CATEGORICAL}
    result = {}
    for name, part in splits.items():
        frame = part["x"].copy()
        for col in CATEGORICAL:
            frame[col] = pd.Categorical(frame[col], categories=categories[col])
        result[name] = frame
    return result
