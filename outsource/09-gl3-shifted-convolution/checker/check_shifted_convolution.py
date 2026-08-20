#!/usr/bin/env python3
"""Checker for 09-gl3-shifted-convolution: verify mathematical and labelling correctness."""
import sys, os

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"Checking GL₃ shifted convolution submission in: {path}")
    print()
    errors = []

    # Required files
    required = ["statement.md", "proof.md", "dependencies.yaml",
                "limitations.md", "novelty.md"]
    for f in required:
        full = os.path.join(path, f)
        if os.path.exists(full):
            print(f"  [PASS] Found: {f}")
        else:
            print(f"  [FAIL] Missing: {f}")
            errors.append(f)

    # Status labels: must NOT use [THM] for the core problems
    for fname in ["statement.md", "proof.md"]:
        full = os.path.join(path, fname)
        if not os.path.exists(full):
            continue
        content = open(full).read()
        if "[THM]" in content:
            # Check if it's only citing external [THM] results, not claiming our own
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "[THM]" in line and "status:" not in line.lower():
                    print(f"  [WARN] {fname}:{i+1} contains [THM] — verify it cites external result, not our own")
        if "[OBL]" in content:
            print(f"  [PASS] {fname} correctly uses [OBL] for research problems")

    # Forbidden: C_Π(h) main term CLAIM (not negation)
    for fname in ["statement.md", "proof.md"]:
        full = os.path.join(path, fname)
        if not os.path.exists(full):
            continue
        content = open(full).read()
        lines = content.split("\n")
        for i, line in enumerate(lines):
            low = line.lower()
            if "c_Π(h)" in low and "rankin" in low:
                # Only flag if it's a positive claim, not a negation
                if "not presuppose" not in low and "not" not in low.split("rankin")[0]:
                    print(f"  [FAIL] {fname}:{i+1} claims Rankin–Selberg gives C_Π(h) — unsubstantiated for h ≠ 0")
                    errors.append(fname)

    # Forbidden: large sieve individual bound
    for fname in ["statement.md", "proof.md", "limitations.md"]:
        full = os.path.join(path, fname)
        if not os.path.exists(full):
            continue
        content = open(full).read()
        if "N^{5/6}" in content or "N^{5 / 6}" in content:
            print(f"  [FAIL] {fname} contains N^{5/6} bound — invalid for individual shifted sums")
            errors.append(fname)

    # Required: DLY averaged mechanism mentioned
    for fname in ["statement.md", "proof.md"]:
        full = os.path.join(path, fname)
        if not os.path.exists(full):
            continue
        content = open(full).read()
        if "averaged" in content.lower() and "dly" in content.lower():
            print(f"  [PASS] {fname} correctly describes DLY averaged mechanism")
        elif "averaged" not in content.lower():
            print(f"  [FAIL] {fname} missing averaged shifted convolution discussion")
            errors.append(fname)

    # Required: holomorphic vs spherical distinction
    for fname in ["statement.md", "proof.md"]:
        full = os.path.join(path, fname)
        if not os.path.exists(full):
            continue
        content = open(full).read()
        if "holomorphic" in content.lower() and "spherical" in content.lower():
            print(f"  [PASS] {fname} distinguishes holomorphic vs spherical")
        else:
            print(f"  [FAIL] {fname} missing holomorphic/spherical distinction")
            errors.append(fname)

    # Required: correct Kuznetsov references
    deps = os.path.join(path, "dependencies.yaml")
    if os.path.exists(deps):
        content = open(deps).read()
        if "Blomer" in content or "Goldfeld" in content:
            print(f"  [PASS] dependencies.yaml has corrected GL₃ references")
        else:
            print(f"  [FAIL] dependencies.yaml missing corrected GL₃ references")
            errors.append(deps)

    # Required: 09 not claimed as necessary for M-1/M-2
    stmt = os.path.join(path, "statement.md")
    if os.path.exists(stmt):
        content = open(stmt).read()
        if "not a logical prerequisite" in content or "sufficient, not necessary" in content.lower():
            print(f"  [PASS] statement.md correctly notes 09 is not a necessary condition")
        else:
            print(f"  [WARN] statement.md should clarify 09 is sufficient, not necessary for M-1/M-2")

    print()
    if errors:
        print(f"FAILED: {len(errors)} checks failed")
        sys.exit(1)
    else:
        print("All checks passed")
        sys.exit(0)

if __name__ == "__main__":
    main()
