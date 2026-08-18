# Witness — GL_3 AFE computation

`grid_values.json` contains:

1. **Certificate**: module, status, method, N_terms, X, grid ranges,
   minimum |L(s)| over the grid, spot-check L(2).
   **certifies_zero_free = false** — finite grid cannot certify continuous region.
2. **Grid**: list of {sigma, t, L_re, L_im, L_mod, method} for 70 points:
   - 5x9 = 45 points in critical strip [0.6, 1.0] x [-20, 20] (single-sum AFE)
   - 5x5 = 25 points in Re(s) > 1 region [1.01, 2.0] x [0, 20] (Dirichlet)

**Key finding:** min |L(s)| = 0.404207 at (sigma=0.6, t=0) via single-sum AFE.
This is a DISCOVERY-TIER diagnostic, NOT a certified L(s) value.

**What this is NOT:**
- NOT a certified L(s) evaluation (missing dual sum, no Arb intervals).
- NOT a zero-free region certificate (finite grid, no continuity argument).
- NOT suitable as a premise for downstream proofs.

**Spot-check:** L(2) = 0.805913 via truncated Dirichlet (N=200).
The tail error is O(N^{-1}) ~ 5e-3, so this matches to ~3 digits, not 6.
