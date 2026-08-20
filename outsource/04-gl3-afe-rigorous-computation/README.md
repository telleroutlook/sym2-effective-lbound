# Batch 04 — GL_3 AFE computation for L(s, sym^2 Delta)

**Status:** METHOD-DESCRIPTION + DISCOVERY (not a theorem).

## What this batch is

A computational method description and discovery-tier numerical prototype
for evaluating L(s, sym^2 Delta) via the GL_3 approximate functional
equation. The AFE structure is correct. All rigorous error layers are
[OBL] (not yet closed).

## What this batch is NOT

- NOT a certified computation of L(1)
- NOT a proved zero-free region
- NOT a premise for downstream obligations
- NOT self-contained (missing heartbeat.py, tail_bound.py, baseline/)

## Mathematical goal

Evaluate L(s, sym^2 Delta) at points in the critical strip using the
two-term AFE:

```
L(s) = sum_{n<=N} A(n)/n^s * V(n/X, s) + dual_sum + tails
```

with weight functions from Mellin inversion.

## Discovery-tier results

- L(1) ~ 0.63179295 (mpmath, not certified)
- Min |L(s)| ~ 0.170 on 5x41 grid (numerical observation, not proved)

## Critical gaps [OBL]

1. Exact coefficient chain (float -> exact rational)
2. Mellin quadrature error bound
3. Contour tail bound
4. AFE tail bound (N vs 2N is NOT rigorous)
5. Zero-free region (finite differences != derivative bounds)
6. Unified error budget

See `limitations.md` for full details.

## Contents

- `statement.md` — method description
- `proof.md` — method and gap analysis
- `src/` — AFE implementation (discovery-tier)
- `checker/` — independent verifier
- `witness/` — numerical certificates (discovery-tier)
- `dependencies.yaml` — dependency graph
- `limitations.md` — scope and limitations
- `novelty.md` — what is new

## Integrity

MANIFEST.sha256 lists SHA-256 hashes for all source files.
