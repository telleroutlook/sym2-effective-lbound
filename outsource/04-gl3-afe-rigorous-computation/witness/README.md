# Witness — GL_3 AFE computation

`grid_values.json` contains:

1. **Certificate**: module, status, method, N_coeffs, N_afe, X, grid ranges,
   minimum |L(s)| over the grid, spot-check L(2).
   **certifies_zero_free = false** — finite grid cannot certify continuous region.
2. **Grid**: list of {sigma, t, L_re, L_im, L_mod, method} for 70 points:
   - 5x9 = 45 points in critical strip [0.6, 1.0] x [-20, 20] (two-term AFE)
   - 5x5 = 25 points in Re(s) > 1 region [1.01, 2.0] x [0, 20] (Dirichlet)

**Key finding (machine-derived, checker/recompute_stats.py):** min |L(s)| = 0.33403921 at (sigma=0.6, t=-20) via the TWO-TERM (main + dual) AFE — the grid values were produced by the dual-sum code; the old 'single-sum only / dual sum present' note in the JSON was stale metadata from a previous version and has been corrected in this README. All statistics are recomputed from the JSON; hand-copied values are forbidden.
This is a DISCOVERY-TIER diagnostic, NOT a certified L(s) value.

**What this is NOT:**
- NOT a certified L(s) evaluation (mpmath floats, no Arb intervals).
- NOT a zero-free region certificate (finite grid, no continuity argument).
- NOT suitable as a premise for downstream proofs.

**Spot-check:** L(2) = 0.805913 via truncated Dirichlet (N=200).
The tail error is O(N^{-1}) ~ 5e-3, so this matches to ~3 digits.

**Coefficient computation:** Uses exact tau(n) from Euler product, but
computes c_p = tau(p)/p^{5.5} in floating point. For proof-tier,
should use rational tau(p)^2/p^{11}.
