# Limitations — F-2 v5

## F-2A — PASS / [THM/REFEREED]

- Applies only to unitary cuspidal π with trivial central character ω = 1
- The constant c_Q depends on normalization choices
- Does not give an explicit numerical value (only positivity)
- W quantifier: W_φ ∈ W⁰(π; ψ), not ambient W(π; ψ)
- Citation chain: §4.3(2) + §4.5(5) + §4.6(i)

## F-2B

- Adjoint factor correctly has 3 Euler factors (degree 3 adjoint)
- **Canonical L_v^{can} vs actual Ψ_v = h_v·L_v^{can}**: clearly distinguished (v5)
- L_∞^{can}(1) = 2^{1-k}π^{-(k+1)}Γ(k) is canonical; Ψ_∞(1) = h_∞(1)·L_∞^{can}(1)
- Euler product attribution: pure tensor + Fubini, not strong approximation
- Local integral attribution: JS/Rankin–Selberg Whittaker, not Godement–Jacquet
- **Φ_p ∈ S(Q_p²) = C_c^∞(Q_p²)**, not C_c^∞(GL₂(Q_p)) (v5, corrected per reviewer)
- Z_∞ derivation: real Weil-group ρ_{k-1} parameter (consistency argument, not full derivation)
- **[BLOCKER]** Ramified factors Z_p(1) = h_p(1)·L_p^{can}(1) still not computed
- **[BLOCKER]** Normalization constant h_∞(1) for archimedean place not computed
- Pure-tensor hypothesis required for factorization

## F-2C

- **Trivial nebentypus ω = 1 enforced throughout** (v5, corrected per reviewer)
- Conductor notation split: N_π ≠ N_{sym²} ≠ N_{Ad}
- Minimum over family F_{N_0}, not over integer N
- **Steinberg twist conductor: a(χ·St) = 1 if χ unramified, 2a(χ) if χ ramified** (v5)
- Uniformity argument requires explicit nonvanishing (continuity alone insufficient)
- Product bound C(F_{N_0}) properly separated from individual c_loc
- Existence → quantitative: need |Z_p(1)| ≥ c_v > 0, not just ≠ 0
- If c_v < 1, product ∏ |Z_p(1)| may degenerate as N grows

## Checker

- Structural verification only (checker PASS ≠ proof PASS)
- Checker does NOT check: Euler factor math, exact Γ-factor,
  quantitative bound, Z_∞ correctness, h_∞(1) computation
- v5: Updated forbidden patterns (S(Q_p²), Steinberg conductor)
- v5: F-2A allowed [THM/REFEREED] status

## Scope

- Does NOT claim GRH
- Does NOT give an explicit general lower bound (that is c_eff)
- Does NOT treat the Siegel zero (that is M-3)
- **Trivial central character only** (ω ≠ 1 requires Ad π ≅ Sym² π ⊗ ω⁻¹ reformulation)
