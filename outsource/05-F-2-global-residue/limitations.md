# Limitations — F-2 v3

## F-2A

- Applies only to unitary cuspidal π with trivial central character
- The constant c_Q depends on normalization choices
- Does not give an explicit numerical value (only positivity)
- Citation chain corrected: JS81 §4.3(2) + §4.5(5) + §4.6(i), not "Lemma 4.4 + 4.6(i)"

## F-2B (v3 corrections)

- Adjoint factor now correctly has 3 Euler factors (was 1 — load-bearing error fixed in v2)
- **Z_∞(1) corrected: 2^{1-k}π^{-(k+1)}Γ(k) (was wrong by 2^k factor in v2)**
- Euler product attribution corrected: pure tensor + Fubini, not strong approximation
- Local integral attribution corrected: JS/Rankin–Selberg Whittaker, not Godement–Jacquet
- Ramified factors still not computed explicitly [OBL]
- Pure-tensor hypothesis required for factorization
- Archimedean derivation is a sketch, not a full proof from local integral [OBL]

## F-2C (v3 corrections)

- **Conductor notation split: N_π ≠ N_{sym²} ≠ N_{Ad} (was self-contradicting in v2)**
- **Minimum over family F_{N_0}, not over integer N (was insufficient in v2)**
- Z_∞(1) corrected to 2^{1-k}π^{-(k+1)}Γ(k) (was 2π^{-k-1}Γ(k) in v2, off by 2^k)
- Uniformity argument now requires explicit nonvanishing (continuity alone insufficient)
- Product bound C(F_{N_0}) properly separated from individual c_loc
- Local type classification uses N_π, not N_{sym²}

## Checker

- 5 tests pass (structural verification only)
- Checker explicitly does NOT check: Euler factor math, exact Γ-factor,
  quantitative bound, Z_∞ correctness
- checker PASS ≠ proof PASS

## MANIFEST (v2 issues)

- v2 used 16-char SHA-256 prefixes (not full 64-char)
- v2 included .pytest_cache files not in ZIP
- v3: full 64-char SHA-256, no build artifacts

## Scope

- Does NOT claim GRH
- Does NOT give an explicit general lower bound (that is c_eff)
- Does NOT treat the Siegel zero (that is M-3)
