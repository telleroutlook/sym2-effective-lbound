# M-2: Mean Value Estimate — Rewritten

## Desired Statement

Let Π = sym²π be the symmetric-square lift of a non-CM/non-dihedral holomorphic
Hecke eigenform of weight k on SL₂(Z). Let a_Π(n) denote the Dirichlet
coefficients of L(s, Π).

**Corrected main term**: The second moment has leading order T log T, not T.

**Statement (conjectural/obligation)**: There exist explicit A_Π > 0, B_Π, δ > 0
such that:

    ∫_T^{2T} |L(½ + it, Π)|² dt = A_Π T log T + B_Π T + O_Π(T^{1-δ})

This is NOT a standard known theorem. The GL₃ t-aspect second moment with
power-saving error is at the research frontier (Dasgupta–Leung–Young 2024,
Pal 2022).

## Why the original was wrong

1. **Main term c_Π T is wrong**: The diagonal of |L(½+it,Π)|² produces
   Σ |a_Π(n)|²/n which diverges logarithmically (Rankin–Selberg pole at s=1).
   Therefore the leading term is T log T, not T.

2. **Infinite Dirichlet series expansion is wrong**: At Re s = ½ the Dirichlet
   series for L does NOT converge absolutely. Cannot unfold |L|² as a double
   sum without regularization. Must use AFE.

3. **coefficient-square series ≠ RS L-function**: The series Σ |a_Π(n)|² n^{-s}
   is NOT equal to L(s, Π × Π̃). They have related Euler factors but differ by
   local correction factors H_Π(s) = Π_p H_{Π,p}(s) that must be computed
   prime-by-prime.

## Scope

- Fixed Π (not a family), t-aspect (T → ∞)
- Non-CM/non-dihedral required for cuspidal Π
- The power-saving error O(T^{1-δ}) is NOT currently known for general GL₃

## Status: [OBL]

This is a research-level obligation, not a routine computation.
