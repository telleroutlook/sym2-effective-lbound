# GL₃ Shifted Convolution — Limitations

## What this package does

This package describes a **research-level obligation**: the GL₃ shifted
convolution estimate for fixed Π at the critical shift scale.

## What this package does NOT do

- Does NOT contain a proof
- Does NOT contain numerical computation
- Does NOT contain any [THM]-labelled result
- Does NOT advance beyond the current state of the art

## Current state of the art

### Upper bounds (not asymptotics)

| Source | Bound | Method | Scope |
|--------|-------|--------|-------|
| DLY 2024 | ∫\|L\|² ≪ T^{4/3+ε} | Hybrid | Holomorphic GL₃ |
| Pal 2025 | ∫\|L\|² ≪ T^{3/2-3/32+ε} | Spectral | Hecke–Maaß GL₃ |
| Trivial | S(h,N) ≪ N^{1+ε} | Cauchy–Schwarz | Any GL₃ |

None of these give an asymptotic with main term + error.

### The gap

The estimate needed for M-1/M-2 requires:

1. **Main term identification**: C_Π(h) = Σ_{d|h} (multiplicative function of d)
   This is formal/algebraic and CAN be computed.

2. **Power-saving error**: S(h,N) = C_Π(h)·N + O(N^{1-δ}) for some δ > 0.
   This is the hard part. No δ > 0 is known for fixed Π.

3. **Uniformity in Π**: The implied constant must be effective enough
   for the downstream application in M-1/M-2.

## Why this is hard

### GL₃ Kloosterman sums

The GL₃ Kuznetsov/Voronoi formula involves GL₃ Kloosterman sums
S₃(m,n;c). The best known bound is:

    |S₃(m,n;c)| ≪ c^{3/2+ε}

This is the trivial bound (size of the sum). No non-trivial cancellation
is known in general. For comparison, GL₂ Kloosterman sums satisfy the
Weil bound |S₂(m,n;c)| ≤ d₃(c) · c^{1/2+ε}, which is essential for
GL₂ analytic number theory.

### Spectral theory

The GL₃ spectral theory is far less developed than GL₂:

- The Petersson formula involves GL₃ Kloosterman sums (which are not understood)
- The spectral sums are not absolutely convergent
- The Rankin–Selberg method gives upper bounds but not asymptotics
- The "fundamental lemma" for GL₃ is not as strong as for GL₂

### Critical scale

The shift h ≍ T^{1/2} is the "critical scale" where:
- For h ≫ T^{1/2}: the off-diagonal is smaller (known)
- For h ≪ T^{1/2}: the main term dominates (known)
- For h ≍ T^{1/2}: main term ≈ error, no separation (UNKNOWN)

## What would solve this

A breakthrough in one of:

1. **GL₃ Kloosterman sum bounds**: Non-trivial bounds for S₃(m,n;c)
   beyond the trivial c^{3/2+ε}. Even a saving of c^{ε} would help.

2. **GL₃ spectral theory**: Absolute convergence of GL₃ spectral sums,
   or a "fundamental lemma" as strong as the GL₂ case.

3. **Moment methods**: Direct bound on ∫|L(½+it,Π)|²dt without
   individual shifted convolution estimates (e.g., using the
   approximate functional equation more cleverly).

4. **Hybrid methods**: Combining GL₃ Voronoi with GL₂ spectral theory
   in a way that gives the missing cancellation.

## Status: [OBL]

This is the fundamental analytic obstruction blocking the explicit
lower bound project. No proof is known or expected in the near future.
