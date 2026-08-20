# F-2A: Diagonal Global Residue Positivity — Proof

## Mathematical content

### Correct integral formula

The Jacquet–Shalika (1981) local Rankin–Selberg integral is:

    Ψ(s, W', W, Φ) = ∫_{N(A)G(Q)\G(A)} W'(g) · conj(W(g)) · Φ(εg) · |det g|^s dg

**Critical correction**: The integrand contains conj(W(g)), NOT W̃(g). This produces
a norm-square when W' = W, which is essential for the positivity argument.

### Why the original F-2 was wrong

The original package wrote:

    Res_{s=1} Ψ(s, W, W̃, Φ) = Φ̂(0) · κ_F · L(1, π, Ad) · |W|²

This has two fatal errors:

1. **Scaling contradiction**: Ψ is linear in W̃, but |W|² is independent of W̃.
   Multiplying W̃ by i multiplies the LHS by i while RHS is unchanged.

2. **Variable mismatch**: The original claimed the residue depends on independent
   W and W̃, but the correct formula uses W and conj(W) (same vector).

### Correct residue formula

By JS81 §4.2-4.6, for W' = W:

    Res_{s=1} Ψ(s, W, W, Φ) = c_Q · Φ̂(0) · ∫|φ(g)|² dg

where c_Q > 0 is explicit, and the integral is positive by construction.

### Why this is [THM/REFEREED]

This is NOT a new theorem. It is a direct specialization of:
- Jacquet & Shalika, "Euler products for the general linear group", Ann. Math. 114 (1981), 459–512
- Specifically: Lemma 4.4 (Eisenstein pole) + Lemma 4.6(i) (Whittaker unfolding)

The specialization is: take π' = π (same representation), W' = W (same vector),
Φ̂(0) > 0 (test function with positive transform at 0).

### Dependencies

- **Source-backed**: JS81 Lemma 4.4, Lemma 4.6(i) (verified against original text)
- **No GRH required**
- **No L(1, π, Ad) > 0 required** (residue is positive by norm-square, not by adjoint)

## Why this closes

F-2A establishes that the diagonal global residue is strictly positive, using only:
1. π is cuspidal (given)
2. W ≠ 0 (by choice)
3. Φ̂(0) > 0 (by choice)
4. The Haar measure is positive-definite (by construction)

This is the "easy part" that the original F-2 obscured by introducing independent W̃.
