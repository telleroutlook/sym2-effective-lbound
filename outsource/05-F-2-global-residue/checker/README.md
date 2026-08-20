# F-2 Checker README (v5)

## What it checks

1. **Required files**: statement.md, proof.md, dependencies.yaml, limitations.md, novelty.md
2. **[OBL] status**: No file promotes F-2B/F-2C to [THM] without [OBL] tag
3. **F-2A coverage**: diagonal, norm-square, jacquet–shalika in proof-F-2A.md
4. **F-2B coverage**: euler factor, archimedean, ramified in proof-F-2B.md
5. **F-2C coverage**: uniformity, local, explicit in proof-F-2C.md
6. **Forbidden patterns** (v5):
   - "Ann. Math. 114" — wrong JS81 citation
   - Old Z_∞(1) formula: "2π^{-k-1}Γ(k)" (off by 2^k)
   - Old "Lemma 4.4" as citation chain (should be §4.3(2) + §4.5(5) + §4.6(i))
   - Old "min over N ≤ N₀" (should be min over f ∈ F_{N₀})
   - Old "Godement–Jacquet" for local integral (should be JS/Rankin–Selberg Whittaker)
   - Old "C_c^∞(GL₂(Q_p))" for test function space (should be S(Q_p²))
   - Old "conductor exponent 1" for Steinberg without clarifying χ-dependence

## What it does NOT check

- Mathematical correctness of Euler factors
- Exact Γ-factor computation
- Quantitative bounds
- Whether Z_∞ derivation is from local integral vs degree counting
- Whether ramified factors are actually computed
- Whether h_∞(1) has been computed
- Whether the checker README accurately describes its own capabilities

## Version history

- v1 (2026-08-20): Initial checker
- v2 (2026-08-20): Added citation, Adjoint factor, uniformity forbidden patterns
- v4 (2026-08-20): Added old formula, old HL94 pages, old citation chain, old min patterns
- v5 (2026-08-20): Removed overclaims from README; added S(Q_p²), Steinberg conductor patterns
