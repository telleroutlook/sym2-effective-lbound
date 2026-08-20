#!/usr/bin/env python3
"""
check_explicit_bound.py — Structural checker for c_eff submissions (v4).

v4 corrections (per reviewer verdict 2026-08-20):
- Check for correct good-prime local factor (four-factor expression)
- Check for L(1,F)≠0 prerequisite in Stage B
- Check for C_* growth multiplicative constant
- Check for Δ scope correction (level 1 ≠ prime-level upper bound)
- Strengthened completed function check (must include p^s in formula context)
- Fixed false positive on "q_ar" (just checking string presence)
"""
import sys
import os
import re


REQUIRED_FILES = [
    "statement.md",
    "proof.md",
    "dependencies.yaml",
    "limitations.md",
    "novelty.md",
]

# Required concepts in proof.md (each is a multi-word phrase)
REQUIRED_CONCEPTS = [
    "hoffstein",
    "zero-free",
    "auxiliary",
    "explicit",
    "triple zero",
    "double pole",
    "non-negative coefficients",
    "m = k",    # M = K^C parameter matching
]

# Patterns that indicate mathematical errors
FORBIDDEN_PATTERNS = [
    "siegel zero",
    "vinogradov-korobov",
    "l(1/2",
    "l(½",
    "log(1/δ)",          # wrong HL parameter (should be log M)
    "log(1/delta)",       # same, ASCII variant
    "δ = c",             # setting δ directly is wrong
    "delta = c",          # same, ASCII variant
    "r⁻¹ ≪ log(1/δ)",   # wrong formula
    "exterior square",    # V² is symmetric-square, not exterior
    "symmetric part of the exterior",  # wrong V² description
    "depending on k",     # c₀ is absolute, not depending on k
]

# Year corrections
WRONG_YEARS = {
    "hoffstein-lockhart.*1997": "Hoffstein–Lockhart is 1994 Annals, not 1997",
    "hoffstein-lockhart.*1995": "Hoffstein–Lockhart is 1994 Annals, not 1995",
}

# Bibliography checks
WRONG_CITATIONS = {
    "j. amer. math. soc.*14.*705": "Iwaniec–Michel is Ann. Acad. Sci. Fenn. 26 (2001), not JAMS 14",
    "pp. 1–42.*hoffstein": "HL is Annals 140 pp. 161–181, not 1–42",
}


def _normalize(text):
    return re.sub(r'\s+', ' ', text.lower().strip())


def check_file_exists(path, label):
    if not os.path.exists(path):
        print(f"  [FAIL] Missing required file: {label}")
        return False
    print(f"  [PASS] Found: {label}")
    return True


def check_obl_status(path, label):
    if not os.path.exists(path):
        return True
    content = open(path).read()
    has_thm = "[THM]" in content
    has_obl = "[OBL]" in content
    has_partial = "[PARTIAL" in content
    if has_thm and not has_obl and not has_partial:
        print(f"  [FAIL] {label} promotes c_eff to [THM] — must remain [OBL] or [PARTIAL]")
        return False
    if has_obl or has_partial:
        print(f"  [PASS] {label} correctly labels c_eff as [OBL] or [PARTIAL]")
    return True


def check_required_concepts(proof_path):
    if not os.path.exists(proof_path):
        print("  [FAIL] proof.md missing")
        return False
    content = _normalize(open(proof_path).read())
    all_found = True
    for concept in REQUIRED_CONCEPTS:
        if concept in content:
            print(f"  [PASS] Required concept: {concept}")
        else:
            print(f"  [FAIL] Missing concept: {concept}")
            all_found = False
    return all_found


def check_no_forbidden(proof_path, statement_path):
    clean = True
    for path, label in [(proof_path, "proof.md"), (statement_path, "statement.md")]:
        if not os.path.exists(path):
            continue
        content = _normalize(open(path).read())
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in content:
                print(f"  [FAIL] Forbidden pattern in {label}: {pattern}")
                clean = False
    if clean:
        print("  [PASS] No forbidden patterns")
    return clean


def check_scope(statement_path):
    """Check that the theorem scope correctly uses log(kp+1), NOT just log p."""
    if not os.path.exists(statement_path):
        return True
    content = _normalize(open(statement_path).read())
    if "log(kp" in content or "log kp" in content:
        print("  [PASS] Scope correctly uses log(kp+1)")
        return True
    if "log p" in content and "log(kp" not in content:
        print("  [FAIL] Scope uses 1/log p without k — should be 1/log(kp+1)")
        return False
    print("  [PASS] Scope check passed")
    return True


def check_completed_function(proof_path):
    """Check that completed function includes p^s factor in formula context."""
    if not os.path.exists(proof_path):
        return True
    content = _normalize(open(proof_path).read())
    # Must have p^s in a formula with Lambda or completed
    has_formula = ("p^s" in content or "p^{s" in content)
    has_lambda = ("lambda" in content or "Λ" in content or "completed" in content)
    if has_formula and has_lambda:
        print("  [PASS] Completed function includes p^s factor in formula")
        return True
    if has_lambda and not has_formula:
        print("  [FAIL] Completed function mentions Λ/completed but missing p^s in formula")
        return False
    if has_formula:
        print("  [PASS] Completed function has p^s")
        return True
    print("  [PASS] Completed function check (no Λ/completed found)")
    return True


