"""สร้าง notebook จากไฟล์จริงและตรวจว่า %%writefile ให้ไฟล์ตรงกันทุก byte"""
import json
import shlex
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cell(kind, source):
    result = {"cell_type": kind, "metadata": {}, "source": source.splitlines(keepends=True)}
    if kind == "code":
        result.update(execution_count=None, outputs=[])
    return result


# ป้ายกำกับเหนือเซลล์ %%writefile แต่ละไฟล์: ไฟล์นี้คืออะไร และอยู่ขั้นใดของระบบ (ตารางที่ 3 ในเล่ม)
FILE_LABELS = {
    "requirements.txt": "รายชื่อแพ็กเกจและเวอร์ชันที่ล็อกไว้ (เซลล์ขั้นที่ 1 อ่านรายการเดียวกันนี้)",
    "pytest.ini": "ค่าตั้งของชุดทดสอบอัตโนมัติ pytest",
    "config.py": "ค่าตั้งการทดลองทั้งหมด: รัฐ GA, seed 17/29/43, k = 2/4/8, ไฮเปอร์พารามิเตอร์ (ตารางที่ ค1) · "
                 "โหมด QUICK สุ่ม 20,000 รายการต่อ seed",
    "run_pilot.py": "จุดเริ่มรันการทดลอง: อ่านค่าตั้งจาก config.py แล้วเรียก `fairgroups.run` (ใช้ในขั้นที่ 7)",
    "src/fairgroups/__init__.py": "ไฟล์ประกาศแพ็กเกจ `fairgroups` (ไม่มีขั้นตอนคำนวณ)",
    "src/fairgroups/acs_run.py": "**[รอบแรก ACS — ไม่ใช้ในผลของเล่ม]** การทดลองนำร่องบนข้อมูลรายได้ ACS "
                                 "เก็บไว้เพื่อทำซ้ำได้ เรียกเมื่อสั่ง `--dataset acs` เท่านั้น",
    "src/fairgroups/clustering.py": "**[ค้นหากลุ่ม]** ฟังก์ชันจัดกลุ่ม k-means และวัดความตรงกับกลุ่มอ้างอิง (ARI/NMI) "
                                    "หลังจัดกลุ่มเสร็จแล้วเท่านั้น",
    "src/fairgroups/data.py": "**[รอบแรก ACS]** โหลดข้อมูล ACS และนิยามกลุ่มอ้างอิง · ตัวชี้วัดของ HMDA "
                              "เรียกใช้บางฟังก์ชันจากไฟล์นี้",
    "src/fairgroups/demo.py": "**[หน้าสาธิต]** หน้า Gradio: รับข้อมูลใบคำขอ (ไม่รับข้อมูลประชากร) → แสดงความน่าจะเป็น"
                              "อนุมัติของแบบจำลองปกติเทียบแบบจำลองที่ลดอคติ ผลหลังปรับเกณฑ์ กลุ่มที่ผู้ขออยู่ และการ์ดอธิบายกลุ่ม",
    "src/fairgroups/dro.py": "**[ลดอคติแบบที่ 1: group DRO]** สร้างนิยามกลุ่ม 4 รูปแบบ (cy, cy_bal, c, c_bal — ตารางที่ ค5) "
                             "และ loss ที่เพิ่มน้ำหนักให้กลุ่มที่ผิดพลาดมาก",
    "src/fairgroups/efficiency.py": "**[วัดประสิทธิภาพ]** วัดหน่วยความจำ เวลาฝึก/อนุมาน และนับพารามิเตอร์/FLOPs (ตารางที่ 5)",
    "src/fairgroups/explanations.py": "**[อธิบายกลุ่ม]** ต้นไม้ตัดสินใจลึก ≤ 3 สร้างกฎอธิบายแต่ละกลุ่ม วัด fidelity F1 "
                                      "และทดสอบความต่างของตัวแปร → การ์ดอธิบายกลุ่ม (RQ2)",
    "src/fairgroups/hmda.py": "**[เตรียมข้อมูล]** โหลด HMDA จอร์เจีย 2566 คัดกรอง ตัดตัวแปรที่เกิดหลังการตัดสินใจ "
                              "ตรวจข้อมูลรั่ว แบ่งชุด 60/20/20 และแปลงตัวแปร (fit บนชุดฝึกเท่านั้น)",
    "src/fairgroups/hmda_groups.py": "**[ค้นหากลุ่ม]** ตัวจัดกลุ่มสำหรับ HMDA: k-means บนตัวแทนข้อมูล, HBAC, "
                                     "กลุ่มทางภูมิศาสตร์ และการกำหนดกลุ่มให้รายการใหม่โดยไม่ใช้ผลอนุมัติ",
    "src/fairgroups/hmda_reporting.py": "**[สรุปผล]** สร้างตารางสรุป ablation และกราฟจากไฟล์ผล CSV (ไม่ใช้ชุดทดสอบเลือกวิธี)",
    "src/fairgroups/metrics.py": "**[ตัวชี้วัด]** accuracy, F1, AUROC, ช่องว่างอัตราอนุมัติ, EO gap และกลุ่มแย่สุด "
                                 "รายกลุ่มเชื้อชาติ/เพศ (ใช้ข้อมูลประชากรเฉพาะขั้นวัดผลนี้)",
    "src/fairgroups/models.py": "**[แบบจำลองตัดสินใจ]** MLP d → 64 → 64 → 1 การฝึกแบบปกติ (ERM) และแบบ group DRO "
                                "พร้อมเลือก checkpoint ด้วยชุดตรวจสอบ",
    "src/fairgroups/postprocess.py": "**[ลดอคติแบบที่ 2: ปรับเกณฑ์รายกลุ่ม]** หาเกณฑ์อนุมัติแยกตามกลุ่มที่ค้นพบบนชุดตรวจสอบ "
                                     "(parity / EO) พร้อมเงื่อนไข accuracy ลดไม่เกิน 2 จุด และกลุ่มสุ่ม/oracle เป็นตัวเทียบ",
    "src/fairgroups/postprocess_reporting.py": "**[สรุปผล]** ตารางสรุปผลการปรับเกณฑ์รายกลุ่ม และ sanity check",
    "src/fairgroups/reporting.py": "**[สรุปผล]** ฟังก์ชันสร้างตาราง markdown และกราฟพื้นฐานจากไฟล์ CSV",
    "src/fairgroups/representations.py": "**[เรียนรู้ตัวแทนข้อมูล]** ตัวเข้ารหัส SCARF (contrastive, ไม่ใช้ป้ายกำกับ) "
                                         "d → 64 → 64 → 32 และตัวแทนจากค่าความผิดพลาด (OOF)",
    "src/fairgroups/run.py": "**[ตัวควบคุมการทดลอง]** ร้อยทุกขั้นเข้าด้วยกัน: เตรียมข้อมูล → SCARF → จัดกลุ่ม → "
                             "ฝึก ERM/JTT/DRO → ปรับเกณฑ์ → อธิบายกลุ่ม → วัดผล → บันทึก MLflow และไฟล์ผล ทุก seed",
    "src/fairgroups/tracking.py": "**[บันทึกการทดลอง]** บันทึกค่าตั้งและผลทุกการรันลง MLflow (SQLite)",
    "tests/conftest.py": "ตั้งค่าให้ pytest หาโค้ดใน `src` ได้",
    "tests/test_groupdef.py": "ทดสอบนิยามกลุ่ม 4 รูปแบบของ DRO และสูตรถ่วงคลาส",
    "tests/test_hmda.py": "ทดสอบการเตรียมข้อมูล HMDA และการตัดตัวแปรที่รั่ว",
    "tests/test_leakage.py": "ทดสอบว่าไม่มีข้อมูลรั่วจากชุดตรวจสอบ/ทดสอบเข้าสู่การฝึก",
    "tests/test_methods.py": "ทดสอบสูตร group DRO ตัวชี้วัด และการฝึก MLP",
    "tests/test_postprocess.py": "ทดสอบการปรับเกณฑ์: ใช้ชุดตรวจสอบเท่านั้น และไม่ใช้ข้อมูลประชากรตอนทำนาย",
    "tests/test_tracking.py": "ทดสอบว่า MLflow อ่านผลกลับได้",
    "tests/test_tuning.py": "ทดสอบการรวมกลุ่มเล็ก การถ่วง loss และการเลือกต้นไม้อธิบาย",
}

