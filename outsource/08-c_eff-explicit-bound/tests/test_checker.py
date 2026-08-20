#!/usr/bin/env python3
"""
test_checker.py — Tests for c_eff structural checker (rewritten).
"""
import subprocess
import tempfile
import os


CHECKER = os.path.join(os.path.dirname(__file__), "..", "checker", "check_explicit_bound.py")


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


def _base_files(tmpdir, statement_content, proof_content):
    """Write all required files."""
    _write(os.path.join(tmpdir, "statement.md"), statement_content)
    _write(os.path.join(tmpdir, "proof.md"), proof_content)
    _write(os.path.join(tmpdir, "dependencies.yaml"),
           "stages:\n  - name: test\n    status: '[OBL]'\n")
    _write(os.path.join(tmpdir, "limitations.md"),
           "# Limits\n[OBL] Some.\n")
    _write(os.path.join(tmpdir, "novelty.md"),
           "# Novelty\n[OBL] Some.\n")
    _write(os.path.join(tmpdir, "checker", "README.md"),
           "# Checker\n[OBL] Notes.\n")


def test_pass_on_well_structured():
    """Well-structured submission with correct architecture should PASS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir,
            "# Statement\n[OBL] L(1, sym² f) ≥ c_*/log(kp+1).\n",
            """# Proof
The Hoffstein–Lockhart auxiliary Dirichlet series Φ(s) = ζ(s)L(s,Π)²L(s,Π×Π̃)
has non-negative coefficients. For prime level + trivial character, the
GL(1)-lift obstruction does not arise. The zero-free region gives
L(1,Π) ≥ c₁/log(kp+1). Explicit constant extraction and interval
certification follow.
""")
        code, output = _run_checker(tmpdir)
        assert code == 0, f"Expected PASS but got FAIL:\n{output}"


def test_fail_on_wrong_scope():
    """1/log p without k should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir,
            "# Statement\n[OBL] L(1, sym² f) ≥ c_eff/log p for all p.\n",
            """# Proof
Auxiliary Dirichlet series. Hoffstein–Lockhart. Zero-free region.
Explicit constants.
""")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"


def test_fail_on_case2():
    """Case 2 (exceptional branch) should FAIL for prime/trivial."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir,
            "# Statement\n[OBL] L(1, sym² f) ≥ c_*/log(kp+1).\n",
            """# Proof
Case 1: no exceptional zero. Case 2: exceptional zero β > 1 - c₀/log p.
Hadamard factorization.
""")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"
        assert "forbidden" in output.lower() or "case 2" in output.lower()


def test_no_false_positive_trivial():
    """Trivial content should not pass."""
    with tempfile.TemporaryDirectory() as tmpdir:
        content = "[OBL] 0 normalization factors\n"
        for f in ["statement.md", "proof.md", "dependencies.yaml",
                   "limitations.md", "novelty.md", "checker/README.md"]:
            _write(os.path.join(tmpdir, f), content)

        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL on trivial content but got PASS"
