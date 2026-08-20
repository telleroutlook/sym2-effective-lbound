# GL₃ Shifted Convolution — Novelty

## What is new in this package

This package is **not a theorem** but a **research gap documentation**.
Its novelty is in:

1. **Precise formulation**: Identifying the exact analytic estimate needed
   for the GL₃ shifted convolution at the critical shift scale for fixed
   symmetric-square Π.

2. **Dependency mapping**: Showing that this single estimate blocks both
   M-1 (mollifier) and M-2 (mean value), making it the fundamental
   analytic obstruction.

3. **Literature synthesis**: Combining DLY 2024, Pal 2025, and the
   GL₃ spectral theory to explain why the estimate is not yet known.

4. **Approach analysis**: Identifying the four possible approaches
   (GL₃ Kuznetsov, spectral, hybrid, moment) and their obstacles.

## What is NOT new

- The GL₃ Kuznetsov/Voronoi formula is classical (Iwaniec, Goldfeld)
- The AFE for L(½+it, Π) is known (Goldfeld, Hoffstein–Luo–Sarnak)
- The upper bounds of DLY and Pal are in the literature
- The difficulty of GL₃ Kloosterman sums is well-known

## Relationship to existing packages

| Package | Relationship |
|---------|-------------|
| 03-partial-sum-bound | Provides AFE input; uses GL₂ shifted convolution |
| 04-gl3-afe | Provides the GL₃ AFE structure; same obstruction |
| 05-F-2-global-residue | Provides main term C_Π(h); algebraic |
| 06-M-1-mollifier | Blocked by this estimate |
| 07-M-2-mean-value | Blocked by this estimate |
| 08-c_eff | Blocked by M-1/M-2, hence by this estimate |

## Status: [OBL]

No new theorem is claimed. This is a research gap documentation.
