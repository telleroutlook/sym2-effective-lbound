#!/usr/bin/env python3
"""
test_checker.py — Tests for F-2 structural checker.

Verifies that the checker correctly identifies:
- PASS for well-structured submissions
- FAIL for submissions with missing concepts
- FAIL for submissions that promote to [THM] without [OBL]
"""
import subprocess
import tempfile
import os
import shutil


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


def test_pass_on_well_structured_submission():
    """A well-structured submission should PASS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write all required files with correct content
        _write(os.path.join(tmpdir, "statement.md"), """# F-2A Statement
[OBL] This is the desired statement for diagonal global residue positivity.
""")
        _write(os.path.join(tmpdir, "proof-F-2A.md"), """# F-2A Proof
The diagonal global residue is positive by norm-square positivity.
Jacquet–Shalika 1981 Lemma 4.4 and 4.6(i) give the result.
""")
        _write(os.path.join(tmpdir, "proof-F-2B.md"), """# F-2B Proof
The Euler factor extraction involves archimedean and ramified factors.
""")
        _write(os.path.join(tmpdir, "proof-F-2C.md"), """# F-2C Proof
The uniformity of local factors for level ≤ N₀ gives explicit control.
""")
        _write(os.path.join(tmpdir, "proof.md"), """# F-2 Proof
Combined proof of F-2A, F-2B, F-2C.
""")
        _write(os.path.join(tmpdir, "dependencies.yaml"), """F-2A:
  status: "[OBL]"
""")
        _write(os.path.join(tmpdir, "limitations.md"), "# Limitations\n[OBL] Some limitations.\n")
        _write(os.path.join(tmpdir, "novelty.md"), "# Novelty\n[OBL] Some novelty.\n")
        _write(os.path.join(tmpdir, "checker", "README.md"), "# Checker\n[OBL] Some notes.\n")

        code, output = _run_checker(tmpdir)
        assert code == 0, f"Expected PASS but got FAIL:\n{output}"
        assert "PASS" in output


def test_fail_on_missing_F2A_concepts():
    """Submission missing F-2A concepts should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _write(os.path.join(tmpdir, "statement.md"), "# Statement\n[OBL] Some statement.\n")
        _write(os.path.join(tmpdir, "proof-F-2A.md"), "# F-2A Proof\nSome wrong content.\n")
        _write(os.path.join(tmpdir, "proof-F-2B.md"), "# F-2B Proof\nEuler factor archimedean ramified.\n")
        _write(os.path.join(tmpdir, "proof-F-2C.md"), "# F-2C Proof\nUniformity local explicit.\n")
        _write(os.path.join(tmpdir, "proof.md"), "# Proof\nSome content.\n")
        _write(os.path.join(tmpdir, "dependencies.yaml"), "# Deps\nSome content.\n")
        _write(os.path.join(tmpdir, "limitations.md"), "# Limits\nSome content.\n")
        _write(os.path.join(tmpdir, "novelty.md"), "# Novelty\nSome content.\n")
        _write(os.path.join(tmpdir, "checker", "README.md"), "# Checker\nSome content.\n")

        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"
        assert "diagonal" in output.lower() or "F-2A" in output


def test_fail_on_THM_without_OBL():
    """Submission promoting to [THM] without [OBL] should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _write(os.path.join(tmpdir, "statement.md"), "# Statement\n[THM] This is proved.\n")
        _write(os.path.join(tmpdir, "proof-F-2A.md"), "# F-2A\nDiagonal norm-square jacquet–shalika.\n")
        _write(os.path.join(tmpdir, "proof-F-2B.md"), "# F-2B\nEuler factor archimedean ramified.\n")
        _write(os.path.join(tmpdir, "proof-F-2C.md"), "# F-2C\nUniformity local explicit.\n")
        _write(os.path.join(tmpdir, "proof.md"), "# Proof\nSome content.\n")
        _write(os.path.join(tmpdir, "dependencies.yaml"), "# Deps\nSome content.\n")
        _write(os.path.join(tmpdir, "limitations.md"), "# Limits\nSome content.\n")
        _write(os.path.join(tmpdir, "novelty.md"), "# Novelty\nSome content.\n")
        _write(os.path.join(tmpdir, "checker", "README.md"), "# Checker\nSome content.\n")

        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"
        assert "THM" in output and "OBL" in output


def test_no_false_positive_on_trivial_content():
    """Trivial content like '[OBL] 0 normalization factors' should NOT pass all checks."""
    with tempfile.TemporaryDirectory() as tmpdir:
        content = "[OBL] 0 normalization factors\n"
        _write(os.path.join(tmpdir, "statement.md"), content)
        _write(os.path.join(tmpdir, "proof-F-2A.md"), content)
        _write(os.path.join(tmpdir, "proof-F-2B.md"), content)
        _write(os.path.join(tmpdir, "proof-F-2C.md"), content)
        _write(os.path.join(tmpdir, "proof.md"), content)
        _write(os.path.join(tmpdir, "dependencies.yaml"), content)
        _write(os.path.join(tmpdir, "limitations.md"), content)
        _write(os.path.join(tmpdir, "novelty.md"), content)
        _write(os.path.join(tmpdir, "checker", "README.md"), content)

        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL on trivial content but got PASS:\n{output}"
