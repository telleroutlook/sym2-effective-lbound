# F-2: Global Residue Positivity — Combined Statement (v4)

**Status**: [OBL] (restructured v4, 2026-08-20)

## Overview

This obligation establishes that the global Rankin–Selberg residue is strictly
positive and extracts the exact Euler factors for use in explicit lower bounds.

## F-2A: Diagonal global residue positivity

See `statement-F-2A.md`. Core argument verified correct by reviewer (2026-08-20).

**v4 corrections (per reviewer verdict 2026-08-20):**
- W quantifier: W_φ ∈ W⁰(π; ψ) (not ambient W(π; ψ))
- Citation chain: §4.3(2) + §4.5(5) + §4.6(i) (not "Lemma 4.4")

**Status**: [OBL — CONDITIONAL, ready for PASS after v4]

## F-2B: Exact Euler-factor extraction

See `statement-F-2B.md`.

**v3 corrections:**
1. Adjoint Euler factor: 3 factors [(1-x)(1-αβ⁻¹x)(1-βα⁻¹x)]⁻¹ (was 1 — load-bearing error)
2. Pure-tensor hypothesis W = ⊗_v W_v for ∏_v factorization
3. Satake parameters: inverses α⁻¹, β⁻¹ for π̃ (not complex conjugates)
4. Archimedean factor: Z_∞(1) = 2^{1-k}π^{-(k+1)}Γ(k) (was 2π^{-k-1}Γ(k), off by 2^k)
5. Local integral: JS/Rankin–Selberg Whittaker (not Godement–Jacquet)

**v4 corrections (per reviewer verdict 2026-08-20):**
- Z_∞ derivation: explicit local integral sketch added (not just "degree 4")
- Langlands parameter: real Weil-group ρ_{k-1} (not "μ = (k-1,-(k-1))")
- Bad primes: explicitly marked as main blocker [OBL]

**Status**: [OBL] — ramified local factors Z_p(1) not computed

## F-2C: Target-family local positivity/uniformity

See `statement-F-2C.md`.

**v3 corrections:**
- Conductor notation split: N_π ≠ N_{sym²} ≠ N_{Ad}
- Minimum over family F_{N_0}, not integer N
- Z_∞(1) corrected to 2^{1-k}π^{-(k+1)}Γ(k)
- Uniformity: explicit nonvanishing required (continuity alone insufficient)

**v4 corrections (per reviewer verdict 2026-08-20):**
- From existence to quantitative: explicit formula → Z_p(1)≠0 → quantitative lower bound
- Downstream needs uniform bound C(F_{N_0}), not just existence for individual forms

**Status**: [OBL] — no explicit Z_p(1) formulas, no quantitative C(F_{N_0})

## Dependencies

- JS81 §4.3(2), §4.5(5), §4.6(i) (Am. J. Math. 103(3) (1981), 499–558)
- JS/Rankin–Selberg Whittaker local integrals (JS81 §4.7, §1, §3)
- Casselman newvector theory (Math. Ann. 201 (1973), 301–314)
- L(s, π × π̃) = ζ(s) · L(s, π, Ad) factorization (standard)
- Hoffstein–Lockhart 1994 (Ann. Math. 140(1) (1994), 161–181)

## What is NOT claimed

- GRH is NOT assumed
- L(1, π, Ad) > 0 is NOT a prerequisite
- An explicit general lower bound is NOT given (that is c_eff)

## Blockers (v4)

1. **F-2B**: Ramified local factors Z_p(1) for Steinberg/ramified principal/supercuspidal [OBL]
2. **F-2B**: Consistent normalization of Haar measures, Whittaker functions, Φ_v [OBL]
3. **F-2B**: Full archimedean derivation from local integral (not degree counting) [OBL]
4. **F-2C**: Explicit nonvanishing proof for each local type [OBL]
5. **F-2C**: Quantitative C(F_{N_0}) computation (not just existence) [OBL]
