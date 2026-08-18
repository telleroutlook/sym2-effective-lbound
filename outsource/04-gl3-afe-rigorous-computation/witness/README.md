# Witness — GL_3 AFE computation

`grid_values.json` contains:

1. **Certificate**: module, status, method, N_terms, X, grid ranges,
   minimum certified |L(s)| over the grid, spot-check L(2).
2. **Grid**: list of {sigma, t, L_re, L_im, L_mod, method} for 70 points:
   - 5x9 = 45 points in critical strip [0.6, 1.0] x [-20, 20] (AFE method)
   - 5x5 = 25 points in Re(s) > 1 region [1.01, 2.0] x [0, 20] (Dirichlet)

**Key finding:** min |L(s)| = 0.404207 at (sigma=0.6, t=0), suggesting
L(s) != 0 in the critical strip. This is discovery-tier (mpmath floats);
proof-tier requires Arb outward rounding to certify 0 not in [L_lo, L_hi].

**Spot-check:** L(2) = 0.805913 via truncated Dirichlet (N=200), matching
the known value to 6 digits.
