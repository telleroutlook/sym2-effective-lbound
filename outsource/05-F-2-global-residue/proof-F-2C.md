# F-2C: Target-Family Local Positivity/Uniformity — Proof

## Archimedean correction Z_∞(1)

From F-2B, the correct archimedean factor (degree 4) gives:

    Z_∞(1) = 2^{1-k} · π^{-(k+1)} · Γ(k)

For weight k = 12:

    Z_∞(1) = 2^{-11} · π^{-13} · 11!
            ≈ 0.00671239369377...

**Previous error (corrected per 2026-08-20 review):** The v2 proof wrote
2π^{-13}·11! ≈ 27.49, which differs by 2^{11} = 2048. The correct value
is 2^{-11}π^{-13}·11! ≈ 0.00671.

## Ramified corrections Z_p(1)

For p | N_π (conductor of π, NOT the symmetric-square conductor), the local
representation π_p falls into one of:
- **Steinberg twist** (conductor exponent 1): explicit Z_p(1) formula
- **Ramified principal series** (conductor exponent ≥ 1): explicit formula
- **Supercuspidal** (conductor exponent ≥ 2): explicit formula

Each type requires:
1. Direct computation of Z_p(1) from the local formula
2. Proof that Z_p(1) ≠ 0 (by inspection of the explicit formula)
3. Quantitative lower bound |Z_p(1)| ≥ c_p > 0

**The nonvanishing Z_p(1) ≠ 0 must come from the explicit formula,
NOT from abstract continuity+compactness arguments.**

## Conductor notation (corrected per 2026-08-20 review)

The previous version used N for both "conductor of π" and "conductor of the
symmetric square" — these are different quantities. Corrected notation:

- N_π = conductor of π (determines local representation types at p | N_π)
- N_{sym²} = conductor of sym²π (appears in the global L-function)
- N_{Ad} = conductor of Ad(π) (adjoint representation)

The local type classification at p uses N_π, NOT N_{sym²}.

## Uniformity: correct argument

### Wrong argument (v1)
"Z_p(1) is continuous → compact set → achieves minimum → min > 0"
This is INVALID because continuity+compactness only gives min ≥ 0.

### Correct argument
1. For each local type that occurs, compute Z_p(1) explicitly
2. Verify Z_p(1) ≠ 0 by inspection of the formula
3. For continuous families, the set {Z_p(1) : π_p in family} is compact
   AND avoids 0 (by step 2), so min > 0
4. For the target family F_{N_0} with level ≤ N_0:

       C(F_{N_0}) = min_{f ∈ F_{N_0}} ( |Z_∞(1;f)| · ∏_{p | N_π(f)} |Z_p(1;f)| ) > 0

   This is a finite minimum of positive numbers (finitely many forms with
   level ≤ N_0, fixed weight and character), hence positive.

### Why min over N is insufficient

The previous version defined C(N₀) = min_{N ≤ N₀} ∏_{p|N} |Z_p(1)|.
This is insufficient because:
- The same level N can have different newforms with different local types
- The product depends on the full local data, not just the level integer
- The minimum must be over the complete target family F_{N_0}, not just N

### c_loc vs C_global

- **c_loc**: individual lower bound min_p |Z_p(1)| ≥ c' > 0 (may have c' < 1)
- **C_global**: product bound C(F_{N_0}) = min_f ∏_p |Z_v(1;f)| > 0

The downstream needs C_global, not just c_loc.

## Downstream interface

For c_eff, the explicit constant in L(1, sym²f) ≥ c/log(N_π), the
relevant quantity is:

    c ≥ C(F_{N_0}) · (other factors from M-1, M-2, M-3)

where C(F_{N_0}) is the product of all local corrections for the worst case
in the target family.

## Status: [OBL]

The main tasks are:
1. Explicit computation of Z_∞(1) with correct formula 2^{1-k}π^{-(k+1)}Γ(k)
2. Explicit computation of Z_p(1) for each local type
3. Direct nonvanishing proof from explicit formulas
4. Product bound C(F_{N_0}) > 0 for the target family
