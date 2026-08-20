# F-2 Global Residue Positivity — Restructured (F-2A / F-2B / F-2C)

**Date:** 2026-08-20
**Reviewer verdict:** FAIL on original F-2; restructuring required before resubmission.

## Restructuring rationale

The original F-2 contained a fundamental scaling contradiction in the residue formula
and a misreading of Jacquet–Shalika 1981. The reviewer identified three independent issues:

1. **Scaling contradiction**: The integral Ψ(s, W, W̃, Φ) is linear in W̃, but the claimed
   residue formula Φ̂(0)·κ_F·L(1,π,Ad)·|W|² is independent of W̃. This is impossible.

2. **JS81 misread**: JS81 uses W'(g)·conjugate(W(g)), producing a norm-square |W(g)|².
   The original package incorrectly rewrote this as W̃(g)·W(g) and conflated π' = π
   (diagonal condition) with π̃ = π (self-dual condition).

3. **Archimedean scope**: The original fixed Γ_R(s+1)·Γ_C(s+11), which is specific to
   holomorphic weight 12, not general GL₂.

The reviewer recommends splitting into three obligations:

## F-2A — Diagonal global residue positivity [THM/REFEREED candidate]

**Claim**: For unitary cuspidal π ⊂ GL₂(A_Q), same automorphic vector, W' = W,
conjugate(W) ∈ W(π̃, ψ⁻¹), Φ̂(0) > 0:

    Res_{s=1} Ψ(s, W, W, Φ) = c_Q · Φ̂(0) · |φ|² > 0

**Status**: Essentially a specialization of Jacquet–Shalika §4.2–4.6.
**Target**: Upgrade to [THM/REFEREED] by precise JS81 citation.

## F-2B — Exact Euler-factor extraction [OBL]

**Claim**: The global integral factors as:

    Ψ(s, W, W, Φ) = L^S(s, π × π̃) · ∏_{v∈S} Z_v(s)

and L(s, π × π̃) = ζ(s) · L(s, π, Ad). All normalization, finite ramified places,
and ∞-place explicit.

**Target**: The real technical obligation.

## F-2C — Target-family local positivity/uniformity [OBL]

**Claim**: For the specific modular form family needed downstream (fixed level, weight,
nebentypus, newvector normalization, Haar measures, archimedean vector, bad-prime type):

    Z_p(1) and Z_∞(1) are computed explicitly.

**Target**: Interface with GHL / M-1 / M-2 / c_eff.

## Key corrections from original F-2

- Integral formula: W'(g)·conjugate(W(g)), NOT W̃(g)·W(g)
- Diagonal condition: π' = π, NOT π̃ = π
- Residue source: norm-square |φ|² > 0 from JS81 Lemma 4.4
- Archimedean factor: must be parameterized or narrowed to specific weight
- Bad-place blocker: existence of suitable local data (JS81), not arbitrary-data positivity