OVERVIEW = """# ต้นแบบนำร่อง: ค้นหากลุ่มเสียเปรียบที่ซ่อนอยู่ในการอนุมัติสินเชื่อ (HMDA)
**วิธีใช้:** เลือก Runtime → Run all บน CPU ไม่ต้องอัปโหลดโค้ดหรือข้อมูล · ใช้เวลารวมประมาณ 25–35 นาที

ข้อมูล HMDA รัฐจอร์เจีย ปี 2566 · ข้อมูลประชากร (เชื้อชาติ/เพศ) ใช้เฉพาะขั้นวัดผลและตัวเทียบ oracle เท่านั้น

| ขั้น | เซลล์ทำอะไร |
|---|---|
| 1 | ติดตั้งแพ็กเกจ |
| 2 | เตรียมโฟลเดอร์งาน |
| 3 | เขียนไฟล์ค่าตั้ง (requirements, pytest, config, run_pilot) |
| 4 | เขียนโค้ดต้นแบบ 19 ไฟล์ (`src/fairgroups/`) — แต่ละเซลล์มีป้ายบอกว่าเป็นองค์ประกอบใดของระบบ |
| 5 | เขียนชุดทดสอบอัตโนมัติ 8 ไฟล์ (`tests/`) |
| 6 | รันชุดทดสอบ pytest |
| 7 | **รันการทดลองนำร่อง** (3 seed · ส่วนที่ใช้เวลานานที่สุด) |
| 8 | แสดงตารางสรุปและกราฟ |
| 9 | ดาวน์โหลดผล `pilot_results.zip` |
| 10 | เปิดหน้าสาธิต Gradio |

ขั้นที่ 3–5 เป็นเซลล์ `%%writefile` ที่เขียนไฟล์ลงดิสก์เท่านั้น ยังไม่คำนวณอะไร การคำนวณจริงเกิดในขั้นที่ 6–7
"""


