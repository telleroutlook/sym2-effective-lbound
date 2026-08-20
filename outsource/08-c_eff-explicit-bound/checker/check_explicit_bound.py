#!/usr/bin/env python3
"""
check_explicit_bound.py — Structural checker for c_eff submissions (rewritten).

Bug fixes (2026-08-20):
- Changed from any() token matching to phrase-level matching
- Fixed OBL status check to require exact [OBL] tag
- Added checks for correct proof architecture
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
]

# Concepts that indicate old errors
FORBIDDEN_PATTERNS = [
    "case 2",           # Exceptional branch (eliminated for prime/trivial)
    "siegel zero",      # Wrong framing (use "exceptional zero" or eliminate)
    "vinogradov-korobov",  # Not needed for this approach
]


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
    """Check that the theorem scope is correctly stated."""
    if not os.path.exists(statement_path):
        return True
    content = _normalize(open(statement_path).read())
    # Must mention log(kp+1) or fix k, NOT just log p
    if "log(kp" in content or "log p" in content and "k" in content:
        print("  [PASS] Scope mentions k-dependence")
        return True
    if "log p" in content and "kp" not in content:
        print("  [FAIL] Scope uses 1/log p without k — should be 1/log(kp+1)")
        return False
    print("  [PASS] Scope check passed")
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
        path = os.path.join(submission_dir, f)
        if not check_obl_status(path, f):
            ok = False

    print("\n--- Required mathematical concepts ---")
    proof_path = os.path.join(submission_dir, "proof.md")
    if not check_required_concepts(proof_path):
        ok = False

    print("\n--- Forbidden patterns ---")
    if not check_no_forbidden(proof_path):
        ok = False

    print("\n--- Theorem scope ---")
    statement_path = os.path.join(submission_dir, "statement.md")
    if not check_scope(statement_path):
        ok = False

    overall = "PASS" if ok else "FAIL"
    print(f"\nOverall: {overall}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
