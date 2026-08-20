# Limitations — F-2 v4

## F-2A

- Applies only to unitary cuspidal π with trivial central character
- The constant c_Q depends on normalization choices
- Does not give an explicit numerical value (only positivity)
- **v4**: W quantifier fixed: W_φ ∈ W⁰(π; ψ), not ambient W(π; ψ)
- **v4**: Citation chain fixed: §4.3(2) + §4.5(5) + §4.6(i), not "Lemma 4.4"

## F-2B

- Adjoint factor now correctly has 3 Euler factors (was 1 — load-bearing error)
- **Z_∞(1) corrected: 2^{1-k}π^{-(k+1)}Γ(k) (was wrong by 2^k in v2)**
- Euler product attribution corrected: pure tensor + Fubini, not strong approximation
- Local integral attribution corrected: JS/Rankin–Selberg Whittaker, not Godement–Jacquet
- **v4**: Z_∞ derivation: real Weil-group ρ_{k-1} parameter (not just "degree 4")
- **v4**: Z_∞ derivation is still a consistency argument, not full local integral [OBL]
- **[BLOCKER]** Ramified factors Z_p(1) still not computed [OBL]
- Pure-tensor hypothesis required for factorization
- Normalization constant c_∞(1) for Ψ_∞ = c_∞ · L_∞ not computed [OBL]

## F-2C

- **Conductor notation split: N_π ≠ N_{sym²} ≠ N_{Ad}**
- **Minimum over family F_{N_0}, not over integer N**
- Z_∞(1) corrected to 2^{1-k}π^{-(k+1)}Γ(k)
- Uniformity argument requires explicit nonvanishing (continuity alone insufficient)
- Product bound C(F_{N_0}) properly separated from individual c_loc
- **v4**: Existence → quantitative: need |Z_p(1)| ≥ c_v > 0, not just ≠ 0
- **v4**: If c_v < 1, product ∏ |Z_p(1)| may degenerate as N grows

## Checker

- 5 tests pass (structural verification only)
- Checker explicitly does NOT check: Euler factor math, exact Γ-factor,
  quantitative bound, Z_∞ correctness
- checker PASS ≠ proof PASS

## MANIFEST

- v2 used 16-char SHA-256 prefixes (not full 64-char)
- v2 included .pytest_cache files not in ZIP
- v3: full 64-char SHA-256, no build artifacts

## Scope

- Does NOT claim GRH
- Does NOT give an explicit general lower bound (that is c_eff)
- Does NOT treat the Siegel zero (that is M-3)
