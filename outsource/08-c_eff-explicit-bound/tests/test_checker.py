#!/usr/bin/env python3
"""
test_checker.py — Tests for c_eff structural checker (v2).
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


def _base_files(tmpdir, statement_content, proof_content, deps_content=None):
    """Write all required files."""
    _write(os.path.join(tmpdir, "statement.md"), statement_content)
    _write(os.path.join(tmpdir, "proof.md"), proof_content)
    if deps_content is None:
        deps_content = (
            "# Dependencies\n"
            "dependencies:\n"
            "  - id: HL-1994\n"
            "    source: Hoffstein-Lockhart (1994)\n"
            "    status: '[THM]'\n"
        )
    _write(os.path.join(tmpdir, "dependencies.yaml"), deps_content)
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
            "# Statement\n[OBL] L(1, sym² f) ≥ c₀/log(kp+1).\n",
            """# Proof
## Stage A — Normalization
Λ(s, F) = p^s L_∞(s) L(s, F) with q_ar = p².

## Stage B — GHL zero-free region
Following Hoffstein–Lockhart (1994) and Goldfeld–Hoffstein–Lieman (1994),
the auxiliary series φ(s) = ζ(s) L(s,F)³ L(s,F,V²) has double pole at s=1.
If L(β,F)=0, triple zero at β contradicts GHL zero-count lemma.
L(s,F) ≠ 0 for 1 − c₀/log(kp+1) < s < 1.

## Stage C — HL lower bound
A(s) = ζ(s) L(s,F) has residue L(1,F) at s=1.
HL Proposition 1.1 gives L(1,F) ≥ c₁/log(kp+1).

## Stage D — Numerical constants [OBL]
Explicit constant extraction and interval certification.
""")
        code, output = _run_checker(tmpdir)
        assert code == 0, f"Expected PASS but got FAIL:\n{output}"


def test_fail_on_wrong_scope():
    """1/log p without k should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir,
            "# Statement\n[OBL] L(1, sym² f) ≥ c_eff/log p for all p.\n",
            """# Proof
Auxiliary Dirichlet series. Hoffstein-Lockhart. Zero-free region.
Explicit constants. Triple zero. Double pole.
""")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"


def test_fail_on_l_half():
    """L(1/2) in statement should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir,
            "# Statement\n[OBL] L(½, sym² f) ≥ c₀/log(kp+1).\n",
            """# Proof
Hoffstein-Lockhart. Zero-free region. Auxiliary. Explicit.
Triple zero. Double pole.
""")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"
        assert "l(1/2" in output.lower() or "forbidden" in output.lower()


def test_fail_on_wrong_hl_year():
    """Hoffstein-Lockhart 1997 should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir,
            "# Statement\n[OBL] L(1, sym² f) ≥ c₀/log(kp+1).\n",
            """# Proof
Hoffstein-Lockhart. Zero-free region. Auxiliary. Explicit.
Triple zero. Double pole.
""",
            "# Dependencies\ndependencies:\n  - id: HL\n    source: Hoffstein-Lockhart (1997)\n    status: '[THM]'\n")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"
        assert "1994" in output or "year" in output.lower()


def test_fail_on_cubic_conductor():
    """Analytic conductor k³ should FAIL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _base_files(tmpdir,
            "# Statement\n[OBL] L(1, sym² f) ≥ c₀/log(kp+1).\nq_an ≈ p²k³\n",
            """# Proof
Hoffstein-Lockhart. Zero-free region. Auxiliary. Explicit.
Triple zero. Double pole.
""")
        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL but got PASS:\n{output}"
        assert "k³" in output or "k^3" in output or "conductor" in output.lower()


def test_no_false_positive_trivial():
    """Trivial content should not pass."""
    with tempfile.TemporaryDirectory() as tmpdir:
        content = "[OBL] 0 normalization factors\n"
        for f in ["statement.md", "proof.md", "dependencies.yaml",
                   "limitations.md", "novelty.md", "checker/README.md"]:
            _write(os.path.join(tmpdir, f), content)

        code, output = _run_checker(tmpdir)
        assert code == 1, f"Expected FAIL on trivial content but got PASS"
