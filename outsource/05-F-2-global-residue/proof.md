# F-2: Global Residue Positivity — Combined Proof

**Status**: [OBL] (restructured 2026-08-20)

## Overview

This document describes the proof strategy for establishing global residue
positivity and extracting exact Euler factors.

## F-2A: Diagonal global residue positivity

See `proof-F-2A.md` for the detailed proof.

**Key insight**: The residue is positive by norm-square positivity, NOT by
L(1, π, Ad) > 0. The Jacquet–Shalika 1981 result gives:

    Res_{s=1} Ψ(s, W, W, Φ) = c_Q · Φ̂(0) · ∫|φ(g)|² dg > 0

The integral ∫|φ(g)|² dg > 0 for any nonzero automorphic form φ.

**Correct integral formula**: W'(g) · conj(W(g)), NOT W̃(g) · W(g).
**Diagonal condition**: π' = π, NOT π̃ = π.

## F-2B: Euler factor extraction

See `proof-F-2B.md` for the detailed proof.

**Factorization**: The global integral unfolds to a product of local integrals:

    Ψ(s) = ∏_v Ψ_v(s)

For unramified v: Ψ_v(s) = L_v(s, π_v × π̃_v).
For ramified v: explicit local computation required.
For v = ∞: archimedean factor depends on weight k (NOT fixed at k=11).

**L(s, π × π̃) = ζ(s) · L(s, π, Ad)**: Standard for GL₂ with trivial central character.

## F-2C: Target-family uniformity

See `proof-F-2C.md` for the detailed proof.

**Uniformity**: For level ≤ N₀, the product ∏_{p|N} Z_p(1) is bounded below
by an explicit constant c' depending only on N₀.

**Interface**: The constant c' feeds into M-1 (mollifier), M-2 (mean value),
and c_eff (explicit bound).

## Blockers

1. **Archimedean factor Z_∞(1)**: Must be computed for weight k (F-2B)
2. **Ramified factors Z_p(1)**: Must be computed for each p | N (F-2B)
3. **Uniformity constant c'**: Must be computed for level ≤ N₀ (F-2C)
4. **Normalization consistency**: All measures, functions, test functions (F-2B)
