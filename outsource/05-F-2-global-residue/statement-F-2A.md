# F-2A: Diagonal Global Residue Positivity (v5)

**Status**: [THM/REFEREED] — PASS (verified 2026-08-20)

## Statement

Let π ⊂ GL₂(A_Q) be a unitary cuspidal automorphic representation with trivial
central character ω = 1. Fix a Whittaker datum (N, ψ).

Let φ be a nonzero cuspidal automorphic vector in the space of π, and let
W_φ ∈ W⁰(π; ψ) be its global Whittaker function (JS81 §4.5, pp. 549–550).

For Φ ∈ S(A²) with Φ̂(0) > 0, define the unfolded Rankin–Selberg integral
(Jacquet–Shalika §4.5):

    Ψ(s, W_φ, W_φ, Φ) = ∫_{N(A)\GL₂(A)} W_φ(g) · W̄_φ(g) · Φ(e₂ g) · |det g|^s dg

**Theorem (Jacquet–Shalika 1981, specialized):**

    Res_{s=1} Ψ(s, W_φ, W_φ, Φ) = c_Q · Φ̂(0) · ∫|φ(g)|² dg > 0

where:
- c_Q > 0 is an explicit positive constant depending only on normalization
- |φ|² = ∫_{Z(A)G(Q)\G(A)} |φ(g)|² dg > 0 is the L²-norm of the automorphic form

## Proof strategy

Specialization of Jacquet–Shalika, "On Euler Products and the Classification of
Automorphic Representations I", American Journal of Mathematics 103(3) (1981),
499–558.

**Citation chain:**

1. **§4.3 eq. (2)** (p. ~548): The automorphic integral I(s, Φ, φ, φ') has a
   simple pole at s = 1 when π = π'. The residue is proportional to
   Φ̂(0) · ∫|φ(g)|² dg.

2. **§4.5 eq. (5)** (p. ~550): The unfolding identity I(s) = Ψ(s, W', W, Φ)
   via Whittaker–Fourier expansion of E(g, Φ, s).

3. **§4.6(i)** (p. ~551): When π' = π and W' = W_φ ∈ W⁰(π; ψ), the pole of
   Ψ(s) at s = 1 follows from §4.3 + §4.5, with positive residue by
   norm-square W_φ(g)·W̄_φ(g) = |W_φ(g)|².

## Scope

- Trivial central character: ω = 1
- Archimedean: parameterized (not fixed to weight 12)
- No GRH required
- No L(1, π, Ad) > 0 assumed (residue is positive by norm-square)

## Why this closes

F-2A is a direct specialization of JS81 with:
- π' = π (diagonal condition)
- W' = W_φ ∈ W⁰(π; ψ) (same Whittaker vector, producing norm-square)
- Φ̂(0) > 0 (by choice)

The residue is strictly positive by construction. The formula
Res_{s=1} Ψ = c_Q · Φ̂(0) · ∫|φ|² dg > 0 is the complete result.
