# GL₃ Shifted Convolution for Fixed Π — Proof

**Status:** RESEARCH GAP (not a theorem; no proof exists).

## §1. Problem decomposition

The GL₃ shifted convolution for fixed Π arises from the AFE expansion
of |L(½+it, Π)|². After squaring the two-term AFE and integrating over
t ∈ [T, 2T], the off-diagonal contributions involve:

### Same-half off-diagonal (I_{++}^{off}, I_{--}^{off})

    Σ_{r≠r'} a_Π(r) ā_Π(r') · kernel(r, r', t)

After dyadic decomposition and stationary phase, the critical contribution
comes from pairs (r, r') with |r - r'| ≍ h (the shift), giving a shifted
convolution sum:

    Σ_n a_Π(n) ā_Π(n+h) · (smooth weight)

### Cross terms (I_{+-}, I_{-+})

    Σ_{r,s} a_Π(r) ā_Π(s) · X_Π(t) · kernel(r, s, t)

These involve the t-dependent gamma phase X_Π(t) and require separate
analysis (stationary phase in t).

## §2. What is known

### GL₃ Kuznetsov formula (Iwaniec, Goldfeld)

The GL₃ Voronoi summation formula provides a transformation for sums
Σ_n a_Π(n) e(nα) that can be applied to shifted convolutions. The
resulting dual sum involves GL₃ Kloosterman sums.

### Current bounds (no power-saving)

- **Trivial bound**: S(h, N) ≪ N^{1+ε} (from |a_Π(n)| ≤ d₃(n) ≪ n^ε)
- **Large sieve**: S(h, N) ≪ (N/h^{1/2} + h^{1/2}) N^ε
- **DLY upper bound**: ∫|L|² ≪ T^{4/3+ε} (not an asymptotic)

### The obstruction

For the power-saving estimate S(h, N) = C_Π(h)·N + O(N^{1-δ}), one needs:

1. **Main term identification**: C_Π(h) from the Rankin–Selberg decomposition
   of L(s, Π × Π̃). This is formal/algebraic and CAN be done.

2. **Off-diagonal cancellation**: The error term requires cancelling the
   oscillatory kernel against a_Π(n)ā_Π(n+h). This is the hard part.

3. **Uniformity in h**: The shift h ≍ T^{1/2} is at the "critical scale"
   where the main term and error are comparable. For h ≫ T^{1/2}, the
   sum is smaller; for h ≪ T^{1/2}, the main term dominates.

## §3. Possible approaches

### Approach A: GL₃ Kuznetsov + stationary phase

Apply GL₃ Voronoi to the shifted sum, then use stationary phase on the
dual integral. The GL₃ Kloosterman sums contribute a main term from
the identity orbit, and the error from the non-identity orbits.

**Obstacle**: The GL₃ Kloosterman sums are not well-understood enough
to give power-saving cancellation. The best known bound is
|S₃(m,n;c)| ≪ c^{3/2+ε} (trivial), which is insufficient.

### Approach B: Spectral decomposition over GL₃

Expand the shifted convolution spectrally over GL₃ automorphic forms.
The main term comes from the identity representation; the error from
the cuspidal spectrum.

**Obstacle**: The spectral theory of GL₃ is far less developed than GL₂.
The GL₃ Petersson formula involves Kloosterman sums, and the spectral
sums are not absolutely convergent.

### Approach C: Hybrid bounds (DLY approach)

Use the "hybrid" bound: bound the shifted sum in a range where both
the shift h and the length N appear. This gives sub-optimal but
non-trivial bounds.

**Status**: DLY achieve T^{4/3+ε} using this approach. This is the
current state of the art but does NOT give the power-saving needed
for M-1/M-2.

### Approach D: Moment method + mollifier (M-1 route)

Instead of bounding individual shifted convolutions, use the mollifier
to average over shifts. This converts the problem to bounding the
mollified second moment, which has different (potentially easier)
analytic structure.

**Status**: This is the approach of M-1, but the mollified moment
itself requires shifted-convolution bounds for the error terms.

## §4. What would constitute a proof

A proof would need to:

1. Establish the GL₃ shifted convolution estimate with power-saving
   error for fixed Π at the critical shift scale h ≍ T^{1/2}.

2. Show that the implied constant is effective (or at least uniform
   enough for the downstream applications).

3. Handle the archimedean place correctly (the gamma phase X_Π(t)
   in the cross terms).

## §5. Dependencies

This package depends on:
- **03-partial-sum-bound**: The Friedlander–Iwaniec bound on GL₂
  partial sums (used in the AFE expansion)
- **05-F-2-global-residue**: The global residue formula (for the
  main term C_Π(h))

This package blocks:
- **06-M-1-mollifier**: The mollified second moment estimate
- **07-M-2-mean-value**: The unmollified second moment estimate

## Status: [OBL]

No proof exists. This is the fundamental research gap blocking
the explicit lower bound project at the analytic level.