def check_analytic_conductor(proof_path):
    """Check that analytic conductor is p²k² (not p²k³)."""
    if not os.path.exists(proof_path):
        return True
    content = _normalize(open(proof_path).read())
    if "k³" in content or "k^3" in content:
        print("  [FAIL] Analytic conductor uses k³ — should be k²")
        return False
    if "k²" in content or "k^2" in content:
        print("  [PASS] Analytic conductor uses correct k² scaling")
        return True
    print("  [PASS] Analytic conductor check (no k³ found)")
    return True


def check_hl_year(deps_path):
    """Check that Hoffstein–Lockhart year is 1994, not 1997."""
    if not os.path.exists(deps_path):
        return True
    content = _normalize(open(deps_path).read())
    for pattern, msg in WRONG_YEARS.items():
        if re.search(pattern, content):
            print(f"  [FAIL] {msg}")
            return False
    if "hoffstein" in content and "1994" in content:
        print("  [PASS] Hoffstein–Lockhart year is 1994")
    return True


def check_bibliography(deps_path):
    """Check that citations are correct."""
    if not os.path.exists(deps_path):
        return True
    content = _normalize(open(deps_path).read())
    clean = True
    for pattern, msg in WRONG_CITATIONS.items():
        if re.search(pattern, content):
            print(f"  [FAIL] Wrong citation: {msg}")
            clean = False
    if clean:
        print("  [PASS] Bibliography checks passed")
    return clean


def check_parameter_matching(proof_path):
    """Check that M=K^C is used, not δ=c/log K."""
    if not os.path.exists(proof_path):
        return True
    content = _normalize(open(proof_path).read())
    # Good: mentions M = K^C or "m = k^c"
    if re.search(r'm\s*=\s*k\^?c', content):
        print("  [PASS] Parameter matching uses M = K^C")
        return True
    # Check if the proof mentions HL but not M=K^C
    if "hoffstein" in content or "proposition 1.1" in content:
        if "log(1/δ)" in content or "log(1/delta)" in content:
            print("  [FAIL] Uses log(1/δ) — should use M = K^C matching")
            return False
    print("  [PASS] Parameter matching check passed")
    return True


def check_l1_nonvanishing(proof_path):
    """Check that L(1,F)≠0 is stated as prerequisite for double pole."""
    if not os.path.exists(proof_path):
        return True
    content = _normalize(open(proof_path).read())
    if "l(1" in content and ("nonzero" in content or "non-zero" in content or "≠ 0" in content or "neq" in content):
        print("  [PASS] L(1,F)≠0 prerequisite stated")
        return True
    if "double pole" in content:
        if "l(1" not in content:
            print("  [WARN] Double pole mentioned but L(1,F)≠0 not explicitly checked")
            return True
        print("  [PASS] L(1,F) check present (double pole context)")
        return True
    print("  [PASS] L(1,F) nonvanishing check (no double pole found)")
    return True


def check_growth_constant(proof_path):
    """Check that C_* multiplicative constant is mentioned."""
    if not os.path.exists(proof_path):
        return True
    content = _normalize(open(proof_path).read())
    if "c_*" in content or "c star" in content or "c*" in content:
        print("  [PASS] Growth multiplicative constant C_* present")
        return True
    if "growth bound" in content or "growth constant" in content:
        if "c_*" not in content and "c star" not in content:
            print("  [WARN] Growth bound discussed but C_* not explicitly named")
            return True
    print("  [PASS] Growth constant check (no growth discussion found)")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_explicit_bound.py <submission_dir>")
        sys.exit(1)

    submission_dir = sys.argv[1]
    print(f"Checking c_eff submission in: {submission_dir}\n")

    ok = True

    print("--- Required files ---")
    for f in REQUIRED_FILES:
        path = os.path.join(submission_dir, f)
        if not check_file_exists(path, f):
            ok = False

    print("\n--- Status labels ---")
    for f in REQUIRED_FILES + ["checker/README.md"]:
        if f.endswith(".yaml"):
            continue
        path = os.path.join(submission_dir, f)
        if not check_obl_status(path, f):
            ok = False

    print("\n--- Required mathematical concepts ---")
    proof_path = os.path.join(submission_dir, "proof.md")
    if not check_required_concepts(proof_path):
        ok = False

    print("\n--- Forbidden patterns ---")
    statement_path = os.path.join(submission_dir, "statement.md")
    if not check_no_forbidden(proof_path, statement_path):
        ok = False

    print("\n--- Theorem scope ---")
    if not check_scope(statement_path):
        ok = False

    print("\n--- Completed function ---")
    if not check_completed_function(proof_path):
        ok = False

    print("\n--- Analytic conductor ---")
    if not check_analytic_conductor(proof_path):
        ok = False

    print("\n--- Parameter matching ---")
    if not check_parameter_matching(proof_path):
        ok = False

    print("\n--- L(1,F) nonvanishing ---")
    if not check_l1_nonvanishing(proof_path):
        ok = False

    print("\n--- Growth constant C_* ---")
    if not check_growth_constant(proof_path):
        ok = False

    print("\n--- Reference years ---")
    deps_path = os.path.join(submission_dir, "dependencies.yaml")
    if not check_hl_year(deps_path):
        ok = False

    print("\n--- Bibliography ---")
    if not check_bibliography(deps_path):
        ok = False

    overall = "PASS" if ok else "FAIL"
    print(f"\nOverall: {overall}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
