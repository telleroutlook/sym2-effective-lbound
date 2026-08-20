# F-2B: Exact Euler-Factor Extraction

## Desired Statement

Let π ⊂ GL₂(A_Q) be a unitary cuspidal automorphic representation with trivial
central character. Choose **decomposable** (pure-tensor) vectors:

    W = ⊗_v W_v,    W' = ⊗_v W'_v,    Φ = ⊗_v Φ_v

For the unfolded integral Ψ(s, W, W, Φ) defined in F-2A:

**Statement [OBL]**: There exist explicit local factors Z_v(s) for each place v of Q
such that:

    Ψ(s, W, W, Φ) = ∏_v Ψ_v(s, W_v, W_v, Φ_v) = L^S(s, π × π̃) · ∏_{v∈S} Z_v(s)

where S is a finite set of places (including ∞ and all ramified primes).

**CRITICAL**: The product factorization ∏_v Ψ_v requires the pure-tensor
hypothesis W = ⊗_v W_v. For general (non-factorizable) vectors, Ψ(s) is a
finite sum of such products, not a single Euler product.

## Adjoint L-function (corrected)

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

For p ∤ N, the local Godement–Jacquet integral gives:

    Ψ_p(s, W_p, W_p, Φ_p) = L_p(s, π_p × π̃_p)

using the Casselman–Shalika formula for spherical vectors.

## Ramified places (bad primes) [OBL]

For p | N, the local integral depends on the local newvector type:
- **Spherical** (p ∤ conductor): standard computation
- **Special/Steinberg twist**: conductor exponent 1
- **Ramified principal series**: higher conductor
- **Supercuspidal**: most complex

Each type requires explicit computation of the local Whittaker function,
Haar measure, and test function Φ_p.

## Archimedean place

The archimedean local integral Ψ_∞ depends on the representation π_∞.
The full Rankin–Selberg completion has degree 4, so Z_∞(s) must include
the ζ_∞(s) factor as well:

    Z_∞(s) = Γ_R(s) · Γ_R(s+1) · Γ_C(s+k-1)

where Γ_R(s) = π^{-s/2} Γ(s/2) and Γ_C(s) = 2(2π)^{-s} Γ(s).

**Note**: The degree is 1 + 1 + 2 = 4, matching the Rankin–Selberg degree.
The previous version had degree 3 (missing the ζ_∞ factor).

## Status: [OBL]

Main obstructions:
1. Explicit computation of ramified local factors Z_p(1) for each type
2. Consistent normalization of all Haar measures, Whittaker functions, Φ_v
3. Archimedean factor with correct degree 4
