# Novelty — c_eff v4

## What is new in v4 (correcting v3)

1. **Fixed good-prime local factor**: v3 wrote (1−q^{−s})⁻¹(1−q^{−s−1})⁻¹
   for all primes (bad-prime factor only). Correct good-prime factor:
   (1−α_q²q^{−s})⁻¹(1−q^{−s})⁻²(1−β_q²q^{−s})⁻¹. Positivity verified
   via local expansion; general level taken from GHL.

2. **Added L(1,F) ≠ 0 prerequisite**: Double-pole argument now explicitly
   requires this. From Jacquet–Shalika / standard GL₃ non-vanishing.

3. **Added growth multiplicative constant C_***: Growth bound is now
   |A(1/2+it)| ≤ C_* K^{A_0}(1+|t|)^B. Essential for numerical extraction;
   absorbed into C via log C_*/log 5 for existence proof.

4. **Removed Δ upper bound claim**: Δ is level 1, outside prime-level scope.
   Its L(1) is a sanity check only, not an upper bound for c_eff.

## What is new in v3 (correcting v2)

5. **Fixed Stage C parameter chain**: M = K^C matching (not δ = c₀/log K).
6. **Fixed positivity reason**: Local factors, not "symmetric-square coefficients".
7. **Fixed V² description**: "symmetric-square L-series of F".
8. **Fixed c₀**: absolute effective, not "depending on k".
9. **Fixed witness/README.md**: Δ gives c_eff ≤ 1.62, not c₀ ≤ 0.63.
10. **Fixed bibliography**: HL pp. 161–181; Iwaniec–Michel Ann. Acad. Sci. Fenn.
11. **Simplified Stage D**: no inf_{k,p} needed (all constants absolute).

## What is new (from v1)

12. **Corrects the theorem scope**: 1/log(kp+1) instead of 1/log p.
13. **Eliminates unnecessary blockers**: M-1, M-2, F-2, Voronoi not needed.
14. **Corrects the proof architecture**: 4 stages with proper separation.

## What is NOT new

- The GHL/HL approach itself is from 1994
- The effective constants were already proven to exist by GHL/HL
- The generic zero-free region argument is in GHL Appendix

## Honest novelty statement

Our contribution is NOT "making GHL effective" (it already was). Rather:
- Extracting fully explicit numerical constants from the HL computation
- Producing a machine-verifiable interval certificate [a, b] with a > 0
- Providing a replay script for independent verification
