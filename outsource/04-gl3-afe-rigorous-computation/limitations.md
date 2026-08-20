# Limitations — GL_3 AFE computation

## Critical gaps (reviewer BLOCKED verdict, 2026-08-20)

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
- Cell coverage by disks does not follow from center coverage alone
- Continuity radius r computed from approximate, not rigorous, derivative

### 6. J certificate blocked [OBL]

Depends on certified L(1) and S1, neither of which is rigorous.

### 7. MANIFEST.sha256 failures

Multiple file hashes mismatch. Missing files referenced (grid_values.json,
grid_values_arb.json, proof/04b-zero-free-region.md).

### 8. Local paths in certificates

unified_certificate.json contains /Users/I041705/github/... paths.

### 9. Missing dependencies

Code references heartbeat.py, tail_bound.py,
baseline/s1_full_certificate.json — none provided in bundle.

## What IS correct

- AFE structure (two-term identity, gamma ratio, self-duality)
- Symmetric-square coefficient recurrence (Hecke, degree-3)
- Root number (+1) and Gamma factor G(s)
- Discovery-tier numerical values (L(1) ~ 0.6318, min |L(s)| ~ 0.170)
- Partial-sum bound S(X) = O_eps(X^{1/2+eps}) via FI2005 (separate batch)

## Scope

- Does NOT provide a certified L(1) value
- Does NOT provide a proved zero-free region
- Does NOT serve as a premise downstream
- Status: METHOD-DESCRIPTION + DISCOVERY only
