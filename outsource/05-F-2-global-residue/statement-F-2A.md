# F-2A: Diagonal Global Residue Positivity (v4)

**Status**: [OBL] — CONDITIONAL after reviewer verdict 2026-08-20

## Desired Statement

Let π ⊂ GL₂(A_Q) be a unitary cuspidal automorphic representation with trivial
central character. Fix a Whittaker datum (N, ψ).

**Quantifier corrected (v4):** Let φ be a nonzero cuspidal automorphic vector
in the space of π, and let W_φ ∈ W⁰(π; ψ) be its global Whittaker function
(i.e., the unique Whittaker function associated to φ by Fourier–Whittaker
expansion; JS81 §4.5, pp. 549–550).

**NOT**: "for any W ∈ W(π, ψ), W ≠ 0" — the ambient Whittaker space W(π, ψ)
is larger than the space W⁰(π; ψ) spanned by Whittaker functions of cuspidal
automorphic vectors. The residue formula requires W = W_φ ∈ W⁰(π; ψ).

For Φ ∈ S(A²) with Φ̂(0) > 0, define the **unfolded** Rankin–Selberg integral
(Jacquet–Shalika §4.5):

    Ψ(s, W_φ, W_φ, Φ) = ∫_{N(A)\GL₂(A)} W_φ(g) · W̄_φ(g) · Φ(e₂ g) · |det g|^s dg

where e₂ = (0, 1) is the standard basis vector.

**Theorem (Jacquet–Shalika 1981, specialized):**

    Res_{s=1} Ψ(s, W_φ, W_φ, Φ) = c_Q · Φ̂(0) · ∫|φ(g)|² dg > 0

where:
- c_Q > 0 is an explicit positive constant depending only on normalization
- |φ|² = ∫_{Z(A)G(Q)\G(A)} |φ(g)|² dg > 0 is the L²-norm of the automorphic form
- φ is the automorphic form whose Whittaker function is W_φ

## Proof strategy

Specialization of Jacquet–Shalika, "On Euler Products and the Classification of
Automorphic Representations I", American Journal of Mathematics 103(3) (1981),
499–558:

**Citation chain (corrected, v4 — NOT "Lemma 4.4"):**

1. **§4.3 eq. (2)** (p. ~548): The automorphic integral I(s, Φ, φ, φ') has a
   simple pole at s = 1 when π = π'. The residue is proportional to
   Φ̂(0) · ∫|φ(g)|² dg.

2. **§4.5 eq. (5)** (p. ~550): The unfolding identity I(s) = Ψ(s, W', W, Φ)
   via Whittaker–Fourier expansion of E(g, Φ, s).

3. **§4.6(i)** (p. ~551): When π' = π and W' = W_φ ∈ W⁰(π; ψ), the pole of
   Ψ(s) at s = 1 follows from §4.3 + §4.5, with positive residue by
   norm-square W_φ(g)·W̄_φ(g) = |W_φ(g)|².

**NOT** "Lemma 4.4" — Lemma 4.4 gives a pole criterion; the actual residue
formula comes from the chain §4.3(2) → §4.5(5) → §4.6(i).

## Scope

- Narrowed to: unitary cuspidal π with trivial central character
- Archimedean: parameterized (not fixed to weight 12)
- No GRH required
- No L(1, π, Ad) > 0 assumed (residue is positive by norm-square)

## Status: [OBL — CONDITIONAL]

Core mathematical argument verified by reviewer (2026-08-20) as correct.
Two precision issues remain:
1. ✅ Fixed: W quantifier → W_φ ∈ W⁰(π; ψ)
2. ✅ Fixed: Citation chain → §4.3(2) + §4.5(5) + §4.6(i)
After v4 corrections, F-2A is ready for PASS/REFEREED.
