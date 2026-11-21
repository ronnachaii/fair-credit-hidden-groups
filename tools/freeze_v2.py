"""พิมพ์ SHA-256 ของไฟล์โค้ด + config + แผนวิเคราะห์ v2.0 เพื่อให้ผู้ใช้ตรึง v2.0 (แผน v2.0 V6 ข้อ 3-4)

manifest v2.0 รวมไฟล์ของ v1.0 + src/fairgroups/design_b/*.py + tools/freeze_v2.py และเป็นเงื่อนไขปลดล็อก C (--unlock-C)
สคริปต์นี้ ไม่ git tag และ ไม่ commit และโดยค่าเริ่มต้น ไม่เขียนไฟล์ใด ๆ
  python tools/freeze_v2.py                 # แสดง hash เท่านั้น (dry-run)
  python tools/freeze_v2.py --verify        # เทียบกับ freeze/v2_0_manifest.json
  python tools/freeze_v2.py --write         # สร้าง freeze/v2_0_manifest.json (ผู้ใช้สั่งเอง ไม่เขียนทับของเดิม)
  python tools/freeze_v2.py --addendum              # แสดงไฟล์ที่ต่างจาก v2.0 (dry-run)
  python tools/freeze_v2.py --write-addendum        # สร้าง freeze/v2_1_manifest.json (addendum หลังเปิด C; ไม่แก้ v2_0)
  python tools/freeze_v2.py --verify --tier v2.1    # ตรวจกับ addendum
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
# เหตุผลของไฟล์ที่เปลี่ยนหลังเปิด C (addendum v2.1; รายละเอียดใน deviations.md) ต้องมีครบทุกไฟล์ที่ต่างจาก v2.0
ADDENDUM_REASONS = {
    "src/fairgroups/hmda_groups.py": "group_scores: silhouette_score(sample_size=1000) raised ValueError when the sample held one label "
        "(A OH 2024, seed 17); now returns NaN for silhouette only",
    "src/fairgroups/freeze.py": "tier v2.1 uses the v2.0 file list; verify_manifest checks an addendum (base manifest untouched, "
        "same plan, every changed file listed with reason and hashes)",
    "src/fairgroups/access_guard.py": "tier C accepts manifest v2.1 (then v2.0); tier R accepts the v2.0 plan under v2.1 only when "
        "--unlock-R and --unlock-C both equal the plan SHA (design B re-reads 2023 CA/OH); same checks and open_log otherwise",
    "tools/freeze_v2.py": "adds --addendum / --write-addendum / --tier",
}
DEFAULT_PLAN = ROOT.parent / "09_แผนวิเคราะห์" / "แผนวิเคราะห์_v2.0_ร่าง.md"


def build_addendum(plan):
    """manifest v2.1 = hash ปัจจุบัน + อ้างอิง v2.0 (hash ของไฟล์ manifest เดิม) + เหตุผลของไฟล์ที่เปลี่ยน"""
    base_path = freeze.manifest_path("v2.0")
    base = json.loads(base_path.read_text(encoding="utf-8"))
    now = freeze.build_manifest(plan, "v2.1", ROOT)
    if now["plan_sha256"] != base["plan_sha256"]:
        raise SystemExit("แผนไม่ตรงกับ manifest v2.0")
    changes = {}
    for k in sorted(set(base["files"]) | set(now["files"])):
        if base["files"].get(k) != now["files"].get(k):
            if k not in ADDENDUM_REASONS:
                raise SystemExit(f"ไฟล์ {k} เปลี่ยนจาก v2.0 แต่ไม่มีเหตุผลใน ADDENDUM_REASONS")
            changes[k] = {"sha256_before": base["files"].get(k), "sha256_after": now["files"].get(k),
                          "reason": ADDENDUM_REASONS[k]}
    now.update(supersedes="v2.0", base_manifest_file_sha256=freeze.sha256_file(base_path), changes=changes,
               note="addendum after tier C was opened (see deviations.md); v2_0_manifest.json is unchanged")
    return now


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", default=str(DEFAULT_PLAN), help="ไฟล์แผนวิเคราะห์ v2.0 ที่ตรึง")
    ap.add_argument("--write", action="store_true", help="เขียน freeze/v2_0_manifest.json (ไม่ tag/commit)")
    ap.add_argument("--verify", action="store_true", help="ตรวจว่าโค้ดปัจจุบันตรงกับ manifest v2.0 ที่มีอยู่")
    ap.add_argument("--tier", default=TIER, choices=["v2.0", "v2.1"], help="tier ที่ใช้กับ --verify")
    ap.add_argument("--addendum", action="store_true", help="แสดงไฟล์ที่ต่างจาก manifest v2.0 (dry-run)")
    ap.add_argument("--write-addendum", action="store_true", help="เขียน freeze/v2_1_manifest.json (ไม่แก้ v2_0)")
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
    if args.addendum or args.write_addendum:
        add = build_addendum(plan)
        for k, c in add["changes"].items():
            print(f"CHANGED {k}", f"  {c['sha256_before']} -> {c['sha256_after']}", f"  {c['reason']}", sep="\n")
        print(f"v2.1 code+config SHA : {add['code_config_combined_sha256']}")
        if args.write_addendum:
            path = freeze.manifest_path("v2.1")
            if path.exists():
                raise SystemExit(f"มี addendum อยู่แล้ว ไม่เขียนทับ: {path}")
            path.write_text(json.dumps(add, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"เขียน {path} แล้ว (v2_0_manifest.json ไม่ถูกแตะ)")
        raise SystemExit(0)
    if args.verify:
        ok, info = freeze.verify_manifest(args.tier, manifest["plan_sha256"], ROOT)
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
