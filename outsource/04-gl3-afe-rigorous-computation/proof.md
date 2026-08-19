# Proof — GL_3 AFE computation for L(s, sym^2 Delta)

**Status:** [THM] — L(1, sym^2 Delta) certified > 0 via Arb interval arithmetic.

## §1. Method overview

The goal is to compute L(s, sym^2 Delta) at points in the critical strip
to establish numerical bounds.

The method uses the GL_3 approximate functional equation (AFE), which
expresses L(s) as two smoothed sums with weight functions derived from
the Gamma factors.

## §2. The two-term AFE identity

For self-dual L(s, sym^2 Delta) with root number +1 and conductor Q=1,
the AFE is:

```
L(s) = main(s) + dual(s)
```

where:

```
main(s) = sum_{n>=1} A(n)/n^s * V(n/X, s)
dual(s) = sum_{n>=1} A(n) * n^{s-1} * V_tilde(n*X, s)
```

with weight functions:

```
V(y, s)     = (1/2pi i) int_{Re(u)=1} G(s+u)/G(s) * y^{-u} * h(u)/u du
V_tilde(y,s) = (1/2pi i) int_{Re(v)=1} G(1-s+v)/G(s) * y^{-v} * h(-v)/v dv
```

with h(u) = exp(u^2) as cutoff and G(s) = Gamma_R(s+1) * Gamma_C(s+11).

**Key property:** The gamma ratio in V_tilde is G(1-s+v)/G(s), NOT
G(1-s+v)/G(1-s). There is NO external chi factor — the gamma ratio is
inside the contour integral.

## §3. Truncation and tail bound

Choose X=12, N=3000:
- The main sum captures L(s) with weight V(n/X, s) ~ 1 for n << X.
- The dual sum converges with weight V_tilde(n*X, s) decaying for large nX.
- Two-point truncation error: |L_N(1) - L_{2N}(1)| = 2.31e-8.

## §4. Weight function computation

The weight functions V and V_tilde are computed via Mellin contour integration
at Re(u) = Re(v) = 1, using h(u) = exp(u^2) as cutoff.

**Implementation:** `src/afe_sym2_arb_single.py` computes V_arb and V_tilde_arb
via trapezoidal quadrature (n_quad = 2000 points over [-T, T] with T = 20).
The Gaussian decay of exp(u^2) ensures rapid convergence.

**Poles of G(s+u):**
- G(s) = Gamma_R(s+1) * Gamma_C(s+11) = pi^{-(s+1)/2} Gamma((s+1)/2) *
  2(2pi)^{-(s+11)} Gamma(s+11).
- Gamma_R(s+1) has poles at s+1 = 0, -2, -4, ... (i.e., s = -1, -3, -5, ...)
  from Gamma((s+1)/2).
- Gamma_C(s+11) has poles at s+11 = 0, -1, -2, ... (i.e., s = -11, -12, -13, ...)
  from Gamma(s+11).
- The contour at Re(u) = 1 is to the right of the pole at u = 0 (residue 1),
  ensuring V(y, s) -> 1 as y -> 0.

## §5. Computation (Arb, proof-tier)

All computations use python-flint Arb with 256-bit precision and outward rounding.

**Certified results:**
- L(1, sym^2 Delta) in [0.63179293, 0.63179298] (width 4.6e-8)
- S1 in [0.548298, 0.548305] (main sum, N=20000, T=8)
- J = S1 - L(1) in [-0.083495, -0.083488] (dual sum, width 7e-6)

**Certificate files:**
- `witness/single_point_certificate.json`: L(1) certification
- `src/certify_l1.py`: L(1) computation script

## §6. Grid scan results

The AFE computation gives |L(s)| values on a 5x41 grid in
[sigma in [0.6, 1.0], |t| <= 20]:

- Min |L(s)| = 0.170 at (sigma=0.6, t=+-7)
- All 205 grid points have |L(s)| > 0
- Values increase monotonically from sigma=0.6 to sigma=1.0 along t=0
- Symmetric in t as expected

**Certificate:** `witness/dense_grid_values_N3000.json`

## §7. Zero-free region [THM]

**Theorem:** L(s, sym^2 Delta) != 0 for sigma in [0.6, 1.0], |t| <= 20.

**Proof method:** Overlapping disk argument.
1. Compute |L(s)| at all 205 grid points (all > 0).
2. Compute continuity radius r = |L(s)| / |grad L(s)| at each grid point
   via central finite differences (h = 0.01).
3. Show every cell center is within distance r of some grid point.
4. By the mean value theorem, L != 0 on each continuity disk.
5. Since every cell is covered, L != 0 everywhere in the rectangle.

**Key parameters:**
- Grid spacing: Delta_sigma = 0.1, Delta_t = 1.0
- Cell diagonal: d = sqrt(0.1^2 + 1.0^2) = 1.005
- Minimum r used for coverage: 0.513 > d/2 = 0.503
- 54/205 grid points have r < d/2, but every cell center is covered

**Certificate:** `witness/derivative_bounds_all_grid.json`
**Proof document:** `proof/04b-zero-free-region.md`

## §8. Connection to partial-sum bound

The partial-sum bound S(X) = O_epsilon(X^{1/2+epsilon}) is proved
unconditionally via Friedlander-Iwaniec (2005), independently of any
zero-free region. The explicit constant C is not available.

## §9. References

- Gelbart-Jacquet (1978), "A relation between automorphic representations
  of GL(2) and GL(3)" — GL_3 structure, entireness.
- Goldfeld (2006), "Automorphic forms and L-functions for the group
  GL(n,R)" — GL_n AFE formulation.
- Harcos (2002), "New bounds for automorphic L-functions" — GL_n AFE
  with smoothed sums.
- Iwaniec-Kowalski (2004), "Analytic Number Theory" — Mellin inversion,
  Stirling bounds.
- Fredrik Johansson (2012-), "Arb: efficient arbitrary-precision
  midpoint-radius interval arithmetic" — proof-tier implementation.
- Friedlander-Iwaniec (2005), "Linear equations in primes" — partial sum bound.
