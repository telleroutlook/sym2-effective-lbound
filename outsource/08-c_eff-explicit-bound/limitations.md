# Limitations — c_eff v2

## Scope

- f ∈ S_k^new(Γ₀(p)), k ≥ 2, p prime
- Trivial central character
- f non-dihedral (non-CM)
- Bound: L(1, sym² f) ≥ c₀/log(kp+1)

## What is NOT achieved

- No numerical c₀ is computed
- No interval [a, b] with a > 0 is certified
- No machine-readable witness exists
- The explicit constant extraction (Stage D) is [OBL]

## Corrected from v1

1. Deleted L(1/2) statement — GHL/HL gives L(1) lower bound, not L(1/2)
2. Added p^s to completed function: Λ(s,F) = p^s L_∞(s) L(s,F)
3. Fixed analytic conductor: p² k² (not p² k³)
4. Rewrote Stage B: correct factorization ζ·L³·L(V²), triple-zero/double-pole
5. Separated Stage B (GHL zero-free) from Stage C (HL residue)
6. Deleted wrong residue formula involving L(Π×Π̃) which has a pole at s=1
7. Fixed HL year: 1994 Annals, not 1997

## Downstream impact

The constant c₀ feeds into:
- The general theorem: L(1, sym² f) ≥ c₀/log(kp+1) for all eligible f
- For specific forms (e.g., Δ), the certified L(1) > 0 from F-3 provides
  a numerical anchor, but the general bound needs the HL constant extraction
