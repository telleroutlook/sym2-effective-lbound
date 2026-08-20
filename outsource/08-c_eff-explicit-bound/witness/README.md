# Witness — c_eff v4

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
- C_*, A_0, B from functional equation
- c(B) from HL contour integral
- c_eff = 1/(c(B)·C) as certified interval
- Replay script

## What EXISTS (but is not a witness for c_eff)

For the specific form Δ (k=12, level 1):
- L(1, sym²Δ) ∈ [0.63179293, 0.63179298] (certified via Arb)
- This is F-3, not c_eff

**Important scope note**: Δ is level 1, which is outside the prime-level
scope of this package. The numerical value L(1, sym²Δ) serves only as an
independent sanity check for the L-function computation pipeline. It does
NOT provide an upper bound on c_eff for the prime-level family, because
the universal constant c₀ applies to all eligible f (including those with
larger L(1)), and a level-1 form does not constrain the family maximum.

## v4 corrections

- Growth bound now includes multiplicative constant C_* (essential for numerics)
- Positivity of ζ(s)L(s,F) verified with correct good-prime local factors
- L(1,F) ≠ 0 prerequisite made explicit in Stage B
- Δ claim corrected: sanity check only, not upper bound for prime-level c_eff
