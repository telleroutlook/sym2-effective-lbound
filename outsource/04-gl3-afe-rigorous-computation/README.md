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

## v3 corrections (2026-08-20)

- All witness JSONs downgraded from CERTIFIED to DISCOVERY
- C_V computation bug documented (missing G factor)
- AFE tail X-direction error documented
- Dual tail hardcoded value documented
- proof.md §5: 3 code-level bugs identified
- limitations.md: expanded from 9 to 10 gap categories

## Discovery-tier results

- L(1) ~ 0.63179295 (mpmath, not certified)
- Min |L(s)| ~ 0.170 on 5x41 grid (numerical observation, not proved)

## Critical gaps [OBL]

1. Exact coefficient chain (float -> exact rational)
2. Mellin quadrature error bound
3. Contour tail bound
4. AFE tail bound (N vs 2N is NOT rigorous; X-direction error in code)
5. Zero-free region (finite differences != derivative bounds)
6. Unified error budget
7. C_V missing G(s+1+it)/G(s) factor
8. Dual tail hardcoded (no derivation)

See `limitations.md` for full details.

## Contents

- `statement.md` — method description
- `proof.md` — method and gap analysis (v3: 6 error layers + 3 code bugs)
- `src/` — AFE implementation (discovery-tier, bugs documented)
- `checker/` — independent verifier
- `witness/` — numerical observations (all DISCOVERY, no CERTIFIED)
- `dependencies.yaml` — dependency graph
- `limitations.md` — scope and limitations (v3: 10 categories)
- `novelty.md` — what is new

## Integrity

MANIFEST.sha256 lists SHA-256 hashes for all source files.
