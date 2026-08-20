# F-2C: Target-Family Local Positivity/Uniformity

## Desired Statement

For the specific modular form family needed downstream (L(1, sym² f) ≥ c/log N):

**Statement [OBL]**: Fix:
- Weight k (holomorphic weight of f)
- Nebentypus χ (if applicable)
- Newvector normalization
- Haar measures on GL₂(A_Q)
- Archimedean vector φ_∞ (holomorphic discrete series of weight k)
- Local type at each p | N_π (Steinberg, ramified principal, supercuspidal)

Then:

1. **Archimedean correction**: Z_∞(1) = 2^{1-k}π^{-(k+1)}Γ(k) (corrected per 2026-08-20 review)

2. **Ramified corrections**: For each p | N_π, Z_p(1) is computed explicitly
   for the specific local type

3. **Local nonvanishing**: For each local type that occurs, Z_v(1) ≠ 0.
   This must be proved by DIRECT COMPUTATION of the local formula,
   NOT by continuity+compactness.

4. **Uniform lower bound**: For the family F_{N_0} of forms with level ≤ N_0:

    C(F_{N_0}) = min_{f ∈ F_{N_0}} ( |Z_∞(1;f)| · ∏_{p | N_π(f)} |Z_p(1;f)| ) > 0

   where the minimum is over the COMPLETE TARGET FAMILY, not just over
   the integer N.

## Why the original uniformity argument was wrong

The original argued: "Z_p(1) is continuous → compact set → achieves minimum → minimum > 0."
This is INVALID because:

- Continuity + compactness gives min ≥ 0, NOT min > 0
- To get min > 0, must first prove Z_p(1) ≠ 0 for every local type
- The nonvanishing must come from EXPLICIT LOCAL FORMULAS, not abstract arguments

Correct order:
    explicit local formula → Z_p(1) ≠ 0 → quantitative lower bound

## Conductor notation (corrected per 2026-08-20 review)

The previous version used N for both "conductor of π" and "conductor of the
symmetric square" — these are different quantities. Corrected notation:

- N_π = conductor of π (determines local representation types at p | N_π)
- N_{sym²} = conductor of sym²π (appears in the global L-function)
- N_{Ad} = conductor of Ad(π) (adjoint representation)

The local type classification at p uses N_π, NOT N_{sym²}.

## Product bound: c_loc vs C_global

The downstream needs the PRODUCT bound ∏ |Z_v(1)| ≥ C > 0, not just individual
bounds min |Z_p(1)| ≥ c' > 0.

If c' < 1, then ∏ |Z_p(1)| ≥ (c')^{ω(N)} which degenerates.

Correct approach: define

    C(F_{N_0}) = min_{f ∈ F_{N_0}} ( |Z_∞(1;f)| · ∏_{p | N_π(f)} |Z_p(1;f)| )

directly (finite minimum over finitely many forms with level ≤ N_0).

## Why min over N is insufficient

The same level N can have:
- Different newforms (different eigenvalues)
- Different local types at the same prime
- Different local Z_p(1) values

The minimum must be over the COMPLETE FAMILY of forms, not just over
the level integers.

## Local type classification

For level-N_π forms, the local representation at p | N_π falls into:
- **Steinberg twist** (conductor exponent 1)
- **Ramified principal series** (conductor exponent ≥ 1)
- **Supercuspidal** (conductor exponent ≥ 2)

Each type has a distinct Z_p(1) formula. The classification must use
the conductor of π (N_π), NOT the symmetric-square conductor N_{sym²}.

## Status: [OBL]

This is the most concrete obligation and directly interfaces with the
computational pipeline.
