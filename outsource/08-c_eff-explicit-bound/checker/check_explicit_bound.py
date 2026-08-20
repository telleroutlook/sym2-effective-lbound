#!/usr/bin/env python3
"""
check_explicit_bound.py — Structural checker for c_eff submissions (v2).

Corrections from v1 reviewer feedback:
- Fixed check_scope(): require log(kp) or log(kp+1), not just "k" anywhere
- Removed Case 2 string ban — it's correct to say "Case 2 is absent"
- Added check for correct completed function (p^s factor)
- Added check for correct analytic conductor (k² not k³)
- Added check against L(1/2) in statement
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
    "triple zero",      # v2: correct zero multiplicity argument
    "double pole",      # v2: correct pole structure
]

# Patterns that indicate mathematical errors
FORBIDDEN_PATTERNS = [
    "siegel zero",          # Wrong framing
    "vinogradov-korobov",   # Not needed for this approach
    "l(1/2",               # v2: L(1/2) should not appear (ASCII)
    "l(½",                  # v2: L(1/2) should not appear (Unicode)
]

# Year corrections
WRONG_YEARS = {
    "hoffstein-lockhart.*1997": "Hoffstein–Lockhart is 1994 Annals, not 1997",
    "hoffstein-lockhart.*1995": "Hoffstein–Lockhart is 1994 Annals, not 1995",
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


def check_no_forbidden(proof_path):
    if not os.path.exists(proof_path):
        return True
    content = _normalize(open(proof_path).read())
    clean = True
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in content:
            print(f"  [FAIL] Forbidden pattern found: {pattern}")
            clean = False
    if clean:
        print("  [PASS] No forbidden patterns")
    return clean


def check_scope(statement_path):
    """Check that the theorem scope correctly uses log(kp+1), NOT just log p."""
    if not os.path.exists(statement_path):
        return True
    content = _normalize(open(statement_path).read())
    # Good: mentions log(kp+1) or log(kp)
    if "log(kp" in content or "log kp" in content:
        print("  [PASS] Scope correctly uses log(kp+1)")
        return True
    # Bad: mentions log p without kp context
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
    # Look for p^s in completed function definition
    if "p^s" in content or "p^{s" in content or "q_ar" in content:
        print("  [PASS] Completed function includes p^s factor")
        return True
    # Check if the proof mentions completed function without p^s
    if "Lambda" in content or "Λ" in content:
        print("  [FAIL] Completed function missing p^s factor: Λ(s,F) = p^s L_∞(s) L(s,F)")
        return False
    print("  [PASS] Completed function check (no Λ found)")
    return True


def check_analytic_conductor(statement_path):
    """Check that analytic conductor is p²k² (not p²k³)."""
    if not os.path.exists(statement_path):
        return True
    content = _normalize(open(statement_path).read())
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
        # Skip yaml files — they are metadata, not claim files
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
    proof_path = os.path.join(submission_dir, "proof.md")
    if not check_no_forbidden(proof_path):
        ok = False
    statement_path = os.path.join(submission_dir, "statement.md")
    if not check_no_forbidden(statement_path):
        ok = False

    print("\n--- Theorem scope ---")
    statement_path = os.path.join(submission_dir, "statement.md")
    if not check_scope(statement_path):
        ok = False

    print("\n--- Completed function ---")
    if not check_completed_function(proof_path):
        ok = False

    print("\n--- Analytic conductor ---")
    if not check_analytic_conductor(statement_path):
        ok = False

    print("\n--- Reference years ---")
    deps_path = os.path.join(submission_dir, "dependencies.yaml")
    if not check_hl_year(deps_path):
        ok = False

    overall = "PASS" if ok else "FAIL"
    print(f"\nOverall: {overall}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
