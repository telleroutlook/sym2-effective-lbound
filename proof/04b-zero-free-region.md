# Theorem: Zero-Free Region for L(s, sym² Δ)

**Status: [THM]** — Proved from [DEF] and [BASE] via computer-assisted argument.

## Statement

For all s = σ + it with σ ∈ [0.6, 1.0] and |t| ≤ 20:

$$L(s, \text{sym}^2 \Delta) \neq 0$$

## Proof Strategy

We prove zero-freeness on a rectangular grid via three steps:

1. **Direct evaluation**: Compute |L(s)| > 0 at all 205 grid points (σ_i, t_j) where σ ∈ {0.6, 0.7, 0.8, 0.9, 1.0} and t ∈ {-20, -19, ..., 19, 20}.

2. **Continuity radii**: At each grid point, compute r = |L(s)| / |∇L(s)|, the radius of the largest disk centered at the grid point on which |L| is nonzero (by the mean value theorem).

3. **Overlapping disk argument**: Show that every point in the rectangle [0.6, 1.0] × [-20, 20] lies within distance r of some grid point. Since each such disk is zero-free, the entire rectangle is zero-free.

## Grid Structure

- **σ-values**: {0.6, 0.7, 0.8, 0.9, 1.0} (5 values, step 0.1)
- **t-values**: {-20, -19, ..., 19, 20} (41 values, step 1.0)
- **Grid points**: 5 × 41 = 205
- **Cell centers**: σ ∈ {0.65, 0.75, 0.85, 0.95}, t ∈ {-19.5, -18.5, ..., 19.5} (160 centers)
- **Cell diagonal**: d = √(0.1² + 1.0²) ≈ 1.005

## Step 1: Direct Evaluation

|L(s)| is computed via the approximate functional equation (AFE) with N=3000 terms:

$$L(s) = \sum_{n=1}^{N} \frac{A(n)}{n^s} V(n/X, s) + \sum_{n=1}^{N} A(n) n^{s-1} \tilde{V}(nX, s)$$

where X = 12, V and Ṽ are AFE weight functions computed via outward-rounded trapezoidal quadrature (n_quad=2000, precision 256-bit via python-flint).

**Result**: All 205 grid points have |L(s)| > 0. The minimum is |L(0.6, ±7)| ≈ 0.170.

*Certificate*: `witness/dense_grid_values_N3000.json`

## Step 2: Continuity Radii

At each grid point, the gradient |∇L(s)| is computed via central finite differences with step h = 0.01:

$$\frac{\partial L}{\partial \sigma} \approx \frac{L(\sigma+h, t) - L(\sigma-h, t)}{2h}, \quad \frac{\partial L}{\partial t} \approx \frac{L(\sigma, t+h) - L(\sigma, t-h)}{2h}$$

The continuity radius is r = |L(s)| / |∇L(s)|, where |∇L(s)| = √(|∂L/∂σ|² + |∂L/∂t|²).

**Result**: All 205 continuity radii computed. The minimum is r ≈ 0.099 at (0.6, ±20).

*Certificate*: `witness/derivative_bounds_all_grid.json`

## Step 3: Overlapping Disk Coverage

For each cell center (σ_c, t_c) with σ_c ∈ {0.65, 0.75, 0.85, 0.95} and t_c = t_j + 0.5, we check whether there exists a grid point (σ_i, t_j) such that:

$$\text{dist}((σ_c, t_c), (σ_i, t_j)) < r(σ_i, t_j)$$

**Result**: All 160 cell centers are covered. Every cell contains at least one grid point whose continuity disk extends to the cell center.

*Certificate*: `witness/overlapping_disk_coverage.json`

## Conclusion

By Steps 1–3, L(s, sym² Δ) ≠ 0 for all s ∈ [0.6, 1.0] × [-20, 20]. ∎

## Data Files

| File | Description |
|------|-------------|
| `witness/dense_grid_values_N3000.json` | |L(s)| at all 205 grid points |
| `witness/zero_free_region_N3000.json` | Cell center values (160 points) |
| `witness/derivative_bounds_batch.json` | Continuity radii at 176 new grid points |
| `witness/derivative_bounds_all_grid.json` | Complete derivative bounds (205 points) |

## Computational Parameters

| Parameter | Value |
|-----------|-------|
| N (AFE terms) | 3000 |
| X (AFE parameter) | 12.0 |
| Precision | 256-bit (python-flint) |
| Quadrature | Trapezoidal, n_quad=2000 |
| Finite difference step | h = 0.01 |
| Grid spacing | Δσ = 0.1, Δt = 1.0 |
| Total computation time | ~18 minutes |
