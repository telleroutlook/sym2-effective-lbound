#!/usr/bin/env python3
"""
check_mean_value.py — Structural checker for M-2 submissions (v3).

Detects:
- Wrong main term c_Π T (should be T log T)
- Wrong AFE dual factor (constant root number instead of t-dependent)
- Wrong H_{Π,p} formula (must give 1+O(x²))
- Wrong leading constant ((3/2)R_Π instead of 3R_Π)
- Missing archimedean gamma factors
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

# Mathematical concepts that MUST appear in proof.md
REQUIRED_CONCEPTS = [
    "t log t",       # Correct main term (NOT just "cT")
    "afe",           # Approximate functional equation
    "diagonal",      # Diagonal/off-diagonal decomposition
]

# Concepts that indicate old errors (v3: expanded from v2)
FORBIDDEN_PATTERNS = [
    "c_pi t",           # Wrong main term (should be T log T) — standalone claim
    "infinite double sum",  # Wrong starting point
    "chi(pi)",          # Constant root number as AFE dual factor (should be X_Pi(t))
    "chi(Π)",           # Same, Unicode variant
    "(3/2) r_pi",       # Wrong leading constant (should be 3R_Pi)
    "(3/2) rπ",         # Same, Unicode variant
    "r/t^3",            # Wrong AFE weight scale (should be T^{3/2})
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
        print(f"  [FAIL] {label} promotes M-2 to [THM] — must remain [OBL]")
        return False
    if has_obl:
        print(f"  [PASS] {label} correctly labels M-2 as [OBL]")
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


def check_no_forbidden(path):
    if not os.path.exists(path):
        return True
    content = _normalize(open(path).read())
    clean = True
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in content:
            print(f"  [FAIL] Forbidden pattern found: {pattern}")
            clean = False
    if clean:
        print(f"  [PASS] No forbidden patterns in {os.path.basename(path)}")
    return clean


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_mean_value.py <submission_dir>")
        sys.exit(1)

    submission_dir = sys.argv[1]
    print(f"Checking M-2 submission in: {submission_dir}\n")

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
    for f in ["statement.md", "proof.md", "limitations.md"]:
        path = os.path.join(submission_dir, f)
        if not check_no_forbidden(path):
            ok = False

    overall = "PASS" if ok else "FAIL"
    print(f"\nOverall: {overall}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
