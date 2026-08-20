# Witness — c_eff v2

## Status

No numerical witness exists. The explicit constant extraction and interval
certification are [OBL].

## What would constitute a witness

1. Explicit computation of c₀ ∈ [a, b] with a > 0
2. Verification using Arb/python-flint with outward rounding
3. Machine-readable certificate with SHA-256
4. Replay script for independent verification

## Current state

The following are [OBL]:
- c₁(k, p) from HL computation (Stage D)
- inf_{k,p} c₁ (universal lower bound)
- Interval [a, b] containing c₀
- Replay script

## What EXISTS (but is not a witness for c_eff)

For the specific form Δ (k=12, level 1):
- L(1, sym²Δ) ∈ [0.63179293, 0.63179298] (certified via Arb)
- This is F-3, not c_eff
- The general c₀ ≤ 0.63179293 is a valid upper bound for the universal constant,
  but not a lower bound
