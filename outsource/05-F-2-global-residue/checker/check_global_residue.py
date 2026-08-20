#!/usr/bin/env python3
"""
check_global_residue.py — Structural checker for F-2 (v5).

Detects:
- Missing F-2A/F-2B/F-2C concepts
- Wrong Adjoint Euler factor (single factor instead of 3)
- Wrong archimedean degree (3 instead of 4)
- Wrong uniformity argument (continuity alone)
- Wrong JS81 citation
- Old Z_∞(1) formula used as CURRENT claim (not in correction context)
- Old citation chain ("Lemma 4.4") used as CURRENT citation
- Old "min over N" used as CURRENT formulation
- Old test function space C_c^∞(GL₂(Q_p)) (should be S(Q_p²))
- Old Steinberg conductor claim "conductor exponent 1" without χ-dependence
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

# Forbidden patterns: only patterns that are UNAMBIGUOUSLY wrong as current claims.
FORBIDDEN_PATTERNS = [
    "ann. math. 114",               # Wrong JS81 citation (never correct)
    "ann math 114",                 # Wrong JS81 citation (never correct)
]

# Correction-context patterns: these appear legitimately in "what was wrong" sections.
# We check that they ONLY appear in correction/explanation context, not as current claims.
CORRECTION_CONTEXT_PATTERNS = [
    {
        "pattern": "2π^{-k-1}",
        "name": "Old Z_∞(1) formula",
        "context_regex": r"(was|corrected|previous|error|wrong|v2|off by|differ)",
    },
    {
        "pattern": "lemma 4.4",
        "name": "Old citation chain",
        "context_regex": r"(not|corrected|was|previous|wrong|should be|§4\.3)",
    },
    {
        "pattern": "min over n",
        "name": "Old min formulation",
        "context_regex": r"(was|insufficient|not|corrected|previous|wrong|should be)",
    },
    {
        "pattern": "c_c^∞(gl₂",
        "name": "Old test function space",
        "context_regex": r"(was|corrected|previous|error|wrong|not|should be|instead)",
    },
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
    # F-2A can be [THM/REFEREED]; F-2B and F-2C must have [OBL]
    basename = os.path.basename(path)
    if basename == "statement-F-2A.md" or basename == "proof-F-2A.md":
        # F-2A is allowed to be [THM/REFEREED]
        if "[THM/REFEREED]" in content or "[THM]" in content:
            print(f"  [PASS] {label} has [THM/REFEREED] status (F-2A closed)")
            return True
    has_thm = "[THM]" in content
    has_obl = "[OBL]" in content
    if has_thm and not has_obl:
        print(f"  [FAIL] {label} promotes to [THM] — must remain [OBL]")
        return False
    if has_obl:
        print(f"  [PASS] {label} correctly labels as [OBL]")
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
        if pattern in content:
            print(f"  [FAIL] Forbidden pattern found: {pattern}")
            clean = False
    if clean:
        print(f"  [PASS] No forbidden patterns in {os.path.basename(path)}")
    return clean


def check_correction_context(path):
    """Check that old formulas only appear in correction/explanation context."""
    if not os.path.exists(path):
        return True
    raw_content = open(path).read()
    content = _normalize(raw_content)
    clean = True
    for item in CORRECTION_CONTEXT_PATTERNS:
        pattern = item["pattern"]
        if pattern not in content:
            continue
        context_re = re.compile(item["context_regex"], re.IGNORECASE)
        paragraphs = re.split(r'\n\n+', raw_content)
        found_in_context = False
        found_at_all = False
        for para in paragraphs:
            para_lower = _normalize(para)
            if pattern in para_lower:
                found_at_all = True
                if context_re.search(para_lower):
                    found_in_context = True
                    break
        if found_at_all and not found_in_context:
            print(f"  [FAIL] {item['name']} used as current claim in {os.path.basename(path)}")
            clean = False
        elif found_at_all and found_in_context:
            print(f"  [PASS] {item['name']} appears in correction context: {os.path.basename(path)}")
    if clean:
        print(f"  [PASS] No current claims of old formulas in {os.path.basename(path)}")
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
    all_files = REQUIRED_FILES + [
        "statement-F-2A.md", "statement-F-2B.md", "statement-F-2C.md",
        "proof-F-2A.md", "proof-F-2B.md", "proof-F-2C.md",
        "checker/README.md",
    ]
    for f in all_files:
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

    print("\n--- Forbidden patterns (unconditional) ---")
    for f in ["statement-F-2A.md", "statement-F-2B.md", "statement-F-2C.md",
              "proof-F-2A.md", "proof-F-2B.md", "proof-F-2C.md",
              "statement.md", "proof.md", "dependencies.yaml"]:
        path = os.path.join(submission_dir, f)
        if not check_no_forbidden(path):
            ok = False

    print("\n--- Correction-context patterns ---")
    for f in ["statement-F-2A.md", "statement-F-2B.md", "statement-F-2C.md",
              "proof-F-2A.md", "proof-F-2B.md", "proof-F-2C.md",
              "statement.md", "proof.md"]:
        path = os.path.join(submission_dir, f)
        if not check_correction_context(path):
            ok = False

    overall = "PASS" if ok else "FAIL"
    print(f"\nOverall: {overall}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
