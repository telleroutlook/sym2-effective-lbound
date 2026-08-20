# M-1: Mollifier Construction — Rewritten v4

## Desired Statement

Let π be a holomorphic Hecke eigenform of weight k on SL₂(Z), non-CM/non-dihedral,
and let Π = sym²π be its symmetric-square lift to GL₃. Fix T > 0 and let
C_Π(t) ≍ t³ denote the analytic conductor of L(s, Π) at height t.

Define the mollified second moment:

    I(T) = ∫_T^{2T} |M(½ + it, Π)|² dt

where M(s, Π) = M_X(s) · L(s, Π) and M_X(s) = Σ_{m≤X} b_m m^{-s} is a
reciprocal mollifier of length X = T^θ for some θ ∈ (0,1).

**Goal [OBL]**: Prove there exist explicit θ ∈ (0,1), C_{Π,θ} > 0, T₀ > 0, δ > 0
such that:

    I(T) = C_{Π,θ} · T + O(T^{1-δ})    for all T ≥ T₀

with C_{Π,θ} > 0.

## Why the original was wrong

1. **Wrong bridge lemma**: The original claimed I(T) ≥ c₀T ⟹ L(½, Π) > 0.
   This is FALSE. The integral ∫_T^{2T} lives at |t| ≥ T₀ > 0 and has no
   logical connection to the central value L(½, Π) = L(½+0·i, Π).

2. **Wrong main term for mollified moment**: The unmollified second moment
   has CONJECTURAL diagonal scale T·log T (from the Rankin–Selberg pole).
   But M(s)·L(s) ≈ 1 for a good reciprocal mollifier, so I(T) ≍ T,
   NOT T·log T. The T·log T appears in the UNMOLLIFIED moment.

3. **Wrong normalization bridge**: L(½, Π) > 0 does NOT imply L(1, sym²f) > 0
   without specifying the normalization shift.

## Current status

The unmollified second moment for fixed GL₃ cusp form currently has only
UPPER BOUNDS (DLY 2024: T^{4/3+ε}; Pal IMRN 2025: T^{3/2-3/32+ε}).
The CONJECTURAL diagonal main term T·log T is NOT proved. The mollified
version is even further from the frontier.

**Note on literature**: DLY and Pal provide upper bound context for
related GL₃ moment problems. Their results are NOT direct dependencies
for M-1: DLY treats unmollified moments, Pal treats Hecke–Maaß (not
holomorphic) forms on SL(3,Z). Neither solves the fixed-Π t-aspect
mollified moment that M-1 requires.

## Revised goal

The correct t-aspect goal is: establish I(T) = C_{Π,θ} T + o(T) with C_{Π,θ} > 0.
This is a statement about the average behavior of |M(½+it) L(½+it)|² on
[t ∈ [T,2T]]. It does NOT directly imply anything about L(½, Π) itself.

If the project's ultimate target is L(1, sym²f) > 0, that requires a
completely different route (e.g., Rankin–Selberg/Petersson residue), NOT
this mollifier moment.

## v4 corrections (per reviewer verdict 2026-08-20)

1. **AFE notation**: B(s) sum variable changed from s to r (avoids collision
   with complex variable s)
2. **FE factor normalization**: X_Π(s) = ε_Π q_Π^{1/2-s} L_∞(1-s,π̃)/L_∞(s,Π)
   with |X_Π(½+it)| = 1 (was N^{1-2s} without ε_Π or q_Π)
3. **I_{--} gamma phase corrected**: Phase |X|² = 1 cancels; gamma oscillation
   concentrated in cross blocks I_{+-}, I_{-+} only (was incorrectly stated
   to appear in I_{--} as well)
4. **Literature tightened**: DLY/Pal listed as context (upper bounds), not
   direct dependencies; CKLT2026 noted as adjacent (Dirichlet family, not
   fixed Π)
5. **D_X squarefree proxy**: Moved from main proof dependency to aside

## Status: [OBL]

The core analytic lemma (mollified twisted GL₃ moment) is at the research frontier.
v4 fixes technical errors in AFE notation, FE normalization, and gamma-phase
description. The analytic proof remains [OBL].
