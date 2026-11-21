# รายการไฟล์โค้ดที่เปลี่ยนจาก v1.0 (tag `prereg-v1.0`) ถึง v2.0

เอกสารนี้เป็นหลักฐานประกอบการตรึง v2.0 ไม่ใช่ manifest ห้ามแก้ `freeze/v1_0_manifest.json` (ยังคงเป็นบันทึกของสถานะ v1.0)
ที่มา: `git diff --stat prereg-v1.0` (ไฟล์ที่ track อยู่) และการเทียบรายการไฟล์ที่ตรึงของ v2.0 กับ v1.0 (ไฟล์ใหม่ที่ยังไม่ track)
ยังไม่ได้ commit/tag: รณชัยทำเอง

## ไฟล์ที่ v1.0 hash ไว้และถูกแก้ (2 ไฟล์ 30 บรรทัดเพิ่ม 7 บรรทัดลบ)

```
 src/fairgroups/freeze.py | 17 ++++++++++-------
 src/fairgroups/hmda.py   | 20 ++++++++++++++++++++
```

| ไฟล์ | สิ่งที่เปลี่ยน | เหตุผล | กระทบตัวเลขผลหรือไม่ |
|---|---|---|---|
| `src/fairgroups/freeze.py` | `code_files(root, tier="v1.0")`, `build_manifest_files_only(root, tier)` และ `verify_manifest` รู้จัก tier: v1.0 ใช้รายการเดิมทุกประการ, v2.0 เพิ่ม `src/fairgroups/design_b/*.py` ข้อความ error ชี้ทั้ง freeze_v1/freeze_v2 | แผน v2.0 V6 ข้อ 3: manifest v2.0 ต้องครอบคลุม design_b ซึ่งอยู่ในโฟลเดอร์ย่อยจึงไม่เคยถูก glob แบบไม่ลงลึกของ v1.0 `access_guard.py` ไม่ต้องแก้ เพราะส่ง tier ให้ `verify_manifest` อยู่แล้ว | ไม่ (เป็นเครื่องมือตรึง ไม่แตะการคำนวณ) |
| `src/fairgroups/hmda.py` | เพิ่ม `REQUIRED_COLUMNS`, `SchemaError`, `check_header()` และเรียก `check_header(path)` ก่อน `pd.read_csv` ใน `load_hmda` (อ่านเฉพาะ header ไม่อ่านแถว) | ข้อเสนอใน `09_แผนวิเคราะห์/ตรวจ_schema_HMDA2024.md` ข้อ 2: ถ้าชื่อคอลัมน์ของ CSV ปี 2567 ต่างจาก 2566 ให้หยุดพร้อมรายชื่อคอลัมน์ที่หาย แทนที่จะเจอ AttributeError กลางทาง ไม่มีการแมปชื่ออัตโนมัติ | ไม่: ไฟล์ 2566 ทั้ง 5 รัฐ (GA, ID, NM, CA, OH) ผ่านการตรวจ header ครบ จึงอ่านและกรองข้อมูลเหมือนเดิม (ทดสอบใน `tests/test_freeze_v2_schema.py`) |

## ไฟล์ใหม่ (ยังไม่ track ใน Git ณ ตอนเขียน จึงไม่ปรากฏใน `git diff prereg-v1.0`)

| ไฟล์ | เหตุผล | อยู่ใน manifest v1.0? |
|---|---|---|
| `tools/freeze_v2.py` | สคริปต์ตรึง v2.0 (`--write` / `--verify`, แผนเริ่มต้น `แผนวิเคราะห์_v2.0_ร่าง.md`) | ไม่ แต่ glob `tools/*.py` ของ v1.0 จับได้ จึงทำให้ `freeze_v1.py --verify` รายงานไฟล์เกิน |
| `src/fairgroups/design_b/__init__.py`, `__main__.py`, `core.py` | ออกแบบ B (transfer 2566 → 2567, ผลรอง) รวม `--rounds` (ค่าเริ่มต้น 2,000) | ไม่ (อยู่นอก glob v1.0) อยู่ใน manifest v2.0 |
| `tests/test_design_b.py`, `tests/test_freeze_v2_schema.py` | การทดสอบ | ไม่ hash ทั้งสองรุ่น (tests ไม่อยู่ในรายการตรึง) |

ไฟล์อื่นที่ manifest v1.0 hash ไว้ (config.py, run_pilot.py, requirements.txt, `src/fairgroups/*.py` ที่เหลือ, `tools/*.py` ที่เหลือ, สคริปต์และผลเลือกรัฐ) **ไม่เปลี่ยน** ตามผล `git diff --stat prereg-v1.0`

## ผลต่อการตรวจ v1.0

`python tools/freeze_v1.py --verify` จะรายงาน "ไม่ตรง" ที่ `src/fairgroups/freeze.py`, `src/fairgroups/hmda.py` และ `tools/freeze_v2.py` และด่าน R ของ `access_guard` (`--unlock-R`) จะถูกปฏิเสธเช่นกัน นี่เป็นผลที่คาดไว้และไม่เป็นปัญหา เพราะ R เปิดและรันครั้งเดียวไปแล้ว (แผน §4.4 ห้ามรันซ้ำ) และผลของ R รันจากโค้ด v1.0 ตามที่ตรึง

**วิธีตรวจว่าโค้ดที่ใช้รัน R ตรงกับ v1.0 แทน `freeze_v1.py --verify`:**

```powershell
git diff prereg-v1.0 --stat                 # ต้องเห็นเฉพาะ freeze.py และ hmda.py ตามตารางข้างบน
git diff prereg-v1.0 -- src/fairgroups/freeze.py src/fairgroups/hmda.py
git ls-files --others --exclude-standard tools src tests   # ไฟล์ใหม่ที่ยังไม่ track
```

ผู้ตรวจสอบย้อนหลังที่ต้องการเทียบกับ manifest v1.0 ตรง ๆ ให้ checkout tag `prereg-v1.0` ไปยังโฟลเดอร์แยก (`git worktree add ..\_v1_check prereg-v1.0`) แล้วรัน `freeze_v1.py --verify` ที่นั่น (ไฟล์ใน `09_แผนวิเคราะห์` ที่ manifest อ้างอยู่นอก repo ต้องไม่ถูกแก้)

## วิธีตรวจ v2.0 (หลังรณชัยตรึงเอง)

```powershell
python tools/freeze_v2.py                  # dry-run: แสดงรายการไฟล์และ hash (ไม่เขียน)
python tools/freeze_v2.py --write          # รณชัยสั่งเอง: เขียน freeze/v2_0_manifest.json
python tools/freeze_v2.py --verify         # ตรวจโค้ดปัจจุบันกับ manifest v2.0
```

dry-run ก่อนตรึง (2026-11-21) รวม 72 ไฟล์ ได้แก่ไฟล์ของ v1.0 ทั้งหมด + `tools/freeze_v2.py` + `design_b/__init__.py`, `__main__.py`, `core.py` หากแก้ไฟล์ใดหลังจากนี้ต้องคำนวณใหม่ก่อน `--write`
