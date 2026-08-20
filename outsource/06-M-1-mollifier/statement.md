# M-1: Mollifier Construction — Rewritten

## Desired Statement

Let π be a holomorphic Hecke eigenform of weight k on SL₂(Z), non-CM/non-dihedral,
and let Π = sym²π be its symmetric-square lift to GL₃. Fix T > 0 and let
Q(Π, T) denote the analytic conductor of L(s, Π) at height T.

Define the mollified second moment:

    I(T) = ∫_T^{2T} |M(½ + it) L(½ + it, Π)|² dt

where M(s) is a mollifier of length X ≤ Q(Π, T)^η.

**Goal**: Prove there exist explicit θ ∈ (0, 1), c₀ > 0, T₀ > 0, δ > 0 such that:

    I(T) ≥ c₀ T    for all T ≥ T₀

with X = Q(Π, T)^θ, and deduce L(½, Π) > 0 (hence L(1, sym² f) > 0).

## Critical corrections from review

1. **Mollifier definition**: The squarefree mollifier μ(n)a_Π(n) is NOT a true
   reciprocal mollifier. It misses p² and p³ terms in the local Euler inverse.
   Either use true reciprocal coefficients ρ_Π(n), or prove a squarefree
   approximation lemma.

2. **Square expansion**: |M(½+it)L(½+it,Π)|² produces a twisted moment
   J_{m,n}(T) = ∫_T^{2T} (n/m)^{it} |L(½+it,Π)|² dt, NOT a factorized
   ∫|L|² × Σ coefficients.

3. **No family orthogonality**: We work with a FIXED Π, not a family. The
   near-orthogonality comes from t-integration, not Hecke eigenvalue averaging.

4. **CM/dihedral exclusion**: Must assume π non-CM/non-dihedral for Π to be
   cuspidal GL₃.

## Status: [OBL]

The core analytic lemma (mollified twisted GL₃ moment) is at the research frontier.
See Dasgupta–Leung–Young (2024), Pal (2022) for current state of GL₃ second moments.
