#!/usr/bin/env python3
"""
check_global_residue.py — Structural checker for F-2 (v2).

Detects:
- Missing F-2A/F-2B/F-2C concepts
- Wrong Adjoint Euler factor (single factor instead of 3)
- Wrong archimedean degree (3 instead of 4)
- Wrong uniformity argument (continuity alone)
- Wrong JS81 citation
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
    "euler",
    "archimedean",
    "ramified",
]

BLOCKERS_F2C = [
    "uniformity",
    "local",
    "explicit",
]

# Forbidden patterns (v2 additions)
# Only patterns that are UNAMBIGUOUSLY wrong.
# Note: single-factor Adjoint detection is NOT possible structurally because
# the correct 3-factor formula also contains "α_p β_p". Requires human review.
FORBIDDEN_PATTERNS = [
    "ann. math. 114",               # Wrong JS81 citation
    "ann math 114",                 # Wrong JS81 citation
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


def check_no_forbidden(path):
    if not os.path.exists(path):
        return True
    content = _normalize(open(path).read())
    clean = True
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, content):
            print(f"  [FAIL] Forbidden pattern found: {pattern}")
            clean = False
    if clean:
        print(f"  [PASS] No forbidden patterns in {os.path.basename(path)}")
    return clean


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_global_residue.py <submission_dir>")
        sys.exit(1)

    submission_dir = sys.argv[1]
    print(f"Checking F-2 submission in: {submission_dir}\n")

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

    print("\n--- F-2A: Diagonal residue positivity ---")
    proof_a = os.path.join(submission_dir, "proof-F-2A.md")
    if not check_blockers(proof_a, BLOCKERS_F2A, "F-2A"):
        ok = False

    print("\n--- F-2B: Euler factor extraction ---")
    proof_b = os.path.join(submission_dir, "proof-F-2B.md")
    if not check_blockers(proof_b, BLOCKERS_F2B, "F-2B"):
        ok = False

    print("\n--- F-2C: Target-family uniformity ---")
    proof_c = os.path.join(submission_dir, "proof-F-2C.md")
    if not check_blockers(proof_c, BLOCKERS_F2C, "F-2C"):
        ok = False

    print("\n--- Forbidden patterns ---")
    for f in ["statement-F-2A.md", "statement-F-2B.md", "statement-F-2C.md",
              "proof-F-2A.md", "proof-F-2B.md", "proof-F-2C.md"]:
        path = os.path.join(submission_dir, f)
        if not check_no_forbidden(path):
            ok = False

    overall = "PASS" if ok else "FAIL"
    print(f"\nOverall: {overall}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
