# Witness — c_eff

## Status

No numerical witness exists. The explicit constant extraction and interval
certification are [OBL].

## What would constitute a witness

1. Explicit computation of c_* ∈ [a, b] with a > 0
2. Verification using Arb/python-flint with outward rounding
3. Machine-readable certificate with SHA-256
4. Replay script for independent verification

## Current state

The following are [OBL]:
- c₁(k, p) from HL computation
- inf_{k,p} c₁ (universal lower bound)
- Interval [a, b] containing c_*
- Replay script
