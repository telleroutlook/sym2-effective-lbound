# Witness — c_eff v3

## Status

No numerical witness exists. The explicit constant extraction and interval
certification are [OBL].

## What would constitute a witness

1. Explicit computation of c_eff ∈ [a, b] with a > 0
2. Verification using Arb/python-flint with outward rounding
3. Machine-readable certificate with SHA-256
4. Replay script for independent verification

## Current state

The following are [OBL]:
- c_ZF from GHL zero-count lemma
- A_0, B from functional equation
- c(B) from HL contour integral
- c_eff = 1/(c(B)·C) as certified interval
- Replay script

## What EXISTS (but is not a witness for c_eff)

For the specific form Δ (k=12, level 1):
- L(1, sym²Δ) ∈ [0.63179293, 0.63179298] (certified via Arb)
- This is F-3, not c_eff
- The bound c_eff ≤ L(1,sym²Δ)·log(13) ≈ 1.62052 gives an upper bound
  on the universal constant, but not a lower bound
- Δ is level 1, outside the prime-level scope of this package
