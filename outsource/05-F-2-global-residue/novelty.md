# Novelty — F-2 v5

## What is new (cumulative v1→v5)

### v1→v2
1. **Corrected integral definition**: N(A)\GL₂(A) with Φ(e₂ g), not N(A)G(Q)\G(A) with Φ(g).
2. **Corrected Adjoint Euler factor**: From single factor to correct 3-factor [(1-x)(1-αβ⁻¹x)(1-βα⁻¹x)]⁻¹.
3. **Corrected citation**: JS81 is Am. J. Math. 103(3) (1981), 499–558.
4. **Added pure-tensor hypothesis**: Factorization ∏_v Ψ_v requires W = ⊗_v W_v.
5. **Corrected archimedean degree**: Z_∞ degree 4 (includes ζ_∞).

### v2→v3
6. **Corrected Z_∞(1) formula**: 2^{1-k}π^{-(k+1)}Γ(k) (was 2π^{-k-1}Γ(k), off by 2^k).
7. **Fixed uniformity argument**: Nonvanishing from explicit formulas, then continuity+compactness gives min > 0.
8. **Separated c_loc from C_global**: Product bound C(F_{N_0}) defined correctly.
9. **Conductor notation split**: N_π ≠ N_{sym²} ≠ N_{Ad}.
10. **Local integral attribution**: JS/Rankin–Selberg Whittaker (not Godement–Jacquet).

### v3→v4 (per reviewer verdict 2026-08-20)
11. **F-2A quantifier**: W_φ ∈ W⁰(π; ψ) (not ambient W(π; ψ)).
12. **F-2A citation chain**: §4.3(2) + §4.5(5) + §4.6(i) (not "Lemma 4.4").
13. **Z_∞ derivation**: Real Weil-group ρ_{k-1} = Ind((z/|z|)^{k-1}) parameter.
14. **F-2C quantitative**: Existence → quantitative bound |Z_p(1)| ≥ c_v > 0.

### v4→v5 (per reviewer verdict 2026-08-20)
15. **F-2A upgraded**: [THM/REFEREED] — PASS (reviewer confirmed diagonal positivity correct).
16. **Canonical L_v^{can} vs actual Ψ_v = h_v·L_v^{can}**: clearly distinguished throughout.
    Z_∞(1) is canonical; Ψ_∞(1) = h_∞(1)·L_∞^{can}(1) is actual zeta integral.
17. **Φ_p space corrected**: S(Q_p²) = C_c^∞(Q_p²), not C_c^∞(GL₂(Q_p)) (JS81 §4.5).
18. **Steinberg conductor corrected**: a(χ·St) = 1 if χ unramified, 2a(χ) if χ ramified.
    Not always conductor exponent 1.
19. **Trivial nebentypus scope**: ω = 1 enforced throughout. For ω ≠ 1, Ad ≅ Sym²⊗ω⁻¹.
20. **Checker updated**: v5 patterns, F-2A [THM/REFEREED] allowed, README overclaims removed.

## What is NOT new

- F-2A diagonal positivity argument (established in v1, just definition fixed)
- The factorization L(s, π × π̃) = ζ(s) · L(s, π, Ad)
- The local newvector theory (Casselman 1973)
- Hoffstein–Lockhart 1994 (the target reference for downstream)
