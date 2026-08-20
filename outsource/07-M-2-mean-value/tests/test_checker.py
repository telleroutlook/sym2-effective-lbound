#!/usr/bin/env python3
"""
test_checker.py — Tests for M-2 structural checker (v2).
"""
import subprocess
import tempfile
import os


CHECKER = os.path.join(os.path.dirname(__file__), "..", "checker", "check_mean_value.py")


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


def _base_files(tmpdir, stmt="# [OBL] M-2.\n", proof="# Proof\nafe diagonal t log t.\n"):
    _write(os.path.join(tmpdir, "statement.md"), stmt)
    _write(os.path.join(tmpdir, "proof.md"), proof)
    _write(os.path.join(tmpdir, "dependencies.yaml"),
           "ingredients:\n  - id: AFE\n    status: '[OBL]'\n")
    _write(os.path.join(tmpdir, "limitations.md"), "# Limits\n[OBL] Limits.\n")
    _write(os.path.join(tmpdir, "novelty.md"), "# Novelty\n[OBL] Novelty.\n")
    _write(os.path.join(tmpdir, "checker", "README.md"), "# Checker\n[OBL] Notes.\n")


def test_pass_on_well_structured():
    """Well-structured submission with correct concepts should PASS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir)
        code, output = _run_checker(tmpdir)
        assert code == 0, f"Expected PASS but got FAIL:\n{output}"


def test_fail_on_wrong_main_term():
    """Main term c_Π T (not T log T) should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir, proof="# Proof\nc_Π T + O(T^{1-δ}).\n")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"
        assert "forbidden" in output.lower()


def test_fail_on_no_afe_concept():
    """Missing AFE keyword should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir,
            proof="# Proof\nc_Π T log T + O(T^{1-δ}). Off-diagonal shifted.\n")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"


def test_fail_on_trivial_proof():
    """Proof with no mathematical content should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir,
            proof="# Proof\nThe result follows from standard methods.\n")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"


def test_fail_on_missing_concepts():
    """Missing AFE or diagonal should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir, proof="# Proof\nSome math.\n")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"


def test_no_false_positive_trivial():
    """Trivial content should not pass."""
    with tempfile.TemporaryDirectory() as tmpdir:
        content = "[OBL] 0 normalization factors\n"
        for f in ["statement.md", "proof.md", "dependencies.yaml",
                   "limitations.md", "novelty.md", "checker/README.md"]:
            _write(os.path.join(tmpdir, f), content)
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL on trivial content but got PASS"
