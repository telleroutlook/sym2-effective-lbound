# F-2B: Exact Euler-Factor Extraction — Proof

## Pure-tensor factorization

Choose decomposable vectors W = ⊗_v W_v, W' = ⊗_v W'_v, Φ = ⊗_v Φ_v.
Then by strong approximation:

    Ψ(s, W, W, Φ) = ∏_v Ψ_v(s, W_v, W_v, Φ_v)

**This factorization requires the pure-tensor hypothesis.** For general
(non-factorizable) vectors, Ψ(s) is a finite sum of such products.

## Unramified places (good primes)

For p ∤ N, with inverse Satake parameters α_p⁻¹, β_p⁻¹ for π̃_p:

    L_p(s, π_p × π̃_p) = [(1 - p⁻ˢ)(1 - p⁻ˢ)(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

For trivial central character (α_p β_p = 1):

    = [(1 - p⁻ˢ)²(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

This equals ζ_p(s) · L_p(s, π, Ad) where:

    L_p(s, π, Ad) = [(1 - p⁻ˢ)(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

**NOT** the single-factor formula from the original. The adjoint representation
is 3-dimensional: parameters {1, αβ⁻¹, βα⁻¹}.

## Ramified places (bad primes) [OBL]

For p | N, the local integral Ψ_p depends on the local newvector type.
The computation requires:
1. Local Whittaker function W_p (Casselman's formula for Iwahori)
2. Local Haar measure normalization
3. Local test function Φ_p
4. The type-specific local L-factor

## Archimedean place

The full Rankin–Selberg L-function has degree 4, so:

    Z_∞(s) = Γ_R(s) · Γ_R(s + 1) · Γ_C(s + k - 1)

where:
- Γ_R(s) = π^{-s/2} Γ(s/2) [degree 1, from ζ_∞]
- Γ_R(s + 1) = π^{-(s+1)/2} Γ((s+1)/2) [degree 1]
- Γ_C(s + k - 1) = 2(2π)^{-(s+k-1)} Γ(s+k-1) [degree 2]

Total degree: 1 + 1 + 2 = 4, matching L(s, π × π̃).

**At s = 1**:

    Z_∞(1) = Γ_R(1) · Γ_R(2) · Γ_C(k)
            = 1 · π⁻¹ · 2(2π)^{-k} Γ(k)
            = 2π^{-k-1} Γ(k)

**CORRECTION**: The original missed the Γ_R(1) = 1 factor and the π^{-1}
from Γ_R(2). The correct value has an extra π^{-1}.

## Status: [OBL]

Main obstructions: ramified local factors, consistent normalization.
