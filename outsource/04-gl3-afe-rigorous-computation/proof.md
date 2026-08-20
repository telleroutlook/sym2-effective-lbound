# Proof — GL_3 AFE computation for L(s, sym^2 Delta)

**Status:** METHOD-DESCRIPTION + DISCOVERY (not a theorem; all rigorous layers are [OBL]).

## §1. Method overview

The goal is to compute L(s, sym^2 Delta) at points in the critical strip
using the GL_3 approximate functional equation (AFE), as a stepping stone
toward rigorous certified evaluation.

**Current status:** The AFE structure is correct. The numerical values are
discovery-tier. The rigorous error closure (quadrature error, contour tail,
AFE tail, exact coefficients) is NOT yet closed. No THM or CERTIFIED labels
apply to any result in this batch.

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

**Self-duality:** Since sym^2 Delta is self-dual with root number +1,
the dual Dirichlet series B(s) = A(s), so b(n) = A(n). [BASE, standard]

## §3. Hypotheses verification

**Degree m = 3:** L(s, sym^2 Delta) is a degree-3 L-function
(automorphic representation on GL_3). [THM, GJ78]

**Conductor D = 1:** Level 1, no ramified primes. [THM]

**Archimedean parameters:** kappa = (1, 11, 12) from
Gamma_R(s+1) * Gamma_C(s+11). [THM, Iwaniec-Michel]

**Coefficient bound:** |A(n)| <= d_3(n) << n^epsilon. [THM, Deligne]

**Entireness:** L(s, sym^2 Delta) is entire (root number +1). [THM, IM]

## §4. [OBL] Rigorous error layers — NOT YET CLOSED

The following error layers must ALL be closed before any certified
statement can be made:

### 4a. Exact coefficients [OBL]

Current code uses float c_p = tau(p)/p^5.5, then acb(float(an)).
This does NOT prove A_exact(n) in A_Arb(n).

**Required:** Use exact rational c_p^2 = tau(p)^2/p^11 throughout the
prime-power recurrence, producing rigorous Arb enclosures for each A(n).

### 4b. Mellin quadrature error [OBL]

The weight function V(y,s) is computed by trapezoidal quadrature at
Re(u)=1 over [-T,T]. The error E_quad = |integral - Q_h| is NOT bounded.

**Required:** Prove E_quad <= explicit bound using:
- h''(u) bound on the integrand
- Euler-Maclaurin or Poisson summation remainder
- Super-exponential decay of exp(u^2) ensuring rapid convergence

### 4c. Contour tail [OBL]

The integral is truncated at |t|=T. The error
E_contour = |int_{|t|>T} ... dt| is NOT bounded.

**Required:** Prove exponential decay of integrand for large |t| using
Stirling bounds on Gamma factors, giving explicit T-dependent bound.

### 4d. AFE tail (n>N) [OBL]

The main sum is truncated at N. The tail
E_tail = sum_{n>N} |A(n)|/n^sigma * |V(n/X,s)| is NOT bounded.

**Required:** Use |A(n)| <= d_3(n) and proved decay of V(y,s) to get
explicit N-dependent bound. The "N vs 2N difference" currently used
is NOT a rigorous tail bound (|S_{2N}-S_N| does not bound |S_inf-S_N|).

### 4e. Dual sum tail [OBL]

Similarly, the dual sum truncation error is NOT bounded.

### 4f. Unified error budget [OBL]

All five layers must be combined:

```
L(1) in B_arithmetic + B_quadrature + B_contour + B_AFE_tail + B_dual_tail
```

where each B is a certified interval. This does NOT exist yet.

## §5. Code-level bugs found in review (v3)

### 5a. C_V computation missing G factor [BUG]

`afe_sym2_arb_final.py::compute_C_V_rigorous()` computes:

```python
f = exp(1-t*t) / sqrt(1+t*t)
```

but the actual integrand for the AFE tail bound should include
|G(s+1+it)/G(s)|. The function name claims to bound this integral
but the Gamma-ratio factor is entirely absent.

### 5b. AFE tail X-direction error [BUG]

From the contour at Re(u)=1:

```
|V(n/X, s)| <= C(s) * (X/n)^1
```

since |(n/X)^{-1-it}| = X/n. But the code writes:

```python
main_tail = C_V / X * exact_part
```

which divides by X instead of multiplying. The correct majorant should
have X in the numerator for the main tail.

### 5c. Dual tail hardcoded [BUG]

```python
dual_tail = 1e-12
```

This is a magic constant with no derivation. The dual tail must be
bounded using the same style of integral majorant as the main tail.

## §6. Discovery-tier numerical results

The following are numerical observations, NOT certified results:

- L(1, sym^2 Delta) ~ 0.63179295 (mpmath 30-digit floats)
- S1 ~ 0.5483 (main sum, N=20000, T=8)
- J = S1 - L(1) ~ -0.0835
- Min |L(s)| ~ 0.170 on 5x41 grid in [0.6,1] x [-20,20]
- All 205 grid points have |L(s)| > 0 (numerical observation)

**None of these are certified.** The certificates in witness/ are
generated from code that has the gaps described in §4 and §5.

## §7. Zero-free region — NOT PROVED

The claim "L(s) != 0 for sigma in [0.6,1], |t| <= 20" is NOT proved.

**Why the current argument fails:**

1. Finite differences (L(s+h)-L(s-h))/(2h) approximate L'(s) but do NOT
   give a rigorous supremum bound on the derivative over each cell.

2. The continuity radius r = |L(s)|/|L'(s)| is computed from this
   approximation, not from a rigorous derivative bound.

3. Different N values (N=60 for derivative scan, N=3000 for grid) produce
   different |L(s)| values at the same point — the approximations are
   not mutually consistent (~20% relative difference at s=0.6+20i).

4. "Every cell center is covered by some disk" does not imply "every
   point in the cell is covered" — only 128/160 cells are fully covered
   by single-disk argument.

5. Minimum radius in derivative_bounds_all_grid.json (~0.099 at
   (0.6,-20)) differs from zero_free_region_N3000.json (0.133 at
   (0.6,-7)), indicating stale data.

**The 205-point nonzero observation is discovery-tier only.**

## §8. Connection to partial-sum bound

The partial-sum bound S(X) = O_epsilon(X^{1/2+epsilon}) is proved
unconditionally via Friedlander-Iwaniec (2005), independently of any
zero-free region. [THM, FI2005 — see batch 03]

## §9. What is NOT available

1. **Certified L(1) interval:** Error closure not closed (§4).
2. **Proved zero-free region:** Derivative bounds not rigorous (§7).
3. **Certified J value:** Depends on certified L(1) and S1.
4. **Explicit C(epsilon) for partial sums:** Not from this batch.
5. **Self-contained reproducibility:** Missing dependencies
   (heartbeat.py, tail_bound.py, baseline/s1_full_certificate.json).

## §10. References

- Gelbart-Jacquet (1978), GL_3 structure, entireness.
- Goldfeld (2006), GL_n AFE formulation.
- Harcos (2002), GL_n AFE with smoothed sums.
- Iwaniec-Kowalski (2004), Mellin inversion, Stirling bounds.
- Johansson (2012-), Arb interval arithmetic library.
- Friedlander-Iwaniec (2005), "Summation Formulae for Coefficients of
  L-functions", Canad. J. Math. 57, 494-505 — partial sum bound.
