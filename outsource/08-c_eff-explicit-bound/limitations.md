# Limitations — c_eff v4

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
- All constants c_ZF, C_*, A_0, B, c(B), C, c_eff are formulas, not numbers

## Corrected from v2

1. **Stage C parameter chain rewritten**: v2 wrote δ = c₀/log K
   then R⁻¹ ≪ log(1/δ), which is wrong (HL Prop 1.1 uses M, not δ).
   Correct: set M = K^C with C ≥ max(A_0, c_ZF⁻¹), giving
   R⁻¹ ≤ c(B)·C·log K.

2. **Positivity reason corrected**: v2 claimed non-negative coefficients
   follow from "positivity of symmetric-square coefficients" — wrong
   (L(sym²f) coefficients are not generally non-negative).
   Correct: A(s) = ζ(s)L(s,F) has non-negative coefficients because
   each local factor has positive coefficients.

3. **V² description corrected**: v2 wrote "symmetric part of the exterior
   square ⊗² minus the symmetric square" — misleading.
   Correct: V² is the symmetric-square L-series of F.

4. **c₀ is absolute effective**: v2 said "depending on k".
   Correct: GHL gives absolute constants (uniform in weight).

5. **Stage D simplified**: v2 unnecessarily complicated the infimum
   argument. Since all constants are absolute, c_eff = 1/(c(B)·C)
   is already a universal lower bound. No inf_{k,p} needed.

6. **Bibliography corrected**: HL pp. 161–181 (not 1–42);
   Iwaniec–Michel Ann. Acad. Sci. Fenn. 26 (not JAMS 14).

## Corrected from v3 (per reviewer verdict 2026-08-20)

7. **Good-prime local factor fixed**: v3 wrote A_q(s) = (1−q^{−s})⁻¹(1−q^{−s−1})⁻¹
   for ALL primes — this is the bad-prime factor. Correct good-prime factor:
   A_q(s) = (1−α_q²q^{−s})⁻¹(1−q^{−s})⁻²(1−β_q²q^{−s})⁻¹.
   Positivity of the full series is taken from GHL for general level;
   for prime level the local verification is clean.

8. **L(1,F) ≠ 0 added to Stage B**: Double-pole argument requires this
   explicitly. From Jacquet–Shalika / standard GL₃ non-vanishing.

9. **Growth multiplicative constant C_* added**: Growth bound is now
   |A(1/2+it)| ≤ C_* K^{A_0}(1+|t|)^B. C_* must be tracked for
   numerical extraction (absorbed into C via log C_*/log 5 for existence).

10. **Δ upper bound claim removed**: Δ is level 1, outside prime-level
    scope. Its L(1) value is a sanity check only, not an upper bound
    for the prime-level universal constant.

## Downstream impact

The constant c₀ feeds into:
- The general theorem: L(1, sym² f) ≥ c₀/log(kp+1) for all eligible f
- For specific forms (e.g., Δ), the certified L(1) > 0 from F-3 provides
  a numerical sanity check, but the general bound needs the HL constant extraction
