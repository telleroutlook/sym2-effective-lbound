# GL₃ Shifted Convolution for Fixed Π — Statement

## Mathematical Problem

Let Π = sym²π be a fixed cuspidal automorphic representation of GL₃(A_ℚ)
with trivial central character, arising as the symmetric-square lift of a
holomorphic Hecke eigenform of weight k on SL₂(ℤ).

**Core Estimate [OBL]**: For the GL₃ shifted convolution sum

    S(h, N, Π) = Σ_{n ≤ N} a_Π(n) ā_Π(n+h)

with shift h ≍ T^{1/2} and summation length N ≍ T^{3/2}, prove:

    S(h, N, Π) = C_Π(h) · N + O_Π(N^{1-δ})    for some δ > 0

where C_Π(h) is the expected main term from the Rankin–Selberg decomposition,
and the implied constant is effective in Π.

## Why this is needed

This estimate is the fundamental analytic obstruction blocking:

1. **M-1 (mollifier second moment)**: The mollified moment
   ∫₀ᵀ |L(½+it,Π)|²·|M(t)|² dt requires bounding shifted convolutions
   with shift h ≍ T^{1/2} after AFE expansion. Without power-saving in h,
   the error cannot be bounded below the main term.

2. **M-2 (unmollified second moment)**: The unmollified moment
   ∫_T^{2T} |L(½+it,Π)|² dt requires the same type of estimate for
   the diagonal + off-diagonal decomposition.

## Current literature status

- **Dasgupta–Leung–Young (2024)**: arXiv:2407.06962
  Upper bound: ∫_{-T}^T |L(f,½+it)|² dt ≪ T^{4/3+ε}
  This is NOT an asymptotic; no main term is identified.

- **Pal (2025)**: arXiv:2212.14620v3, IMRN 2025
  Upper bound: T^{3/2 - 3/32 + ε} for Hecke–Maaß GL₃ forms (NOT holomorphic).
  The 3/32 exponent is the current best for degree-3 L-functions.

- **For fixed Π (symmetric-square of holomorphic form)**:
  No power-saving second moment is known. The off-diagonal contribution
  from the AFE expansion remains open.

## Scope

- Fixed non-CM/non-dihedral Π, t-aspect (T → ∞)
- Level one (SL₂(ℤ)): all primes unramified
- Shift scale h ≍ T^{1/2} from degree-3 AFE length N ≍ T^{3/2}
- The estimate must be uniform in Π (or at least effective for each fixed Π)

## Status: [OBL]

This is a research-level obligation at the current frontier of analytic
number theory. No proof exists in the literature for the specific form
of the estimate needed here.