def label(text):
    return cell("markdown", text + "\n")


def embedded_files():
    candidates = [ROOT / "config.py", ROOT / "run_pilot.py"] + sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "tests").glob("*.py"))
    return [path for path in candidates if not path.name.startswith("._")]


def build():
    """เซลล์แรกติดตั้งตาม requirements โดยไม่ต้องมี repo"""
    requirement = (ROOT / "requirements.txt").read_text()
    first = "# รันเซลล์นี้บน Colab เท่านั้น: ในเครื่องใช้ venv เดิมและไม่ติดตั้งเพิ่ม\n"
    first += "import sys, subprocess\n"
    first += f"REQUIREMENTS = {requirement!r}\n"
    first += "all_pins = REQUIREMENTS.split()\nhbac_pins = [p for p in all_pins if p.startswith('unsupervised-bias-detection==')]\npins = [p for p in all_pins if p not in hbac_pins]\n"
    first += (
        "# Colab โหลด numpy/pandas/torch ฯลฯ ไว้ในหน่วยความจำตั้งแต่เปิด runtime ถ้าติดตั้งเวอร์ชันอื่นทับ\n"
        "# จะเกิด ImportError ปะปนสองเวอร์ชัน (เช่น numpy._core.umath) จนกว่าจะรีสตาร์ต จึงคงเวอร์ชันของ Colab ไว้\n"
        "# และล็อกไม่ให้ pip เปลี่ยน ส่วนแพ็กเกจอื่นติดตั้งตาม requirements · เวอร์ชันจริงบันทึกใน results/environment.json\n"
        "import importlib.metadata as md, tempfile\n"
        "KEEP = {'numpy', 'pandas', 'scipy', 'scikit-learn', 'torch', 'matplotlib', 'joblib', 'threadpoolctl', 'psutil'}\n"
        "def installed(name):\n"
        "    try:\n"
        "        return md.version(name)\n"
        "    except md.PackageNotFoundError:\n"
        "        return None\n"
        "keep = {p.split('==')[0]: installed(p.split('==')[0]) for p in pins if p.split('==')[0] in KEEP}\n"
        "constraints = tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False)\n"
        "constraints.write('\\n'.join(f'{n}=={v}' for n, v in keep.items() if v)); constraints.close()\n"
        "to_install = [p for p in pins if not keep.get(p.split('==')[0])]\n"
        "print('ใช้เวอร์ชันของ Colab:', {n: v for n, v in keep.items() if v})\n"
        "try:\n"
        "    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *to_install, '-c', constraints.name])\n"
        "except subprocess.CalledProcessError:\n"
        "    # ถ้าเวอร์ชันที่ล็อกไว้เข้ากับแพ็กเกจหลักของ Colab ไม่ได้ ให้ pip เลือกเวอร์ชันที่เข้ากันเอง (ยังล็อกแพ็กเกจหลัก)\n"
        "    print('ติดตั้งตามเวอร์ชันที่ล็อกไม่ได้ ใช้เวอร์ชันที่เข้ากับ Colab แทน')\n"
        "    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *[p.split('==')[0] for p in to_install], '-c', constraints.name])\n"
        "# HBAC 0.2.6 ระบุ numpy<2 ใน metadata แต่ทดสอบกับ numpy 2 แล้ว จึงติดตั้งแบบ --no-deps\n"
        "subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', '--no-deps', *hbac_pins])\n"
    )
    setup = '''# ปล่อยว่างได้: notebook จะสร้างโค้ด src ให้ครบเอง
REPO_URL = "https://github.com/ronnachaii/fair-credit-hidden-groups.git"
QUICK = True
from pathlib import Path
import subprocess, os
BASE = Path('/content/rsu_fair_pilot') if Path('/content').exists() else Path.cwd() / 'colab_pilot'
if REPO_URL and not BASE.exists():
    subprocess.check_call(['git', 'clone', REPO_URL, str(BASE)])
BASE.mkdir(parents=True, exist_ok=True)
os.chdir(BASE)
for folder in ['src/fairgroups', 'tests', 'results']:
    Path(folder).mkdir(parents=True, exist_ok=True)
# ไฟล์ embedded ด้านล่างเป็นเวอร์ชันเดียวกับชุดส่งงาน แม้เลือก clone repo
'''
    cells = [cell("markdown", OVERVIEW),
             label("## ขั้นที่ 1 ติดตั้งแพ็กเกจ\n"
                   "ติดตั้งไลบรารีที่ต้นแบบใช้ (LightGBM, MLflow, Gradio, HBAC ฯลฯ) โดยคงเวอร์ชัน numpy/pandas/torch "
                   "ที่ Colab โหลดไว้แล้ว เพื่อไม่ให้ไลบรารีปะปนสองเวอร์ชัน"),
             cell("code", first),
             label("## ขั้นที่ 2 เตรียมโฟลเดอร์งาน\n"
                   "clone ที่เก็บโค้ดจาก GitHub ไปที่ `/content/rsu_fair_pilot` และสร้างโฟลเดอร์ `src`, `tests`, `results` · "
                   "`QUICK = True` คือโหมดนำร่อง (เปลี่ยนเป็น `False` = โหมดเต็ม ทั้งรัฐ 5 seed ใช้เวลานานมาก)"),
             cell("code", setup),
             label("## ขั้นที่ 3 เขียนไฟล์ค่าตั้ง\n"
                   "เซลล์ `%%writefile` เขียนไฟล์ลงดิสก์ตามชื่อในบรรทัดแรก (ยังไม่คำนวณ)\n\n"
                   "**`requirements.txt`** — " + FILE_LABELS["requirements.txt"]),
             cell("code", "%%writefile requirements.txt\n" + requirement),
             label("**`pytest.ini`** — " + FILE_LABELS["pytest.ini"]),
             cell("code", "%%writefile pytest.ini\n" + (ROOT / "pytest.ini").read_text())]
    for path in embedded_files():
        relative = path.relative_to(ROOT).as_posix()
        text = f"**`{relative}`** — {FILE_LABELS[relative]}"
        if relative == "src/fairgroups/__init__.py":
            text = ("## ขั้นที่ 4 เขียนโค้ดต้นแบบ (`src/fairgroups/`)\n"
                    "ป้ายในวงเล็บเหลี่ยมบอกว่าไฟล์เป็นองค์ประกอบใดของระบบ (ตารางที่ 3 ในเล่ม) "
                    "ลำดับการทำงานจริงอยู่ใน `run.py`\n\n" + text)
        elif relative == "tests/conftest.py":
            text = ("## ขั้นที่ 5 เขียนชุดทดสอบอัตโนมัติ (`tests/`)\n"
                    "ตรวจสูตรที่มีผลต่อข้อสรุปและตรวจว่าไม่มีข้อมูลรั่ว จะรันจริงในขั้นที่ 6\n\n" + text)
        cells += [label(text), cell("code", f"%%writefile {relative}\n" + path.read_text())]
    cells += [label("## ขั้นที่ 6 รันชุดทดสอบ\n"
                    "รัน pytest ทุกไฟล์ก่อนเริ่มทดลอง ถ้าผ่านจะเห็น `passed` ไม่มี `failed`"),
              cell("code", "import sys, subprocess\nsubprocess.check_call([sys.executable, '-m', 'pytest', 'tests', '-q'])\n"),
              label("## ขั้นที่ 7 รันการทดลองนำร่อง (ใช้เวลานานที่สุด)\n"
                    "ดาวน์โหลดข้อมูล HMDA จาก CFPB และคัดกรอง → เรียนรู้ตัวแทน SCARF → จัดกลุ่ม → ฝึก ERM/JTT/group DRO → "
                    "ปรับเกณฑ์รายกลุ่ม → อธิบายกลุ่ม → วัดผลบนชุดทดสอบ ทำ 3 seed แล้วรันชุดทดสอบซ้ำ · "
                    "ผลบันทึกลงโฟลเดอร์ `results/` และ MLflow · บรรทัด `Wall time` คือเวลาที่ใช้"),
              cell("code", "import time\nstart = time.perf_counter()\n"
                   "subprocess.check_call([sys.executable, 'run_pilot.py', '--quick' if QUICK else '--full'])\n"
                   "print(f'Wall time: {time.perf_counter()-start:.1f} seconds')\n"
                   "subprocess.check_call([sys.executable, '-m', 'pytest', 'tests', '-q'])\n"),
              label("## ขั้นที่ 8 แสดงตารางสรุปและกราฟ\n"
                    "แสดง `results/hmda_pilot_summary.md` (ค่าเฉลี่ย ± SD ข้าม 3 seed ทุกวิธี) และกราฟใน `results/figures/`"),
              cell("code", "from IPython.display import display, Markdown, Image\n"
                   "display(Markdown(Path('results/hmda_pilot_summary.md').read_text()))\n"
                   "for path in sorted(Path('results/figures').glob('*.png')):\n    display(Image(filename=str(path)))\n"),
              label("## ขั้นที่ 9 ดาวน์โหลดผล\n"
                    "บีบอัดโฟลเดอร์ `results/` เป็น `pilot_results.zip` แล้วดาวน์โหลดลงเครื่อง"),
              cell("code", "# ดาวน์โหลดผลรวม (ไม่รวม data และ mlruns ที่มีขนาดใหญ่)\n"
                   "import shutil\nshutil.make_archive('pilot_results', 'zip', 'results')\n"
                   "try:\n    from google.colab import files\n    files.download('pilot_results.zip')\n"
                   "except ImportError:\n    print(Path('pilot_results.zip').resolve())\n")]
    cells += [label("## ขั้นที่ 10 หน้าสาธิต Gradio\n"
                    "เปิดหน้าเว็บทดลองทำนาย (ลิงก์ `gradio.live` ขึ้นใต้เซลล์) · ต้นแบบเพื่อการวิจัยเท่านั้น"),
              cell("code", "# หน้าสาธิตท้าย notebook: ต้นแบบเพื่อการวิจัยเท่านั้น\nimport sys\nsys.path.insert(0, str(BASE / 'src'))\nfrom fairgroups.demo import build_interface\ndemo = build_interface(BASE / 'results')\ndemo.launch(share=True)\n")]
    notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python", "version": "3.11"}, "colab": {"name": "pilot_colab.ipynb"}},
                "nbformat": 4, "nbformat_minor": 5}
    # nbformat 4.5 ใช้ id ของเซลล์เพื่อไม่ให้ Colab เตือน schema
    for index, item in enumerate(cells):
        item["id"] = f"pilot-{index:03d}"
    target = ROOT / "notebooks/pilot_colab.ipynb"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return target


