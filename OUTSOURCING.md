# Self-contained outsourced research tasks

These two tasks can be assigned independently.  A solution may use standard
published theorems, but every external input must be cited by exact theorem
number and verified against a primary source.  Discovery-tier computations may
motivate a strategy but have no evidentiary force.

## Common rules

1. Do not claim either task is complete based on numerical agreement.
2. All numerical constants in a final certificate must use outward-rounded
   interval arithmetic (`python-flint`/Arb or an equivalent certified backend).
3. Every infinite sum, integral tail, dyadic decomposition, and cancellation
   step needs an explicit proof or certified bound.
4. Code deliverables must be deterministic and must not import `discovery/`.
5. The independent checker must not import `src/`.
6. Include tests that reject a tampered constant, tail, endpoint, or claim.
7. State all changes in English and keep repository status labels intact.

---

## Task V: explicit `C_GL3` from Miller--Schmid Theorem 1.18

### Input

Use exactly Miller--Schmid, *Automorphic distributions, L-functions, and
Voronoi summation for GL(3)*, Ann. of Math. (2) **164** (2006), 423--488,
Theorem 1.18:

```text
sum_{n != 0} a_{q,n} e(-n a/c) f(n)
  = sum_{d | c q} |c/d|
      sum_{n != 0} A(n,d)/|n|
      S(q a_bar, n; q c/d)
      F(n d^2 / (c^3 q)).
```

The normalization factors `|c/d|`, `A(n,d)/|n|`, the Kloosterman modulus
`q c/d`, and the argument `n d^2/(c^3 q)` are mandatory.  The source-backed
entry is `MS-V.1` in `baseline/REFERENCE_BASELINE.md`; repository details are
in `proof/05-voronoi-constant.tex`.

### Goal

Choose and specify a test-function class `T` relevant to the AFE dual/contour
term, and prove an explicit estimate

```text
| sum_{n != 0} a_{q,n} e(-n a/c) phi(n/X) |
    <= C_voronoi(phi) X^alpha
```

for all `X >= X0` and all `(q,c)` required by that term.  The exponent
`alpha <= 2/3 + epsilon` is desired, but a rigorously larger explicit exponent
may be submitted if it still certifies the intended application.  The constants
`C_voronoi(phi)`, `X0`, and every hidden parameter must be computable.

### Required ledger

The write-up must separately quantify:

1. the exact coefficient normalization and `A(n,d)` convention;
2. a Rankin--Selberg coefficient moment with all powers of `d`;
3. the Kloosterman bound and its constant;
4. an `L^1`/`L^2`/Sobolev norm of the normalized transform `F`;
5. the dyadic decomposition and the resulting `c`- and `d`-sum exponents;
6. truncation and tail bounds for every infinite or conditionally convergent sum;
7. the connection from this estimate to either the `J` certificate or M-3.

### Explicitly forbidden

- Replacing Theorem 1.18 by a generic `c^{-2} K_nu(...)` expression.
- Reporting the empirical `C_GL3` from a finite scan.
- Using the threshold `7.4880` or margin over it as proof.
- Silently dropping the `d | cq`, `c`, or `n` tails.
- Treating the self-dual `q=c=1` identity as a cancellation estimate.

### Acceptance

Provide:

1. a complete mathematical PDF or LaTeX derivation;
2. interval-arithmetic code reproducing every numerical constant;
3. an independent checker and negative tamper tests;
4. commands equivalent to:

```bash
pytest tests/test_voronoi_constant.py -q
ruff check .
```

The reviewer will additionally run the repository-wide test suite and inspect
the source-level citation ledger before accepting the result.

---

## Task J: certified AFE dual term for `L(1,sym^2 Delta)`

### Mathematical object

Let `tau(n)` denote Ramanujan's tau function and define normalized symmetric
square coefficients by

```text
A(1)=1,  A(2)=tau(2)^2/2^11-1=-23/32,
```
and by the GL(3) Satake recurrence multiplicatively at every prime.  Let

```text
L(s) = sum_{n>=1} A(n) n^{-s}
```

be `L(s,sym^2 Delta)`.  For the AFE normalization used in this repository set

```text
G(s) = Gamma_R(s) * Gamma_C(s+11),
Gamma_R(s) = pi^(-s/2) Gamma(s/2),
Gamma_C(s) = 2 (2 pi)^(-s) Gamma(s),

A(t) = G(1/2+i t)/G(1)
       * 12^(-1/2+i t)
       * exp((-1/2+i t)^2) / (-1/2+i t),

J = (1/(2 pi)) integral_{-infinity}^{infinity}
    Re( L(1/2+i t) A(t) ) dt.
```

The repository's discovery computations suggest `J` is approximately `-0.083`
and `L(1,sym^2 Delta)=S1-J` is approximately `0.631793`; neither value may be
assumed.

### Goal

Produce a certificate `J in [J_lo,J_hi]` with width at most `1e-6`, together
with a proof of the identity and every tail bound used.  A wider interval may
be submitted only if it still gives a useful certified `L(1)` interval when
combined with a certified infinite main-sum tail.

### Acceptable routes

A submission may use any fully proved route, including:

1. derive an absolutely convergent dual Dirichlet series from Miller--Schmid
   Theorem 1.18 and bound its tail with Arb;
2. prove a sufficiently explicit numerical zero-free/size region for
   `L(s,sym^2 Delta)` and integrate with certified interval arithmetic;
3. supply another rigorous functional-equation or modular-identity argument.

Route selection is part of the task.  The final proof must make clear why the
conditionally convergent critical-strip object has been replaced by an
absolutely convergent or otherwise rigorously controlled quantity.

### Explicitly forbidden

- Cesaro averaging, numpy/mpmath floats, or convergence tables as proof.
- Interchanging a limit/integral without a dominated convergence argument.
- Using an empirical zero-free scan or the absence of observed zeros.
- Claiming `J` or `L(1)` from the new finite certificate
  `src/afe_s1_arb.py`: that file certifies only `S1[N,T]`.
- Using `[OBL M-3]` or Task V as if it were already proved.

### Required certificate fields

The JSON certificate must identify:

1. the mathematical route;
2. the exact test functions and normalization;
3. Arb precision and all interval endpoints;
4. every truncation length;
5. an explicit proof-level tail bound;
6. a false `certifies_l1` field unless an independently certified `S1` tail is
   also supplied;
7. a SHA-256 checksum for any exact integer coefficient vector.

### Acceptance

Provide the mathematical write-up, generator, independent checker, and tests.
The reviewer will run:

```bash
pytest tests/test_certified_j.py -q
python checker/check_certified_j.py certificates/j_sym2_delta.json
ruff check .
```

The checker must fail after changing any endpoint by one unit in its final
printed digit, after extending a claimed tail, or after setting a promotion
flag to true.
