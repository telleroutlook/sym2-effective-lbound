# Checker — GL_3 AFE computation (v3)

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
- The missing G factor in C_V computation.
- The X-direction error in AFE tail bound.
- Whether coefficients use exact rational or float.

**STRUCTURAL/CROSS-CHECKER ONLY — not a theorem certificate.**

## v3 corrections

- Updated to note checker uses mpmath, not Arb
- Added known bugs to "does NOT verify" list
- Status: DISCOVERY-TIER cross-check, not rigorous verification
