#!/usr/bin/env python3
"""Checker for 09-gl3-shifted-convolution: verify [OBL] status is correct."""
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

    # Status labels
    status_files = {
        "statement.md": "statement.md",
        "proof.md": "proof.md",
    }
    for fname, label in status_files.items():
        full = os.path.join(path, fname)
        if not os.path.exists(full):
            continue
        content = open(full).read()
        has_thm = "[THM]" in content
        has_obl = "[OBL]" in content
        if has_thm:
            print(f"  [FAIL] {label} contains [THM] — this is a research gap, not a theorem")
            errors.append(fname)
        elif has_obl:
            print(f"  [PASS] {label} correctly uses [OBL] (research gap)")
        else:
            print(f"  [WARN] {label} has no status label")

    # Check proof.md has required sections
    proof = os.path.join(path, "proof.md")
    if os.path.exists(proof):
        content = open(proof).read()
        required_sections = ["Kuznetsov", "spectral", "shifted convolution",
                            "power-saving", "critical"]
        for sec in required_sections:
            if sec.lower() in content.lower():
                pass
            else:
                print(f"  [FAIL] proof.md missing required section/concept: {sec}")
                errors.append(proof)

    # Check dependencies.yaml has references
    deps = os.path.join(path, "dependencies.yaml")
    if os.path.exists(deps):
        content = open(deps).read()
        if "references:" in content:
            print(f"  [PASS] dependencies.yaml has references")
        else:
            print(f"  [FAIL] dependencies.yaml missing references")
            errors.append(deps)

    print()
    if errors:
        print(f"FAILED: {len(errors)} checks failed")
        sys.exit(1)
    else:
        print("All checks passed")
        sys.exit(0)

if __name__ == "__main__":
    main()
