# Checker — GL_3 AFE computation

`check_grid.py` independently recomputes L(s) at every grid point from
scratch (no imports from `src/`). It uses:

1. Its own tau sieve (same algorithm, independent implementation).
2. Its own sym^2 coefficient computation.
3. Its own Gamma factor and AFE weight function.
4. Truncated Dirichlet series for Re(s) > 1 (spot-check).
5. AFE smoothed sum for critical strip points.

**Current result:** All 70 grid points pass with relative error < 10^{-8}.

**What the checker does NOT verify:**
- The quadrature error in the AFE weight integral (analytic bound needed).
- The truncation error from N=60 terms in the AFE sum.
- The "grid ⇒ continuous region" extension (continuity argument needed).
- Arb interval arithmetic (mpmath floats only; not proof-tier).
