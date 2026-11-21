"""Addendum v2.1 (after tier C was opened): C accepts v2.1, R re-read by design B accepts the v2.0 plan under v2.1,
everything else (wrong plan SHA, unchanged-reason, edited base manifest, code drift, unlisted data) still blocks."""
import json
import pytest
from fairgroups import freeze
from fairgroups.access_guard import AccessDenied, require_access


def _setup(tmp_path):
    root = tmp_path / "repo"
    (root / "src" / "fairgroups").mkdir(parents=True)
    (root / "tools").mkdir()
    (root / "src" / "fairgroups" / "a.py").write_text("x = 1\n")
    (root / "config.py").write_text("K = 8\n")
    (root / "run_pilot.py").write_text("pass\n")
    (root / "requirements.txt").write_text("numpy\n")
    plan = tmp_path / "plan.md"
    plan.write_text("plan v2.0", encoding="utf-8")
    fdir = tmp_path / "freeze"
    fdir.mkdir()
    base = freeze.build_manifest(plan, "v2.0", root)
    freeze.manifest_path("v2.0", fdir).write_text(json.dumps(base), encoding="utf-8")
    return root, plan, fdir, freeze.sha256_file(plan)


def _addendum(root, plan, fdir, reason="fix"):
    base_path = freeze.manifest_path("v2.0", fdir)
    base = json.loads(base_path.read_text(encoding="utf-8"))
    now = freeze.build_manifest(plan, "v2.1", root)
    changes = {k: {"sha256_before": base["files"].get(k), "sha256_after": v, "reason": reason}
               for k, v in now["files"].items() if base["files"].get(k) != v}
    now.update(supersedes="v2.0", base_manifest_file_sha256=freeze.sha256_file(base_path), changes=changes)
    freeze.manifest_path("v2.1", fdir).write_text(json.dumps(now), encoding="utf-8")
    return now


def _args(root, plan, fdir, sha, **kw):
    return dict(plan_file=plan, root=root, freeze_dir=fdir, **kw)


def test_c_blocked_after_code_change_until_addendum_then_passes(tmp_path):
    root, plan, fdir, sha = _setup(tmp_path)
    assert require_access("GA", 2024, unlock_C=sha, **_args(root, plan, fdir, sha)) == "C"
    (root / "src" / "fairgroups" / "a.py").write_text("x = 2\n")
    with pytest.raises(AccessDenied, match="เปลี่ยนหลังตรึง"):
        require_access("GA", 2024, unlock_C=sha, **_args(root, plan, fdir, sha))
    _addendum(root, plan, fdir)
    assert require_access("GA", 2024, unlock_C=sha, **_args(root, plan, fdir, sha)) == "C"
    log = (fdir / "open_log.csv").read_text(encoding="utf-8").splitlines()
    assert len(log) == 3 and ",GA,2024,C," in log[-1]                      # every open still logged


def test_c_still_blocked_by_wrong_plan_sha_and_by_drift_after_addendum(tmp_path):
    root, plan, fdir, sha = _setup(tmp_path)
    (root / "config.py").write_text("K = 2\n")
    _addendum(root, plan, fdir)
    with pytest.raises(AccessDenied):
        require_access("GA", 2024, unlock_C="0" * 64, **_args(root, plan, fdir, sha))
    with pytest.raises(AccessDenied):
        require_access("GA", 2024, **_args(root, plan, fdir, sha))          # no unlock at all
    (root / "config.py").write_text("K = 3\n")                              # changed again after v2.1
    with pytest.raises(AccessDenied, match="เปลี่ยนหลังตรึง"):
        require_access("GA", 2024, unlock_C=sha, **_args(root, plan, fdir, sha))


def test_addendum_must_explain_each_change_and_not_touch_base(tmp_path):
    root, plan, fdir, sha = _setup(tmp_path)
    (root / "config.py").write_text("K = 2\n")
    add = _addendum(root, plan, fdir)
    add["changes"] = {}                                                      # reason removed
    freeze.manifest_path("v2.1", fdir).write_text(json.dumps(add), encoding="utf-8")
    with pytest.raises(AccessDenied, match="เหตุผล"):
        require_access("GA", 2024, unlock_C=sha, **_args(root, plan, fdir, sha))
    _addendum(root, plan, fdir)
    assert require_access("GA", 2024, unlock_C=sha, **_args(root, plan, fdir, sha)) == "C"
    base_path = freeze.manifest_path("v2.0", fdir)                          # base manifest edited afterwards
    base = json.loads(base_path.read_text(encoding="utf-8"))
    base["python"] = "tampered"
    base_path.write_text(json.dumps(base), encoding="utf-8")
    with pytest.raises(AccessDenied, match="ถูกแก้"):
        require_access("GA", 2024, unlock_C=sha, **_args(root, plan, fdir, sha))


def test_r_reread_by_design_b_needs_both_unlocks_with_v2_plan_and_manifest_v2_1(tmp_path):
    root, plan, fdir, sha = _setup(tmp_path)
    (root / "config.py").write_text("K = 2\n")
    with pytest.raises(AccessDenied):                                        # no v2.1 yet, no v1.0 manifest
        require_access("CA", 2023, unlock_R=sha, unlock_C=sha, **_args(root, plan, fdir, sha))
    _addendum(root, plan, fdir)
    assert require_access("CA", 2023, unlock_R=sha, unlock_C=sha, **_args(root, plan, fdir, sha)) == "R"
    assert ",CA,2023,R," in (fdir / "open_log.csv").read_text(encoding="utf-8").splitlines()[-1]
    with pytest.raises(AccessDenied):                                        # only unlock-R with the v2.0 plan
        require_access("CA", 2023, unlock_R=sha, **_args(root, plan, fdir, sha))
    with pytest.raises(AccessDenied):                                        # unlocks disagree
        require_access("CA", 2023, unlock_R=sha, unlock_C="1" * 64, **_args(root, plan, fdir, sha))
    with pytest.raises(AccessDenied):                                        # both wrong
        require_access("CA", 2023, unlock_R="0" * 64, unlock_C="0" * 64, **_args(root, plan, fdir, sha))
    with pytest.raises(AccessDenied):                                        # states/years outside the plan stay refused
        require_access("TX", 2023, unlock_R=sha, unlock_C=sha, **_args(root, plan, fdir, sha))
    (root / "config.py").write_text("K = 9\n")
    with pytest.raises(AccessDenied):                                        # code drift after v2.1
        require_access("OH", 2023, unlock_R=sha, unlock_C=sha, **_args(root, plan, fdir, sha))
