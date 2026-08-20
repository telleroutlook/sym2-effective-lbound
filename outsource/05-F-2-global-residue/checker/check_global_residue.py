#!/usr/bin/env python3
"""
check_global_residue.py — Structural checker for F-2 restructured (F-2A/F-2B/F-2C).

Verifies that submissions address all three sub-obligations and preserve [OBL] status.
Does NOT verify mathematical proofs (human review required).

Bug fixes (2026-08-20):
- Changed blocker check from any() to phrase-level matching
- Fixed OBL status check to require exact [OBL] tag
- Added F-2A/F-2B/F-2C structure checks
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

BLOCKERS_F2A = [
    "diagonal",
    "norm-square",
    "jacquet–shalika",
]

BLOCKERS_F2B = [
    "euler factor",
    "archimedean",
    "ramified",
]

BLOCKERS_F2C = [
    "uniformity",
    "local",
    "explicit",
]


def _normalize(text):
    """Lowercase and collapse whitespace for comparison."""
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
        print(f"  [FAIL] {label} promotes F-2 to [THM] — must remain [OBL]")
        return False
    if has_obl:
        print(f"  [PASS] {label} correctly labels F-2 as [OBL]")
    return True


def check_blockers(proof_path, blockers, label):
    if not os.path.exists(proof_path):
        print(f"  [FAIL] {label} proof missing")
        return False
    content = _normalize(open(proof_path).read())
    all_found = True
    for b in blockers:
        phrase = _normalize(b)
        if phrase in content:
            print(f"  [PASS] {label} concept: {b}")
        else:
            print(f"  [FAIL] {label} concept NOT found: {b}")
            all_found = False
    return all_found


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_global_residue.py <submission_dir>")
        sys.exit(1)

    submission_dir = sys.argv[1]
    print(f"Checking F-2 restructured submission in: {submission_dir}\n")

    ok = True

    # Check required files
    print("--- Required files ---")
    for f in REQUIRED_FILES:
        path = os.path.join(submission_dir, f)
        if not check_file_exists(path, f):
            ok = False

    # Check [OBL] status preserved
    print("\n--- Status labels ---")
    for f in REQUIRED_FILES + ["checker/README.md"]:
        path = os.path.join(submission_dir, f)
        if not check_obl_status(path, f):
            ok = False

    # Check F-2A concepts
    print("\n--- F-2A: Diagonal residue positivity ---")
    proof_a = os.path.join(submission_dir, "proof-F-2A.md")
    if not check_blockers(proof_a, BLOCKERS_F2A, "F-2A"):
        ok = False

    # Check F-2B concepts
    print("\n--- F-2B: Euler factor extraction ---")
    proof_b = os.path.join(submission_dir, "proof-F-2B.md")
    if not check_blockers(proof_b, BLOCKERS_F2B, "F-2B"):
        ok = False

    # Check F-2C concepts
    print("\n--- F-2C: Target-family uniformity ---")
    proof_c = os.path.join(submission_dir, "proof-F-2C.md")
    if not check_blockers(proof_c, BLOCKERS_F2C, "F-2C"):
        ok = False

    overall = "PASS" if ok else "FAIL"
    print(f"\nOverall: {overall}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
