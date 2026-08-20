# Limitations — M-1 Rewritten v2

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
   The integral lives at |t| ≥ T₀ and cannot detect the central value.

2. **Deleted L(½) → L(1) deduction**: The normalization shift between
   automorphic L(½,Π) and classical L(1,sym²f) was never specified.

3. **Deleted squarefree approximation**: The stated sum was identically zero.

## What this package actually proves

M-1 establishes the ALGEBRAIC SETUP for the mollified moment:
- True reciprocal coefficients ρ_Π(n) [THM]
- Exact identity I(T) = Σ b_m b̄_n / √(mn) · J_{m,n}(T) [THM]
- Correct 4-variable reduction to convolution coefficients c_X(q) [THM]
- The analytic bound I(T) = C·T + O(T^{1-δ}) remains [OBL]

## Downstream impact

M-1 cannot serve as a premise for c_eff. The mollified moment estimate
is a standalone research-level problem in GL₃ analytic number theory.
