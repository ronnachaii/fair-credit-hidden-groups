"""วัดทรัพยากรจริงและนับต้นทุนของชั้น Linear"""
import platform
import threading
import time
import importlib.metadata as metadata
import subprocess
from pathlib import Path
import psutil
import torch


class ResourceMonitor:
    """สุ่ม RSS ทุก 10 ms ค่านี้รวมหน่วยความจำของกระบวนการ Python"""
    def __enter__(self):
        self.process = psutil.Process()
        self.peak = self.process.memory_info().rss
        self.peak_start = self.peak
        self.start = time.perf_counter()
        self.stop = threading.Event()
        self.worker = threading.Thread(target=self._sample, daemon=True)
        self.worker.start()
        return self

    def _sample(self):
        while not self.stop.wait(0.01):
            self.peak = max(self.peak, self.process.memory_info().rss)

    def __exit__(self, *args):
        self.stop.set()
        self.worker.join()
        self.peak = max(self.peak, self.process.memory_info().rss)
        self.seconds = time.perf_counter() - self.start
        self.peak_mb = self.peak / 1024**2


def network_cost(model):
    """FLOPs นับเฉพาะ Linear ตามโจทย์ ไม่รวม activation/bias"""
    return {"parameters": sum(p.numel() for p in model.parameters()),
            "flops_per_row": sum(2 * m.in_features * m.out_features
                                 for m in model.modules() if isinstance(m, torch.nn.Linear))}


def inference_seconds(predict, x):
    """อุ่นหนึ่งรอบแล้วเฉลี่ยสามรอบ คืนวินาทีต่อ 1,000 แถว"""
    sample = x[:min(1000, len(x))]
    predict(sample)
    start = time.perf_counter()
    for _ in range(3):
        predict(sample)
    return (time.perf_counter() - start) / 3 * 1000 / len(sample)


def environment(config):
    """บันทึกเวอร์ชันและทรัพยากรที่มีให้ใช้"""
    packages = ["numpy", "pandas", "scipy", "threadpoolctl", "scikit-learn", "lightgbm", "torch",
                "mlflow", "folktables", "matplotlib", "psutil", "pytest", "gradio", "unsupervised-bias-detection", "joblib"]
    cpu_model = platform.processor() or platform.machine()
    if platform.system() == "Darwin":
        try:
            cpu_model = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"], text=True).strip()
        except (OSError, subprocess.CalledProcessError):
            pass
    elif Path("/proc/cpuinfo").exists():
        cpu_model = next((line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines()
                          if line.startswith("model name")), cpu_model)
    return {"python": platform.python_version(), "platform": platform.platform(),
            "libraries": {p: metadata.version(p) for p in packages},
            "installed_packages": dict(sorted((d.metadata["Name"], d.version) for d in metadata.distributions() if d.metadata["Name"])),
            "cpu": cpu_model,
            "logical_cpus": psutil.cpu_count(),
            "ram_gb": psutil.virtual_memory().total / 1024**3,
            "gpu_available": torch.cuda.is_available(), "device_used": "cpu",
            "config": config.to_dict(), "seeds": list(config.seeds)}
