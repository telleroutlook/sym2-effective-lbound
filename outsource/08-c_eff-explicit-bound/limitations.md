# Limitations — c_eff Rewritten

## Scope

- f ∈ S_k^new(Γ₀(p)), k ≥ 2, p prime
- Trivial central character
- f non-CM (non-dihedral)
- Bound: L(1, sym² f) ≥ c_*/log(kp+1)

## What is NOT achieved

- No numerical c_* is computed
- No interval [a, b] with a > 0 is certified
- No machine-readable witness exists
- The explicit constant extraction (Stage 4) is [OBL]
- The interval certification (Stage 5) is [OBL]

## Key correction from original

The original claimed 1/log p independent of k. The corrected bound is
1/log(kp+1), which is weaker but correct.

## Downstream impact

The constant c_* feeds into:
- F-3: L(1, sym²Δ) > 0 (already proved for Δ specifically)
- The general theorem: L(1, sym² f) ≥ c_*/log(kp+1) for all f
