"""ตรวจสูตรที่มีผลต่อข้อสรุป ไม่ใช่เพียงตรวจว่าโค้ดเรียกได้"""
import numpy as np
import torch
from config import Config
from fairgroups.dro import group_dro_loss
from fairgroups.metrics import group_metrics
from fairgroups.models import train_mlp, predict_mlp
from fairgroups.efficiency import network_cost


def test_dro_averages_groups_not_examples():
    losses = torch.tensor([1., 1., 4.], requires_grad=True)
    groups = torch.tensor([0, 0, 1])
    value = group_dro_loss(losses, groups, torch.zeros(2), eta=0)
    assert float(value.detach()) == 2.5
    value.backward()
    np.testing.assert_allclose(losses.grad.numpy(), [0.25, 0.25, 0.5])


def test_known_fairness_values():
    y = np.array([1, 1, 0, 0, 1, 1, 0, 0])
    pred = np.array([1, 1, 0, 0, 1, 0, 1, 0])
    scores = group_metrics(y, pred, np.array(["a"]*4 + ["b"]*4))
    assert scores["eo_gap"] == 0.5
    assert scores["dp_difference"] == 0
    assert scores["worst_group_accuracy"] == 0.5


def test_average_selection_is_invariant_to_population_groups():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(40, 4)).astype(np.float32)
    y = (x[:, 0] > 0).astype(int)
    cfg = Config(epochs=3, hidden=8, batch_size=16)
    a, _ = train_mlp(x, y, x, y, np.zeros(40), cfg, seed=17)
    b, _ = train_mlp(x, y, x, y, np.arange(40) % 4, cfg, seed=17)
    assert a["average"][1] == b["average"][1]
    np.testing.assert_array_equal(predict_mlp(a["average"][0], x), predict_mlp(b["average"][0], x))


def test_linear_flops_formula():
    model = torch.nn.Sequential(torch.nn.Linear(3, 4), torch.nn.ReLU(), torch.nn.Linear(4, 1))
    assert network_cost(model) == {"parameters": 21, "flops_per_row": 32}
