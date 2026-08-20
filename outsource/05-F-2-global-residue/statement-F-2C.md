# F-2C: Target-Family Local Positivity/Uniformity

## Desired Statement

For the specific modular form family needed downstream (L(1, sym² f) ≥ c/log N):

**Statement [OBL]**: Fix:
- Level N (conductor of the symmetric square)
- Weight k (holomorphic weight of f)
- Nebentypus χ (if applicable)
- Newvector normalization
- Haar measures on GL₂(A_Q)
- Archimedean vector φ_∞ (holomorphic discrete series of weight k)
- Local type at each p | N (Steinberg, ramified principal, supercuspidal)

Then:

1. **Archimedean correction**: Z_∞(1) is computed explicitly in terms of k
   (with correct degree-4 factorization from F-2B)

2. **Ramified corrections**: For each p | N, Z_p(1) is computed explicitly
   for the specific local type

3. **Local nonvanishing**: For each local type that occurs, Z_v(1) ≠ 0.
   This must be proved by DIRECT COMPUTATION of the local formula,
   NOT by continuity+compactness.

4. **Uniform lower bound**: For the family of forms with level ≤ N₀:

    C(N₀) = min_{N ≤ N₀} ∏_{v | N∞} |Z_v(1)| > 0

   where the product is over ALL places (finite and archimedean) that vary.

## Why the original uniformity argument was wrong

The original argued: "Z_p(1) is continuous → compact set → achieves minimum → minimum > 0."
This is INVALID because:

- Continuity + compactness gives min ≥ 0, NOT min > 0
- To get min > 0, must first prove Z_p(1) ≠ 0 for every local type
- The nonvanishing must come from EXPLICIT LOCAL FORMULAS, not abstract arguments

Correct order:
    explicit local formula → Z_p(1) ≠ 0 → quantitative lower bound

## Product bound: c_loc vs C_global

The downstream needs the PRODUCT bound ∏ |Z_v(1)| ≥ C > 0, not just individual
bounds min |Z_p(1)| ≥ c' > 0.

If c' < 1, then ∏ |Z_p(1)| ≥ (c')^{ω(N)} which degenerates.

Correct approach: define

    C(N₀) = min_{N ≤ N₀} ∏_{p | N} |Z_p(1)| > 0

directly (finite minimum over finitely many N ≤ N₀).

## Local type classification

For level-N forms, the local representation at p | N falls into:
- **Steinberg twist** (conductor exponent 1)
- **Ramified principal series** (conductor exponent ≥ 1)
- **Supercuspidal** (conductor exponent ≥ 2)

Each type has a distinct Z_p(1) formula. The classification must use
the conductor of π (NOT the symmetric-square conductor N_{sym²π}).

## Status: [OBL]

This is the most concrete obligation and directly interfaces with the
computational pipeline.
