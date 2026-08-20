# Limitations — M-2 Rewritten v3

## Scope

- Fixed non-CM/non-dihedral Π, t-aspect (T → ∞)
- Level one (SL₂(Z)): all primes unramified
- The power-saving error O(T^{1-δ}) is NOT currently known

## What is NOT achieved

- No explicit A_Π, B_Π, δ are computed (only formulas given)
- The GL₃ shifted-convolution sum is at the research frontier
- No numerical witness exists
- Cross terms I_{+-}, I_{-+} not shown to be o(T log T)

## Corrected from v2

1. **AFE weight scale fixed**: V_t(r/T^3) → W_t(r) with support r ≪ T^{3/2}.
   The T^3 scale was inconsistent with the degree-3 AFE length.

2. **4-term decomposition**: v2 wrote |L|² = (diagonal)+(off-diagonal).
   Correct: |S₁+XS_2|² = |S₁|²+|S₂|²+S₁·X̄·S̄₂+S̄₁·X·S₂. Cross terms
   with gamma phase X_Π(t) must be controlled.

3. **Step 1 downgraded**: Smooth AFE with explicit weight and truncation
   error is [OBL], not [THM] as v2 claimed.

4. **A_Π=3R_Π made conditional**: The leading constant holds IF cross terms
   are o(T log T). v2 stated this as [THM] without the condition.

5. **H_Π(1)≠0 justification added**: From D_{Π,p}(x)>0 and L_p positivity,
   the quotient is positive at x=1/p.

## What this package actually proves

M-2 establishes the ALGEBRAIC SETUP for the unmollified second moment:
- Correct AFE structure with t-dependent X_Π(t) [THM]
- Correct H_{Π,p} formula for level-one symmetric-square [THM]
- Leading constant formula A_Π = 3R_Π [CONDITIONAL on cross terms]
- The analytic bound with power-saving error remains [OBL]

## Downstream impact

M-2 cannot serve as a premise for c_eff until the power-saving
off-diagonal estimate is proved.
