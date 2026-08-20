# Checker — c_eff v2

## Status

Structural checker only. Does NOT verify mathematical correctness.

## What it checks

1. Required files exist
2. Status labels: c_eff must remain [OBL]
3. Required concepts in proof.md: hoffstein, zero-free, auxiliary, explicit, triple zero, double pole
4. Forbidden patterns: siegel zero, vinogradov-korobov, L(1/2)
5. Theorem scope: must use log(kp+1), not just log p
6. Completed function: must include p^s factor
7. Analytic conductor: must use k², not k³
8. Reference years: Hoffstein–Lockhart must be 1994

## What it does NOT check

- Mathematical correctness of proofs
- Numerical validity of constants
- Correctness of the zero-count argument
- Whether the residue formula is valid

## Run

    python3 check_explicit_bound.py <submission_dir>
