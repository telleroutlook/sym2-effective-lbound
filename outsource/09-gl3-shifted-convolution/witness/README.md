# Witness: GL₃ Shifted Convolution

This package is a **research gap documentation**, not a theorem.
No numerical witness or replay script is applicable.

## Why no witness?

A witness would require:
1. A proof of the GL₃ shifted convolution estimate (which doesn't exist)
2. Numerical computation of the shifted sum (which confirms the difficulty)
3. A certified bound on the error term (which is [OBL])

Since none of these exist, no witness can be produced.

## What could be done (discovery-tier only)

A numerical exploration could:
1. Compute S(h, N, Π) for small h, N and specific Π
2. Compare with the expected main term C_Π(h)·N
3. Estimate the error term |S(h,N) - C_Π(h)·N|

This would NOT be a proof but could provide evidence for/against the estimate.
Such computation is OUTSIDE the scope of this package (discovery-tier only).
