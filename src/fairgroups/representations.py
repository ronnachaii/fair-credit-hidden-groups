"""SCARF ไม่มีป้ายกำกับ และ error representation จาก OOF ภายใน train"""
import numpy as np
import torch
from torch import nn
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from lightgbm import LGBMClassifier
from .models import set_seed


class ScarfEncoder(nn.Module):
    """สุ่มแทนค่าทีละ feature จาก marginal ของ train ก่อนทำ one-hot"""
    def __init__(self, input_dim, hidden, embedding):
        super().__init__()
        self.encoder = nn.Sequential(nn.Linear(input_dim, hidden), nn.ReLU(),
                                     nn.Linear(hidden, hidden), nn.ReLU(),
                                     nn.Linear(hidden, embedding))
        self.projector = nn.Sequential(nn.Linear(embedding, embedding), nn.ReLU(),
                                       nn.Linear(embedding, embedding))

    def forward(self, x):
        return self.encoder(x)


def contrastive_loss(a, b, temperature):
    """NT-Xent: คู่จริงคือแถวเดิมกับแถวที่แทนค่าบาง feature"""
    n = len(a)
    z = nn.functional.normalize(torch.cat([a, b]), dim=1)
    similarity = z @ z.T / temperature
    similarity.fill_diagonal_(-1e9)
    targets = (torch.arange(2*n) + n) % (2*n)
    return nn.functional.cross_entropy(similarity, targets)


def train_scarf(frame, processor, config, seed):
    """ไม่รับ y หรือข้อมูลประชากร และ donor มาจาก train เท่านั้น"""
    set_seed(seed, config.threads)
    x = processor.transform(frame)
    model = ScarfEncoder(x.shape[1], config.hidden, config.embedding)
    model.fit_ids_ = frame.index.to_numpy().copy()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate,
                                 weight_decay=config.weight_decay)
    rng = np.random.default_rng(seed)
    # สร้าง corrupted view ครั้งละ epoch เพื่อให้หมวดหมู่ยังเป็นค่าที่ถูกต้อง
    for _ in range(config.scarf_epochs):
        corrupted = frame.copy()
        for col in frame.columns:
            donors = rng.integers(0, len(frame), len(frame))
            mask = rng.random(len(frame)) < config.corruption_rate
            corrupted.loc[mask, col] = frame[col].to_numpy()[donors[mask]]
        cx = processor.transform(corrupted)
        order = rng.permutation(len(x))
        model.train()
        for start in range(0, len(x), config.batch_size):
            ids = order[start:start+config.batch_size]
            if len(ids) < 2:
                continue
            optimizer.zero_grad()
            a = model.projector(model(torch.as_tensor(x[ids])))
            b = model.projector(model(torch.as_tensor(cx[ids])))
            loss = contrastive_loss(a, b, config.temperature)
            loss.backward()
            optimizer.step()
    return model


def encode_scarf(model, x):
    """แช่แข็ง encoder ตอนจัดกลุ่ม ไม่ใช้ projection head"""
    model.eval()
    with torch.no_grad():
        return np.concatenate([model(torch.as_tensor(x[i:i+2048])).numpy()
                               for i in range(0, len(x), 2048)])


def crossfit_error(x, y, ids, config, seed):
    """ใช้ป้ายกำกับเท่าที่มี และตรวจว่าแถวที่ทายไม่เคยเข้าโมเดล fold นั้น"""
    probability = np.full(len(y), np.nan)
    coverage = np.zeros(len(y), dtype=int)
    folds = []
    splitter = StratifiedKFold(n_splits=config.oof_folds, shuffle=True, random_state=seed)
    for train, held in splitter.split(x, y):
        assert set(ids[train]).isdisjoint(ids[held])
        model = LGBMClassifier(n_estimators=config.trees, num_leaves=15, max_depth=5,
                               verbosity=-1, n_jobs=config.threads, random_state=seed,
                               deterministic=True, force_col_wise=True)
        model.fit(x[train], y[train])
        probability[held] = model.predict_proba(x[held])[:, 1]
        coverage[held] += 1
        folds.append({"fit_ids": ids[train].tolist(), "heldout_ids": ids[held].tolist()})
    assert np.all(coverage == 1) and np.isfinite(probability).all()
    p = np.clip(probability, 1e-6, 1-1e-6)
    loss = -(y * np.log(p) + (1-y) * np.log(1-p))
    scaler = StandardScaler()
    representation = scaler.fit_transform(np.column_stack([loss, y, p])).astype(np.float32)
    return representation, {"fit_ids": ids.tolist(), "folds": folds,
                            "oof_coverage_min": int(coverage.min()),
                            "oof_coverage_max": int(coverage.max())}
