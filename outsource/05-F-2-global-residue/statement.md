# F-2: Global Residue Positivity — Combined Statement (v5)

**Status**: [PARTIAL] (restructured v5, 2026-08-20)

## Overview

This obligation establishes that the global Rankin–Selberg residue is strictly
positive and extracts the exact Euler factors for use in explicit lower bounds.

**Scope:** Trivial central character ω = 1 throughout. For ω ≠ 1, replace
L(s, π × π̃) with L(s, Ad π) where Ad π ≅ Sym² π ⊗ ω⁻¹.

## F-2A: Diagonal global residue positivity

See `statement-F-2A.md`.

**v5 status: PASS / [THM/REFEREED]**

The diagonal residue formula is verified correct by reviewer (2026-08-20).
Core argument: JS81 §4.3(2) + §4.5(5) + §4.6(i), with W_φ ∈ W⁰(π; ψ),
producing norm-square |W_φ(g)|² → positive residue.

## F-2B: Exact Euler-factor extraction

See `statement-F-2B.md`.

**v5 corrections:**
- Canonical L_∞^{can} vs actual Z_∞ = h_∞(1)·L_∞^{can}(1): clearly distinguished
- Φ_p ∈ S(Q_p²), not C_c^∞(GL₂(Q_p)) (JS81 §4.5)

**Status**: [OBL] — ramified local factors Z_p(1) not computed;
normalization constant h_∞(1) not computed.

## F-2C: Target-family local positivity/uniformity

See `statement-F-2C.md`.

**v5 corrections:**
- Steinberg twist conductor: a(χ·St) = 1 if χ unramified, 2a(χ) otherwise
- Trivial nebentypus scope: ω = 1 enforced throughout

**Status**: [OBL] — no explicit Z_p(1) formulas, no quantitative C(F_{N_0})

## Dependencies

- JS81 §4.3(2), §4.5(5), §4.6(i) (Am. J. Math. 103(3) (1981), 499–558)
- JS/Rankin–Selberg Whittaker local integrals (JS81 §4.7, §1, §3)
- Casselman newvector theory (Math. Ann. 201 (1973), 301–314)
- L(s, π × π̃) = ζ(s) · L(s, π, Ad) factorization (standard)
- Hoffstein–Lockhart 1994 (Ann. Math. 140(1) (1994), 161–181)

## What is NOT claimed

- GRH is NOT assumed
- L(1, π, Ad) > 0 is NOT a prerequisite (residue positivity is by norm-square)
- An explicit general lower bound is NOT given (that is c_eff)

## Blockers (v5)

1. **F-2B**: Ramified local factors Z_p(1) for each local type [OBL]
2. **F-2B**: Consistent normalization of Haar measures, Whittaker functions, Φ_v [OBL]
3. **F-2B**: Normalization constant h_∞(1) (not c_∞(1)) for Z_∞ = h_∞·L_∞^{can} [OBL]
4. **F-2B**: Full archimedean derivation from local integral (not degree counting) [OBL]
5. **F-2C**: Explicit nonvanishing proof for each local type [OBL]
6. **F-2C**: Quantitative C(F_{N_0}) computation (not just existence) [OBL]
