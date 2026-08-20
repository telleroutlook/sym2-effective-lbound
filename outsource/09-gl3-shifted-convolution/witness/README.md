# Witness: GL₃ Shifted Convolution

This package is a **research gap documentation** (09-A) and **technical
verification task** (09-B'), not a theorem. No numerical witness is
applicable.

## Why no witness?

- 09-A (individual shifted convolution): No proof exists, so no witness.
- 09-B' (smooth-weight transfer): This is a technical verification that
  Wang 2026's box-cutoff estimate can be promoted to smooth weight. It
  requires a mathematical argument, not a numerical computation.

## What could be done (discovery-tier only)

A numerical exploration could:
1. Compute Σ_{h≤H} Σ_{N<n≤2N} λ_{sym²f}(n) λ_{sym²f}(n+h) for small N, H
2. Compare with expected main term from Rankin–Selberg (h=0 case)
3. Verify that the averaged bound is non-trivial at H = N^{1/3}

This would NOT be a proof but could provide evidence. Such computation
is OUTSIDE the scope of this package.
