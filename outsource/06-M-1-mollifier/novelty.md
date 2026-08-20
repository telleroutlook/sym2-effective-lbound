# Novelty — M-1 v4

## What is new in v4 (correcting v3)

1. **Fixed AFE notation**: B(s) sum variable changed from s to r (avoids
   collision with complex variable s in the AFE expansion).

2. **Fixed FE factor normalization**: X_Π(s) = ε_Π q_Π^{1/2-s} L_∞(1-s,π̃)/L_∞(s,Π)
   with |X_Π(½+it)| = 1. Was missing root number ε_Π and conductor q_Π.

3. **Fixed I_{--} gamma phase**: Since |X_Π(½+it)| = 1 on the critical line,
   I_{--} = |M·X·B|² = |M|²|B|² has NO gamma oscillation. The gamma-phase
   oscillation is concentrated in the two cross blocks I_{+-} and I_{-+} only.

4. **Tightened literature**: DLY/Pal listed as upper-bound context, not
   direct dependencies. Neither solves the fixed-Π t-aspect mollified moment.

5. **D_X moved to aside**: Squarefree proxy discussion no longer a main
   proof dependency.

## What is new in v3 (correcting v2)

6. **Fixed Step D**: Four blocks (I_{++}, I_{--}, I_{+-}, I_{-+}) instead of
   single quadratic form.
7. **Fixed coefficient bound**: Weighted Σ|c_X(q)|²/q ≪ Q^ε.
8. **Fixed shift scale**: H ≲ T^{1/2+θ}.
9. **Fixed D_X interpretation**: Coefficient difference, not truncation error.
10. **Fixed T·log T scale**: Conjectural, not proved.

## What is new in v2 (correcting v1)

11. **Deleted wrong bridge lemma**: I(T) ≥ c₀T ⟹ L(½,Π) > 0 is FALSE.
12. **Deleted wrong normalization**: L(½,Π) > 0 does not imply L(1,sym²f) > 0.
13. **Corrected main term scale**: I(T) ≍ T for reciprocal mollifier.
14. **Deleted algebraically vacuous squarefree lemma**.

## What is NOT new

- The mollifier strategy itself is classical
- The AFE-based reduction is standard
- The identification of GL₃ shifted-convolution as the obstruction is known

## Adjacent recent work (2026, context only)

- DLY (2024): upper bound T^{4/3+ε} for unmollified GL₃ moment
- Pal (IMRN 2025): upper bound T^{3/2-3/32+ε} for Maaß SL(3,Z)
- CKLT (2026): PGL₃ Dirichlet-twist family (arXiv:2607.00282)

None of these solve the fixed-Π t-aspect mollified moment required by M-1.
