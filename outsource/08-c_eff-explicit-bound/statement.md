# c_eff: Explicit Lower Bound for L(1, sym² f) — Rewritten v2

## Theorem Statement

**Theorem** (Hoffstein–Lockhart 1994 + Goldfeld–Hoffstein–Lieman 1994).
Let f ∈ S_k^new(Γ₀(p)) be a holomorphic Hecke eigenform of weight k ≥ 2
on prime level p, with trivial central character. Assume f is non-dihedral.
Let F = sym² f be the symmetric-square lift to GL₃.

Then there exists an absolute effective constant c₀ > 0 such that

    L(1, sym² f) ≥ c₀ / log(kp + 1).

The existence and effectivity of c₀ follow from Hoffstein–Lockhart (1994)
Theorem 0.1 together with the Goldfeld–Hoffstein–Lieman (1994) effective
zero-free argument. The present project seeks to extract and certify a
concrete numerical value c_eff ≤ c₀.

**Scope**: The denominator is log(kp+1), NOT log p. Hoffstein–Lockhart
explicitly states that for holomorphic forms, the Maass-form parameter λN
is replaced by kN. For prime level p, this gives kp.

**Status**: [OBL] — the effective constant c₀ exists by HL/GHL, but no
concrete numerical value has been computed.

## Proof Architecture (4 stages)

### Stage A — Normalization [THM]
- Fix f ∈ S_k^new(Γ₀(p)), a_f(1) = 1 (Hecke normalization)
- F = sym² f, arithmetic conductor q_ar = p²
- Completed L-function: Λ(s, F) = p^s L_∞(s) L(s, F)
- Gamma factors from Iwaniec–Michel (2001)

### Stage B — GHL zero-free region [THM, constants OBL]
- Auxiliary series φ(s) = ζ(s) L(s,F)² L(s,F×F)
- Factorization: L(s,F×F) = L(s,F) L(s,F,V²)
- Non-dihedral ⟹ L(s,F,V²) has simple pole at s=1
- Therefore φ has double pole at s=1
- GHL zero-count lemma: if L(β,F) = 0, then φ has triple zero at β
  but double pole at 1 ⟹ at most 2 zeros near 1 ⟹ contradiction
- Result: L(s,F) ≠ 0 for 1 − c₀/log(kp+1) < s < 1

### Stage C — HL lower bound [THM, constants OBL]
- Apply HL Proposition 1.1 to A(s) = ζ(s) L(s,F)
  - Coefficients nonnegative
  - Simple pole at s=1 with residue L(1,F)
  - Zero-free region from Stage B
- HL gives: L(1,F)⁻¹ ≪ log(kp+1)
- Therefore: L(1, sym² f) ≥ c₁ / log(kp+1)

### Stage D — Numerical constant extraction [OBL]
- Trace through all O(1), ≪, c(B), C in HL computation
- Instantiate: gamma derivatives, M = 1+D·max|c_i|, contour parameters,
  bad-prime bounds
- Obtain c_eff > 0 as certified interval [a,b]
- Arb/python-flint with outward rounding

## What is NOT needed (corrected from previous version)

1. **M-1 (mollifier)**: Not needed for the HL-based approach
2. **M-2 (mean value)**: Not needed for the HL-based approach
3. **F-2 (global residue)**: Not needed; HL uses auxiliary series
4. **GL₃ Voronoi**: Not needed; no Kloosterman sums in HL approach
5. **Case 2 (exceptional zero)**: Eliminated for prime level + trivial char

## Status: [OBL]

The main tasks are:
1. Trace HL computation with all constants explicit (Stage D)
2. Compute interval [a, b] with a > 0 using Arb (Stage D)
