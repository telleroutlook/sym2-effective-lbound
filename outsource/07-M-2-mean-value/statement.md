# M-2: Mean Value Estimate — Rewritten v4

## Desired Statement

Let Π = sym²π be the symmetric-square lift of a non-CM/non-dihedral holomorphic
Hecke eigenform of weight k on SL₂(Z). Let a_Π(n) denote the Dirichlet
coefficients of L(s, Π) in automorphic normalization.

**Statement [OBL]**: There exist explicit A_Π > 0, B_Π, δ > 0 such that:

    ∫_T^{2T} |L(½ + it, Π)|² dt = A_Π T log T + B_Π T + O_Π(T^{1-δ})

This is NOT a standard known theorem. The GL₃ t-aspect second moment with
power-saving error is at the research frontier.

## Why the original was wrong

1. **Main term c_Π T is wrong**: The diagonal of |L(½+it,Π)|² produces
   Σ |a_Π(n)|²/n which diverges logarithmically (Rankin–Selberg pole at s=1).
   Therefore the leading term is T log T, not T.

2. **AFE dual factor is WRONG**: The original wrote χ(Π) (a constant root
   number) in front of the dual sum. The correct dual factor is t-dependent.

3. **Local Euler correction H_{Π,p} is WRONG**: The original gave wrong
   formula that didn't match 1+O(x²). Correct:
   H_{Π,p}(x) = 1 - A_p²x² + 2(A_p²-1)x³ - A_p²x⁴ + x⁶

4. **Leading constant missing factor 2**: Each AFE half contributes
   (3/2)R_Π log T (from AFE length T^{3/2}). Together: A_Π = 3R_Π.

5. **Wrong normalization bridge**: L(½,Π) > 0 does NOT imply L(1,sym²f) > 0.

## v4 corrections (per reviewer verdict 2026-08-20)

1. **H_{Π,p}(1/p) > 0 proof fixed**: Now uses factorization
   H_{Π,p}(x) = (1-x)²(1+x+x²-A_px)(1+x+x²+A_px) with explicit
   positivity at endpoint x = 1/p (was open-interval gap).

2. **Step 2 diagonal corrected**: R_Π T log T → (3/2)R_Π T log T per half.
   The AFE length T^{3/2} introduces factor 3/2 from log(T^{3/2}).

3. **A_Π = 3R_Π conditional expanded**: Now requires three conditions:
   (a) precise diagonal-weight asymptotic, (b) cross terms o(T log T),
   (c) same-half off-diagonal o(T log T). Was only conditional on (b).

4. **FE factor normalization**: Added ε_Π, q_Π (level one: ε_Π=1, q_Π=1).

## Status: [OBL]

This is a research-level obligation, not a routine computation.
