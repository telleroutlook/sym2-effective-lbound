# Limitations — M-2 Rewritten

## Scope

- Fixed non-CM/non-dihedral Π, t-aspect (T → ∞)
- The power-saving error O(T^{1-δ}) is NOT currently known

## What is NOT achieved

- No explicit A_Π, B_Π, δ are computed
- The GL₃ shifted-convolution sum is at the research frontier
- The archimedean factor is identified but not explicitly evaluated
- Bad-prime factors are not computed

## Key correction

The original claimed ∫|L|² = c_Π T + O(T^{1-δ}). This is WRONG.
The correct leading term is A_Π T log T + B_Π T + O(T^{1-δ}).

## Downstream impact

M-2 cannot serve as a premise for M-1 or c_eff until:
1. The T log T main term is established
2. The power-saving error is proved
3. The explicit constants are computed
