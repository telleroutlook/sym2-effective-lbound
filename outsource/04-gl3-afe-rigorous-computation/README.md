# Batch 04 — Rigorous GL_3 AFE computation for L(s, sym^2 Delta)

This directory is a self-contained review batch. Send all files in this
directory to the reviewer.

## Mathematical goal

Compute L(s, sym^2 Delta) at specific points in the critical strip
{sigma + it : 0.5 <= sigma <= 1.0, |t| <= T_max} using the GL_3
approximate functional equation, with RIGOROUS error bounds that
certify L(s) != 0 at every grid point.

## Why this is needed

The L(1) value requires the Cesàro truncation error J, which depends on
the partial sums S(X). The partial-sum bound |S(X)| << X^{1/2} follows
from a zero-free region for L(s, sym^2 Delta). The GL_3 AFE provides a
way to:

1. Evaluate L(s) at any point in the critical strip.
2. Bound the truncation error rigorously.
3. Show L(s) != 0 on a region, giving the zero-free region.

## The GL_3 AFE formula

For Re(s) > 0, the smoothed-sum identity gives:

```
sum_{n>=1} A(n)/n^s * V(n/X, s) = L(s) + error(X, s)
```

where V(y, s) is the weight function from Mellin inversion:

```
V(y, s) = (1/2pi i) int_{Re(u)=c} G(s+u)/G(s) * y^{-u} * h(u)/u du
```

with G(s) = Gamma_R(s) * Gamma_C(s+11) and h(u) a suitable
cutoff function (e.g., h(u) = exp(u^2)).

The key properties:
- V(y, s) decays exponentially for large y (like exp(-c*y^{2/3})).
- The truncated sum with N ~ X^{3/2} captures L(s) to precision
  exp(-c*N^{2/3}).
- The dual sum contributes O(X^{-1/2}) via Stirling + convexity.

## What the reviewer should produce

1. A rigorous computation of L(s) at a grid of points in the critical
   strip, with certified error bounds (e.g., using Arb/python-flint).
2. Verification that L(s) != 0 at every grid point (|L(s)| > delta > 0).
3. An explicit zero-free region: L(s) != 0 for Re(s) >= sigma_0 with
   sigma_0 < 1 (the smaller the better).
4. Any gaps in the error analysis must be clearly identified.

## Suggested implementation

1. Use python-flint (Arb library) for interval arithmetic.
2. Compute the weight function V(y, s) via the Mellin integral with
   rigorous error bounds (contour shift, gamma factor bounds).
3. Compute the truncated sum sum_{n<=N} A(n)/n^s * V(n/X, s) with
   rigorous rounding (outward for upper bound, inward for lower).
4. Bound the tail sum via the decay of V(y, s) and |A(n)| <= d_3(n).

## Contents

- `statement.md` — formal statement of the computation goal
- `proof.md` — description of the method and error analysis
- `dependencies.yaml` — dependency graph with evidence levels
- `limitations.md` — scope and limitations
- `novelty.md` — what is new
- `checker/` — independent verification code
- `witness/` — computational witnesses (certified L(s) values)
- `_REVIEW_RETURN_TEMPLATE.md` — structured review checklist
- `tests/` — test file
- `MANIFEST.sha256` — integrity hashes

## Reviewer requirements

Please review the mathematical method and error analysis first, against
the checkpoints in `_REVIEW_RETURN_TEMPLATE.md`. The finite checker
verifies the arithmetic but not the analytic bounds. Return the completed
template with one of: PASS, PASS WITH MINOR REVISIONS, FAIL, INCONCLUSIVE.

## Optional local checks

`python3 -m pytest tests/ -q` inside a fresh unpack of this batch.
Test count as measured in this exact bundle: to be determined.

## Integrity

`MANIFEST.sha256` lists SHA-256 hashes for every sent source file except the
manifest itself.
