# c_eff: Explicit Lower Bound for L(1, sym² f) — Rewritten

## Corrected Theorem Statement

**Theorem** (GHL 1994 specialized + explicit constants). Let f ∈ S_k^new(Γ₀(p))
be a holomorphic Hecke eigenform of weight k ≥ 2 on prime level p, with trivial
central character. Assume f is non-CM (non-dihedral). Let q_ar = p² denote the
arithmetic conductor of sym² f.

Then there exists an explicitly computable constant c_* > 0 depending only on k
such that:

    L(½, sym² f) ≥ c_* / log(kp + 1)

Equivalently, with the completed L-function and explicit normalization:

    L(1, sym² f) ≥ c_*(k) / log(kp + 1)

**Scope correction**: The original claimed 1/log p independent of k. This is
not supported by Hoffstein–Lockhart, which gives scales involving kN (here kp).
The correct uniform bound involves log(kp+1).

**Alternative** (if k must be fixed): For each fixed k₀, there exists c_eff(k₀) > 0
such that L(1, sym² f) ≥ c_eff(k₀)/log p for all f ∈ S_{k₀}^new(Γ₀(p)).

## Proof Architecture (GHL/Hoffstein–Lockhart correct route)

The proof proceeds in FIVE stages, not the original five blockers:

### Stage 1: Normalization and conductor [THM]
- Fix f ∈ S_k^new(Γ₀(p)), a_f(1) = 1 (Hecke normalization)
- Compute sym² Euler factors at each prime
- Arithmetic conductor: q_ar = p²
- Analytic conductor depends on k: q_an(k, p) = p² · (k/2π)³ approximately
- Completed L-function: L_∞(s) · L(s, sym² f) with Iwaniec–Michel gamma factors

### Stage 2: Zero-free region [THM for Δ, OBL general]
- Explicit zero-free region for L(s, sym² f) on σ ∈ [σ₀, 1]
- For Δ (k=12, p=1): proved computationally
- For general (k, p): use symmetric-square zero-free results from existing literature
- NOT requiring general GL₃ Vinogradov–Korobov

### Stage 3: Hoffstein–Lockhart residue proposition [THM, constants OBL]
- HL Proposition 1.1: auxiliary Dirichlet series with non-negative coefficients
- Φ(s) = ζ(s) L(s, F)² L(s, F × F) with appropriate F
- For prime p + trivial character: the GL(1)-lift / monomial obstruction does NOT arise
- Therefore only the "generic" branch applies: residue gives L(1) ≥ c₁/log(kp+1)
- Constants c₁ from HL are effective but not yet numerically explicit

### Stage 4: Explicit constant extraction [OBL]
- Trace through HL computation with explicit constants at each step:
  - Rankin–Selberg residue R_Π
  - Zero-free region parameter σ₀
  - Gamma factor constants
  - Bad Euler factor bounds
- Obtain c₁(k, p) and show inf_{k,p} c₁ > 0

### Stage 5: Interval certification [OBL]
- Compute c_* ∈ [a, b] with a > 0 using Arb/python-flint
- Outward rounding for certified lower bound
- Machine-readable witness with SHA-256
- Replay script for independent verification

## What is NOT a blocker (corrected from original)

1. **M-1 (mollifier)**: Not needed for the HL-based approach
2. **M-2 (mean value)**: Not needed for the HL-based approach
3. **F-2 (global residue)**: Not needed; HL uses auxiliary series, not Rankin–Selberg directly
4. **GL₃ Voronoi**: Not needed; the HL approach doesn't require Kloosterman sums
5. **General GL₃ VK**: Existing symmetric-square zero-free results suffice
6. **Case 2 (exceptional zero)**: Eliminated for prime level + trivial character

## Status: [OBL]

The main tasks are:
1. Verify prime + trivial char eliminates GL(1)-lift obstruction
2. Trace HL computation with explicit constants
3. Compute interval [a, b] containing c_*
