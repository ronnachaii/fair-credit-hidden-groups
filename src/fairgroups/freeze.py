"""SHA-256 ของไฟล์ที่ต้องตรึง (v1.0 / v2.0) และการตรวจว่าโค้ดยังตรงกับที่ตรึงไว้ (แผนวิเคราะห์ §4.2)

ไม่ tag และไม่ commit ให้: สร้างเฉพาะ manifest ที่ผู้ใช้เป็นคนสั่งเขียนเอง (tools/freeze_v1.py --write)
"""
import hashlib
import json
import os
import platform
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FREEZE_DIR = ROOT / "freeze"
# ไลบรารีที่มีผลต่อตัวเลข: ถ้าเวอร์ชันเปลี่ยนหลังตรึง ถือว่าไม่ตรงกับที่ตรึง
TRACKED_LIBRARIES = ["numpy", "pandas", "scipy", "scikit-learn", "lightgbm", "torch", "threadpoolctl",
                     "unsupervised-bias-detection"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def code_files(root=ROOT, tier="v1.0"):
    """ไฟล์โค้ด+config ที่ตรึง (ไม่รวม tests, README, results, data)
    v1.0 = รายการเดิม; v2.0 = รายการเดิม + src/fairgroups/design_b/*.py (tools/*.py รวม freeze_v2.py อยู่แล้ว)"""
    root = Path(root)
    files = sorted(root.glob("src/fairgroups/*.py")) + sorted(root.glob("tools/*.py"))
    if tier == "v2.0":
        files += sorted(root.glob("src/fairgroups/design_b/*.py"))
    files += [p for p in [root / "config.py", root / "run_pilot.py", root / "requirements.txt"] if p.exists()]
    # สคริปต์เลือกรัฐและผลของมัน (แผน §4.2 / §9 ข้อ 5) อยู่ในโฟลเดอร์ 09_แผนวิเคราะห์ ข้างโฟลเดอร์โค้ด
    plan_dir = root.parent / "09_แผนวิเคราะห์"
    files += [p for p in [plan_dir / "เลือกรัฐ_01_profile.py", plan_dir / "เลือกรัฐ_02_select.py"] if p.exists()]
    if (plan_dir / "เลือกรัฐ_ผล").is_dir():
        files += sorted(p for p in (plan_dir / "เลือกรัฐ_ผล").rglob("*") if p.is_file())
    return files


def manifest_key(path, root=ROOT):
    """ชื่อไฟล์ใน manifest: path สัมพัทธ์กับ root (ไฟล์นอก root ขึ้นต้นด้วย ../)"""
    return os.path.relpath(path, root).replace("\\", "/")


def library_versions():
    out = {}
    for name in TRACKED_LIBRARIES:
        try:
            out[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            out[name] = None
    return out


def build_manifest(plan_file, tier="v1.0", root=ROOT):
    """คืน dict ที่ใช้เขียนเป็น freeze/<tier>_manifest.json; ไม่เขียนไฟล์เอง"""
    root = Path(root)
    plan_file = Path(plan_file)
    files = {manifest_key(p, root): sha256_file(p) for p in code_files(root, tier)}
    combined = hashlib.sha256("\n".join(f"{k}:{v}" for k, v in sorted(files.items())).encode()).hexdigest()
    return {"tier": tier, "plan_file": plan_file.name, "plan_sha256": sha256_file(plan_file),
            "files": files, "code_config_combined_sha256": combined,
            "libraries": library_versions(), "python": platform.python_version()}


def manifest_path(tier, freeze_dir=FREEZE_DIR):
    return Path(freeze_dir) / f"{tier.replace('.', '_')}_manifest.json"


def verify_manifest(tier, plan_sha256, root=ROOT, freeze_dir=FREEZE_DIR):
    """คืน (ok, ข้อความ). ต้องมี manifest, plan_sha256 ตรง, ไฟล์โค้ด/config และเวอร์ชันไลบรารีตรงกับที่ตรึง"""
    path = manifest_path(tier, freeze_dir)
    if not path.exists():
        return False, f"ไม่พบ manifest การตรึง {tier}: {path} (ต้องให้ผู้ใช้ตรึงด้วย tools/freeze_v1.py (v1.0) หรือ tools/freeze_v2.py (v2.0) --write ก่อน)"
    saved = json.loads(path.read_text(encoding="utf-8"))
    if saved.get("plan_sha256") != plan_sha256:
        return False, "SHA-256 ของแผนไม่ตรงกับ manifest ที่ตรึงไว้"
    now = build_manifest_files_only(root, tier)
    changed = sorted(k for k in set(now) | set(saved["files"]) if now.get(k) != saved["files"].get(k))
    if changed:
        return False, "โค้ด/config เปลี่ยนหลังตรึง: " + ", ".join(changed[:8])
    drift = {k: (v, library_versions().get(k)) for k, v in saved.get("libraries", {}).items()
             if library_versions().get(k) != v}
    if drift:
        return False, f"เวอร์ชันไลบรารีไม่ตรงกับที่ตรึง: {drift}"
    return True, saved["code_config_combined_sha256"]


def build_manifest_files_only(root=ROOT, tier="v1.0"):
    root = Path(root)
    return {manifest_key(p, root): sha256_file(p) for p in code_files(root, tier)}
