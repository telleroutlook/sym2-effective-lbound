# Limitations — M-2 v4

## Scope

- Fixed non-CM/non-dihedral Π, t-aspect (T → ∞)
- Level one (SL₂(Z)): all primes unramified
- The power-saving error O(T^{1-δ}) is NOT currently known

## What is NOT achieved

- No explicit A_Π, B_Π, δ are computed (only formulas given)
- The GL₃ shifted-convolution sum is at the research frontier
- No numerical witness exists

## Corrected from v2

1. **AFE weight scale**: V_t(r/T^3) → W_t(r) with support r ≪ T^{3/2}.
2. **4-term decomposition**: |S₁+XS_2|² = |S₁|²+|S₂|²+S₁·X̄·S̄₂+S̄₁·X·S₂.
3. **Step 1 downgraded**: Smooth AFE with truncation error is [OBL].
4. **A_Π=3R_Π made conditional**: Requires cross terms o(T log T).

## Corrected from v3 (per reviewer verdict 2026-08-20)

5. **H_{Π,p}(1/p) > 0**: Proof now uses factorization
   (1-x)²(1+x+x²-A_px)(1+x+x²+A_px) with explicit endpoint positivity.
   v3 had open-interval → endpoint gap.

6. **Step 2 diagonal**: R_Π → (3/2)R_Π per half (AFE length T^{3/2}
   introduces factor from log(T^{3/2}) = (3/2) log T).

7. **A_Π = 3R_Π conditional expanded**: Now requires diagonal-weight
   asymptotic + cross terms + same-half off-diagonal, not just cross terms.

8. **FE factor**: Added ε_Π, q_Π normalization (level one: ε_Π=1, q_Π=1).

## What this package actually proves

M-2 establishes the ALGEBRAIC SETUP for the unmollified second moment:
- Correct AFE structure with t-dependent X_Π(t) [THM]
- Correct H_{Π,p} formula for level-one symmetric-square [THM]
- H_{Π,p}(1/p) > 0 via factorization [THM]
- Leading constant formula A_Π = 3R_Π [CONDITIONAL on 3 items]
- The analytic bound with power-saving error remains [OBL]

## Downstream impact

M-2 cannot serve as a premise for c_eff until the power-saving
off-diagonal estimate is proved.
