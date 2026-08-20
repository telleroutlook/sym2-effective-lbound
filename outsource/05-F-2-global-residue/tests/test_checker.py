#!/usr/bin/env python3
"""
test_checker.py — Tests for F-2 structural checker (v2).
"""
import subprocess
import tempfile
import os


CHECKER = os.path.join(os.path.dirname(__file__), "..", "checker", "check_global_residue.py")


def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def _run_checker(submission_dir):
    result = subprocess.run(
        ["python3", CHECKER, submission_dir],
        capture_output=True, text=True
    )
    return result.returncode, result.stdout


def _base_files(tmpdir, stmt="# [OBL] F-2.\n", proof_a=None, proof_b=None, proof_c=None):
    _write(os.path.join(tmpdir, "statement.md"), stmt)
    _write(os.path.join(tmpdir, "proof.md"), "# Proof\n[OBL] Combined.\n")
    _write(os.path.join(tmpdir, "proof-F-2A.md"),
           proof_a or "# F-2A\nDiagonal norm-square jacquet–shalika.\n")
    _write(os.path.join(tmpdir, "proof-F-2B.md"),
           proof_b or "# F-2B\nEuler factor archimedean ramified.\n")
    _write(os.path.join(tmpdir, "proof-F-2C.md"),
           proof_c or "# F-2C\nUniformity local explicit.\n")
    _write(os.path.join(tmpdir, "dependencies.yaml"), "F-2A:\n  status: '[OBL]'\n")
    _write(os.path.join(tmpdir, "limitations.md"), "# Limits\n[OBL] Limits.\n")
    _write(os.path.join(tmpdir, "novelty.md"), "# Novelty\n[OBL] Novelty.\n")
    _write(os.path.join(tmpdir, "checker", "README.md"), "# Checker\n[OBL] Notes.\n")


def test_pass_on_well_structured():
    """Well-structured submission should PASS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir)
        code, output = _run_checker(tmpdir)
        assert code == 0, f"Expected PASS but got FAIL:\n{output}"


def test_fail_on_wrong_citation():
    """Wrong JS81 citation (Ann. Math. 114) should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir,
            proof_a="# F-2A\nDiagonal norm-square jacquet–shalika.\n"
                    "Ann. Math. 114 (1981), 459–512.\n")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"


def test_fail_on_missing_F2A():
    """Missing F-2A concepts should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir,
            proof_a="# F-2A\nSome wrong content without key concepts.\n")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"


def test_fail_on_THM_without_OBL():
    """Promoting to [THM] without [OBL] should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir, stmt="# Statement\n[THM] Proved.\n")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"


def test_no_false_positive_trivial():
    """Trivial content should not pass."""
    with tempfile.TemporaryDirectory() as tmpdir:
        content = "[OBL] 0 normalization factors\n"
        for f in ["statement.md", "proof.md", "proof-F-2A.md", "proof-F-2B.md",
                   "proof-F-2C.md", "dependencies.yaml", "limitations.md",
                   "novelty.md", "checker/README.md"]:
            _write(os.path.join(tmpdir, f), content)
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL on trivial content but got PASS"
