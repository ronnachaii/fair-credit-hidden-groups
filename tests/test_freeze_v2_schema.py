"""ตัวตรึง v2.0 (รวม design_b) และการตรวจ header ของ CSV ใน load_hmda (ไม่มีการเข้าถึงข้อมูล R/C)"""
import json
from pathlib import Path
import pandas as pd
import pytest
from fairgroups import freeze, hmda
from fairgroups.access_guard import require_access
from fairgroups.hmda import SchemaError, REQUIRED_COLUMNS, check_header, load_hmda

ROOT = Path(__file__).resolve().parents[1]


def test_code_files_v1_unchanged_and_v2_adds_design_b_and_freeze_v2():
    v1 = {freeze.manifest_key(p, ROOT) for p in freeze.code_files(ROOT)}
    v1b = {freeze.manifest_key(p, ROOT) for p in freeze.code_files(ROOT, "v1.0")}
    v2 = {freeze.manifest_key(p, ROOT) for p in freeze.code_files(ROOT, "v2.0")}
    assert v1 == v1b and not any("design_b" in k for k in v1)
    assert v2 - v1 == {f"src/fairgroups/design_b/{n}" for n in ("__init__.py", "__main__.py", "core.py")}
    assert v1 <= v2 and "tools/freeze_v2.py" in v1 and "tools/freeze_v2.py" in v2   # tools/*.py globbed


def test_v2_manifest_verify_and_access_guard_c_uses_design_b(tmp_path):
    root = tmp_path / "repo"
    (root / "src" / "fairgroups" / "design_b").mkdir(parents=True)
    (root / "tools").mkdir()
    (root / "src" / "fairgroups" / "a.py").write_text("x = 1\n")
    (root / "src" / "fairgroups" / "design_b" / "core.py").write_text("y = 1\n")
    (root / "config.py").write_text("K = 8\n")
    plan = tmp_path / "plan.md"
    plan.write_text("แผน v2", encoding="utf-8")
    fdir = tmp_path / "freeze"
    fdir.mkdir()
    freeze.manifest_path("v2.0", fdir).write_text(json.dumps(freeze.build_manifest(plan, "v2.0", root)))
    sha = freeze.sha256_file(plan)
    assert require_access("GA", 2024, unlock_C=sha, plan_file=plan, root=root, freeze_dir=fdir) == "C"
    (root / "src" / "fairgroups" / "design_b" / "core.py").write_text("y = 2\n")      # แก้ design_b หลังตรึง
    with pytest.raises(Exception, match="design_b/core.py"):
        require_access("GA", 2024, unlock_C=sha, plan_file=plan, root=root, freeze_dir=fdir)
    ok, _ = freeze.verify_manifest("v2.0", sha, root, fdir)
    assert not ok


def _csv(path, cols, rows=2):
    pd.DataFrame({c: [1] * rows for c in cols}).to_csv(path, index=False)


def test_check_header_reports_missing_columns_without_reading_rows(tmp_path):
    p = tmp_path / "h.csv"
    cols = [c for c in REQUIRED_COLUMNS if c not in ("applicant_age", "loan_to_value_ratio")]
    _csv(p, cols)
    with pytest.raises(SchemaError) as e:
        check_header(p)
    assert "applicant_age" in str(e.value) and "loan_to_value_ratio" in str(e.value) and "2 คอลัมน์" in str(e.value)
    _csv(p, REQUIRED_COLUMNS + ["extra_new_column"])
    assert "extra_new_column" in check_header(p)                      # คอลัมน์เกินไม่เป็นปัญหา


def test_load_hmda_raises_before_reading_rows_when_columns_missing(tmp_path, monkeypatch):
    (tmp_path / "hmda").mkdir()
    _csv(tmp_path / "hmda" / "hmda_2023_GA.csv", [c for c in REQUIRED_COLUMNS if c != "derived_sex"])
    calls = []
    real = pd.read_csv
    monkeypatch.setattr(hmda.pd, "read_csv", lambda *a, **k: (calls.append(k.get("nrows")), real(*a, **k))[1])
    with pytest.raises(SchemaError, match="derived_sex"):
        load_hmda(tmp_path, "GA", 2023)
    assert calls == [0]                                                   # อ่านเฉพาะ header เท่านั้น


def test_real_2023_headers_have_all_required_columns():
    for f in sorted((ROOT / "data" / "hmda").glob("hmda_2023_*.csv")):
        check_header(f)                                                   # header เท่านั้น: 2023 ต้องผ่านเหมือนเดิม
