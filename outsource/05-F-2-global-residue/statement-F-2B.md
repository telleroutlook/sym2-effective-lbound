# F-2B: Exact Euler-Factor Extraction

## Desired Statement

Let π ⊂ GL₂(A_Q) be a unitary cuspidal automorphic representation with trivial
central character. For the global integral Ψ(s, W, W, Φ) defined in F-2A:

**Statement**: There exist explicit local factors Z_v(s) for each place v of Q such that:

    Ψ(s, W, W, Φ) = L^S(s, π × π̃) · ∏_{v∈S} Z_v(s)

where S is a finite set of places (including ∞ and all ramified primes), and:

    L(s, π × π̃) = ζ(s) · L(s, π, Ad)

with the adjoint L-function defined via:

    L(s, π, Ad) = ∏_p (1 − α_p β_p^{−1} p^{−s})^{−1}

for unramified p, where α_p, β_p are the Satake parameters.

## What remains

1. **Archimedean factor Z_∞(s)**: Must be computed for the specific archimedean
   representation. For holomorphic weight k: Z_∞ involves Γ_R(s+1)·Γ_C(s+k−1)
   (NOT fixed at k=11 as in original).

2. **Ramified finite factors Z_p(s)**: For each p | N, compute the local integral
   explicitly in terms of the local newvector and local Whittaker function.

3. **Normalization**: All Haar measures, Whittaker functions, and test functions
   must be normalized consistently. The "ε-factors" and root numbers must be tracked.

4. **The identity L(s, π × π̃) = ζ(s) · L(s, π, Ad)**: This is standard for
   GL₂ with trivial central character, but the proof must be included for
   completeness.

## Status: [OBL]

This is the real technical obligation. The key tools are:
- Godement–Jacquet theory for GL₂ local factors
- Casselman–Shalika formula for unramified computation
- Local newvector theory (Casselman, Casselman–Piatetski-Shapiro)
