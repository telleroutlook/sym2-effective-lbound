# F-2: Global Residue Positivity — Combined Statement

**Status**: [OBL] (restructured 2026-08-20)

## Overview

This obligation establishes that the global Rankin–Selberg residue is strictly
positive, and extracts the exact Euler factors for use in explicit lower bounds.

## F-2A: Diagonal global residue positivity

See `statement-F-2A.md` for the detailed statement.

**Summary**: For unitary cuspidal π ⊂ GL₂(A_Q), same vector W, conjugate(W) ∈ W(π̃, ψ⁻¹),
Φ̂(0) > 0:

    Res_{s=1} Ψ(s, W, W, Φ) = c_Q · Φ̂(0) · |φ|² > 0

**Status**: [THM/REFEREED candidate] — specialization of Jacquet–Shalika 1981.

## F-2B: Exact Euler-factor extraction

See `statement-F-2B.md` for the detailed statement.

**Summary**: The global integral factors as:

    Ψ(s) = L^S(s, π × π̃) · ∏_{v∈S} Z_v(s)

with L(s, π × π̃) = ζ(s) · L(s, π, Ad). All normalization explicit.

**Status**: [OBL] — the real technical obligation.

## F-2C: Target-family local positivity/uniformity

See `statement-F-2C.md` for the detailed statement.

**Summary**: For the specific modular form family (fixed level, weight, nebentypus,
newvector normalization, Haar measures, archimedean vector, bad-prime type):

    Z_p(1) and Z_∞(1) computed explicitly; product bounded below uniformly.

**Status**: [OBL] — interfaces with downstream (M-1, M-2, c_eff).

## Dependencies

- JS81 Lemma 4.4, 4.6(i) (verified against original text)
- Godement–Jacquet local zeta integrals
- Casselman newvector theory
- L(s, π × π̃) = ζ(s) · L(s, π, Ad) factorization

## What is NOT claimed

- GRH is NOT assumed
- L(1, π, Ad) > 0 is NOT a prerequisite (residue is positive by norm-square)
- An explicit general lower bound is NOT given (that is c_eff)
