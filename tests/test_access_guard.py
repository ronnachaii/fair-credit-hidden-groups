"""พิสูจน์ว่าตัวป้องกันปี 2567 / รัฐใหม่ (ชุดทดสอบ R/C) ทำงาน: ปฏิเสธก่อนอ่านไฟล์หรือดาวน์โหลดใด ๆ"""
import json
import shutil
import urllib.request
from pathlib import Path
import pytest
from config import Config, V1_FROZEN, make_v1_config
from fairgroups import access_guard, freeze
from fairgroups.access_guard import AccessDenied, classify, require_access
from fairgroups.hmda import load_hmda
from fairgroups.run import run_experiment

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def no_network(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("ห้ามดาวน์โหลดก่อนผ่านด่านป้องกัน")
    monkeypatch.setattr(urllib.request, "urlretrieve", boom)


def test_classification_of_states_and_years():
    assert classify("GA", 2023) == "D"
    assert classify("ID", 2023) == "T" and classify("nm", 2023) == "T"
    assert all(classify(s, 2023) == "R" for s in ["CA", "OH", "FL"])
    assert all(classify(s, 2024) == "C" for s in ["GA", "ID", "NM", "CA", "TX"])
    assert classify("TX", 2023) == "UNLISTED"


@pytest.mark.parametrize("state,year", [("CA", 2023), ("OH", 2023), ("FL", 2023), ("GA", 2024), ("ID", 2024),
                                        ("CA", 2024), ("TX", 2023)])
def test_loader_refuses_restricted_data_without_touching_files_or_network(state, year, tmp_path, no_network):
    with pytest.raises(AccessDenied):
        load_hmda(tmp_path / "data", state, year)
    assert not (tmp_path / "data").exists()                       # ไม่แม้แต่สร้างโฟลเดอร์แคช


def test_development_and_timing_states_pass_without_flags():
    assert require_access("GA", 2023) == "D" and require_access("ID", 2023) == "T" and require_access("NM", 2023) == "T"


def test_flags_without_valid_hash_or_manifest_are_refused(tmp_path):
    plan = tmp_path / "plan.md"
    plan.write_text("แผน v1", encoding="utf-8")
    good = freeze.sha256_file(plan)
    with pytest.raises(AccessDenied):                                     # ไม่มีแฟล็ก
        require_access("CA", 2023, plan_file=plan, freeze_dir=tmp_path)
    with pytest.raises(AccessDenied):                                     # แฟล็กไม่ใช่ SHA-256
        require_access("CA", 2023, unlock_R="yes", plan_file=plan, freeze_dir=tmp_path)
    with pytest.raises(AccessDenied):                                     # SHA ไม่ตรงกับไฟล์แผน
        require_access("CA", 2023, unlock_R="0" * 64, plan_file=plan, freeze_dir=tmp_path)
    with pytest.raises(AccessDenied):                                     # SHA ตรง แต่ยังไม่มี manifest การตรึง
        require_access("CA", 2023, unlock_R=good, plan_file=plan, freeze_dir=tmp_path)
    with pytest.raises(AccessDenied):                                     # ปลดล็อก R ใช้เปิดปี 2567 ไม่ได้
        require_access("CA", 2024, unlock_R=good, plan_file=plan, freeze_dir=tmp_path)


def _mini_repo(tmp_path):
    root = tmp_path / "repo"
    (root / "src" / "fairgroups").mkdir(parents=True)
    (root / "tools").mkdir()
    (root / "src" / "fairgroups" / "a.py").write_text("x = 1\n")
    (root / "config.py").write_text("K = 8\n")
    (root / "run_pilot.py").write_text("pass\n")
    (root / "requirements.txt").write_text("numpy\n")
    plan = tmp_path / "plan.md"
    plan.write_text("แผน v1 ตรึง", encoding="utf-8")
    return root, plan


def test_unlock_succeeds_only_with_matching_hash_manifest_and_unchanged_code(tmp_path):
    root, plan = _mini_repo(tmp_path)
    fdir = tmp_path / "freeze"
    fdir.mkdir()
    manifest = freeze.build_manifest(plan, "v1.0", root)
    freeze.manifest_path("v1.0", fdir).write_text(json.dumps(manifest), encoding="utf-8")
    sha = freeze.sha256_file(plan)
    assert require_access("CA", 2023, unlock_R=sha, plan_file=plan, root=root, freeze_dir=fdir) == "R"
    log = (fdir / "open_log.csv").read_text(encoding="utf-8").splitlines()
    assert len(log) == 2 and ",CA,2023,R," in log[1]                   # บันทึกการเปิดลง open_log
    (root / "config.py").write_text("K = 2\n")                            # แก้ config หลังตรึง
    with pytest.raises(AccessDenied, match="เปลี่ยนหลังตรึง"):
        require_access("OH", 2023, unlock_R=sha, plan_file=plan, root=root, freeze_dir=fdir)
    (root / "config.py").write_text("K = 8\n")
    plan.write_text("แผนถูกแก้", encoding="utf-8")                      # แก้แผนหลังตรึง
    with pytest.raises(AccessDenied):
        require_access("OH", 2023, unlock_R=freeze.sha256_file(plan), plan_file=plan, root=root, freeze_dir=fdir)


def test_2024_needs_its_own_v2_manifest(tmp_path):
    root, plan = _mini_repo(tmp_path)
    fdir = tmp_path / "freeze"
    fdir.mkdir()
    freeze.manifest_path("v1.0", fdir).write_text(json.dumps(freeze.build_manifest(plan, "v1.0", root)))
    sha = freeze.sha256_file(plan)
    with pytest.raises(AccessDenied):
        require_access("GA", 2024, unlock_C=sha, plan_file=plan, root=root, freeze_dir=fdir)
    freeze.manifest_path("v2.0", fdir).write_text(json.dumps(freeze.build_manifest(plan, "v2.0", root)))
    assert require_access("GA", 2024, unlock_C=sha, plan_file=plan, root=root, freeze_dir=fdir) == "C"


def test_run_experiment_refuses_before_creating_output(tmp_path, no_network):
    for state, year in [("CA", 2023), ("GA", 2024)]:
        out = tmp_path / f"out_{state}_{year}"
        with pytest.raises(AccessDenied):
            run_experiment(Config(state=state, year=year, split_seed=17), tmp_path, output_dir=out)
        assert not out.exists()


def test_frozen_config_values_are_the_agreed_v1_values():
    cfg = make_v1_config()
    assert (cfg.k_main, cfg.delta_min, cfg.theta_neg, cfg.m_benefit) == (8, 0.01, 0.10, 0.01)
    assert (cfg.threads, cfg.device, cfg.split_seed, cfg.mode) == (2, "cpu", 17, "confirm")
    assert cfg.seeds == (17, 29, 43, 59, 71) and len(cfg.cheap_seeds) == 10
    assert cfg.ks == (2, 4, 8) and cfg.max_rows == 0 and V1_FROZEN["no_training_set_cap"]
    assert cfg.bootstrap_rounds == 2000 and cfg.random_sets >= 30


def test_freeze_manifest_covers_code_and_config_but_not_results():
    files = freeze.build_manifest_files_only(ROOT)
    assert "config.py" in files and "src/fairgroups/access_guard.py" in files and "run_pilot.py" in files
    assert not any(k.startswith(("results", "data", "tests")) for k in files)
