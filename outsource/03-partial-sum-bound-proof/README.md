# Batch 03 — Partial-sum bound for sym^2 Delta coefficients

This directory is a self-contained review batch. Send all files in this
directory to the reviewer.

## Mathematical goal

Prove a partial-sum bound of the form

```
S(X) := sum_{n<=X} A(n)  =  O_epsilon(X^{1/2 + epsilon})
```

where A(n) are the normalized symmetric-square coefficients of the
weight-12 cusp form Delta in S_12(SL_2(Z)):

```
L(s, sym^2 Delta) = sum_{n>=1} A(n) / n^s
```

with A(1) = 1, A(p) = c_p^2 - 1 (c_p = tau(p)/p^{5.5}), and A
multiplicative with the GL_3 Hecke recurrence for prime powers.

## Why this is needed

The L(1) value is computed as L(1) = S1 - J where:
- S1 is the "main sum" (certified to [0.548298, 0.548305]).
- J is the Abel summation truncation error from approximating L(1) by
  a finite Dirichlet sum.

By Abel summation:

```
L(1) = sum_{n<=N} A(n)/n - S(N)/N + integral_N^inf S(x)/x^2 dx
```

When |S(X)| <= C * X^alpha with alpha < 1, this gives:

```
|L(1) - sum_{n<=N} A(n)/n| <= C * (1 + 1/(1-alpha)) * N^{alpha-1}
```

## Proved result

**Theorem** (Friedlander-Iwaniec 2005, Proposition 3.2):
For every epsilon > 0:

```
S(X) = O_epsilon(X^{1/2 + epsilon})
```

unconditionally. No GRH, no zero-free region needed.

**What is NOT available:** The explicit constant C(epsilon). The empirical
value max |S(X)|/X^{0.5} = 0.259 for X in [100, N] is discovery-tier only.

## Contents

- `statement.md` — formal statement of the partial-sum bound
- `proof.md` — proof via Friedlander-Iwaniec Proposition 3.2
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

## Integrity

`MANIFEST.sha256` lists SHA-256 hashes for every sent source file except the
manifest itself.
