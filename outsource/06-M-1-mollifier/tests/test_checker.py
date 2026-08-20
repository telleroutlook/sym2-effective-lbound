#!/usr/bin/env python3
"""
test_checker.py — Tests for M-1 structural checker (rewritten).
"""
import subprocess
import tempfile
import os


CHECKER = os.path.join(os.path.dirname(__file__), "..", "checker", "check_mollifier.py")


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
               "# M-1 Statement\n[OBL] Mollified moment I(T) ≥ c₀T.\n")
        _write(os.path.join(tmpdir, "proof.md"), """# M-1 Proof
The mollified moment identity with mollifier M(s) is:
I(T) = Σ_{m,n} (b_m b̄_n / √(mn)) J_{m,n}(T)
where J_{m,n}(T) = ∫_T^{2T} (n/m)^{it} |L(½+it,Π)|² dt.
Diagonal terms give the main term. Off-diagonal shifted convolution
is bounded using the AFE with length T^{3/2}.
""")
        _write(os.path.join(tmpdir, "dependencies.yaml"),
               "assumptions:\n  - id: NON-CM\n    status: '[OBL]'\n")
        _write(os.path.join(tmpdir, "limitations.md"),
               "# Limits\n[OBL] Some limits.\n")
        _write(os.path.join(tmpdir, "novelty.md"),
               "# Novelty\n[OBL] Some novelty.\n")
        _write(os.path.join(tmpdir, "checker", "README.md"),
               "# Checker\n[OBL] Notes.\n")

        code, output = _run_checker(tmpdir)
        assert code == 0, f"Expected PASS but got FAIL:\n{output}"


def test_fail_on_missing_phase():
    """Missing (n/m)^{it} phase should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _write(os.path.join(tmpdir, "statement.md"),
               "# M-1 Statement\n[OBL] Some statement.\n")
        # Proof without the (n/m)^{it} phase — the old error
        _write(os.path.join(tmpdir, "proof.md"), """# M-1 Proof
The mollified moment is:
I(T) = (∑ b_m m^{-1/2}) ∫_T^{2T} |L(½+it,Π)|² dt
This factorizes into mollifier sum times the second moment.
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
        assert "n/m" in output.lower()


def test_fail_on_forbidden_pattern():
    """Hecke eigenvalue orthogonality should FAIL (wrong object)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _write(os.path.join(tmpdir, "statement.md"),
               "# Statement\n[OBL] Some.\n")
        _write(os.path.join(tmpdir, "proof.md"), """# Proof
The off-diagonal terms vanish by Hecke eigenvalue orthogonality
over the family of forms.
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
        assert "forbidden" in output.lower()


def test_no_false_positive_trivial():
    """Trivial content should not pass."""
    with tempfile.TemporaryDirectory() as tmpdir:
        content = "[OBL] 0 normalization factors\n"
        for f in ["statement.md", "proof.md", "dependencies.yaml",
                   "limitations.md", "novelty.md", "checker/README.md"]:
            _write(os.path.join(tmpdir, f), content)

        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL on trivial content but got PASS"
