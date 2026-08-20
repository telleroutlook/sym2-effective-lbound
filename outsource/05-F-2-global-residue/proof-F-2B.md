# F-2B: Exact Euler-Factor Extraction — Proof

## Pure-tensor factorization

Choose decomposable vectors W = ⊗_v W_v, W' = ⊗_v W'_v, Φ = ⊗_v Φ_v.
Then by the pure-tensor hypothesis + product Haar measure + absolute convergence/Fubini:

    Ψ(s, W, W, Φ) = ∏_v Ψ_v(s, W_v, W_v, Φ_v)

**This factorization requires the pure-tensor hypothesis.** For general
(non-factorizable) vectors, Ψ(s) is a finite sum of such products.

**Attribution corrected (per 2026-08-20 review):** JS81 §4.7写出 decomposable
data 时的 product factorization，依赖 restricted tensor product + product
measure + absolute convergence/Fubini. NOT "by strong approximation".

## Unramified places (good primes)

For p ∤ N, with inverse Satake parameters α_p⁻¹, β_p⁻¹ for π̃_p:

    L_p(s, π_p × π̃_p) = [(1 - p⁻ˢ)(1 - p⁻ˢ)(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

For trivial central character (α_p β_p = 1):

    = [(1 - p⁻ˢ)²(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

This equals ζ_p(s) · L_p(s, π, Ad) where:

    L_p(s, π, Ad) = [(1 - p⁻ˢ)(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

**NOT** the single-factor formula from the original. The adjoint representation
is 3-dimensional: parameters {1, αβ⁻¹, βα⁻¹}.

**Local integral attribution (corrected):** The local integral Ψ_v is a
JS/Rankin–Selberg type Whittaker local integral (JS81 §4.7, referencing
Sections 1 and 3 of JS81), NOT "the local Godement–Jacquet integral".
Godement–Jacquet (Ann. Math. Studies 26, 1972) provides background on
GL₂ local factors but the specific Ψ_v here is from JS81's own construction.

## Ramified places (bad primes) [OBL]

For p | N, the local integral Ψ_p depends on the local newvector type.
The computation requires:
1. Local Whittaker function W_p (Casselman's formula for newvector)
2. Local Haar measure normalization
3. Local test function Φ_p
4. The type-specific local L-factor

**Each type needs an explicit Z_p(1) formula and nonvanishing proof:**
- Steinberg twist (conductor exponent 1): Z_p(1) = ?
- Ramified principal series (conductor exponent ≥ 1): Z_p(1) = ?
- Supercuspidal (conductor exponent ≥ 2): Z_p(1) = ?

Currently [OBL] — no explicit formulas provided.

## Archimedean place

### Derivation from archimedean Langlands parameter

For π_∞ = holomorphic discrete series of weight k, the archimedean Langlands
parameter is μ = (k-1, -(k-1)) (as a semisimple element in GL₂(C)).

The Rankin–Selberg local integral at ∞ gives the Gamma factor:

    Z_∞(s) = Γ_R(s) · Γ_R(s + 1) · Γ_C(s + k - 1)

where:
- Γ_R(s) = π^{-s/2} Γ(s/2) [degree 1, from ζ_∞(s)]
- Γ_R(s + 1) = π^{-(s+1)/2} Γ((s+1)/2) [degree 1]
- Γ_C(s + k - 1) = 2(2π)^{-(s+k-1)} Γ(s+k-1) [degree 2]

**Derivation:** The full Rankin–Selberg L(s, π × π̃) at ∞ has Gamma factors
coming from the archimedean Whittaker model. For π_∞ in the discrete series
D_k, the local integral Ψ_∞ produces Γ_R(s)·Γ_R(s+1) from the ζ_∞ part,
and Γ_C(s+k-1) from the adjoint part. The total degree is 1+1+2=4, matching
the Rankin–Selberg degree. This follows from the archimedean Rankin–Selberg
integral (Iwaniec–Kowalski §13.1, or Goldfeld–Hundley Vol. 1 §4.7).

**Degree 4 is a consistency check, NOT a derivation.** The actual derivation
comes from the archimedean Whittaker model / local integral.

### Numerical evaluation at s = 1

    Z_∞(1) = Γ_R(1) · Γ_R(2) · Γ_C(k)

where:
- Γ_R(1) = π^{-1/2} Γ(1/2) = π^{-1/2} · √π = 1
- Γ_R(2) = π^{-1} Γ(1) = π^{-1}
- Γ_C(k) = 2(2π)^{-k} Γ(k)

Therefore:

    Z_∞(1) = 1 · π^{-1} · 2(2π)^{-k} Γ(k)
            = 2 · 2^{-k} · π^{-1-k} · Γ(k)
            = 2^{1-k} · π^{-1-k} · Γ(k)

**Correct formula (corrected per 2026-08-20 review):**

    Z_∞(1) = 2^{1-k} · π^{-(k+1)} · Γ(k)

For k = 12:

    Z_∞(1) = 2^{-11} · π^{-13} · 11!
            = (1/2048) · π^{-13} · 39916800
            ≈ 0.00671239369377...

**Previous error:** The v2 proof wrote 2π^{-k-1}Γ(k), which differs by 2^k.
For k=12 this is a factor of 4096. The correct value is 2^{1-k}π^{-k-1}Γ(k).

## Status: [OBL]

Main obstructions:
1. Ramified local factors Z_p(1) for each local type
2. Consistent normalization of Haar measures and Whittaker functions
3. Archimedean derivation from Langlands parameter (above is a sketch, not a proof)
