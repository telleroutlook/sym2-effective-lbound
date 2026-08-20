# F-2B: Exact Euler-Factor Extraction (v5)

**Status**: [OBL] — BLOCKED on ramified factors, normalization, and h_∞(1)

## Desired Statement

Let π ⊂ GL₂(A_Q) be a unitary cuspidal automorphic representation with trivial
central character ω = 1. Choose decomposable (pure-tensor) vectors:

    W = ⊗_v W_v,    W' = ⊗_v W'_v,    Φ = ⊗_v Φ_v

For the unfolded integral Ψ(s, W_φ, W_φ, Φ) defined in F-2A:

**Statement [OBL]**: There exist explicit local factors Z_v(s) for each place v of Q
such that:

    Ψ(s, W_φ, W_φ, Φ) = ∏_v Ψ_v(s, W_v, W_v, Φ_v) = L^S(s, π × π̃) · ∏_{v∈S} Z_v(s)

where S is a finite set of places (including ∞ and all ramified primes).

**CRITICAL**: The product factorization ∏_v Ψ_v requires the pure-tensor
hypothesis W = ⊗_v W_v. For general (non-factorizable) vectors, Ψ(s) is a
finite sum of such products, not a single Euler product.

## Canonical L-factor vs actual local zeta integral

The factorization involves:

    Ψ_v(s, W_v, W_v, Φ_v) = h_v(s) · L_v^{can}(s, π_v × π̃_v)

where:

- **L_v^{can}** is the canonical (standard) local L-factor of the Rankin–Selberg
  L-function at v. This is an intrinsic invariant of the representation π_v.

- **h_v(s)** is a normalization factor that depends on:
  - W_v (choice of Whittaker function / newvector)
  - Φ_v (choice of Schwartz function / test function)
  - Haar measure normalization on GL₂(Q_v) and N(Q_v)

**The canonical L-factor is NOT the local zeta integral.** The local zeta integral
Ψ_v equals h_v · L_v^{can}, and h_v depends on the specific choices made.
Computing h_v (especially h_∞(1)) is a prerequisite for explicit c_eff.

## Adjoint L-function

For GL₂ with trivial central character (α_p β_p = 1), the Rankin–Selberg L-function
factors as:

    L(s, π × π̃) = ζ(s) · L(s, π, Ad)

The adjoint representation of GL₂ is 3-dimensional with local parameters:

    {1, α_p β_p⁻¹, β_p α_p⁻¹}

