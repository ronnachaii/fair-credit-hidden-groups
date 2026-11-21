"""ตัวเลือก device: ค่าเริ่มต้นต้องเป็น cpu, ค่าผิดต้อง error ชัดเจน, และ cuda (ถ้ามี) ต้องให้ผลใกล้ cpu"""
import numpy as np
import pytest
import torch
from config import Config, make_config
from fairgroups.efficiency import environment
from fairgroups.models import resolve_device, train_mlp, predict_mlp, MLP


def test_default_device_is_cpu_and_recorded():
    assert Config().device == "cpu" and make_config(quick=False).device == "cpu"
    env = environment(Config())
    assert env["device_used"] == "cpu"
    assert environment(Config(device="cuda"))["device_used"] == "cuda"


def test_invalid_device_is_rejected():
    with pytest.raises(ValueError):
        resolve_device("tpu")
    if not torch.cuda.is_available():
        with pytest.raises(RuntimeError):
            resolve_device("cuda")


def test_cpu_models_are_on_cpu():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(40, 4)).astype(np.float32)
    y = (x[:, 0] > 0).astype(int)
    cp, final = train_mlp(x, y, x, y, np.zeros(40), Config(epochs=2, hidden=8, batch_size=16), seed=17)
    assert next(cp["average"][0].parameters()).device.type == "cpu"
    assert next(final.parameters()).device.type == "cpu"


@pytest.mark.skipif(not torch.cuda.is_available(), reason="ไม่มี CUDA")
def test_cuda_matches_cpu_closely_and_is_repeatable():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(200, 6)).astype(np.float32)
    y = (x[:, 0] + .3 * x[:, 1] > 0).astype(int)
    groups = np.arange(200) % 4
    def run(device):
        cfg = Config(epochs=3, hidden=8, batch_size=32, device=device)
        cp, _ = train_mlp(x, y, x, y, groups, cfg, seed=17, groups=groups)
        model = cp["average"][0]
        assert next(model.parameters()).device.type == device
        return predict_mlp(model, x)
    cpu, gpu, gpu2 = run("cpu"), run("cuda"), run("cuda")
    np.testing.assert_array_equal(gpu, gpu2)
    np.testing.assert_allclose(cpu, gpu, atol=1e-4)
