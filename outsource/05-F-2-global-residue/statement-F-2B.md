# F-2B: Exact Euler-Factor Extraction (v4)

**Status**: [OBL] — BLOCKED on ramified factors and archimedean derivation

## Desired Statement

Let π ⊂ GL₂(A_Q) be a unitary cuspidal automorphic representation with trivial
central character. Choose **decomposable** (pure-tensor) vectors:

    W = ⊗_v W_v,    W' = ⊗_v W'_v,    Φ = ⊗_v Φ_v

For the unfolded integral Ψ(s, W_φ, W_φ, Φ) defined in F-2A:

**Statement [OBL]**: There exist explicit local factors Z_v(s) for each place v of Q
such that:

    Ψ(s, W_φ, W_φ, Φ) = ∏_v Ψ_v(s, W_v, W_v, Φ_v) = L^S(s, π × π̃) · ∏_{v∈S} Z_v(s)

where S is a finite set of places (including ∞ and all ramified primes).

**CRITICAL**: The product factorization ∏_v Ψ_v requires the pure-tensor
hypothesis W = ⊗_v W_v. For general (non-factorizable) vectors, Ψ(s) is a
finite sum of such products, not a single Euler product.

## Adjoint L-function

For GL₂ with trivial central character (α_p β_p = 1), the Rankin–Selberg L-function
factors as:

    L(s, π × π̃) = ζ(s) · L(s, π, Ad)

The adjoint representation of GL₂ is 3-dimensional with local parameters:

    {1, α_p β_p⁻¹, β_p α_p⁻¹}

So the correct local adjoint factor is:

    L_p(s, π, Ad) = [(1 - p⁻ˢ)(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

**NOT** the single-factor (1 - α_p β_p⁻¹ p⁻ˢ)⁻¹ from the original.

The Rankin–Selberg factor (using inverse Satake parameters for π̃):

    L_p(s, π × π̃) = [(1 - p⁻ˢ)²(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

which equals ζ_p(s) · L_p(s, π, Ad) as expected (degree 4 = 1 + 3).

## Unramified places

For p ∤ N, the local Whittaker integral gives:

    Ψ_p(s, W_p, W_p, Φ_p) = L_p(s, π_p × π̃_p)

using the Casselman–Shalika formula for spherical vectors.

**Attribution (corrected):** The local integral Ψ_v is a
JS/Rankin–Selberg type Whittaker local integral (JS81 §4.7, referencing
Sections 1 and 3 of JS81), NOT "the local Godement–Jacquet integral".

## Ramified places (bad primes) [BLOCKED]

For p | N, the local integral depends on the local newvector type.
**This is the primary blocker for F-2B.**

Each type requires:
1. Local Whittaker function W_p (Casselman's formula for newvector)
2. Local Haar measure normalization
3. Local test function Φ_p
4. The type-specific local L-factor
5. Explicit Z_p(1) formula and nonvanishing proof

**Blocked types:**
- **Steinberg twist** (conductor exponent 1): Z_p(1) = ? [OBL]
- **Ramified principal series** (conductor exponent ≥ 1): Z_p(1) = ? [OBL]
- **Supercuspidal** (conductor exponent ≥ 2): Z_p(1) = ? [OBL]

## Archimedean place

### Derivation from archimedean Langlands parameter

For π_∞ = holomorphic discrete series of weight k, the archimedean Langlands
parameter is the real Weil-group representation:

    ρ_{k-1} = Ind_{W_ℂ}^{W_ℝ}((z/|z|)^{k-1})

This is a 2-dimensional representation of W_ℝ.

The Rankin–Selberg local L-factor at ∞ for ρ_{k-1} ⊗ ρ_{k-1}^∨ decomposes as:

    L_ℝ(s, ρ_{k-1} ⊗ ρ_{k-1}^∨) = L_ℝ(s) · L_ℝ(s+1) · L_ℂ(s+k-1)

where:
- L_ℝ(s) = π^{-s/2} Γ(s/2) [degree 1, from ζ_∞(s)]
- L_ℝ(s+1) = π^{-(s+1)/2} Γ((s+1)/2) [degree 1]
- L_ℂ(s+k-1) = 2(2π)^{-(s+k-1)} Γ(s+k-1) [degree 2]

**Derivation sketch:** The ρ_{k-1} ⊗ ρ_{k-1}^∨ decomposition follows from
the induced representation structure. The local integral Ψ_∞ produces the
Gamma factors from the archimedean Whittaker model, matching the standard
Rankin–Selberg Γ-factor for the real Weil-group parameter.

**Degree 4 = 1+1+2 is a consistency check**, not the derivation itself.
The actual derivation requires computing the local integral Ψ_∞ with
specified W_∞, Φ_∞, and Haar measure — this is [OBL].

### Numerical evaluation at s = 1

    Z_∞(1) = Γ_R(1) · Γ_R(2) · Γ_C(k)

where:
- Γ_R(1) = π^{-1/2} Γ(1/2) = π^{-1/2} · √π = 1
- Γ_R(2) = π^{-1} Γ(1) = π^{-1}
- Γ_C(k) = 2(2π)^{-k} Γ(k)

Therefore:

    Z_∞(1) = 1 · π^{-1} · 2(2π)^{-k} Γ(k)
            = 2^{1-k} · π^{-(k+1)} · Γ(k)

**Correct formula (corrected in v3, verified by reviewer):**

    Z_∞(1) = 2^{1-k} · π^{-(k+1)} · Γ(k)

For k = 12:

    Z_∞(1) = 2^{-11} · π^{-13} · 11!
            ≈ 0.00671239369377...

**Status**: [OBL]

Main obstructions:
1. **[BLOCKER]** Ramified local factors Z_p(1) for each local type
2. Consistent normalization of Haar measures and Whittaker functions
3. Full archimedean derivation from local integral (sketch above, not proof)
4. c_∞(1) normalization constant for Ψ_∞ = c_∞(1) · L_∞(s, π × π̃) [OBL]
