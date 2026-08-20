# Limitations — GL_3 AFE computation (v3)

## Critical gaps (reviewer FAIL verdict, 2026-08-20)

### 1. Exact coefficient chain broken [OBL]

Code uses c_p = tau(p)/p^5.5 as Python float, then acb(float(an)).
This does NOT prove A_exact(n) in A_Arb(n). Must use exact rational
c_p^2 = tau(p)^2/p^11 throughout.

### 2. Mellin quadrature error not bounded [OBL]

Trapezoidal quadrature at Re(u)=1 over [-T,T] has error E_quad that
is NOT rigorously bounded. The certificate "L_radius = 8.1e-74"
reflects Arb rounding of the finite sum, NOT the total integration error.

### 3. Contour tail not bounded [OBL]

Integral truncated at |t|=T. The error E_contour = |int_{|t|>T} ...|
is NOT bounded. No explicit T-dependent bound exists.

### 4. AFE tail (n>N) not bounded [OBL]

Main sum truncated at N. The "N vs 2N difference" used as error is NOT
a rigorous tail bound: |S_{2N}-S_N| does not bound |S_inf-S_N|.
No monotonicity or geometric decay has been proved.

### 5. Zero-free region not proved [OBL]

- Finite differences approximate L'(s) but do NOT give rigorous sup bounds
- Different N values (60 vs 3000) give inconsistent |L(s)| at same point
  (~20% relative difference at s=0.6+20i)
- Cell coverage: only 128/160 cells fully covered by single-disk argument
- Continuity radius r computed from approximate, not rigorous, derivative
- Stale data: min radius 0.099 vs 0.133 in different JSON files

### 6. J certificate blocked [OBL]

Depends on certified L(1) and S1, neither of which is rigorous.

### 7. Code bugs found in v3 review

- C_V computation (afe_sym2_arb_final.py) missing G(s+1+it)/G(s) factor
- AFE tail X-direction error: divides by X instead of multiplying
- Dual tail hardcoded as 1e-12 with no derivation

### 8. Self-containedness FAIL

Code references heartbeat.py, tail_bound.py,
baseline/s1_full_certificate.json — none provided in bundle.
checker/check_grid.py raises FileNotFoundError on missing grid_values.json.

### 9. Old witness files still say CERTIFIED

single_point_certificate.json, j_certificate.json,
zero_free_region_N3000.json all have status "CERTIFIED" despite
the underlying computation having the gaps above.
(Downgraded to DISCOVERY in v3.)

### 10. Unified error budget not formed

No combination of E_coeff + E_quad + E_contour + E_main_tail + E_dual_tail
exists. Therefore no interval [a,b] with a>0 for L(1) is proved.

## What IS correct

- AFE structure (two-term identity, gamma ratio, self-duality)
- Symmetric-square coefficient recurrence (Hecke, degree-3)
- Root number (+1) and Gamma factor G(s) = Gamma_R(s+1)*Gamma_C(s+11)
- Discovery-tier numerical values (L(1) ~ 0.6318, min |L(s)| ~ 0.170)
- Partial-sum bound S(X) = O_eps(X^{1/2+eps}) via FI2005 (separate batch)

## Scope

- Does NOT provide a certified L(1) value
- Does NOT provide a proved zero-free region
- Does NOT serve as a premise downstream
- Status: METHOD-DESCRIPTION + DISCOVERY only
