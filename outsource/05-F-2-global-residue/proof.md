# F-2: Global Residue Positivity — Combined Proof (v5)

**Status**: [PARTIAL] (restructured v5, 2026-08-20)

**Scope:** Trivial central character ω = 1 throughout.

## F-2A: Diagonal global residue positivity

See `proof-F-2A.md`.

**Status: PASS / [THM/REFEREED]**

The diagonal residue formula is verified correct by reviewer (2026-08-20).
Core argument: JS81 §4.3(2) + §4.5(5) + §4.6(i), with W_φ ∈ W⁰(π; ψ),
producing norm-square |W_φ(g)|² → positive residue.

## F-2B: Euler factor extraction

See `proof-F-2B.md`.

**v5 corrections:**
- Canonical L_v^{can} vs actual Ψ_v = h_v·L_v^{can}: clearly distinguished
- Φ_p ∈ S(Q_p²) = C_c^∞(Q_p²), not C_c^∞(GL₂(Q_p)) (JS81 §4.5)
- Normalization factor h_v(s) depends on W_v, Φ_v, Haar measures
- L_∞^{can}(1) = 2^{1-k}π^{-(k+1)}Γ(k) is canonical; Ψ_∞(1) = h_∞(1)·L_∞^{can}(1)

**Status**: [OBL] — ramified local factors Z_p(1) not computed;
h_∞(1) not computed.

## F-2C: Target-family uniformity

See `proof-F-2C.md`.

**v5 corrections:**
- Steinberg twist conductor: a(χ·St) = 1 if χ unramified, 2a(χ) otherwise
- Trivial nebentypus scope: ω = 1 enforced throughout
- Archimedean: Ψ_∞(1) = h_∞(1)·L_∞^{can}(1), not just L_∞^{can}(1)

**Status**: [OBL] — no explicit Z_p(1) formulas, no quantitative C(F_{N_0})

## Blockers (v5)

1. **F-2B**: Ramified local factors Z_p(1) = h_p(1)·L_p^{can}(1) for each type [OBL]
2. **F-2B**: Normalization constant h_∞(1) for archimedean place [OBL]
3. **F-2B**: Consistent normalization of all measures/functions [OBL]
4. **F-2B**: Full archimedean derivation from local integral [OBL]
5. **F-2C**: Explicit nonvanishing proof for each local type [OBL]
6. **F-2C**: Quantitative C(F_{N_0}) computation [OBL]
