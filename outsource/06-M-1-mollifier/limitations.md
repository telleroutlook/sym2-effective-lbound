# Limitations — M-1 Rewritten v3

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
3. **Deleted squarefree approximation**: The stated sum was identically zero.

## Corrected from v2

4. **Step D fixed**: v2 wrote a single quadratic form c_X(q)c̄_X(q') for I(T).
   The actual |M·L|² = |A+XB|² has FOUR blocks with different weights and
   gamma phases. The v2 formula described at most I_{++}, not the full I(T).

5. **Coefficient bound fixed**: v2 wrote ∑|c_X(q)|² ≪ Q^ε (unweighted).
   This is Q too small: for prime q>X, c_X(q)≈a_Π(q), so unweighted sum
   grows like Q^{1+ε}. The correct statement is weighted: ∑|c_X(q)|²/q ≪ Q^ε.

6. **Shift scale fixed**: v2 wrote h ≲ T^{1/2}. With Q ≈ T^{3/2+θ}, the
   correct near-diagonal scale is H ≲ T^{1/2+θ}. Mollification expands the
   shifted-convolution geometry.

7. **D_X interpretation fixed**: v2 called D_X the "truncation error from
   the reciprocal series." It is actually the coefficient-level difference
   between exact reciprocal ρ_Π(n) and squarefree proxy μ(n)a_Π(n).
   NOT the error from truncating L⁻¹.

8. **"Only option" fixed**: The exact reciprocal is a canonical natural choice,
   but NOT the only legitimate mollifier. Squarefree, Selberg/Levinson type,
   and optimized Dirichlet polynomial mollifiers are all valid.

9. **T·log T scale fixed**: The unmollified second moment has CONJECTURAL
   diagonal scale T·log T. Current literature has only upper bounds
   (DLY: T^{4/3+ε}, Pal: T^{3/2-3/32+ε}). Not proved as asymptotic.

## What this package actually proves

M-1 establishes the ALGEBRAIC SETUP for the mollified moment:
- True reciprocal coefficients ρ_Π(n) [THM]
- Exact identity I(T) = Σ b_m b̄_n / √(mn) · J_{m,n}(T) [THM]
- 4-block AFE decomposition structure [OBL — weights and phases not analyzed]
- The analytic bound I(T) = C·T + O(T^{1-δ}) remains [OBL]

## Downstream impact

M-1 cannot serve as a premise for c_eff. The mollified moment estimate
is a standalone research-level problem in GL₃ analytic number theory.
