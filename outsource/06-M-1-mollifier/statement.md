# M-1: Mollifier Construction — Rewritten v3

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

## Revised goal

The correct t-aspect goal is: establish I(T) = C_{Π,θ} T + o(T) with C_{Π,θ} > 0.
This is a statement about the average behavior of |M(½+it) L(½+it)|² on
[t ∈ [T,2T]]. It does NOT directly imply anything about L(½, Π) itself.

If the project's ultimate target is L(1, sym²f) > 0, that requires a
completely different route (e.g., Rankin–Selberg/Petersson residue), NOT
this mollifier moment.

## Status: [OBL]

The core analytic lemma (mollified twisted GL₃ moment) is at the research frontier.
See Dasgupta–Leung–Young (2024), Pal (IMRN 2025) for current state.
