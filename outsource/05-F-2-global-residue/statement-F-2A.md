# F-2A: Diagonal Global Residue Positivity

## Desired Statement

Let π ⊂ GL₂(A_Q) be a unitary cuspidal automorphic representation with trivial
central character. Fix a Whittaker datum (N, ψ) and let W ∈ W(π, ψ), W ≠ 0.
Let W̄ denote the conjugate Whittaker function, satisfying W̄ ∈ W(π̃, ψ⁻¹).

For Φ ∈ S(A²) with Φ̂(0) > 0, define the **unfolded** Rankin–Selberg integral
(Jacquet–Shalika §4.5):

    Ψ(s, W, W, Φ) = ∫_{N(A)\GL₂(A)} W(g) · W̄(g) · Φ(e₂ g) · |det g|^s dg

where e₂ = (0, 1) is the standard basis vector.

**CRITICAL**: This is NOT the automorphic integral

    I(s, Φ, φ, φ') = ∫_{Z(A)G(Q)\G(A)} E(g, Φ, s) · φ'(g) · φ̄(g) dg

which lives on Z(A)G(Q)\G(A). The Ψ integral is the UNFOLDED version after
applying the Whittaker–Fourier expansion to E. It lives on N(A)\GL₂(A)
and involves Φ(e₂ g), NOT Φ(g).

**Theorem (Jacquet–Shalika 1981, §4.2–4.6 specialized)**:

    Res_{s=1} Ψ(s, W, W, Φ) = c_Q · Φ̂(0) · ∫|φ(g)|² dg > 0

where:
- c_Q > 0 is an explicit positive constant depending only on normalization
- |φ|² = ∫_{Z(A)G(Q)\G(A)} |φ(g)|² dg > 0 is the L²-norm of the automorphic form
- φ is the automorphic form associated to W via the Whittaker–Fourier expansion

## Proof strategy

Specialization of Jacquet–Shalika, "On Euler Products and the Classification of
Automorphic Representations I", American Journal of Mathematics 103(3) (1981),
499–558:

1. **Lemma 4.4**: The Eisenstein series integral I(s, Φ, φ, φ') has a simple pole
   at s = 1 when π = π'. The residue is proportional to Φ̂(0) · ∫|φ(g)|² dg.

2. **Unfolding**: The automorphic integral I(s) unfolds to Ψ(s) via the
   Whittaker–Fourier expansion of E(g, Φ, s). This is the key step:
   I(s, Φ, φ, φ') → Ψ(s, W', W, Φ).

3. **Lemma 4.6(i)**: When π' = π (same representation, not dual!), the Whittaker
   unfolding identifies L(s, π × π̃) as the incomplete L-function in Ψ.

4. **Norm-square positivity**: For W' = W, the integrand W(g)·W̄(g) = |W(g)|²,
   so the residue involves ∫|φ(g)|² dg > 0.

## Scope

- Narrowed to: unitary cuspidal π with trivial central character
- Archimedean: parameterized (not fixed to weight 12)
- No GRH required
- No L(1, π, Ad) > 0 assumed (residue is positive by norm-square)

## Status: [THM/REFEREED candidate]

This is a direct specialization of JS81. The citation must be:
Jacquet & Shalika, Am. J. Math. 103(3) (1981), 499–558.
