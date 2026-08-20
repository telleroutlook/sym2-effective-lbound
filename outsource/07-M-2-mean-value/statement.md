# M-2: Mean Value Estimate — Rewritten v2

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
   number) in front of the dual sum. The correct dual factor is:

       X_Π(s) = N^{1-2s} · L_∞(Π, 1-s) / L_∞(Π, s)

   which depends on t through the gamma ratios. For level one, the global
   sign is +1, but the t-dependent gamma ratio is NOT constant.

3. **Local Euler correction H_{Π,p} is WRONG**: The original proposed
   H_{Π,p}(x) = Π_i (1 - |α_i|²x)⁻¹ which gives 1 + 3x + O(x²). But
   D_{Π,p}(x) = L_p(Π×Π̃,x) · H_{Π,p}(x) requires H_{Π,p}(x) = 1 + O(x²)
   (matching coefficient-square series to RS at order x¹). The correct
   formula for level-one symmetric-square is:

       H_{Π,p}(x) = 1 - A_p² x² + 2(A_p² - 1) x³ - A_p² x⁴ + x⁶

   where A_p = a_Π(p). This satisfies H_{Π,p}(x) = 1 + O(x²) as required.

4. **Leading constant missing factor 2**: The AFE has TWO halves (primary
   and dual). Each diagonal contributes (3/2)R_Π log T. Together: A_Π = 3R_Π,
   NOT (3/2)R_Π × "archimedean factor".

5. **Wrong normalization bridge**: The original implied L(½,Π) > 0 ⟹
   L(1,sym²f) > 0. This requires specifying the normalization shift.

## Scope

- Fixed non-CM/non-dihedral Π, t-aspect (T → ∞)
- Level one (SL₂(Z)): all primes unramified, no bad-prime factors needed
- The power-saving error O(T^{1-δ}) is NOT currently known for general GL₃

## Status: [OBL]

This is a research-level obligation, not a routine computation.
