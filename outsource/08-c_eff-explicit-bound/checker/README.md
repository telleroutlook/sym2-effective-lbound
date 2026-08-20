# Checker — c_eff v4

## Status

Structural checker only. Does NOT verify mathematical correctness.

## What it checks

1. Required files exist
2. Status labels: c_eff must remain [OBL]
3. Required concepts: hoffstein, zero-free, auxiliary, explicit, triple zero, double pole, non-negative coefficients, M=K^C
4. Forbidden patterns: siegel zero, vinogradov-korobov, L(1/2), log(1/δ), exterior square, "depending on k"
5. Theorem scope: must use log(kp+1), not just log p
6. Completed function: must include p^s factor in formula context (not just string presence)
7. Analytic conductor: must use k², not k³ (checks proof.md)
8. Parameter matching: M=K^C, not δ=c/log K
9. L(1,F)≠0 prerequisite: must be stated for double-pole argument
10. Growth constant C_*: must be named in growth bound discussion
11. Reference years: Hoffstein–Lockhart must be 1994
12. Bibliography: Iwaniec–Michel is Ann. Acad. Sci. Fenn. 26, not JAMS 14; HL is pp. 161–181, not 1–42

## What it does NOT check

- Mathematical correctness of proofs
- Numerical validity of constants
- Correctness of the zero-count argument
- Whether the residue formula is valid
- Whether the M=K^C matching is carried through correctly
- Whether C_* is actually computed (only checks it's named)

## Run

    python3 check_explicit_bound.py <submission_dir>

## Version history

- v1 (2026-08-20): Initial checker
- v2 (2026-08-20): Fixed scope, added completed function, analytic conductor, year checks
- v3 (2026-08-20): Added M=K^C check, fixed false positive on q_ar
- v4 (2026-08-20): Added L(1,F)≠0, C_*, strengthened completed function check
