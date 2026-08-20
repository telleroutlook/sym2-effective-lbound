# F-2A: Diagonal Global Residue Positivity — Proof

## Mathematical content

### Two distinct integrals

JS81 (Jacquet–Shalika, Am. J. Math. 103(3) (1981)) defines two related but distinct integrals:

1. **Automorphic integral** (before unfolding):

       I(s, Φ, φ, φ') = ∫_{Z(A)G(Q)\G(A)} E(g, Φ, s) · φ'(g) · φ̄(g) dg

   This lives on Z(A)G(Q)\G(A) and involves the Eisenstein series E.

2. **Unfolded integral** (after Whittaker–Fourier expansion):

       Ψ(s, W', W, Φ) = ∫_{N(A)\GL₂(A)} W'(g) · W̄(g) · Φ(e₂ g) · |det g|^s dg

   This lives on N(A)\GL₂(A) and involves Φ(e₂ g), NOT Φ(g).

The unfolding identity I(s) → Ψ(s) is the key step (JS81 §4.3).

### Correct residue formula

By JS81 Lemma 4.4 + Lemma 4.6(i), for W' = W:

    Res_{s=1} Ψ(s, W, W, Φ) = c_Q · Φ̂(0) · ∫|φ(g)|² dg

where c_Q > 0 is explicit. The integral ∫|φ(g)|² dg > 0 for any nonzero φ.

### Why the original was wrong

1. **Wrong quotient space**: Original used N(A)G(Q)\G(A, should be N(A)\GL₂(A)
2. **Wrong test function**: Original used Φ(g), should be Φ(e₂ g)
3. **Wrong citation**: The wrong journal was cited (see limitations.md).
   Correct: Am. J. Math. 103(3) (1981), 499–558.
4. **Conflated integrals**: Original mixed up I(s) and Ψ(s)

### Dependencies

- JS81 Lemma 4.4 (Eisenstein pole): Am. J. Math. 103(3) (1981), 537–538
- JS81 Lemma 4.6(i) (Whittaker unfolding): Am. J. Math. 103(3) (1981), 543–544
- Norm-square positivity: standard

## Why this closes

F-2A is a direct specialization of JS81 with:
- π' = π (diagonal condition)
- W' = W (same vector, producing norm-square)
- Φ̂(0) > 0 (by choice)

The residue is strictly positive by construction.
