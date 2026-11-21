"""ตัวป้องกันข้อมูลชุดทดสอบ R/C (แผนวิเคราะห์ §4.1-§4.2, §4.6)

ระดับข้อมูล:
  D  GA 2566 (ชุดพัฒนา)                      เปิดได้เสมอ
  T  ID, NM 2566 (รัฐเล็ก ใช้ทดสอบเวลาเท่านั้น) เปิดได้เสมอ
  R  CA, OH, FL 2566 (รัฐใหม่)                ต้อง --unlock-R <SHA-256 ของไฟล์แผนที่ตรึง> + manifest v1.0 ที่ตรงกับโค้ดปัจจุบัน
  C  ทุกรัฐ ปี 2567                            ต้อง --unlock-C <SHA-256 ของไฟล์แผน v2.0> + manifest v2.0 ที่ตรงกับโค้ดปัจจุบัน
  อื่น ๆ (รัฐ/ปีที่ไม่อยู่ในแผน เช่น TX)       ปฏิเสธเสมอ

ด่านอยู่ที่ตัวโหลด (hmda.load_hmda) จึงไม่มีการอ่านไฟล์หรือดาวน์โหลดก่อนผ่านด่านนี้
การเปิดสำเร็จบันทึกลง freeze/open_log.csv (เวลา, รัฐ, ปี, tier, hash โค้ด)
"""
import csv
import datetime
import getpass
from pathlib import Path
from . import freeze

DEV = {("GA", 2023)}
TIMING = {("ID", 2023), ("NM", 2023)}
R_STATES = {"CA", "OH", "FL"}
R_YEAR = 2023
C_YEAR = 2024


class AccessDenied(PermissionError):
    pass


def classify(state, year):
    state, year = str(state).upper(), int(year)
    if year == C_YEAR:
        return "C"
    if (state, year) in DEV:
        return "D"
    if (state, year) in TIMING:
        return "T"
    if year == R_YEAR and state in R_STATES:
        return "R"
    return "UNLISTED"


def require_access(state, year=2023, unlock_R=None, unlock_C=None, plan_file=None,
                   root=freeze.ROOT, freeze_dir=freeze.FREEZE_DIR, log=True):
    """ผ่านเงียบ ๆ ถ้าเป็น D/T; มิฉะนั้นต้องมี unlock ที่ถูกต้อง ไม่เช่นนั้น raise AccessDenied. คืนชื่อ tier"""
    tier = classify(state, year)
    if tier in ("D", "T"):
        return tier
    if tier == "UNLISTED":
        raise AccessDenied(f"{state} {year} ไม่อยู่ในแผนวิเคราะห์ ปฏิเสธการโหลด (เพิ่มรัฐ/ปีหลังเห็นผลถือเป็น post-hoc)")
    flag, version, flag_name = ("v1.0", unlock_R, "--unlock-R") if tier == "R" else ("v2.0", unlock_C, "--unlock-C")
    if tier == "R" and flag_value_ok(unlock_R) and flag_value_ok(unlock_C) and unlock_R.strip().lower() == unlock_C.strip().lower():
        # design B re-reads the 2023 source of CA/OH together with 2024: allowed under the v2.1 addendum when BOTH unlocks
        # carry the v2.0 plan SHA (checked against the plan file + manifest v2.1); otherwise the plain v1.0 path below applies
        if plan_file and Path(plan_file).exists() and freeze.sha256_file(plan_file) == unlock_C.strip().lower():
            ok, info = freeze.verify_manifest("v2.1", unlock_C.strip().lower(), root=root, freeze_dir=freeze_dir)
            if ok:
                if log:
                    _log_open(state, year, tier, info, freeze_dir)
                return tier
    if not flag_value_ok(version):
        raise AccessDenied(f"{state} {year} เป็นชุดทดสอบระดับ {tier}: ต้องส่ง {flag_name} <SHA-256 ของไฟล์แผนที่ตรึง> "
                           f"พร้อม --plan-file และ manifest {flag}")
    if not plan_file or not Path(plan_file).exists():
        raise AccessDenied("ต้องระบุ --plan-file ที่มีอยู่จริงเพื่อตรวจ SHA-256 ของแผนที่ตรึง")
    actual = freeze.sha256_file(plan_file)
    if actual != version.strip().lower():
        raise AccessDenied(f"ค่า {flag_name} ไม่ตรงกับ SHA-256 ของไฟล์แผน ({actual[:12]}...)")
    if tier == "C":      # C: manifest v2.1 (addendum) first, then the original v2.0
        errors = []
        for v in ("v2.1", "v2.0"):
            ok, info = freeze.verify_manifest(v, actual, root=root, freeze_dir=freeze_dir)
            if ok:
                break
            errors.append(f"[{v}] {info}")
        else:
            raise AccessDenied("; ".join(errors))
    else:
        ok, info = freeze.verify_manifest(flag, actual, root=root, freeze_dir=freeze_dir)
        if not ok:
            raise AccessDenied(info)
    if log:
        _log_open(state, year, tier, info, freeze_dir)
    return tier


def flag_value_ok(value):
    return isinstance(value, str) and len(value.strip()) == 64 and all(c in "0123456789abcdefABCDEF" for c in value.strip())


def _log_open(state, year, tier, code_hash, freeze_dir):
    path = Path(freeze_dir) / "open_log.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time_utc", "state", "year", "tier", "code_config_sha256", "user"])
        w.writerow([datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                    state, year, tier, code_hash, getpass.getuser()])
