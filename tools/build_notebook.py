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
    first += "# ใช้ wheel CPU เพื่อลดขนาดดาวน์โหลดและไม่ติดตั้ง CUDA ที่ไม่จำเป็น\n"
    first += "subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--index-url', 'https://download.pytorch.org/whl/cpu', *[p for p in pins if p.startswith('torch==')]])\n"
    first += "subprocess.check_call([sys.executable, '-m', 'pip', 'install', *pins])\n"
    first += "# HBAC 0.2.6 ระบุ numpy<2 ใน metadata แต่ทดสอบกับ env numpy2 แล้ว; ติดตั้ง dependency kmodes ใน pins ด้านบน\n"
    first += "subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-deps', *hbac_pins])\n"
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
    cells = [cell("code", first), cell("markdown", "# ต้นแบบนำร่อง Fair Hidden Groups\n"
             "เลือก Runtime → Run all บน CPU; ไม่ต้องอัปโหลด src หรือข้อมูลก่อน\n"
             "HMDA GA 2023; ประชากรใช้ประเมินและ oracle เท่านั้น · MLflow SQLite ไม่มี artifact รายรัน\n"),
             cell("code", setup), cell("code", "%%writefile requirements.txt\n" + requirement),
             cell("code", "%%writefile pytest.ini\n" + (ROOT / "pytest.ini").read_text())]
    for path in embedded_files():
        cells.append(cell("code", f"%%writefile {path.relative_to(ROOT).as_posix()}\n" + path.read_text()))
    cells += [cell("code", "import sys, subprocess\nsubprocess.check_call([sys.executable, '-m', 'pytest', 'tests', '-q'])\n"),
              cell("code", "import time\nstart = time.perf_counter()\n"
                   "subprocess.check_call([sys.executable, 'run_pilot.py', '--quick' if QUICK else '--full'])\n"
                   "print(f'Wall time: {time.perf_counter()-start:.1f} seconds')\n"
                   "subprocess.check_call([sys.executable, '-m', 'pytest', 'tests', '-q'])\n"),
              cell("code", "from IPython.display import display, Markdown, Image\n"
                   "display(Markdown(Path('results/hmda_pilot_summary.md').read_text()))\n"
                   "for path in sorted(Path('results/figures').glob('*.png')):\n    display(Image(filename=str(path)))\n"),
              cell("code", "# ดาวน์โหลดผลรวม (ไม่รวม data และ mlruns ที่มีขนาดใหญ่)\n"
                   "import shutil\nshutil.make_archive('pilot_results', 'zip', 'results')\n"
                   "try:\n    from google.colab import files\n    files.download('pilot_results.zip')\n"
                   "except ImportError:\n    print(Path('pilot_results.zip').resolve())\n")]
    cells.append(cell("code", "# หน้าสาธิตท้าย notebook: ต้นแบบเพื่อการวิจัยเท่านั้น\nimport sys\nsys.path.insert(0, str(BASE / 'src'))\nfrom fairgroups.demo import build_interface\ndemo = build_interface(BASE / 'results')\ndemo.launch(share=True)\n"))
    notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python", "version": "3.11"}, "colab": {"name": "pilot_colab.ipynb"}},
                "nbformat": 4, "nbformat_minor": 5}
    # nbformat 4.5 ใช้ id ของเซลล์เพื่อไม่ให้ Colab เตือน schema
    for index, item in enumerate(cells):
        item["id"] = f"pilot-{index:03d}"
    target = ROOT / "notebooks/pilot_colab.ipynb"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


def validate(path):
    """ทดลองสร้างไฟล์ fallback ในพื้นที่ชั่วคราวภายในโฟลเดอร์งาน"""
    notebook = json.loads(Path(path).read_text())
    assert notebook["nbformat"] == 4
    assert "pip" in "".join(notebook["cells"][0]["source"])
    extracted = {}
    with tempfile.TemporaryDirectory(prefix=".notebook-check-", dir=ROOT) as temp:
        for item in notebook["cells"]:
            source = "".join(item["source"])
            if source.startswith("%%writefile "):
                header, body = source.split("\n", 1)
                relative = shlex.split(header)[1]
                output = Path(temp) / relative
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(body)
                assert output.read_bytes() == (ROOT / relative).read_bytes(), relative
                extracted[relative] = body
                if relative.endswith(".py"):
                    compile(body, relative, "exec")
            elif item["cell_type"] == "code":
                compile(source, "notebook-cell", "exec")
        assert all(p.relative_to(ROOT).as_posix() in extracted for p in embedded_files())
    return {"cells": len(notebook["cells"]), "matching_embedded_files": len(extracted),
            "json_valid": True, "python_cells_compile": True}


if __name__ == "__main__":
    print(json.dumps(validate(build()), indent=2))
