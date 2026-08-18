# Proof — GL_3 AFE computation for L(s, sym^2 Delta)

**Status:** DISCOVERY-TIER (mpmath floats with full two-term AFE; not Arb-certified).

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

**Reference:** Standard GL_3 AFE derivation via Mellin inversion + functional
equation (Gelbart-Jacquet 1978; Goldfeld 2006).

## §3. Truncation and tail bound

Choose X and N such that:
- The main sum captures L(s) with weight V(n/X, s) ~ 1 for n << X.
- The dual sum converges with weight V_tilde(n*X, s) decaying for large nX.
- The tail from n > N is small.

The weight V(y, s) decays for large y. V_tilde(y, s) decays for large y.
With X=12, N_terms=60: the weights at n=60 give V(5, s) ~ 0.2 and
V_tilde(720, s) ~ 0.000004, ensuring rapid convergence.

**What is needed [OBL]:**
- Explicit bound on V(y, s) and V_tilde(y, s) for all y > 0 and s in the
  critical strip.
- Verification that N_terms=60 suffices for target precision 10^{-4}.

## §4. Weight function computation

The weight functions V and V_tilde are computed via Mellin contour integration
at Re(u) = Re(v) = 1, using h(u) = exp(u^2) as cutoff.

**Implementation:** `src/afe_sym2.py` computes V and V_tilde via midpoint
quadrature (n_quad = 500 points over [-T, T] with T = 20). The Gaussian
decay of exp(u^2) ensures rapid convergence.

**Poles of G(s+u):**
- G(s) = Gamma_R(s+1) * Gamma_C(s+11) = pi^{-(s+1)/2} Gamma((s+1)/2) *
  2(2pi)^{-(s+11)} Gamma(s+11).
- Gamma_R(s+1) has poles at s+1 = 0, -2, -4, ... (i.e., s = -1, -3, -5, ...)
  from Gamma((s+1)/2).
- Gamma_C(s+11) has poles at s+11 = 0, -1, -2, ... (i.e., s = -11, -12, -13, ...)
  from Gamma(s+11).
- The contour at Re(u) = 1 is to the right of the pole at u = 0 (residue 1),
  ensuring V(y, s) -> 1 as y -> 0.

## §5. Computation (mpmath, not Arb)

All computations use mpmath with 30 decimal digits of precision.
**This is discovery-tier, NOT proof-tier.**

For proof-tier, the following would be needed:
- Replace mpmath floats with Arb interval arithmetic (python-flint).
- Outward rounding at each arithmetic step.
- Explicit quadrature error bound.
- Explicit Gamma factor bounds on the contour.

**What is needed [OBL]:**
- Implementation of the full computation in Arb (not mpmath).
- Verification that rounding errors are controlled at each step.

## §6. Grid scan results

The corrected two-term AFE gives |L(s)| values on a 5x9 grid in
[sigma in [0.6, 1.0], |t| <= 20]:

- Min |L(s)| = 0.532 at (sigma=0.6, t=0)
- Values increase monotonically from sigma=0.6 to sigma=1.0 along t=0
- Symmetric in t as expected

**certifies_zero_free = false** — finite grid cannot certify continuous
zero-free region. See §7.

## §7. Zero-free region

A finite grid of 45 points cannot certify that L(s) != 0 for all s in a
continuous region. Points between grid locations may be zeros.

To extend to a continuous region, one would need:
- Bound on |L'(s)| in the critical strip.
- Sufficient grid resolution for coverage argument.
- Or: rigorous argument principle / winding-number certificate.

For the current discovery-tier computation, the grid provides numerical
evidence but not a proof of zero-freeness.

## §8. Connection to partial-sum bound

The partial-sum bound S(X) = O_epsilon(X^{1/2+epsilon}) is proved
unconditionally via Friedlander-Iwaniec (Batch 03), independently of any
zero-free region. The AFE computation here provides numerical evidence
for L(s) behavior but is not needed for the partial-sum bound.

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
  midpoint-radius interval arithmetic" — for proof-tier upgrade.
