# Checker — c_eff v3

## Status

Structural checker only. Does NOT verify mathematical correctness.

## What it checks

1. Required files exist
2. Status labels: c_eff must remain [OBL]
3. Required concepts: hoffstein, zero-free, auxiliary, explicit, triple zero, double pole, non-negative coefficients, M=K^C
4. Forbidden patterns: siegel zero, vinogradov-korobov, L(1/2), log(1/δ), exterior square, "depending on k"
5. Theorem scope: must use log(kp+1), not just log p
6. Completed function: must include p^s factor
7. Analytic conductor: must use k², not k³ (now checks proof.md, not just statement.md)
8. Parameter matching: M=K^C, not δ=c/log K
9. Reference years: Hoffstein–Lockhart must be 1994
10. Bibliography: Iwaniec–Michel is Ann. Acad. Sci. Fenn. 26, not JAMS 14; HL is pp. 161–181, not 1–42

## What it does NOT check

- Mathematical correctness of proofs
- Numerical validity of constants
- Correctness of the zero-count argument
- Whether the residue formula is valid
- Whether the M=K^C matching is carried through correctly

## Run

    python3 check_explicit_bound.py <submission_dir>

## Version history

- v1 (2026-08-20): Initial checker
- v2 (2026-08-20): Fixed scope, added completed function, analytic conductor, year checks
- v3 (2026-08-20): Added M=K^C check, fixed false positive on q_ar, checks proof.md for conductor
