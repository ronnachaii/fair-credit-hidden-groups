"""พิมพ์ SHA-256 ของไฟล์โค้ด + config + แผนวิเคราะห์ เพื่อให้ผู้ใช้ตรึง v1.0 (แผนวิเคราะห์ §4.2)

สคริปต์นี้ ไม่ git tag และ ไม่ commit และโดยค่าเริ่มต้น ไม่เขียนไฟล์ใด ๆ
  python tools/freeze_v1.py --plan "<ไฟล์แผนที่ตรึง>"                 # แสดง hash เท่านั้น
  python tools/freeze_v1.py --plan "<ไฟล์แผน>" --write                # สร้าง freeze/v1_0_manifest.json (ผู้ใช้สั่งเอง)
  python tools/freeze_v1.py --plan "<ไฟล์แผน>" --tier v2.0 --write    # ตรึง v2.0 ก่อนเปิดปี 2567
  python tools/freeze_v1.py --plan "<ไฟล์แผน>" --verify               # เทียบกับ manifest ที่มีอยู่

หลังเขียน manifest: การเปิดรัฐใหม่ (R) ใช้ --unlock-R <plan_sha256> --plan-file <ไฟล์แผน> และจะถูกปฏิเสธถ้าโค้ด/config/ไลบรารี
เปลี่ยนไปจากที่ตรึง (ดู src/fairgroups/access_guard.py)
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
from fairgroups import freeze

DEFAULT_PLAN = ROOT.parent / "09_แผนวิเคราะห์" / "แผนวิเคราะห์_v1.0_พร้อมตรึง.md"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", default=str(DEFAULT_PLAN), help="ไฟล์แผนวิเคราะห์ที่ตรึง")
    ap.add_argument("--tier", choices=["v1.0", "v2.0"], default="v1.0")
    ap.add_argument("--write", action="store_true", help="เขียน freeze/<tier>_manifest.json (ไม่ tag/commit)")
    ap.add_argument("--verify", action="store_true", help="ตรวจว่าโค้ดปัจจุบันตรงกับ manifest ที่มีอยู่")
    args = ap.parse_args()
    plan = Path(args.plan)
    if not plan.exists():
        raise SystemExit(f"ไม่พบไฟล์แผน: {plan}")
    manifest = freeze.build_manifest(plan, args.tier, ROOT)
    print(f"tier            : {args.tier}")
    print(f"plan file       : {plan.name}")
    print(f"plan SHA-256    : {manifest['plan_sha256']}")
    print(f"code+config SHA : {manifest['code_config_combined_sha256']}   (รวมจาก {len(manifest['files'])} ไฟล์)")
    for name, digest in manifest["files"].items():
        print(f"  {digest}  {name}")
    print("libraries       :", json.dumps(manifest["libraries"]), "| python", manifest["python"])
    if args.verify:
        ok, info = freeze.verify_manifest(args.tier, manifest["plan_sha256"], ROOT)
        print("VERIFY:", "ตรงกับ manifest" if ok else f"ไม่ตรง -> {info}")
        raise SystemExit(0 if ok else 1)
    if args.write:
        path = freeze.manifest_path(args.tier)
        if path.exists():
            raise SystemExit(f"มี manifest อยู่แล้ว ไม่เขียนทับ: {path} (ลบหรือย้ายเองถ้าต้องการตรึงใหม่)")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"เขียน {path} แล้ว (ยังไม่ได้ git tag/commit: ผู้ใช้ทำเอง)")
    else:
        print("\n(ไม่ได้เขียนไฟล์: ใส่ --write เมื่อผู้ใช้ตัดสินใจตรึง)")


if __name__ == "__main__":
    main()
