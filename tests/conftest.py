"""ให้ pytest หาโมดูลใน src ได้โดยไม่ต้องติดตั้งโปรเจกต์"""
import sys
import os
from pathlib import Path
if sys.platform == "darwin":
    os.environ["OMP_NUM_THREADS"] = "1"
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
