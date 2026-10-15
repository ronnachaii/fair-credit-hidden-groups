"""โมเดล MLP และการเลือก checkpoint ด้วย validation เท่านั้น"""
import copy
import random
import numpy as np
import torch
from torch import nn
from .dro import group_dro_loss


def set_seed(seed, threads=2):
    """ใช้ CPU และตั้ง seed เพื่อให้ทำซ้ำได้"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(threads)
    torch.use_deterministic_algorithms(True)


class MLP(nn.Module):
    """ทุกวิธีใช้ input และโครงข่ายตัดสินใจเดียวกันเพื่อเทียบตรง"""
    def __init__(self, input_dim, hidden):
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(input_dim, hidden), nn.ReLU(),
                                    nn.Linear(hidden, hidden), nn.ReLU(), nn.Linear(hidden, 1))

    def forward(self, x):
        return self.layers(x).squeeze(-1)


def predict_mlp(model, x):
    """ทำนายเป็นชุดเล็กเพื่อลด RAM"""
    model.eval()
    with torch.no_grad():
        return np.concatenate([model(torch.as_tensor(x[i:i+2048])).sigmoid().numpy()
                               for i in range(0, len(x), 2048)])


def validation_scores(y, probability, groups):
    """average ไม่แตะกลุ่มจริง ส่วน worst-group ใช้เพื่อการวิเคราะห์แยก"""
    correct = (probability >= 0.5) == y
    return {"average": float(correct.mean()),
            "worst_group": min(float(correct[groups == g].mean()) for g in np.unique(groups) if str(g) != "Unknown")}


def train_mlp(x, y, xv, yv, val_groups, config, seed, groups=None,
              sample_weights=None, epochs=None):
    """ฝึกจำนวนรอบคงที่และเก็บ checkpoint ดีที่สุดของทั้งสองกติกา"""
    set_seed(seed, config.threads)
    model = MLP(x.shape[1], config.hidden)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate,
                                 weight_decay=config.weight_decay)
    xt, yt = torch.as_tensor(x), torch.as_tensor(y, dtype=torch.float32)
    gt = None if groups is None else torch.as_tensor(groups, dtype=torch.long)
    wt = None if sample_weights is None else torch.as_tensor(sample_weights, dtype=torch.float32)
    log_weights = None if groups is None else torch.zeros(int(np.max(groups)) + 1)
    best_scores = {"average": -1, "worst_group": -1}
    best_states, best_epochs = {}, {}
    for epoch in range(epochs or config.epochs):
        model.train()
        order = torch.randperm(len(y))
        for ids in order.split(config.batch_size):
            optimizer.zero_grad()
            losses = nn.functional.binary_cross_entropy_with_logits(model(xt[ids]), yt[ids], reduction="none")
            if gt is not None:
                loss = group_dro_loss(losses, gt[ids], log_weights, config.dro_eta)
            elif wt is not None:
                # JTT ใช้น้ำหนักคงที่จากโมเดลรอบแรก ไม่เลือกด้วย test
                loss = (losses * wt[ids]).sum() / wt[ids].sum()
            else:
                loss = losses.mean()
            loss.backward()
            optimizer.step()
        scores = validation_scores(yv, predict_mlp(model, xv), val_groups)
        for selection, score in scores.items():
            if score > best_scores[selection]:
                best_scores[selection] = score
                best_states[selection] = copy.deepcopy(model.state_dict())
                best_epochs[selection] = epoch + 1
    result = {}
    for selection, state in best_states.items():
        selected = MLP(x.shape[1], config.hidden)
        selected.load_state_dict(state)
        result[selection] = (selected, best_epochs[selection], best_scores[selection])
    return result, model
