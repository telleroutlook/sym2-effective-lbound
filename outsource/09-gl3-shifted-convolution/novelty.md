# GL₃ Shifted Convolution — Novelty

## What is new in this package

1. **09-B' compatibility check**: Identifying that Wang 2026 covers our
   holomorphic symmetric-square case at the required scale, and that the
   remaining task is a technical smooth-weight transfer verification.

2. **Corrected DLY mechanism**: Voronoi → Poisson → delta → norm → duality →
   twisted Kloosterman → Weil → Gallagher large sieve. NOT GL₃ spectral
   expansion or GL₃ large sieve.

3. **Corrected DLY Theorem 1.2**: N^{4/3+ε}/H^{1/3} + √H·N^{1+ε}
   (previous version had √H·N^ε + N^{1+ε}, missing N in second term).

4. **Corrected dependency logic**: Wang 2026 + 09-B' transfer is sufficient
   for M-1/M-2, not necessary. 09-A (individual) is a separate, stronger
   research problem.

## Previous errors corrected (round 3)

| Error | Correction |
|-------|-----------|
| DLY Theorem 1.2: √H·N^ε + N^{1+ε} | √H·N^{1+ε} |
| "GL₃ spectral expansion / GL₃ large sieve" | Gallagher hybrid character large sieve |
| "cohomological = finite-dimensional at infinity" | (deleted; not used in proof mechanism) |
| "Pal is current best for degree-3" | DLY is stronger (T^{1.333} vs T^{1.466}) |
| 09-B "still open" without Wang 2026 | Wang 2026 covers our scale; 09-B' is transfer check |
| C_Π(h)N in witness/README.md | (deleted) |

## What is NOT new

- Wang 2026's averaged shifted convolution result
- DLY's second moment and shifted convolution results
- The Kloosterman sum bounds (classical Weil, DLY Lemma 2.9)
- The Gallagher large sieve inequality
