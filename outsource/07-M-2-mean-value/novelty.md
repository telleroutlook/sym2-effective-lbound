# Novelty — M-2 Rewritten v2

## What is new in v2 (correcting v1)

1. **Corrected AFE dual factor**: From constant χ(Π) to t-dependent
   X_Π(s) = L_∞(Π,1-s)/L_∞(Π,s). This is load-bearing: the gamma
   ratio oscillates in t and affects the off-diagonal analysis.

2. **Corrected H_{Π,p} formula**: v1 proposed Π_i(1-|α_i|²x)⁻¹ which
   gives 1+3x+O(x²), contradicting the required 1+O(x²). The correct
   formula for level-one symmetric-square is:
   H_{Π,p}(x) = 1 - A_p²x² + 2(A_p²-1)x³ - A_p²x⁴ + x⁶

3. **Corrected leading constant**: A_Π = 3R_Π, not (3/2)R_Π.
   Both AFE halves (primary + dual) contribute diagonal terms.

4. **Deleted bad-prime limitation**: Level-one has no bad primes.

5. **Updated Pal reference**: Now IMRN 2025 with DOI, not preprint.

## What is NOT new

- The AFE-based approach to second moments is standard
- The diagonal/off-diagonal decomposition is standard
- The identification of shifted-convolution as the core difficulty is known
- The archimedean gamma factors (Iwaniec–Michel 2001)
