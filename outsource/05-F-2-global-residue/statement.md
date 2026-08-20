# F-2: Global Residue Positivity — Combined Statement (v2)

**Status**: [OBL] (restructured v2, 2026-08-20)

## Overview

This obligation establishes that the global Rankin–Selberg residue is strictly
positive and extracts the exact Euler factors for use in explicit lower bounds.

## F-2A: Diagonal global residue positivity

See `statement-F-2A.md`. Core思想 correctly established in v1.

**Key correction (v2)**: Integral definition fixed:
- Quotient: N(A)\GL₂(A) (NOT N(A)G(Q)\G(A))
- Test function: Φ(e₂ g) (NOT Φ(g))
- Citation: Am. J. Math. 103(3) (1981), 499–558 (NOT Ann. Math. 114)

**Status**: [THM/REFEREED candidate] — specialization of JS81.

## F-2B: Exact Euler-factor extraction

See `statement-F-2B.md`.

**Key corrections (v2)**:
1. Adjoint Euler factor now has 3 factors: [(1-x)(1-αβ⁻¹x)(1-βα⁻¹x)]⁻¹
   (original had only 1 factor — a load-bearing error)
2. Pure-tensor hypothesis W = ⊗_v W_v added (required for ∏_v factorization)
3. Satake parameters: use inverses α⁻¹, β⁻¹ for π̃ (not complex conjugates)
4. Archimedean factor: degree 4 (was degree 3, missing ζ_∞ factor)

**Status**: [OBL] — the real technical obligation.

## F-2C: Target-family local positivity/uniformity

See `statement-F-2C.md`.

**Key corrections (v2)**:
1. Z_∞(1) now has π^{-1} factor: Γ_R(1)·Γ_R(2)·Γ_C(k) = 2π^{-k-1}Γ(k)
2. Uniformity: nonvanishing must come from explicit formulas, NOT continuity
3. Product bound: C(N₀) = min_N ∏_p |Z_p(1)| > 0, not just individual min
4. Local type classification uses conductor of π (not symmetric-square)

**Status**: [OBL] — interfaces with downstream.

## Dependencies

- JS81 Lemma 4.4, 4.6(i) (Am. J. Math. 103(3) (1981), 499–558)
- Godement–Jacquet local zeta integrals
- Casselman newvector theory
- L(s, π × π̃) = ζ(s) · L(s, π, Ad) factorization

## What is NOT claimed

- GRH is NOT assumed
- L(1, π, Ad) > 0 is NOT a prerequisite
- An explicit general lower bound is NOT given (that is c_eff)
