# F-2C: Target-Family Local Positivity/Uniformity — Proof (v4)

## Archimedean correction Z_∞(1)

From F-2B, the correct archimedean factor (degree 4) gives:

    Z_∞(1) = 2^{1-k} · π^{-(k+1)} · Γ(k)

For weight k = 12:

    Z_∞(1) = 2^{-11} · π^{-13} · 11!
            ≈ 0.00671239369377...

**Previous error (corrected in v3):** The v2 proof wrote
2π^{-13}·11! ≈ 27.49, which differs by 2^{11} = 2048.

## Ramified corrections Z_p(1) [BLOCKED]

For p | N_π (conductor of π, NOT the symmetric-square conductor), the local
representation π_p falls into one of:
- **Steinberg twist** (conductor exponent 1): Z_p(1) = ? [OBL]
- **Ramified principal series** (conductor exponent ≥ 1): Z_p(1) = ? [OBL]
- **Supercuspidal** (conductor exponent ≥ 2): Z_p(1) = ? [OBL]

**This is the primary blocker.** Each type requires:
1. Explicit Z_p(1) formula from local integral computation
2. Proof that Z_p(1) ≠ 0 by inspection of the formula
3. Quantitative lower bound |Z_p(1)| ≥ c_v > 0

**The nonvanishing Z_p(1) ≠ 0 must come from the explicit formula,
NOT from abstract continuity+compactness arguments.**

## From existence to quantitative (v4 correction)

The reviewer (2026-08-20) correctly identified that proving Z_p(1) ≠ 0
for each form individually is not sufficient. The correct logical chain is:

1. Compute Z_p(1) explicitly for each local type
2. Verify Z_p(1) ≠ 0 by inspection
3. Extract quantitative bound |Z_p(1)| ≥ c_v (type-dependent constant)
4. For continuous families within a type, compactness + nonvanishing
   gives type-specific minimum > 0
5. For the product: C(F_{N_0}) = min_f ∏_p |Z_p(1;f)| > 0

**If c_v < 1 for some type, then ∏ |Z_p(1)| ≥ (c_v)^{ω(N)} → 0 as N → ∞.**
So the downstream bound c ≥ C(F_{N_0}) · (other factors) only works if:
- The product ∏ |Z_p(1)| stays bounded away from 0, OR
- The family F_{N_0} is fixed (finite N_0), OR
- The c_v values are > 1 (unusual)

This is an inherent limitation for the general case.

## Conductor notation (corrected)

- N_π = conductor of π (determines local representation types at p | N_π)
- N_{sym²} = conductor of sym²π (appears in the global L-function)
- N_{Ad} = conductor of Ad(π) (adjoint representation)

## Uniformity: correct argument

### Wrong argument (v1)
"Z_p(1) is continuous → compact set → achieves minimum → min > 0"
This is INVALID because continuity+compactness only gives min ≥ 0.

### Correct argument (v4)
1. For each local type that occurs, compute Z_p(1) explicitly
2. Verify Z_p(1) ≠ 0 by inspection of the formula
3. Extract quantitative bound |Z_p(1)| ≥ c_v > 0
4. For the target family F_{N_0} with level ≤ N_0:

       C(F_{N_0}) = min_{f ∈ F_{N_0}} ( |Z_∞(1;f)| · ∏_{p | N_π(f)} |Z_p(1;f)| ) > 0

   This is a finite minimum of positive numbers (finitely many forms with
   level ≤ N_0, fixed weight and character), hence positive.

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
1. **[BLOCKER]** Explicit computation of Z_p(1) for each local type
2. Quantitative lower bound |Z_p(1)| ≥ c_v > 0 for each type
3. Product bound C(F_{N_0}) > 0 for target family
4. Full archimedean derivation (c_∞ normalization)
