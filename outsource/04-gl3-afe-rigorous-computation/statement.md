# Statement — Rigorous GL_3 AFE computation

**Theorem ID:** gl3-afe-rigorous-sym2-delta
**Mathematical status:** METHOD-DESCRIPTION (not a theorem; a computational method)
**Computational status:** DISCOVERY (mpmath floats, not Arb intervals)
**Program ref:** sym2-effective-lbound Q-11
**Paper target:** Paper A (effective L(1) bound)

---

## Goal

Implement a rigorous computation of L(s, sym^2 Delta) at points in the
critical strip using the GL_3 approximate functional equation, with
certified error bounds using Arb interval arithmetic.

## Input

- The symmetric-square coefficients A(n) for n = 1..N (computed from
  the Ramanujan tau function via the Euler sieve).
- The gamma factor G(s) = Gamma_R(s+1) * Gamma_C(s+11).
- A grid of points {(sigma_j, t_k)} in [0.5, 1.0] x [-T_max, T_max].

## Output

For each grid point (sigma, t):
1. A complex ball enclosure L(sigma+it) in [x0 +/- rx] + i[y0 +/- ry] (an Arb
   acb) — a real ordered interval is meaningless for complex values at
   t != 0. [corrected per 2026-08-19 review]
2. A certification that 0 notin B_s, equivalently a rigorous lower bound
   |L(sigma+it)| >= delta_s > 0.

## Method

1. **Smoothed-sum identity**: For Re(s) > 0,
   L(s) = sum_{n<=N} A(n)/n^s * V(n/X, s) + dual_sum + tail,
   where V is the weight function from Mellin inversion.

2. **Weight function**: V(y, s) = (1/2pi i) int G(s+u)/G(s) * y^{-u} * h(u)/u du.
   Computed via contour shift to Re(u) = -m (m = 2 or 3), picking up
   residues from Gamma poles.

3. **Truncation** [corrected per 2026-08-19 review]: with y = n/X and a
   proved bound V(y) <= exp(-c*y^{2/3}), solving exp(-c*(N/X)^{2/3}) < eps
   gives N >= X*(log(1/eps)/c)^{3/2} — the earlier N ~ X^{3/2} scale did not
   follow from the weight bound and is retracted; N must come from a proved
   uniform weight bound with an error budget.
   For target 10^{-6}: N ~ 100, X ~ 20 suffices.

4. **Tail bound**: |tail| <= A_m * sum_{n>N} d_3(n)/n^sigma * |V(n/X, s)|,
   bounded by the exponential decay of V and the Abel sum bound on d_3.

5. **Arb arithmetic**: All computations in outward-rounded interval
   arithmetic to guarantee containment.
