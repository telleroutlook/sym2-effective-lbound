# F-2: Global Residue Positivity — Combined Proof (v4)

**Status**: [OBL] (restructured v4, 2026-08-20)

## F-2A: Diagonal global residue positivity

See `proof-F-2A.md`. Core argument verified correct by reviewer (2026-08-20).

**v4 corrections (per reviewer verdict 2026-08-20):**
- W quantifier: W_φ ∈ W⁰(π; ψ) (not ambient W(π; ψ))
- Citation chain: §4.3(2) + §4.5(5) + §4.6(i) (not "Lemma 4.4")

## F-2B: Euler factor extraction

See `proof-F-2B.md`.

**v3 corrections:**
- Adjoint factor: 3-dimensional {1, αβ⁻¹, βα⁻¹}, not single factor
- Pure-tensor factorization: requires W = ⊗_v W_v
- Archimedean: Z_∞(1) = 2^{1-k}π^{-(k+1)}Γ(k) (was 2π^{-k-1}Γ(k), off by 2^k)
- Local integral: JS/Rankin–Selberg Whittaker (not Godement–Jacquet)

**v4 corrections (per reviewer verdict 2026-08-20):**
- Z_∞ derivation: explicit local integral sketch (real Weil-group parameter)
- Bad primes: explicitly documented as main blocker
- Langlands parameter: ρ_{k-1} = Ind_{W_C}^{W_R}((z/|z|)^{k-1})

## F-2C: Target-family uniformity

See `proof-F-2C.md`.

**v3 corrections:**
- Uniformity via explicit nonvanishing + finite minimum (not continuity)
- C(F_{N_0}) = min_{f ∈ F_{N_0}} ∏_p |Z_p(1;f)| > 0 (family minimum, not integer N)
- Local type classification by conductor of π (N_π)

**v4 corrections (per reviewer verdict 2026-08-20):**
- Existence → quantitative: explicit formula → Z_p(1)≠0 → quantitative bound
- Downstream needs uniform C(F_{N_0}), not just existence

## Blockers (v4)

1. **F-2B**: Ramified local factors Z_p(1) for each local type [OBL]
2. **F-2B**: Consistent normalization of all measures/functions [OBL]
3. **F-2B**: Full archimedean derivation from local integral [OBL]
4. **F-2C**: Explicit nonvanishing proof for each local type [OBL]
5. **F-2C**: Quantitative C(F_{N_0}) computation [OBL]
