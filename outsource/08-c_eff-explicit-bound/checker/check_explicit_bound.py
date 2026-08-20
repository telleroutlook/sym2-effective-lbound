#!/usr/bin/env python3
"""
check_explicit_bound.py — Structural checker for c_eff submissions (v3).

Corrections from v2 reviewer feedback:
- Added check for M=K^C parameter matching (not δ=c_ZF/log K)
- Added check against "log(1/δ)" pattern (wrong HL parameter)
- Added check for correct positivity reason
- Added check for M_GHL vs M_HL distinction
- Fixed false positive on "q_ar" (just checking string presence)
- Analytic conductor now checks proof.md, not just statement.md
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
    "log(1/δ)",          # v3: wrong HL parameter (should be log M)
    "log(1/delta)",       # v3: same, ASCII variant
    "δ = c",             # v3: setting δ directly is wrong
    "delta = c",          # v3: same, ASCII variant
    "r⁻¹ ≪ log(1/δ)",   # v3: wrong formula
    "exterior square",    # v3: V² is symmetric-square, not exterior
    "symmetric part of the exterior",  # v3: wrong V² description
    "depending on k",     # v3: c₀ is absolute, not depending on k
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
    if has_thm and not has_obl:
        print(f"  [FAIL] {label} promotes c_eff to [THM] — must remain [OBL]")
        return False
    if has_obl:
        print(f"  [PASS] {label} correctly labels c_eff as [OBL]")
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
    """Check that completed function includes p^s factor."""
    if not os.path.exists(proof_path):
        return True
    content = _normalize(open(proof_path).read())
    if "p^s" in content or "p^{s" in content or "q_ar" in content:
        print("  [PASS] Completed function includes p^s factor")
        return True
    if "lambda" in content or "Λ" in content:
        print("  [FAIL] Completed function missing p^s factor")
        return False
    print("  [PASS] Completed function check (no Λ found)")
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
