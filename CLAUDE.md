# CLAUDE.md — sym2-effective-lbound

## Project Identity

This repository implements explicit, computer-assisted lower bounds for the symmetric
square L-function $L(1, \mathrm{sym}^2 f)$ of a holomorphic Hecke eigenform $f$.
The authoritative mathematical specification is `spec/SPECIFICATION.md`.

The research target is the technical gap in the Goldfeld–Hoffstein–Lieman (1994)
lower bound $L(1, \mathrm{sym}^2 f) \geq c/\log N$: the constant $c$ is currently
ineffective (non-computable). This repository pursues explicit certified instances
(starting with the Ramanujan $\Delta$ function) and, ultimately, an explicit general
constant.

**Mathematical honesty:** The implication kernel is the deliverable. Any unproved
obligation is explicitly labelled `[OBL]`. The phrase "proved here" is never used
for an `[OBL]` item.

---

## Status Grammar (non-negotiable)

Every item in the claim ledger has exactly one atomic status:

| Status | Meaning | Downstream use |
|--------|---------|----------------|
| `[DEF]` | Definition fixed by the spec | May be unfolded |
| `[BASE]` | Standard theorem admitted as foundation | Usable with stated hypotheses |
| `[THM]` | Theorem proved here from `[DEF]`/`[BASE]` | Usable downstream |
| `[OBL]` | Construction or proof still required | **May NOT be used as a theorem** |
| `[OUT]` | Deliberately outside the certified profile | **No downstream force** |

Composite labels are forbidden. Status is derived by the checker, never self-declared.

---

## Module Dependency (one-way, enforced)

```
M0 foundations
  └─► M1 local factors + global residue   (proof/01, proof/02)
        └─► M2 mollifier construction      (proof/03)   [OBL]
              └─► M3 zero-free region      (proof/04)   [OBL]
                    └─► M4 explicit bound  (proof/04)   [OBL]
```

- M1 must not import M2, M3, M4.
- `checker/` must not import `src/` (independent verification).
- `discovery/` must not be imported by any other module.

---

## Forbidden Patterns

- **Never** write `L(1, sym² f) > 0` as a consequence of an `[OBL]` step.
- **Never** promote a floating-point result to a theorem without interval arithmetic certification.
- **Never** co-modify `checker/` and `src/` in the same commit to make a test pass.
- **Never** self-declare a lower bound without running `checker/check_bound.py`.
- **Never** write the Siegel zero argument as "the zero does not exist" without a certified zero-free region.

---

## Engineering Conventions

- **Long computations (>30 s):** use `~/.local/bin/run_and_wait.sh -t <sec> -- <cmd>`
- **Certified bounds:** `python-flint` / Arb with outward rounding; `mpmath`/floats are discovery-tier only
- **`discovery/` is untrusted:** never imported by `proof/`, `checker/`, or `src/`
- **Commit messages in English.** `git status` before commit. Never stage `discovery/` into the proof chain.
- **Certificates go in only after independent replay.**
- **No PASS self-report anywhere.** `checker/` output is the sole authority.

---

## What This Repository Does NOT Do

- Does not claim to improve the Hoffstein–Lockhart lower bound unconditionally (this is `[OBL]`).
- Does not treat the numerical approximation $L(1, \mathrm{sym}^2 \Delta) \approx 2.406$ as a theorem without the Arb certificate.
- Does not assume GRH in the main bound (GRH-conditional results are labelled `[OUT]`).
- Does not claim the Siegel zero is excluded without an explicit zero-free region certificate.

---

## Session Start Protocol (Mandatory)

Every session working on this repository MUST begin by running:

```bash
pytest tests/ -x -q
```

and confirming all tests pass. If any fail:
1. Stop. Do not touch any other file.
2. Restore the failing tests to passing before proceeding.
