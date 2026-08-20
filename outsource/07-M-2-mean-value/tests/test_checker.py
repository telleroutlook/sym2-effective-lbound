#!/usr/bin/env python3
"""
test_checker.py — Tests for M-2 structural checker (rewritten).
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


def test_pass_on_well_structured():
    """Well-structured submission with correct concepts should PASS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _write(os.path.join(tmpdir, "statement.md"),
               "# M-2 Statement\n[OBL] T log T main term.\n")
        _write(os.path.join(tmpdir, "proof.md"), """# M-2 Proof
The diagonal gives A_Π T log T + B_Π T.
Off-diagonal shifted convolution is bounded using AFE.
""")
        _write(os.path.join(tmpdir, "dependencies.yaml"),
               "ingredients:\n  - id: AFE-GL3\n    status: '[OBL]'\n")
        _write(os.path.join(tmpdir, "limitations.md"),
               "# Limits\n[OBL] Some.\n")
        _write(os.path.join(tmpdir, "novelty.md"),
               "# Novelty\n[OBL] Some.\n")
        _write(os.path.join(tmpdir, "checker", "README.md"),
               "# Checker\n[OBL] Notes.\n")

        code, output = _run_checker(tmpdir)
        assert code == 0, f"Expected PASS but got FAIL:\n{output}"


def test_fail_on_wrong_main_term():
    """Main term c_Π T (not T log T) should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _write(os.path.join(tmpdir, "statement.md"),
               "# Statement\n[OBL] Some.\n")
        _write(os.path.join(tmpdir, "proof.md"), """# Proof
The second moment equals c_Π T + O(T^{1-δ}).
""")
        _write(os.path.join(tmpdir, "dependencies.yaml"),
               "deps:\n  - name: test\n")
        _write(os.path.join(tmpdir, "limitations.md"),
               "# Limits\nSome.\n")
        _write(os.path.join(tmpdir, "novelty.md"),
               "# Novelty\nSome.\n")
        _write(os.path.join(tmpdir, "checker", "README.md"),
               "# Checker\nSome.\n")

        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"
        assert "forbidden" in output.lower() or "main" in output.lower()


def test_fail_on_missing_afe():
    """Missing AFE should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _write(os.path.join(tmpdir, "statement.md"),
               "# Statement\n[OBL] Some.\n")
        _write(os.path.join(tmpdir, "proof.md"), """# Proof
The diagonal gives T log T. Off-diagonal shifted convolution.
""")
        _write(os.path.join(tmpdir, "dependencies.yaml"),
               "deps:\n  - name: test\n")
        _write(os.path.join(tmpdir, "limitations.md"),
               "# Limits\nSome.\n")
        _write(os.path.join(tmpdir, "novelty.md"),
               "# Novelty\nSome.\n")
        _write(os.path.join(tmpdir, "checker", "README.md"),
               "# Checker\nSome.\n")

        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"
        assert "afe" in output.lower()


def test_no_false_positive_trivial():
    """Trivial content should not pass."""
    with tempfile.TemporaryDirectory() as tmpdir:
        content = "[OBL] 0 normalization factors\n"
        for f in ["statement.md", "proof.md", "dependencies.yaml",
                   "limitations.md", "novelty.md", "checker/README.md"]:
            _write(os.path.join(tmpdir, f), content)

        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL on trivial content but got PASS"