So the correct local adjoint factor is:

    L_p^{can}(s, π, Ad) = [(1 - p⁻ˢ)(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

**NOT** the single-factor (1 - α_p β_p⁻¹ p⁻ˢ)⁻¹ from the original.

The Rankin–Selberg factor (using inverse Satake parameters for π̃):

    L_p^{can}(s, π × π̃) = [(1 - p⁻ˢ)²(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

which equals ζ_p(s) · L_p^{can}(s, π, Ad) as expected (degree 4 = 1 + 3).

## Unramified places

For p ∤ N, with inverse Satake parameters α_p⁻¹, β_p⁻¹ for π̃_p:

    Ψ_p(s, W_p, W_p, Φ_p) = h_p(s) · L_p^{can}(s, π_p × π̃_p)

**Canonical factor:**

    L_p^{can}(s, π_p × π̃_p) = [(1 - p⁻ˢ)²(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

For spherical vectors (Casselman–Shalika formula), the normalization factor
h_p(s) is explicit. Computing h_p(s) for specific W_p, Φ_p is standard but
must be done consistently.

**Attribution:** The local integral Ψ_v is a
JS/Rankin–Selberg type Whittaker local integral (JS81 §4.7, referencing
Sections 1 and 3 of JS81), NOT "the local Godement–Jacquet integral".

## Schwartz function space (corrected, v5)

The local test function Φ_p lives in:

    Φ_p ∈ S(Q_p²) = C_c^∞(Q_p²)

NOT C_c^∞(GL₂(Q_p)). This is because the local integral involves Φ_p(e₂ g)
where e₂ = (0,1) ∈ Q_p², so Φ_p is evaluated on the second row of g.
JS81 §4.5 defines the global Φ ∈ S(A^r) for the Rankin–Selberg unfolding,
and the local factors live on Q_p².

## Ramified places (bad primes) [BLOCKED]

For p | N, the local integral Ψ_p depends on the local newvector type.
**This is the primary blocker for F-2B.**

Each type requires:
1. Local Whittaker function W_p (Casselman's formula for newvector)
2. Local Haar measure normalization
3. Local Schwartz function Φ_p ∈ S(Q_p²)
4. The type-specific canonical L-factor L_p^{can}(1)
5. Normalization factor h_p(1) for the specific choices
6. Explicit Z_p(1) = h_p(1) · L_p^{can}(1) formula and nonvanishing proof

**Blocked types:**

Local representation at p | N_π depends on conductor exponent a(π_p):

- **Unramified principal series** (a(π_p) = 0): handled by Casselman–Shalika
- **Steinberg twist χ·St** (a(π_p) = 1 if χ unramified, 2a(χ) otherwise):
  Z_p(1) = ? [OBL]
- **Ramified principal series** (a(π_p) = a(χ₁) + a(χ₂) ≥ 1): Z_p(1) = ? [OBL]
- **Supercuspidal** (a(π_p) ≥ 2): Z_p(1) = ? [OBL]

## Archimedean place

### Canonical L-factor at ∞

For π_∞ = holomorphic discrete series of weight k, the archimedean Langlands
parameter is the real Weil-group representation:

    ρ_{k-1} = Ind_{W_ℂ}^{W_ℝ}((z/|z|)^{k-1})

This is a 2-dimensional representation of W_ℝ.

The canonical Rankin–Selberg L-factor at ∞ for ρ_{k-1} ⊗ ρ_{k-1}^∨ is:

    L_∞^{can}(s) = L_ℝ(s) · L_ℝ(s+1) · L_ℂ(s+k-1)

where:
- L_ℝ(s) = π^{-s/2} Γ(s/2) [degree 1, from ζ_∞(s)]
- L_ℝ(s+1) = π^{-(s+1)/2} Γ((s+1)/2) [degree 1]
- L_ℂ(s+k-1) = 2(2π)^{-(s+k-1)} Γ(s+k-1) [degree 2]

**Numerical evaluation at s = 1:**

    L_∞^{can}(1) = L_ℝ(1) · L_ℝ(2) · L_ℂ(k)
                 = 1 · π^{-1} · 2(2π)^{-k} Γ(k)
                 = 2^{1-k} · π^{-(k+1)} · Γ(k)

For k = 12:

    L_∞^{can}(1) = 2^{-11} · π^{-13} · 11!
                 ≈ 0.00671239369377...

### Actual local zeta integral at ∞

The actual local integral is:

    Ψ_∞(s, W_∞, W_∞, Φ_∞) = h_∞(s) · L_∞^{can}(s)

where h_∞(s) depends on:
- W_∞ (holomorphic discrete series Whittaker function, weight k normalization)
- Φ_∞ ∈ S(R²) (Schwartz function)
- Haar measure on GL₂(R) and N(R)

**Computing h_∞(1) is [OBL].** This is distinct from computing L_∞^{can}(1).
The derivation requires computing the local integral Ψ_∞ directly with:
- Specified W_∞
- Specified Φ_∞
- Specified Haar measures

**Degree 4 = 1+1+2 is a consistency check**, not the derivation itself.

## Status: [OBL]

Main obstructions:
1. **[BLOCKER]** Ramified local factors Z_p(1) = h_p(1)·L_p^{can}(1) for each type
2. **[BLOCKER]** Normalization constant h_∞(1) for archimedean place
3. Consistent normalization of Haar measures and Whittaker functions across all places
4. Full archimedean derivation from local integral (not degree counting)
