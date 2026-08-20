# Limitations — M-1 v4

## Scope

- Applies only to non-CM/non-dihedral holomorphic Hecke eigenforms on SL₂(Z)
- Mollifier length X = T^θ with θ ∈ (0,1) to be optimized
- t-aspect only (fixed Π, T → ∞)

## What is NOT achieved

- No explicit θ, C_{Π,θ}, T₀, δ are computed
- The core analytic lemma (mollified twisted GL₃ moment) is at the research frontier
- No numerical witness exists

## Removed from v1

1. **Deleted false bridge lemma**: I(T) ≥ c₀T does NOT imply L(½,Π) > 0.
2. **Deleted L(½) → L(1) deduction**: The normalization shift was never specified.
3. **Deleted algebraically vacuous squarefree approximation**.

## Corrected from v2

4. **Step D fixed**: v2 wrote a single quadratic form c_X(q)c̄_X(q') for I(T).
   The actual |M·L|² = |A+XB|² has FOUR blocks.
5. **Coefficient bound fixed**: Weighted Σ|c_X(q)|²/q ≪ Q^ε (not unweighted).
6. **Shift scale fixed**: H ≲ T^{1/2+θ} (not h ≲ T^{1/2}).
7. **D_X interpretation fixed**: Coefficient difference, not truncation error.
8. **T·log T scale fixed**: Conjectural, not proved.

## Corrected from v3 (per reviewer verdict 2026-08-20)

9. **AFE notation**: B(s) sum variable s → r (avoids collision with complex s).
10. **FE factor normalization**: X_Π(s) = ε_Π q_Π^{1/2-s} L_∞(1-s,π̃)/L_∞(s,Π)
    (was missing ε_Π and q_Π; N^{1-2s} only consistent if N² = q_Π).
11. **I_{--} gamma phase**: |X_Π(½+it)| = 1, so |MXB|² = |M|²|B|² — no gamma
    oscillation in I_{--}. Gamma oscillation is in cross blocks I_{+-}, I_{-+} only.
12. **Literature**: DLY/Pal listed as upper-bound context, not direct dependencies.
    DLY: unmollified; Pal: Maaß forms. Neither solves fixed-Π t-aspect mollified.

## What this package actually proves

M-1 establishes the ALGEBRAIC SETUP for the mollified moment:
- True reciprocal coefficients ρ_Π(n) [THM]
- Exact identity I(T) = Σ b_m b̄_n / √(mn) · J_{m,n}(T) [THM]
- 4-block AFE decomposition structure [OBL — blocks not analyzed]
- The analytic bound I(T) = C·T + O(T^{1-δ}) remains [OBL]

## Downstream impact

M-1 cannot serve as a premise for c_eff. The mollified moment estimate
is a standalone research-level problem in GL₃ analytic number theory.
