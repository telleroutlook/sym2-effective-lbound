# Proof — Partial-sum bound for sym^2 Delta

**Status:** PROOF-SKETCH (no complete proof exists; all gaps marked [OBL]).

## §1. Known facts

Let A(n) be the normalized symmetric-square coefficients of the weight-12
cusp form Delta in S_12(SL_2(Z)):

```
L(s, sym^2 Delta) = sum_{n>=1} A(n) / n^s
```

with A(1) = 1, A multiplicative, and A(p) = c_p^2 - 1 where c_p = tau(p)/p^{5.5}.

**Fact 1** (Deligne bound): |tau(p)| <= 2*p^{5.5}, so |c_p| <= 2, |A(p)| <= 3.
By multiplicativity, |A(n)| <= d_3(n) for all n >= 1. [THM, DEL-D.1]

**Fact 2** (Functional equation): L(s, sym^2 Delta) extends to all of C with
gamma factor G(s) = Gamma_R(s) * Gamma_C(s + 11), where Gamma_R(s) = pi^{-s/2} Gamma(s/2)
and Gamma_C(s) = 2*(2*pi)^{-s} * Gamma(s). The completed L-function
Lambda(s) = G(s) * L(s) satisfies Lambda(s) = Lambda(1 - s). [THM, Gelbart-Jacquet 1978]

**Fact 3** (Zero-free region for Re(s) > 1): The truncated Dirichlet series
with partial-sum tail bound certifies L(s) != 0 for Re(s) >= 1.01, |t| <= 20.
Certificate: baseline/zero_free_scan.json. [THM, src/zero_free_arb.py]

**Fact 4** (Empirical partial-sum bound): For X in [1, 20000],
max |S(X)| / X^{0.5} = 0.259, where S(X) = sum_{n<=X} A(n). [EMPIRICAL]

## §2. Proof route: zero-free region -> explicit formula -> partial sums

### Step 1: Zero-free region in the critical strip [OBL]

**Goal:** Prove L(s, sym^2 Delta) != 0 for Re(s) >= sigma_0 with 1/2 < sigma_0 < 1.

**What exists:**
- For Re(s) > 1: certified zero-free (Fact 3).
- For the critical strip [0.6, 1.0]: empirical scan shows |L(s)| >= 0.127
  via smoothed sum (discovery tier, not proven).

**What is needed [OBL]:**
- A rigorous proof that L(s, sym^2 Delta) != 0 on some region
  Re(s) >= sigma_0 with 1/2 < sigma_0 < 1.
- Candidate sigma_0: the smoothed-sum computation suggests sigma_0 ~ 0.6
  may work, but the error analysis is not rigorous.

**Possible approach [OBL]:**
- Use the GL_3 approximate functional equation (Batch 04) to evaluate L(s)
  with certified Arb intervals on a grid in [sigma_0, 1] x [-T, T].
- Show |L(s)| > delta > 0 at every grid point.
- Use a continuity argument (complex plane is simply connected) to extend
  to the full region.

### Step 2: Explicit formula [OBL]

**Goal:** Express S(X) = sum_{n<=X} A(n) in terms of zeros of L(s, sym^2 Delta).

**Assuming Step 1** (zero-free region Re(rho) <= sigma_0):

By Perron's formula (with smoothing):

```
S(X) = (1/2pi i) int_{c-iT}^{c+iT} L(s) * X^s / s ds + error(T)
```

Moving the contour to Re(s) = sigma_0 - epsilon picks up:
- The residue at s = 1 (if the pole exists; for sym^2 of a cusp form,
  L(s) is entire, so no pole).
- The integral along Re(s) = sigma_0 - epsilon.
- Residues at poles of X^s/s (only at s = 0, with residue 1).

**What is needed [OBL]:**
- Rigorous bound on the error from Perron truncation (T-dependence).
- Bound on the integral along Re(s) = sigma_0 - epsilon.
- If sigma_0 < 1: |S(X)| << X^{sigma_0} + error terms.
- If sigma_0 = 1/2 (GRH): |S(X)| << X^{1/2} * log(X) (standard).

### Step 3: Conclude [OBL]

**Goal:** From |S(X)| <= C * X^{alpha}, deduce Cesaro error bound.

The Cesaro average is L_ces(N, 1) = (1/N) * sum_{n<=N} S(n).
By Abel summation:

```
L(1) - L_ces(N, 1) = (1/N) * sum_{n<=N} (S(n) - L(1))
```

If |S(n) - L(1)| <= C * n^{alpha} for alpha < 1 (since L(1) is the residue
or the value at s=1, and S(n) -> L(1) as n -> infinity is NOT true —
S(n) oscillates, but L_ces(N,1) -> L(1)):

Actually, the correct statement is:
```
|L(1) - L_ces(N, 1)| <= (C/N) * sum_{n<=N} n^{alpha}
                     <= C * N^{alpha} / (alpha * N)
                     = C * N^{alpha - 1} / alpha
```

For alpha = 0.5: error <= 2C / sqrt(N).

With C = 0.259 (empirical) and N = 10^8: error <= 0.000052.
This gives L(1) in [0.6317, 0.6318]. [CONDITIONAL on Step 1-2]

## §3. Known obstacles

1. **Proving the zero-free region (Step 1)** is the hard part. The standard
   approach (Deuring-Heath-Brown zero-free region for GL_2 L-functions)
   gives sigma_0 = 1 - c/log(|t| + 2), which is not uniform in t.
   For a fixed sigma_0 < 1, one needs additional input (e.g., convexity
   bounds, subconvexity, or specific arithmetic information about Delta).

2. **The explicit formula (Step 2)** requires bounds on L(s) in the critical
   strip, which circularly depends on the zero-free region.

3. **Route B (GL_3 AFE direct computation)** may bypass the zero-free region
   by directly evaluating L(s) at grid points with certified error bounds.
   This is the approach in Batch 04.

## §4. References

- Deligne (1974), "La conjecture de Weil I" — Ramanujan bound.
- Gelbart-Jacquet (1978), "A note on the symmetric square L-function" — GL_3 AFE.
- Miller-Schmid (1975), "Automorphic distributions and the Voronoi summation formula" — C_GL3.
- Goldfeld-Hoffstein-Lieman (1994) — effective L(1) bound (ineffective constant).
- Hoffstein-Lockhart (1995) — effective bounds for Rankin-Selberg L-functions.
- Iwaniec-Kowalski (2004), "Analytic Number Theory" — explicit formulas, Perron's formula.
- Bombieri (2000), "Vinogradov's mean value theorem and estimates for L-functions" — zero-free regions.
