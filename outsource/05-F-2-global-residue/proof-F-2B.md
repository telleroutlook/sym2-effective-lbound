# F-2B: Exact Euler-Factor Extraction — Proof (v4)

## Pure-tensor factorization

Choose decomposable vectors W = ⊗_v W_v, W' = ⊗_v W'_v, Φ = ⊗_v Φ_v.
Then by the pure-tensor hypothesis + product Haar measure + absolute convergence/Fubini:

    Ψ(s, W_φ, W_φ, Φ) = ∏_v Ψ_v(s, W_v, W_v, Φ_v)

**This factorization requires the pure-tensor hypothesis.** For general
(non-factorizable) vectors, Ψ(s) is a finite sum of such products.

**Attribution (corrected):** JS81 §4.7写出 decomposable
data 时的 product factorization，依赖 restricted tensor product + product
measure + absolute convergence/Fubini. NOT "by strong approximation".

## Unramified places (good primes)

For p ∤ N, with inverse Satake parameters α_p⁻¹, β_p⁻¹ for π̃_p:

    L_p(s, π_p × π̃_p) = [(1 - p⁻ˢ)²(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

For trivial central character (α_p β_p = 1):

    = [(1 - p⁻ˢ)²(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

This equals ζ_p(s) · L_p(s, π, Ad) where:

    L_p(s, π, Ad) = [(1 - p⁻ˢ)(1 - α_p β_p⁻¹ p⁻ˢ)(1 - β_p α_p⁻¹ p⁻ˢ)]⁻¹

**NOT** the single-factor formula from the original. The adjoint representation
is 3-dimensional: parameters {1, αβ⁻¹, βα⁻¹}.

**Local integral attribution (corrected):** The local integral Ψ_v is a
JS/Rankin–Selberg type Whittaker local integral (JS81 §4.7, referencing
Sections 1 and 3 of JS81), NOT "the local Godement–Jacquet integral".

## Ramified places (bad primes) [BLOCKED]

For p | N, the local integral Ψ_p depends on the local newvector type.
**This is the primary blocker for F-2B.**

### Steinberg twist (conductor exponent 1)

The local newvector W_p is a Steinberg function. The local integral:

    Ψ_p(s, W_p, W_p, Φ_p) = Z_p(s)

**[OBL]** — no explicit Z_p(1) formula. Expected structure:
Z_p(s) involves local L-factor for Steinberg representation twisted by ψ_p,
but the exact formula depends on choice of Φ_p and normalization.

### Ramified principal series (conductor exponent ≥ 1)

**[OBL]** — no explicit Z_p(1) formula.

### Supercuspidal (conductor exponent ≥ 2)

**[OBL]** — no explicit Z_p(1) formula.

**Each type requires:**
1. Explicit computation of W_p from Casselman's newvector formula
2. Choice of Φ_p ∈ C_c^∞(GL₂(Q_p))
3. Haar measure normalization on GL₂(Q_p) and N(Q_p)
4. Direct evaluation of Ψ_p(1) = ∫_{N(Q_p)\GL₂(Q_p)} |W_p(g)|² Φ_p(e₂ g) |det g| dg
5. Proof that Ψ_p(1) ≠ 0
6. Quantitative lower bound |Z_p(1)| ≥ c_p > 0

## Archimedean place

### Derivation from real Weil-group parameter

For π_∞ = holomorphic discrete series of weight k, the archimedean Langlands
parameter is the 2-dimensional real Weil-group representation:

    ρ_{k-1} = Ind_{W_ℂ}^{W_ℝ}((z/|z|)^{k-1})

The Rankin–Selberg local L-factor at ∞ for ρ_{k-1} ⊗ ρ_{k-1}^∨ decomposes as:

    L_ℝ(s, ρ_{k-1} ⊗ ρ_{k-1}^∨) = L_ℝ(s) · L_ℝ(s+1) · L_ℂ(s+k-1)

**Decomposition sketch:**

The induction Ind_{W_ℂ}^{W_ℝ}(χ) with χ(z) = (z/|z|)^{k-1} has:

    Ind(χ) ⊗ Ind(χ)^∨ ≅ Ind(χ ⊗ χ̄) ⊕ Ind(χ ⊗ χ̄⁻¹)
                       ≅ Ind(1) ⊕ Ind((z/|z|)^{2(k-1)})

where:
- Ind(1) = L_ℝ(s) · L_ℝ(s+1) [degree 2 = 1+1]
- Ind((z/|z|)^{2(k-1)}) = L_ℂ(s+k-1) [degree 2]

This gives total degree 4 = 2+2.

**The derivation requires computing the local integral Ψ_∞ directly with:**
- Specified W_∞ (holomorphic discrete series Whittaker function)
- Specified Φ_∞ ∈ S(R²) (Schwartz function)
- Specified Haar measure on GL₂(R) and N(R)

**This full computation is [OBL]** — the above is a consistency argument,
not a derivation from the local integral.

### Normalization

The local integral Ψ_∞(s) is expected to satisfy:

    Ψ_∞(s) = c_∞(1) · L_ℝ(s, ρ_{k-1} ⊗ ρ_{k-1}^∨)

for an explicit constant c_∞(1) depending on normalization of W_∞, Φ_∞,
and Haar measure. **Computing c_∞(1) is [OBL].** Ideally one normalizes
so that c_∞ = 1.

### Numerical evaluation at s = 1

    Z_∞(1) = L_ℝ(1) · L_ℝ(2) · L_ℂ(k)

where:
- L_ℝ(1) = π^{-1/2} Γ(1/2) = 1
- L_ℝ(2) = π^{-1} Γ(1) = π^{-1}
- L_ℂ(k) = 2(2π)^{-k} Γ(k)

Therefore:

    Z_∞(1) = 2^{1-k} · π^{-(k+1)} · Γ(k)

For k = 12:

    Z_∞(1) = 2^{-11} · π^{-13} · 11! ≈ 0.00671239369377...

**Previous error (v2):** 2π^{-k-1}Γ(k), differing by 2^k = 4096 for k=12.

## Status: [OBL]

Main obstructions:
1. **[BLOCKER]** Ramified local factors Z_p(1) for Steinberg/ramified principal/supercuspidal
2. Consistent normalization of Haar measures and Whittaker functions
3. Full archimedean derivation from local integral
4. Normalization constant c_∞(1) for Ψ_∞ = c_∞ · L_∞(s)
