"""โมเดล MLP และการเลือก checkpoint ด้วย validation เท่านั้น"""
import copy
import os
import random
import numpy as np
import torch
from torch import nn
from .dro import group_dro_loss


def resolve_device(device="cpu"):
    """'cpu' หรือ 'cuda' เท่านั้น; ขอ cuda แต่ไม่มี GPU ให้ error ชัดเจน ไม่ถอยกลับเป็น cpu เงียบ ๆ"""
    if device not in ("cpu", "cuda"):
        raise ValueError(f"device ต้องเป็น 'cpu' หรือ 'cuda' ไม่ใช่ {device!r}")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("ขอใช้ cuda แต่ torch.cuda.is_available() เป็น False")
    return torch.device(device)


def set_seed(seed, threads=2, device="cpu"):
    """ตั้ง seed และ deterministic flags; ค่าเริ่มต้น cpu ให้ผลเหมือนเดิม"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(threads)
    if resolve_device(device).type == "cuda":
        # cuBLAS ต้องมี workspace config นี้ก่อนจึงใช้ deterministic algorithms ได้ (ตั้งเฉพาะในโปรเซสนี้)
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
    torch.use_deterministic_algorithms(True)


def model_device(model):
    return next(model.parameters()).device


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
        device = model_device(model)
        return np.concatenate([model(torch.as_tensor(x[i:i+2048]).to(device)).sigmoid().cpu().numpy()
                               for i in range(0, len(x), 2048)])


def worst_accuracy(correct, groups, min_size=1):
    """ไม่นับ Unknown หรือกลุ่มที่เล็กกว่าเกณฑ์; กลุ่มอนุมานนับทุกกลุ่มที่มีแถว"""
    values = [float(correct[groups == g].mean()) for g in np.unique(groups)
              if str(g) != 'Unknown' and (groups == g).sum() >= min_size]
    if not values:
        raise ValueError('ไม่มี validation group ที่ผ่านเกณฑ์ขนาด')
    return min(values)


def cross_labels(clusters, y):
    """กลุ่ม validation = cluster ที่ตัวจัดกลุ่ม train ทำนาย × ป้าย y"""
    return np.array([f'{c}|y={label}' for c, label in zip(clusters, y)])


def selection_rank(selection, scores, accuracy_floor):
    """ถ้าไม่ผ่าน guard ทุกตัว เลือก average ใกล้ ERM ที่สุดก่อน; เสมอคงตัวแรก"""
    if selection != 'inferred_worst_group':
        return (scores[selection],)
    average = scores['average']; worst = scores[selection]
    passed = average + 1e-12 >= accuracy_floor
    return (passed, worst, average) if passed else (passed, average, worst)


def validation_scores(y, probability, groups):
    """average ไม่แตะกลุ่มจริง ส่วน worst-group เป็นผลเสริมที่ใช้ประชากร"""
    correct = (probability >= 0.5) == y
    return {'average': float(correct.mean()), 'worst_group': worst_accuracy(correct, groups)}


def parameter_distance(model, initial_model):
    """ระยะพารามิเตอร์ L2 จาก ERM เริ่มต้น ไม่รวม buffer"""
    if initial_model is None:
        return 0.0
    return float(sum((a.detach() - b.detach()).double().square().sum()
                     for a, b in zip(model.parameters(), initial_model.parameters())).sqrt())


def train_mlp(x, y, xv, yv, val_groups, config, seed, groups=None,
              sample_weights=None, epochs=None, initial_model=None, learning_rate=None,
              inferred_val_groups=None, accuracy_floor=0.0, inferred_min_size=1):
    """เก็บ checkpoint แต่ละกติกาแยกกัน; guard ใช้กับกติกาหลักของวิธีที่มีกลุ่ม"""
    device = resolve_device(getattr(config, "device", "cpu"))
    set_seed(seed, config.threads, device.type)
    # สร้างและสุ่มค่าเริ่มต้นบน CPU ก่อน แล้วค่อยย้าย เพื่อให้ค่าเริ่มต้นเท่ากันทุก device
    model = MLP(x.shape[1], config.hidden).to(device)
    if initial_model is not None:
        model.load_state_dict(copy.deepcopy(initial_model.state_dict()))
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate or config.learning_rate,
                                 weight_decay=config.weight_decay)
    xt, yt = torch.as_tensor(x).to(device), torch.as_tensor(y, dtype=torch.float32).to(device)
    gt = None if groups is None else torch.as_tensor(groups, dtype=torch.long).to(device)
    wt = None if sample_weights is None else torch.as_tensor(sample_weights, dtype=torch.float32).to(device)
    log_weights = None if groups is None else torch.zeros(int(np.max(groups)) + 1, device=device)
    group_counts = None if groups is None else torch.bincount(gt, minlength=len(log_weights)).float()
    selections = ["average", "worst_group"]
    if inferred_val_groups is not None:
        selections.append("inferred_worst_group")
    best_ranks = {}
    best_states, best_epochs, best_metadata = {}, {}, {}
    for epoch in range(epochs or config.epochs):
        model.train()
        # สลับลำดับบน CPU เสมอ เพื่อให้ลำดับ batch เท่ากันทุก device
        order = torch.randperm(len(y))
        for ids in order.split(config.batch_size):
            ids = ids.to(device)
            optimizer.zero_grad()
            losses = nn.functional.binary_cross_entropy_with_logits(model(xt[ids]), yt[ids], reduction="none")
            if gt is not None:
                # น้ำหนักเฉลี่ยหนึ่งภายใน cluster ก่อนแยก y; ไม่หาร sum(w) ซ้ำจน cy_bal หายไป
                if wt is not None:
                    losses = losses * wt[ids]
                loss = group_dro_loss(losses, gt[ids], log_weights, config.dro_eta,
                                      group_counts, config.dro_adjustment)
            elif wt is not None:
                # JTT ใช้น้ำหนักคงที่จากโมเดลรอบแรก ไม่เลือกด้วย test
                loss = (losses * wt[ids]).sum() / wt[ids].sum()
            else:
                loss = losses.mean()
            loss.backward()
            optimizer.step()
        probability = predict_mlp(model, xv)
        scores = validation_scores(yv, probability, val_groups)
        if inferred_val_groups is not None:
            scores['inferred_worst_group'] = worst_accuracy(
                (probability >= .5) == yv, inferred_val_groups, inferred_min_size)
        weights = None if log_weights is None else torch.softmax(log_weights, dim=0)
        metadata = {**scores, 'accuracy_floor': accuracy_floor,
                    'accuracy_guard_passed': scores['average'] + 1e-12 >= accuracy_floor,
                    'parameter_l2_from_erm': parameter_distance(model, initial_model),
                    'group_weight_min': float(weights.min()) if weights is not None else np.nan,
                    'group_weight_max': float(weights.max()) if weights is not None else np.nan}
        for selection in selections:
            rank = selection_rank(selection, scores, accuracy_floor)
            if selection not in best_ranks or rank > best_ranks[selection]:
                best_ranks[selection] = rank
                best_states[selection] = copy.deepcopy(model.state_dict())
                best_epochs[selection] = epoch + 1
                best_metadata[selection] = metadata.copy()
    result = {}
    for selection, state in best_states.items():
        selected = MLP(x.shape[1], config.hidden).to(device)
        selected.load_state_dict(state)
        selected.selection_metadata_ = best_metadata[selection]
        result[selection] = (selected, best_epochs[selection], best_metadata[selection][selection])
    model.training_diagnostics_ = {
        'final_group_weight_min': float(weights.min()) if weights is not None else np.nan,
        'final_group_weight_max': float(weights.max()) if weights is not None else np.nan,
        'final_parameter_l2_from_erm': parameter_distance(model, initial_model)}
    return result, model
