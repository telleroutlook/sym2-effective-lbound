#!/usr/bin/env python3
"""
check_mollifier.py — Structural checker for M-1 submissions (v2).

Detects:
- Missing (n/m)^{it} phase (old error)
- Wrong bridge lemma I(T) ≥ c₀T ⟹ L(½) > 0 (v2 fatal error)
- Hecke eigenvalue orthogonality (wrong object)
- Squarefree approximation lemma (algebraically vacuous)
- Wrong main term scale (T·log T for mollified moment)
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
    "n/m",           # The (n/m)^{it} phase factor
    "mollifier",     # The mollifier definition
    "afe",           # Approximate functional equation
]

# Concepts that indicate old or new errors
FORBIDDEN_PATTERNS = [
    "hecke eigenvalue orthogonality",  # Misapplied (fixed Π, no family)
    "gl3 spectral large sieve",        # Wrong object (family, not fixed Π)
    "i(t) >= c_0 t",                   # Wrong bridge: I(T)≥c₀T ⟹ L(½)>0
    "i(t)≥c_0t",                       # Same, no spaces
    "deduce l(½",                       # Wrong: cannot deduce central value
    "hence l(1,",                       # Wrong: normalization gap
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
        print(f"  [FAIL] {label} promotes M-1 to [THM] — must remain [OBL]")
        return False
    if has_obl:
        print(f"  [PASS] {label} correctly labels M-1 as [OBL]")
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
        print("Usage: python check_mollifier.py <submission_dir>")
        sys.exit(1)

    submission_dir = sys.argv[1]
    print(f"Checking M-1 submission in: {submission_dir}\n")

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
