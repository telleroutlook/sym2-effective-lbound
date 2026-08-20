# Witness — M-2 v4

## Status

No numerical witness exists. The power-saving GL₃ second moment for fixed Π
is at the research frontier.

## What would constitute a witness

1. Explicit computation of ∫_T^{2T} |L(½+it,Π)|² dt for specific Π and T
2. Verification that the leading term matches A_Π = 3R_Π (not (3/2)R_Π)
3. Verification that the error is O(T^{1-δ}) for some δ > 0

## Note

The v1 witness referenced the wrong leading constant. The correct constant
is A_Π = 3R_Π, from both AFE halves each contributing (3/2)R_Π log T.

## v4 corrections

- H_{Π,p}(1/p) > 0 proof fixed (factorization, endpoint positivity)
- Step 2 diagonal corrected (R_Π → (3/2)R_Π per half)
- A_Π = 3R_Π conditional expanded (diagonal-weight + cross + off-diagonal)

## Current state

The following are [OBL]:
- A_Π = 3R_Π (formula known; R_Π = Res_{s=1} D_Π(s) must be computed per Π)
- B_Π (lower-order term)
- δ (power-saving exponent)
- The GL₃ shifted-convolution estimate itself