def validate(path):
    """ทดลองสร้างไฟล์ fallback ในพื้นที่ชั่วคราวภายในโฟลเดอร์งาน"""
    notebook = json.loads(Path(path).read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    code_cells = [c for c in notebook["cells"] if c["cell_type"] == "code"]
    assert "pip" in "".join(code_cells[0]["source"])
    # ทุกเซลล์โค้ดต้องมีป้ายกำกับ markdown อยู่ก่อนหน้า
    for before, item in zip(notebook["cells"], notebook["cells"][1:]):
        if item["cell_type"] == "code":
            assert before["cell_type"] == "markdown", "".join(item["source"])[:60]
    extracted = {}
    with tempfile.TemporaryDirectory(prefix=".notebook-check-", dir=ROOT) as temp:
        for item in notebook["cells"]:
            source = "".join(item["source"])
            if source.startswith("%%writefile "):
                header, body = source.split("\n", 1)
                relative = shlex.split(header)[1]
                output = Path(temp) / relative
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(body.encode("utf-8"))
                assert output.read_bytes() == (ROOT / relative).read_bytes(), relative
                extracted[relative] = body
                if relative.endswith(".py"):
                    compile(body, relative, "exec")
            elif item["cell_type"] == "code":
                compile(source, "notebook-cell", "exec")
        assert all(p.relative_to(ROOT).as_posix() in extracted for p in embedded_files())
    return {"cells": len(notebook["cells"]), "code_cells": len(code_cells), "matching_embedded_files": len(extracted),
            "json_valid": True, "python_cells_compile": True}


if __name__ == "__main__":
    print(json.dumps(validate(build()), indent=2))
