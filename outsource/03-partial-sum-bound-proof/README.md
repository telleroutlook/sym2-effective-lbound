# Batch 03 — Partial-sum bound for sym^2 Delta coefficients

This directory is a self-contained review batch. Send all files in this
directory to the reviewer.

## Mathematical goal

Prove a partial-sum bound of the form

```
S(X) := sum_{n<=X} A(n)  =  O(X^{1/2 + epsilon})
```

where A(n) are the normalized symmetric-square coefficients of the
weight-12 cusp form Delta in S_12(SL_2(Z)):

```
L(s, sym^2 Delta) = sum_{n>=1} A(n) / n^s
```

with A(1) = 1, A(p) = c_p^2 - 1 (c_p = tau(p)/p^{5.5}), and A
multiplicative with the GL_3 Hecke recurrence for prime powers.

## Why this is needed

The L(1) value decomposes as L(1) = S1 - J where:
- S1 is the "main sum" (certified to [0.548298, 0.548305]).
- J is the "Cesaro truncation error" from approximating L(1) by
  L_ces(N,1) = (1/N) sum_{n<=N} S(n).

The Cesàro error satisfies:
```
|L(1) - L_ces(N,1)| <= C * N^{alpha - 1} / alpha
```
when |S(X)| <= C * X^alpha for all X >= 1.

With the EMPIRICAL bound |S(X)| <= 0.259 * X^{0.5} (verified for X <= 20000),
N = 10^8 gives Cesàro error <= 0.000052, yielding:
```
L(1) in [0.6317, 0.6318]   (CONDITIONAL on the partial-sum bound)
```

Without a PROOF of the partial-sum bound, this is discovery-tier only.

## Empirical evidence

- For X in [1, 20000]: max |S(X)| / X^{0.5} = 0.2590.
- The bound |S(X)| <= X^{0.5} appears to hold with room to spare.
- A zero-free scan (src/zero_free_arb.py) certifies L(s) != 0 for
  Re(s) > 1 (via truncated Dirichlet series with tail bound).
- Discovery-tier scan extends to critical strip [0.6, 1.0] via smoothed
  sum (not yet rigorous).

## Suggested proof routes

### Route A: Zero-free region via explicit formula

1. Prove L(s, sym^2 Delta) != 0 for Re(s) >= sigma_0 with 1/2 < sigma_0 < 1.
2. Apply the explicit formula:
   S(X) = X * (residue at s=1) + sum_{rho} X^rho / rho + O(...)
   where the sum is over non-trivial zeros rho of L(s, sym^2 Delta).
3. If all zeros have Re(rho) <= sigma_0, then |S(X)| << X^{sigma_0}.

### Route B: GL_3 AFE direct computation

1. Use the GL_3 approximate functional equation to evaluate L(s) at
   specific points in the critical strip with certified error bounds.
2. Show L(s) != 0 at enough points to establish a zero-free region.
3. Route A then applies.

### Route C: Analytic number theory methods

1. Use the Rankin-Selberg convolution L(s, sym^2 Delta x sym^2 Delta)
   or other analytic techniques to bound S(X) directly.
2. The bound |A(n)| <= d_3(n) (DEL-D.1) is too weak; need oscillation.

## What the reviewer should produce

1. A proof of |S(X)| <= C * X^{1/2 + epsilon} for some explicit C, epsilon.
2. An explicit constant if possible (smaller C gives tighter L(1) interval).
3. Identification of which proof route succeeds (or a new route).
4. Any dependencies on unproved conjectures must be clearly stated.

## Contents

- `statement.md` — formal statement of the partial-sum bound
- `proof.md` — proof (or proof sketch with gaps identified)
- `dependencies.yaml` — dependency graph with evidence levels
- `limitations.md` — scope and limitations
- `novelty.md` — what is new
- `checker/` — independent verification code
- `witness/` — computational witnesses
- `_REVIEW_RETURN_TEMPLATE.md` — structured review checklist
- `tests/test_partial_sum_bound.py` — test file
- `MANIFEST.sha256` — integrity hashes

## Reviewer requirements

Please review the mathematical proof first, against the checkpoints in
`_REVIEW_RETURN_TEMPLATE.md`. A passing finite checker is not evidence that
the universally quantified theorem is true. Return the completed template
with one of: PASS, PASS WITH MINOR REVISIONS, FAIL, INCONCLUSIVE.

## Optional local checks

`python3 -m pytest tests/ -q` inside a fresh unpack of this batch.
Test count as measured in this exact bundle: to be determined.

## Integrity

`MANIFEST.sha256` lists SHA-256 hashes for every sent source file except the
manifest itself.
