# Novelty — c_eff v3

## What is new (corrected from v2)

6. **Fixed Stage C parameter chain**: v2 wrote δ = c₀/log K then
   R⁻¹ ≪ log(1/δ), which is wrong (HL Prop 1.1 uses M, not δ).
   Correct: M = K^C with C ≥ max(A_0, c_ZF⁻¹).

7. **Fixed positivity reason**: v2 claimed non-negative coefficients
   from "symmetric-square coefficients" — wrong. Correct: local factors
   of A(s) = ζL are positive.

8. **Fixed V² description**: "symmetric-square L-series of F", not
   "symmetric part of exterior square minus symmetric square".

9. **Fixed c₀**: absolute effective, not "depending on k".

10. **Fixed witness/README.md**: Δ gives c_eff ≤ 1.62, not c₀ ≤ 0.63.
    Also Δ is level 1, outside prime-level scope.

11. **Fixed bibliography**: HL pp. 161–181; Iwaniec–Michel Ann. Acad. Sci. Fenn.

12. **Simplified Stage D**: no inf_{k,p} needed (all constants absolute).

## What is new (from v1)

1. **Corrects the theorem scope**: 1/log(kp+1) instead of 1/log p,
   matching Hoffstein–Lockhart's actual statement.

2. **Eliminates unnecessary blockers**: For prime level + trivial character,
   the GL(1)-lift / exceptional branch does not arise. M-1, M-2, F-2,
   Voronoi, and general GL₃ VK are NOT needed.

3. **Corrects the proof architecture**:
   - Stage B: GHL zero-free region via ζ·L(F)³·L(F,V²) with correct
     triple-zero / double-pole argument
   - Stage C: HL Proposition 1.1 with M=K^C matching, separate from Stage B
   - Stage D: explicit constant extraction (the actual new work)

4. **Corrects completed function**: Λ(s,F) = p^s L_∞(s) L(s,F)

5. **Corrects analytic conductor**: p² k² (not p² k³)

## What is NOT new

- The GHL/HL approach itself is from 1994 (Goldfeld–Hoffstein–Lieman,
  Hoffstein–Lockhart)
- The effective constants were already proven to exist by GHL/HL
- The generic zero-free region argument is in GHL Appendix

## Honest novelty statement

Our contribution is NOT "making GHL effective" (it already was). Rather:
- Extracting fully explicit numerical constants from the HL computation
- Producing a machine-verifiable interval certificate [a, b] with a > 0
- Providing a replay script for independent verification
- For specific forms (Δ), providing a certified L(1) > 0 via computation
