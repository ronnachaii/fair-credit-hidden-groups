"""ตัวจับเวลาแยกส่วนประกอบ (T0 ตามแผนวิเคราะห์ §6.4): wall, CPU, RAM สูงสุด และ GPU memory"""
import time
from contextlib import contextmanager
import psutil
import torch
from .efficiency import ResourceMonitor


class ComponentTimer:
    """ใช้เป็น `with timer.section('ชื่อส่วน', k=8): ...` แล้วอ่านผลจาก timer.rows

    - wall_seconds: เวลาจริง (sync CUDA ก่อนหยุดนาฬิกา เพื่อไม่ให้นับงานค้างใน GPU ผิดส่วน)
    - cpu_seconds: เวลา CPU ของโปรเซส (รวมทุกเธรด) จึงอาจมากกว่า wall ได้เมื่อใช้หลายเธรด
    - peak_rss_mb: RAM สูงสุดของโปรเซส (สุ่มทุก 10 ms)
    - peak_gpu_mb: GPU memory สูงสุดที่ torch จัดสรรในส่วนนั้น (ว่างเมื่อไม่ใช้ CUDA)
    ห้ามซ้อน section ภายใน section อื่นที่มีชื่อต่างกัน ถ้าต้องการรวมให้ใช้ชื่อรวมแยก (เช่น 'TOTAL') ต่างหาก
    """
    def __init__(self, device="cpu", **meta):
        meta = {"device": device, **meta}
        self.device, self.meta, self.rows = device, meta, []
        self.cuda = device == "cuda"

    def _sync(self):
        if self.cuda:
            torch.cuda.synchronize()

    @contextmanager
    def section(self, name, **extra):
        process = psutil.Process()
        self._sync()
        if self.cuda:
            torch.cuda.reset_peak_memory_stats()
        cpu0 = time.process_time()
        with ResourceMonitor() as monitor:
            try:
                yield monitor
            finally:
                self._sync()
        self.rows.append({**self.meta, "component": name, **extra,
                          "wall_seconds": monitor.seconds, "cpu_seconds": time.process_time() - cpu0,
                          "peak_rss_mb": monitor.peak_mb,
                          "peak_gpu_mb": torch.cuda.max_memory_allocated() / 1024**2 if self.cuda else None,
                          "process_threads": process.num_threads()})
