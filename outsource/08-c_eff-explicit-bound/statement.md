# c_eff: Explicit Lower Bound for L(1, sym² f) — Rewritten v4

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
- Auxiliary series φ(s) = ζ(s) L(s,F)³ L(s,F,V²)
- Factorization: L(s,F×F) = L(s,F) L(s,F,V²)
- Non-dihedral ⟹ L(s,F,V²) has simple pole at s=1
- **L(1,F) ≠ 0** (Jacquet–Shalika / standard GL₃ non-vanishing)
- Therefore φ has double pole at s=1
- φ has non-negative Dirichlet coefficients (GHL; good-prime local factors
  of ζ(s)L(s,F) are (1−α_q²q^{-s})⁻¹(1−q^{-s})⁻²(1−β_q²q^{-s})⁻¹)
- GHL zero-count lemma: at most 2 zeros near 1
- Triple zero from L(β,F)=0 contradicts this
- Result: L(s,F) ≠ 0 for 1 − c_ZF/log(kp+1) < s < 1

### Stage C — HL lower bound [THM, constants OBL]
- A(s) = ζ(s) L(s,F) has non-negative coefficients and simple pole
- Growth: |A(1/2+it)| ≤ C_* K^{A_0}(1+|t|)^B, K=kp+1
  (C_* is the growth multiplicative constant, essential for numerics)
- Set M = K^C with C ≥ max(A_0 + log C_*/log 5, c_ZF⁻¹)
- Then 1/log M ≤ c_ZF/log K, so GHL zero-free covers HL requirement
- HL Prop 1.1: R⁻¹ ≤ c(B)·log M = c(B)·C·log K
- Therefore L(1,F) ≥ 1/(c(B)·C) · 1/log(kp+1)
- c_eff = 1/(c(B)·C) > 0 (all absolute constants)

### Stage D — Numerical constant extraction [PARTIAL]
- Computation script: src/compute_constants.py
- c_eff ≈ 0.029 > 0 (numerical estimate, not yet Arb-certified)
- B=2.5, C_*=39.48, c_ZF=0.1111, c(B)=3.82, C=9.0
- Needs: Arb interval certification, GHL/HL formula verification

## What is NOT needed (corrected from previous version)

1. **M-1 (mollifier)**: Not needed for the HL-based approach
2. **M-2 (mean value)**: Not needed for the HL-based approach
3. **F-2 (global residue)**: Not needed; HL uses auxiliary series
4. **GL₃ Voronoi**: Not needed; no Kloosterman sums in HL approach
5. **Case 2 (exceptional zero)**: Eliminated for prime level + trivial char

## Status: [OBL]

The main tasks remaining are:
1. Verify c_ZF formula against GHL Appendix
2. Verify c(B) formula against HL Proposition 1.1 proof
3. Arb interval certification of c_eff ∈ [a,b] with a > 0
4. Machine-readable certificate with SHA-256 + replay script
