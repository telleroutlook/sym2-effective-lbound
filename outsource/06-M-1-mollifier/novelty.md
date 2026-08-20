# Novelty — M-1 Rewritten v3

## What is new in v3 (correcting v2)

7. **Fixed Step D**: v2 wrote a single quadratic form for I(T). The actual
   |M·L|² has four blocks (I_{++}, I_{--}, I_{+-}, I_{-+}) with different
   weights, gamma phases, and convolution structures.

8. **Fixed coefficient bound**: v2 wrote unweighted ∑|c_X(q)|² ≪ Q^ε.
   Corrected to weighted ∑|c_X(q)|²/q ≪ Q^ε.

9. **Fixed shift scale**: v2 wrote h ≲ T^{1/2}. Corrected to H ≲ T^{1/2+θ},
   reflecting the expanded geometry from mollification.

10. **Fixed D_X interpretation**: Coefficient difference, not truncation error.

11. **Fixed "only option"**: Canonical natural choice, not unique.

12. **Fixed T·log T scale**: Conjectural, not proved.

## What is new in v2 (correcting v1)

1. **Deleted wrong bridge lemma**: I(T) ≥ c₀T ⟹ L(½,Π) > 0 is FALSE.
2. **Deleted wrong normalization**: L(½,Π) > 0 does not imply L(1,sym²f) > 0.
3. **Corrected main term scale**: For reciprocal mollifier M·L ≈ 1, I(T) ≍ T.
4. **Deleted algebraically vacuous squarefree lemma**.
5. **Corrected AFE structure**: Dual factor is t-dependent X_Π(t).
6. **Corrected convolution structure**: c_X(q) = Σ_{mr=q} b_m a_Π(r).

## What is NOT new

- The mollifier strategy itself is classical
- The AFE-based reduction is standard
- The identification of GL₃ shifted-convolution as the obstruction is known

## Adjacent recent work (2026)

- Conrey–Kwan–Lin–Turnage-Butterbaugh (2026): PGL₃ Dirichlet-twist family
  averaged Dirichlet-polynomial twisted mean-square asymptotic (arXiv:2607.00282).
  Allows mollifiers but averages over character twists q ≤ Q; does NOT
  specialize to fixed Π, pure t-aspect. Does not close M-1.
