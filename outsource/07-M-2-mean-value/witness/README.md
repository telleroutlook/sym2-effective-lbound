# Witness — M-2 v2

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

## Current state

The following are [OBL]:
- A_Π = 3R_Π (formula known; R_Π = Res_{s=1} D_Π(s) must be computed per Π)
- B_Π (lower-order term)
- δ (power-saving exponent)
- The GL₃ shifted-convolution estimate itself
