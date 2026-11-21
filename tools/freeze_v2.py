"""พิมพ์ SHA-256 ของไฟล์โค้ด + config + แผนวิเคราะห์ v2.0 เพื่อให้ผู้ใช้ตรึง v2.0 (แผน v2.0 V6 ข้อ 3-4)

manifest v2.0 รวมไฟล์ของ v1.0 + src/fairgroups/design_b/*.py + tools/freeze_v2.py และเป็นเงื่อนไขปลดล็อก C (--unlock-C)
สคริปต์นี้ ไม่ git tag และ ไม่ commit และโดยค่าเริ่มต้น ไม่เขียนไฟล์ใด ๆ
  python tools/freeze_v2.py                 # แสดง hash เท่านั้น (dry-run)
  python tools/freeze_v2.py --verify        # เทียบกับ freeze/v2_0_manifest.json
  python tools/freeze_v2.py --write         # สร้าง freeze/v2_0_manifest.json (ผู้ใช้สั่งเอง ไม่เขียนทับของเดิม)
v1.0 ตรวจด้วย `git diff prereg-v1.0` (ดู freeze/v1_to_v2_code_changes.md) ไม่ใช่ freeze_v1.py --verify
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
from fairgroups import freeze

TIER = "v2.0"
DEFAULT_PLAN = ROOT.parent / "09_แผนวิเคราะห์" / "แผนวิเคราะห์_v2.0_ร่าง.md"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", default=str(DEFAULT_PLAN), help="ไฟล์แผนวิเคราะห์ v2.0 ที่ตรึง")
    ap.add_argument("--write", action="store_true", help="เขียน freeze/v2_0_manifest.json (ไม่ tag/commit)")
    ap.add_argument("--verify", action="store_true", help="ตรวจว่าโค้ดปัจจุบันตรงกับ manifest v2.0 ที่มีอยู่")
    args = ap.parse_args()
    plan = Path(args.plan)
    if not plan.exists():
        raise SystemExit(f"ไม่พบไฟล์แผน: {plan}")
    manifest = freeze.build_manifest(plan, TIER, ROOT)
    print(f"tier            : {TIER}")
    print(f"plan file       : {plan.name}")
    print(f"plan SHA-256    : {manifest['plan_sha256']}")
    print(f"code+config SHA : {manifest['code_config_combined_sha256']}   (รวมจาก {len(manifest['files'])} ไฟล์)")
    for name, digest in manifest["files"].items():
        print(f"  {digest}  {name}")
    print("libraries       :", json.dumps(manifest["libraries"]), "| python", manifest["python"])
    if args.verify:
        ok, info = freeze.verify_manifest(TIER, manifest["plan_sha256"], ROOT)
        print("VERIFY:", "ตรงกับ manifest" if ok else f"ไม่ตรง -> {info}")
        raise SystemExit(0 if ok else 1)
    if args.write:
        path = freeze.manifest_path(TIER)
        if path.exists():
            raise SystemExit(f"มี manifest อยู่แล้ว ไม่เขียนทับ: {path} (ลบหรือย้ายเองถ้าต้องการตรึงใหม่)")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"เขียน {path} แล้ว (ยังไม่ได้ git tag/commit: ผู้ใช้ทำเอง)")
    else:
        print("\n(ไม่ได้เขียนไฟล์: ใส่ --write เมื่อผู้ใช้ตัดสินใจตรึง)")


if __name__ == "__main__":
    main()
