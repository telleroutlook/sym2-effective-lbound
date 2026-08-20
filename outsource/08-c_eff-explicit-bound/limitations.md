# Limitations — c_eff v3

## Scope

- f ∈ S_k^new(Γ₀(p)), k ≥ 2, p prime
- Trivial central character
- f non-dihedral (non-CM)
- Bound: L(1, sym² f) ≥ c₀/log(kp+1)

## What is NOT achieved

- No numerical c₀ is computed
- No interval [a, b] with a > 0 is certified
- No machine-readable witness exists
- The explicit constant extraction (Stage D) is [OBL]
- All constants c_ZF, A_0, B, c(B), C, c_eff are formulas, not numbers

## Corrected from v2

1. **Stage C parameter chain rewritten**: v2 wrote δ = c₀/log K
   then R⁻¹ ≪ log(1/δ), which is wrong (HL Prop 1.1 uses M, not δ).
   Correct: set M = K^C with C ≥ max(A_0, c_ZF⁻¹), giving
   R⁻¹ ≤ c(B)·C·log K.

2. **Positivity reason corrected**: v2 claimed non-negative coefficients
   follow from "positivity of symmetric-square coefficients" — wrong
   (L(sym²f) coefficients are not generally non-negative).
   Correct: A(s) = ζ(s)L(s,F) has non-negative coefficients because
   each local factor (1−q^{−s})⁻¹(1−q^{−s−1})⁻¹ has positive
   coefficients.

3. **V² description corrected**: v2 wrote "symmetric part of the exterior
   square ⊗² minus the symmetric square" — misleading.
   Correct: V² is the symmetric-square L-series of F.

4. **c₀ is absolute effective**: v2 said "depending on k".
   Correct: GHL gives absolute constants (uniform in weight).

5. **Stage D simplified**: v2 unnecessarily complicated the infimum
   argument. Since all constants are absolute, c_eff = 1/(c(B)·C)
   is already a universal lower bound. No inf_{k,p} needed.

6. **witness/README.md corrected**: v2 claimed c₀ ≤ 0.63179293 from Δ.
   Wrong: the correct relation is c_eff ≤ L(1,sym²Δ)·log(13) ≈ 1.62052.
   Also Δ is level 1, outside prime-level scope.

7. **Bibliography corrected**: HL pp. 161–181 (not 1–42);
   Iwaniec–Michel Ann. Acad. Sci. Fenn. 26 (not JAMS 14).

## Downstream impact

The constant c₀ feeds into:
- The general theorem: L(1, sym² f) ≥ c₀/log(kp+1) for all eligible f
- For specific forms (e.g., Δ), the certified L(1) > 0 from F-3 provides
  a numerical anchor, but the general bound needs the HL constant extraction
