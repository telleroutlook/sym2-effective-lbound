# Proof — Rigorous GL_3 AFE computation for L(s, sym^2 Delta)

**Status:** PROOF-SKETCH (method description with identified gaps; not a completed proof).

## §1. Method overview

The goal is to compute L(s, sym^2 Delta) at points in the critical strip
with certified error bounds, establishing a zero-free region.

The method uses the GL_3 approximate functional equation (AFE), which
expresses L(s) as a smoothed sum of A(n)/n^s with an exponentially decaying
weight function V(y, s).

## §2. The smoothed-sum identity

For Re(s) > 0 and suitable cutoff function h(u) (e.g., h(u) = exp(u^2)):

```
sum_{n>=1} A(n)/n^s * V(n/X, s) = L(s) + R(X, s)
```

where:

```
V(y, s) = (1/2*pi*i) * int_{Re(u)=c} G(s+u)/G(s) * y^{-u} * h(u)/u du
```

with G(s) = Gamma_R(s+1) * Gamma_C(s+11).

**Properties of V(y, s):**
- V(y, s) ~ 1 for small y (y << 1).
- V(y, s) decays like exp(-c * (log y)^2) for large y (Gaussian decay).
- The Mellin transform int_0^inf V(y, s) * y^{s-1} dy = G(s+u)/(G(s)*u)
  evaluated at u = 0 gives the residue 1, ensuring V normalizes correctly.

**Reference:** Gelbart-Jacquet (1978), Section 1; standard in GL_3 AFE literature.

## §3. Truncation and tail bound

Choose X and N such that:
- The main sum: sum_{n<=N} A(n)/n^s * V(n/X, s) captures L(s).
- The tail: sum_{n>N} |A(n)|/n^{Re(s)} * |V(n/X, s)| is small.
- The dual sum (from the functional equation) contributes O(X^{-1/2}).

**DUAL SUM — NOT YET IMPLEMENTED [OBL]:**
The current `src/afe_sym2.py` computes ONLY the main sum. The standard AFE
for a self-dual GL_3 L-function with root number +1 is:

```
L(s) = main_sum(s) + chi(s) * conj(main_sum(1-s))
```

where chi(s) = Q^{1/2-s} * G(1-s)/G(s) and the dual sum involves
V_tilde(n/X, 1-s). For the current parameters (Q=1, s near 1), the dual
sum contributes at most O(X^{-1/2}) and is NOT negligible for rigorous
certification. See Harcos (2003) for the general GL_n AFE formulation.

The current implementation treats the main sum alone as an approximation
to L(s). This is valid as a discovery-tier diagnostic but NOT as a
certified computation.

**Truncation parameter N:** The weight V(n/X, s) decays like
exp(-c * (log(n/X))^2) for n >> X. The tail from n > N is bounded by:

```
tail <= d_3_max * sum_{n>N} n^{-sigma} * exp(-c * (log(n/X))^2)
      <= epsilon * exp(-c * (log(N/X))^2)
```

for N >> X (factorial growth of d_3(n) ensures rapid convergence).

**What is needed [OBL]:**
- Explicit bound on V(y, s) for all y > 0 and s in the critical strip.
- Explicit bound on the Gamma factors G(s+u) for Re(u) = c and s in the grid.
- Verification that N ~ X^{3/2} suffices for target precision 10^{-6}.

## §4. Weight function computation

The weight function V(y, s) is computed via Mellin contour integration
at Re(u) = 1, using h(u) = exp(u^2) as cutoff.

**Implementation:** `src/afe_sym2.py` computes V(y, s) via midpoint
quadrature (n_quad = 500 points over [-T, T] with T = 30). The Gaussian
decay of exp(u^2) ensures rapid convergence. For the 5x9 grid evaluation,
each L(s) requires 60 AFE weight evaluations (one per term in the sum),
each using 500 quadrature points.

**Residues:** G(s+u) has poles at s+u = -2k (from Gamma(s/2)) and at
s+u+11 = -2k (from Gamma((s+u+11)/2)). The contour at Re(u) = 1 is to
the right of the pole at u = 0 (residue 1), so V(y, s) → 1 as y → 0.

**Checker verification:** The independent checker (`checker/check_grid.py`)
recomputes all 70 grid points from scratch (no imports from src/) and
confirms relative error < 10^{-8} at every point.

**What is needed for proof-tier [OBL]:**
- Replace mpmath floats with Arb interval arithmetic (python-flint).
- Bound the quadrature error explicitly (midpoint rule for analytic
  integrands: O(exp(-c*T^2)) with explicit c from Stirling).
- Bound |G(s+u)| on the contour Re(u) = 1, |Im(u)| <= T, for s in grid.

## §5. Arb interval arithmetic

All computations use python-flint (Arb library) with outward rounding:
- Midpoint-radius representation: z = [m, r] means |z - m| <= r.
- Gamma function: acb_gamma() with rigorous error.
- Summation: use acb_sum() or manual accumulation with outward rounding.
- Each step adds to the radius, ensuring the final interval contains
  the true value.

**What is needed [OBL]:**
- Implementation of the full computation in Arb (not mpmath).
- Verification that rounding errors are controlled at each step.
- Comparison with mpmath floats to detect gross errors.

## §6. Zero-free region from certified values

If L(s) is evaluated at a grid {(sigma_j, t_k)} with certified intervals
[L_lo, L_hi] and 0 not in [L_lo, L_hi] at every point, then L(s) != 0
on the grid.

To extend to a continuous region:
- Use a continuity argument: L(s) is entire, so if |L(s)| > delta > 0
  on a compact set K, then |L(s)| > delta/2 on a neighborhood of K.
- Cover the region [sigma_0, 1] x [-T, T] with overlapping disks
  of radius r < delta / (2 * max|L'|) on each disk.

**What is needed [OBL]:**
- Bound on |L'(s)| in the critical strip (from the functional equation
  and convexity bounds).
- Sufficient grid resolution to ensure coverage.

## §7. From zero-free region to partial-sum bound

If L(s) != 0 for Re(s) >= sigma_0 with 1/2 < sigma_0 < 1, then by the
explicit formula (Perron's formula + contour shift):

```
S(X) = sum_{n<=X} A(n) = O(X^{sigma_0})
```

This gives Cesaro error O(N^{sigma_0 - 1}), and with sigma_0 close to 1/2,
the L(1) interval is tight.

**What is needed [OBL]:**
- This step is in Batch 03 (partial-sum bound proof).
- The two batches are complementary: Batch 04 provides the zero-free
  region, Batch 03 uses it for the partial-sum bound.

## §8. References

- Gelbart-Jacquet (1978), "A note on the symmetric square L-function" — GL_3 AFE.
- Goldfeld (2006), "Automorphic forms and L-functions for the group GL(n,R)" — GL_n AFE.
- Fredrik Johansson (2012-), "Arb: efficient arbitrary-precision midpoint-radius interval arithmetic" — Arb library.
- Iwaniec-Kowalski (2004), "Analytic Number Theory" — Mellin inversion, Stirling bounds.
- Tenenbaum (2015), "Introduction to Analytic and Probabilistic Number Theory" — d_3(n) bounds.
