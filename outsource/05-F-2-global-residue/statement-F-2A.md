# F-2A: Diagonal Global Residue Positivity

## Desired Statement

Let π ⊂ GL₂(A_Q) be a unitary cuspidal automorphic representation with trivial
central character. Fix a Whittaker datum (N, ψ) and let W ∈ W(π, ψ), W ≠ 0.
Let conjugate(W) denote the conjugate-dual Whittaker function, satisfying
conjugate(W) ∈ W(π̃, ψ⁻¹).

For Φ ∈ S(A^n) with Φ̂(0) > 0, define the global Rankin–Selberg integral:

    Ψ(s, W, Φ) = ∫_{N(A)G(Q)\G(A)} W(g) · conj(W(g)) · Φ(g) · |det g|^s dg

**Theorem (Jacquet–Shalika 1981, §4.2–4.6 specialized)**:

    Res_{s=1} Ψ(s, W, Φ) = c_Q · Φ̂(0) · |φ|² > 0

where:
- c_Q > 0 is an explicit positive constant depending only on Q (normalization)
- |φ|² = ∫_{Z(A)G(Q)\G(A)} |φ(g)|² dg > 0 is the L²-norm of the automorphic form
- φ is the automorphic form associated to W via the Whittaker–Fourier expansion

## Proof strategy

This is essentially a specialization of Jacquet–Shalika (1981), "Euler products for
the general linear group", Ann. of Math. 114, pp. 459–512:

1. **Lemma 4.4**: The Eisenstein series integral produces a simple pole at s = 1
   with residue proportional to Φ̂(0) · ∫|φ(g)|² dg. The key is that for π = π',
   the Eisenstein series E(g, f_s) has a simple pole, and the residue is a positive
   constant times the squared L²-norm of the residual representation.

2. **Lemma 4.6(i)**: When π' = π (same representation, not dual!), the Whittaker
   unfolding identifies the Rankin–Selberg L-function L(s, π × π̃) = L(s, π × π)
   as the incomplete L-function in the integral. At s = 1, the pole of ζ(s)
   produces the simple pole of Ψ.

3. **Norm-square positivity**: The residue involves ∫|φ(g)|² dg > 0 for any nonzero
   automorphic form φ. This is a consequence of the positive-definite Haar measure.

## Scope

- Narrowed to: unitary cuspidal π with trivial central character
- Archimedean: parameterized (not fixed to weight 12)
- No GRH required
- No L(1, π, Ad) > 0 assumed (the residue is positive by norm-square, not by adjoint)
