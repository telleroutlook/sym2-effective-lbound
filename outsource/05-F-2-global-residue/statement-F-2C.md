# F-2C: Target-Family Local Positivity/Uniformity (v5)

**Status**: [OBL] — BLOCKED on explicit Z_p(1) formulas

## Desired Statement

For the specific modular form family needed downstream (L(1, sym² f) ≥ c/log N):

**Scope (corrected, v5):** Trivial central character ω = 1 throughout.
For ω ≠ 1, the adjoint L-function is Ad π ≅ Sym² π ⊗ ω⁻¹, and the
entire downstream interface must be reformulated. This package treats only ω = 1.

**Statement [OBL]**: Fix:
- Weight k (holomorphic weight of f)
- Central character ω = 1 (trivial)
- Newvector normalization
- Haar measures on GL₂(A_Q)
- Archimedean vector φ_∞ (holomorphic discrete series of weight k)
- Local type at each p | N_π (Steinberg, ramified principal, supercuspidal)

Then:

1. **Archimedean canonical factor**: L_∞^{can}(1) = 2^{1-k}π^{-(k+1)}Γ(k)
   (this is the canonical L-factor, NOT the local zeta integral)

2. **Archimedean normalization**: Z_∞(1) = h_∞(1) · L_∞^{can}(1)
   where h_∞(1) depends on W_∞, Φ_∞, and Haar measures [OBL]

3. **Ramified corrections**: For each p | N_π, compute Z_p(1) = h_p(1)·L_p^{can}(1)
   explicitly for the specific local type

4. **Local nonvanishing**: For each local type that occurs, Z_v(1) ≠ 0.
   Proved by DIRECT COMPUTATION of the local formula.

5. **Quantitative lower bound**: For each local type, |Z_v(1)| ≥ c_v > 0
   where c_v depends on the local type (but not on the specific form within
   the type)

6. **Uniform product bound**: For the family F_{N_0} of forms with level ≤ N_0:

    C(F_{N_0}) = min_{f ∈ F_{N_0}} ( |Z_∞(1;f)| · ∏_{p | N_π(f)} |Z_p(1;f)| ) > 0

   where the minimum is over the COMPLETE TARGET FAMILY, not just over
   the integer N.

## Why the original uniformity argument was wrong

The original argued: "Z_p(1) is continuous → compact set → achieves minimum → minimum > 0."
This is INVALID because:

- Continuity + compactness gives min ≥ 0, NOT min > 0
- To get min > 0, must first prove Z_p(1) ≠ 0 for every local type
- The nonvanishing must come from EXPLICIT LOCAL FORMULAS, not abstract arguments

Correct order (v5):
    explicit local formula → Z_p(1) ≠ 0 → quantitative lower bound |Z_p(1)| ≥ c_v > 0
    → product bound C(F_{N_0}) > 0

## Conductor notation

- N_π = conductor of π (determines local representation types at p | N_π)
- N_{sym²} = conductor of sym²π (appears in the global L-function)
- N_{Ad} = conductor of Ad(π) (adjoint representation)

Local type classification at p uses N_π, NOT N_{sym²}.

## Local type classification (corrected, v5)

For level-N_π forms with trivial central character, the local representation
at p | N_π falls into:

- **Unramified principal series** (a(π_p) = 0): handled by Casselman–Shalika
- **Steinberg twist χ·St** (conductor exponent depends on χ):
  - a(χ·St) = 1 if χ is unramified (a(χ) = 0)
  - a(χ·St) = 2a(χ) if χ is ramified (a(χ) > 0)
- **Ramified principal series** (a(π_p) = a(χ₁) + a(χ₂) ≥ 1):
  a(π_p) can be any positive integer depending on χ₁, χ₂
- **Supercuspidal** (a(π_p) ≥ 2): conductor exponent at least 2

**Note:** Since we require trivial central character ω = 1, the Steinberg twist
character χ is determined by ω and the central character of the inducing data.
The conductor exponent formula is NOT always 1 for Steinberg — it depends on χ.

Each type has a distinct Z_p(1) formula. The classification must use
the conductor of π (N_π), NOT the symmetric-square conductor N_{sym²}.

## Why min over N is insufficient

The same level N can have:
- Different newforms (different eigenvalues)
- Different local types at the same prime
- Different local Z_p(1) values

The minimum must be over the COMPLETE FAMILY of forms, not just over
the level integers.

## Status: [OBL]

The main tasks are:
1. **[BLOCKER]** Explicit computation of Z_p(1) for each local type
2. Quantitative lower bound |Z_p(1)| ≥ c_v > 0 for each type
3. Product bound C(F_{N_0}) > 0 for target family
4. Archimedean normalization h_∞(1) computation
