# F-2B: Exact Euler-Factor Extraction — Proof (v5)

## Pure-tensor factorization

Choose decomposable vectors W = ⊗_v W_v, W' = ⊗_v W'_v, Φ = ⊗_v Φ_v.
Then by the pure-tensor hypothesis + product Haar measure + absolute convergence/Fubini:

    Ψ(s, W_φ, W_φ, Φ) = ∏_v Ψ_v(s, W_v, W_v, Φ_v)

**This factorization requires the pure-tensor hypothesis.** For general
(non-factorizable) vectors, Ψ(s) is a finite sum of such products.

**Attribution:** JS81 §4.7写出 decomposable
data 时的 product factorization，依赖 restricted tensor product + product
measure + absolute convergence/Fubini.

## Canonical L-factor vs local zeta integral

Each local factor decomposes as:

    Ψ_v(s, W_v, W_v, Φ_v) = h_v(s) · L_v^{can}(s, π_v × π̃_v)

where:
- L_v^{can} is the canonical (standard) local L-factor — intrinsic to π_v
- h_v(s) is a normalization factor depending on W_v, Φ_v, and Haar measures

**L_v^{can} ≠ Ψ_v in general.** The local zeta integral equals the canonical
L-factor only when h_v(s) = 1, which requires specific normalization choices.

## Unramified places (good primes)

For p ∤ N, with inverse Satake parameters α_p⁻¹, β_p⁻¹ for π̃_p:

**Canonical factor:**

    L_p^{can}(s, π_p × π̃_p) = [(1 - p⁻ˢ)²(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

For trivial central character (α_p β_p = 1):

    = [(1 - p⁻ˢ)²(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

This equals ζ_p(s) · L_p^{can}(s, π, Ad) where:

    L_p^{can}(s, π, Ad) = [(1 - p⁻ˢ)(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

The adjoint representation is 3-dimensional: parameters {1, αβ⁻¹, βα⁻¹}.

For spherical vectors (Casselman–Shalika formula), the normalization factor
h_p(s) is explicit and typically h_p(s) = 1 for standard choices.

**Local integral attribution:** The local integral Ψ_v is a
JS/Rankin–Selberg type Whittaker local integral (JS81 §4.7, referencing
Sections 1 and 3 of JS81), NOT "the local Godement–Jacquet integral".

## Schwartz function space (corrected, v5)

The local test function lives in:

    Φ_p ∈ S(Q_p²) = C_c^∞(Q_p²)

NOT C_c^∞(GL₂(Q_p)). The local integral involves Φ_p(e₂ g) where
e₂ = (0,1) ∈ Q_p², so Φ_p is evaluated on the second row of g.
JS81 §4.5 defines the global Φ ∈ S(A^r) for the Rankin–Selberg unfolding.

## Ramified places (bad primes) [BLOCKED]

For p | N, the local integral Ψ_p depends on the local newvector type.
**This is the primary blocker for F-2B.**

### Local type classification (corrected, v5)

The conductor exponent a(π_p) determines the local representation type:

- **Unramified principal series** (a(π_p) = 0): handled by Casselman–Shalika
- **Steinberg twist χ·St**: a(χ·St) = 1 if χ unramified, 2a(χ) if χ ramified
- **Ramified principal series** (a(π_p) = a(χ₁) + a(χ₂) ≥ 1)
- **Supercuspidal** (a(π_p) ≥ 2)

**Note:** The conductor exponent of a Steinberg twist is NOT always 1.
When the twisting character χ has conductor a(χ) > 0, the Steinberg twist
has conductor 2a(χ). Only when χ is unramified does a(χ·St) = 1.

### What each type requires [OBL]

1. Local Whittaker function W_p (Casselman's formula for newvector)
2. Local Haar measure normalization
3. Local Schwartz function Φ_p ∈ S(Q_p²)
4. The type-specific canonical L-factor L_p^{can}(1)
5. Normalization factor h_p(1) for the specific choices
6. Explicit Z_p(1) = h_p(1) · L_p^{can}(1) formula
7. Proof that Z_p(1) ≠ 0
8. Quantitative lower bound |Z_p(1)| ≥ c_p > 0

## Archimedean place

### Canonical L-factor at ∞

For π_∞ = holomorphic discrete series of weight k, the archimedean Langlands
parameter is the 2-dimensional real Weil-group representation:

    ρ_{k-1} = Ind_{W_ℂ}^{W_ℝ}((z/|z|)^{k-1})

The canonical Rankin–Selberg L-factor at ∞ for ρ_{k-1} ⊗ ρ_{k-1}^∨ is:

    L_∞^{can}(s) = L_ℝ(s) · L_ℝ(s+1) · L_ℂ(s+k-1)

**Decomposition sketch:**

The induction Ind_{W_ℂ}^{W_ℝ}(χ) with χ(z) = (z/|z|)^{k-1} has:

    Ind(χ) ⊗ Ind(χ)^∨ ≅ Ind(χ ⊗ χ̄) ⊕ Ind(χ ⊗ χ̄⁻¹)
                       ≅ Ind(1) ⊕ Ind((z/|z|)^{2(k-1)})

where:
- Ind(1) = L_ℝ(s) · L_ℝ(s+1) [degree 2 = 1+1]
- Ind((z/|z|)^{2(k-1)}) = L_ℂ(s+k-1) [degree 2]

This gives total degree 4 = 2+2.

### Actual local zeta integral at ∞

The actual local integral is:

    Ψ_∞(s, W_∞, W_∞, Φ_∞) = h_∞(s) · L_∞^{can}(s)

**Computing h_∞(1) is [OBL].** This requires:
- Specified W_∞ (holomorphic discrete series Whittaker function)
- Specified Φ_∞ ∈ S(R²) (Schwartz function)
- Specified Haar measure on GL₂(R) and N(R)

**The full computation of h_∞(1) from the local integral is [OBL]**
— the above decomposition is a consistency argument, not a derivation.

### Numerical evaluation of L_∞^{can} at s = 1

    L_∞^{can}(1) = L_ℝ(1) · L_ℝ(2) · L_ℂ(k)

where:
- L_ℝ(1) = π^{-1/2} Γ(1/2) = 1
- L_ℝ(2) = π^{-1} Γ(1) = π^{-1}
- L_ℂ(k) = 2(2π)^{-k} Γ(k)

Therefore:

    L_∞^{can}(1) = 2^{1-k} · π^{-(k+1)} · Γ(k)

For k = 12:

    L_∞^{can}(1) = 2^{-11} · π^{-13} · 11! ≈ 0.00671239369377...

**The actual zeta integral at ∞ is Ψ_∞(1) = h_∞(1) · L_∞^{can}(1),
NOT L_∞^{can}(1) alone.** Computing h_∞(1) is a separate task [OBL].

## Status: [OBL]

Main obstructions:
1. **[BLOCKER]** Ramified local factors Z_p(1) = h_p(1)·L_p^{can}(1) for each type
2. **[BLOCKER]** Normalization constant h_∞(1) for archimedean place
3. Consistent normalization of Haar measures and Whittaker functions across all places
4. Full archimedean derivation from local integral
