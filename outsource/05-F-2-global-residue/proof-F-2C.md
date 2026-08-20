# F-2C: Target-Family Local Positivity/Uniformity — Proof (v5)

## Scope (corrected, v5)

**Trivial central character ω = 1 throughout.**
For ω ≠ 1, the adjoint L-function is Ad π ≅ Sym² π ⊗ ω⁻¹, and the
entire downstream interface must be reformulated.

## Archimedean correction

### Canonical L-factor

From F-2B, the correct canonical archimedean factor (degree 4) gives:

    L_∞^{can}(1) = 2^{1-k} · π^{-(k+1)} · Γ(k)

For weight k = 12:

    L_∞^{can}(1) = 2^{-11} · π^{-13} · 11!
                 ≈ 0.00671239369377...

### Actual local zeta integral

The actual local zeta integral at ∞ is:

    Ψ_∞(1) = h_∞(1) · L_∞^{can}(1)

where h_∞(1) depends on W_∞, Φ_∞, and Haar measures.
**Computing h_∞(1) is [OBL].**

## Ramified corrections Z_p(1) [BLOCKED]

For p | N_π (conductor of π, NOT the symmetric-square conductor), the local
representation π_p falls into one of:

- **Unramified principal series** (a(π_p) = 0): handled by Casselman–Shalika
- **Steinberg twist χ·St**: a(χ·St) = 1 if χ unramified, 2a(χ) if χ ramified
- **Ramified principal series** (a(π_p) = a(χ₁) + a(χ₂) ≥ 1)
- **Supercuspidal** (a(π_p) ≥ 2)

**This is the primary blocker.** Each type requires:
1. Explicit Z_p(1) = h_p(1) · L_p^{can}(1) formula from local integral computation
2. Proof that Z_p(1) ≠ 0 by inspection of the formula
3. Quantitative lower bound |Z_p(1)| ≥ c_v > 0

**The nonvanishing Z_p(1) ≠ 0 must come from the explicit formula,
NOT from abstract continuity+compactness arguments.**

## Local type classification (corrected, v5)

The conductor exponent a(π_p) determines the local representation type:

- **Unramified principal series** (a(π_p) = 0)
- **Steinberg twist χ·St**: conductor exponent = 1 if χ unramified, = 2a(χ) if χ ramified
- **Ramified principal series** (a(π_p) = a(χ₁) + a(χ₂) ≥ 1)
- **Supercuspidal** (a(π_p) ≥ 2)

**Key correction:** The conductor exponent of a Steinberg twist is NOT
always 1. When the twisting character χ has conductor a(χ) > 0, the
Steinberg twist has conductor 2a(χ).

## From existence to quantitative (v4 correction retained)

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

## Uniformity: correct argument

### Wrong argument (v1)
"Z_p(1) is continuous → compact set → achieves minimum → min > 0"
This is INVALID because continuity+compactness only gives min ≥ 0.

### Correct argument (v5)
1. For each local type that occurs, compute Z_p(1) = h_p(1)·L_p^{can}(1) explicitly
2. Verify Z_p(1) ≠ 0 by inspection of the formula
3. Extract quantitative bound |Z_p(1)| ≥ c_v > 0
4. For the target family F_{N_0} with level ≤ N_0:

       C(F_{N_0}) = min_{f ∈ F_{N_0}} ( |Ψ_∞(1;f)| · ∏_{p | N_π(f)} |Z_p(1;f)| ) > 0

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

where C(F_{N_0}) is the product of all local corrections (including h_∞(1))
for the worst case in the target family.

## Status: [OBL]

The main tasks are:
1. **[BLOCKER]** Explicit computation of Z_p(1) = h_p(1)·L_p^{can}(1) for each local type
2. Quantitative lower bound |Z_p(1)| ≥ c_v > 0 for each type
3. Product bound C(F_{N_0}) > 0 for target family
4. Archimedean normalization h_∞(1) computation
