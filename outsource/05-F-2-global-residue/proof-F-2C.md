# F-2C: Target-Family Local Positivity/Uniformity — Proof

## Archimedean correction Z_∞(1)

From F-2B, the correct archimedean factor (degree 4) gives:

    Z_∞(1) = Γ_R(1) · Γ_R(2) · Γ_C(k) = 2π^{-k-1} Γ(k)

For weight k = 12: Z_∞(1) = 2π^{-13} · 11! ≈ 2 × 1.35 × 10^{-14} × 39916800.

## Ramified corrections Z_p(1)

For p | N, the local representation π_p falls into one of:
- **Steinberg twist** (conductor exponent 1): explicit Z_p(1) formula
- **Ramified principal series** (conductor exponent ≥ 1): explicit formula
- **Supercuspidal** (conductor exponent ≥ 2): explicit formula

Each type requires:
1. Direct computation of Z_p(1) from the local formula
2. Proof that Z_p(1) ≠ 0 (by inspection of the explicit formula)
3. Quantitative lower bound |Z_p(1)| ≥ c_p > 0

**The nonvanishing Z_p(1) ≠ 0 must come from the explicit formula,
NOT from abstract continuity+compactness arguments.**

## Uniformity: correct argument

### Wrong argument (v1)
"Z_p(1) is continuous → compact set → achieves minimum → min > 0"
This is INVALID because continuity+compactness only gives min ≥ 0.

### Correct argument
1. For each local type that occurs, compute Z_p(1) explicitly
2. Verify Z_p(1) ≠ 0 by inspection of the formula
3. For continuous families, the set {Z_p(1) : π_p in family} is compact
   AND avoids 0 (by step 2), so min > 0
4. For finitely many N ≤ N₀, define:

       C(N₀) = min_{N ≤ N₀} ∏_{p | N} |Z_p(1)| > 0

   This is a finite minimum of positive numbers, hence positive.

### c_loc vs C_global

- **c_loc**: individual lower bound min_p |Z_p(1)| ≥ c' > 0 (may have c' < 1)
- **C_global**: product bound C(N₀) = min_N ∏_p |Z_p(1)| > 0

The downstream needs C_global, not just c_loc.

## Status: [OBL]

The main tasks are:
1. Explicit computation of Z_∞(1) with correct degree-4 factor
2. Explicit computation of Z_p(1) for each local type
3. Direct nonvanishing proof from explicit formulas
4. Finite minimum C(N₀) > 0 for the product
