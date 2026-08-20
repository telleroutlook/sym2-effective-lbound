# Limitations — M-2 Rewritten v2

## Scope

- Fixed non-CM/non-dihedral Π, t-aspect (T → ∞)
- Level one (SL₂(Z)): all primes unramified
- The power-saving error O(T^{1-δ}) is NOT currently known

## What is NOT achieved

- No explicit A_Π = 3R_Π, B_Π, δ are computed (only the formula is given)
- The GL₃ shifted-convolution sum is at the research frontier
- No numerical witness exists

## Removed from v1

1. **Bad-prime limitation deleted**: Level-one forms have NO bad primes.
   All finite primes are unramified. This was a template artifact.

2. **Wrong H_{Π,p} formula corrected**: v1 proposed H_{Π,p}(x) =
   Π_i(1-|α_i|²x)⁻¹ which gives 1+3x+O(x²), contradicting the necessary
   1+O(x²). Corrected to the reviewer's formula.

3. **Leading constant corrected**: A_Π = 3R_Π (not (3/2)R_Π).
   Both AFE halves contribute, giving factor 2 × (3/2) = 3.

## What this package actually proves

M-2 establishes the ALGEBRAIC SETUP for the unmollified second moment:
- Correct AFE with t-dependent dual factor [THM]
- Correct H_{Π,p} formula for level-one symmetric-square [THM]
- Leading constant formula A_Π = 3R_Π [THM]
- The analytic bound with power-saving error remains [OBL]

## Downstream impact

M-2 cannot serve as a premise for c_eff until the power-saving
off-diagonal estimate is proved.
