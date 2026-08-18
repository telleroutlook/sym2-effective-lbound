# PROMPT_LINT.md — Adversarial checklist for outsource prompts

Run every check below against the target OB-*.md file BEFORE sending.
All items must PASS. A single FAIL blocks dispatch.

## Circularity (C-series)

| ID | Check | Command |
|---|---|---|
| C-1 | No use of [OBL] claims as hypotheses in [THM] proofs | Manual review: each [OBL] must not appear as a step in a [THM] argument |
| C-2 | No self-referential circularity (prompt proves its own conclusion by assuming it) | Manual review: conclusion must not appear in definitions or hypotheses |
| C-3 | No reference to discovery/ results as certified bounds | `grep -rn 'discovery/' outsource/OB-*.md` → must return empty |

## Status grammar (S-series)

| ID | Check | Command |
|---|---|---|
| S-1 | Every claim is explicitly tagged [DEF], [BASE], [THM], [OBL], or [OUT] | `grep -cE '\[(DEF|BASE|THM|OBL|OUT)\]' outsource/OB-*.md` → must be ≥ 1 per file |
| S-2 | No composite status labels (e.g., [THM OBL], [BASE+THM]) | `grep -E '\[[A-Z]+ +[A-Z]+\]' outsource/OB-*.md` → must return empty |
| S-3 | [OBL] items are not silently promoted to [THM] or [BASE] in the same file | Manual review |

## Self-containment (SC-series)

| ID | Check | Command |
|---|---|---|
| SC-1 | Every symbol is defined before first use (inline, not via external file) | Manual review: no undefined symbols |
| SC-2 | All cited theorems include exact source (author, title, year, theorem number, page) | `grep -E 'Theorem [0-9]' outsource/OB-*.md` → every match must have a citation nearby |
| SC-3 | No dependency on files not present in the prompt (except standard [BASE] references) | `grep -E 'src/|checker/|proof/|spec/' outsource/OB-*.md` → must return empty |
| SC-4 | Definitions section is labelled and contains all notation used in the file | `grep -i 'definitions' outsource/OB-*.md` → must return non-empty |

## Numerical integrity (N-series)

| ID | Check | Command |
|---|---|---|
| N-1 | Every numerical constant states its precision (Arb bits, interval width, or decimal digits) | `grep -E '[0-9]+\.[0-9]+' outsource/OB-*.md` → every float must be in interval notation or have explicit precision |
| N-2 | No mpmath/float used as proof; only Arb/python-flint for certified arithmetic | `grep -iE 'mpmath|float\(\)|numpy' outsource/OB-*.md` → must return empty |
| N-3 | Discovery-tier estimates are explicitly labeled as such and not used in proofs | `grep -i 'discovery' outsource/OB-*.md` → every match must be in a non-proof context |

## Citation integrity (CI-series)

| ID | Check | Command |
|---|---|---|
| CI-1 | Every external reference has a matching row in baseline/REFERENCE_BASELINE.md | Cross-check citation IDs against REFERENCE_BASELINE.md |
| CI-2 | No fabricated or unverifiable citation | Every cited paper must include author, title, journal, year, and page/theorem number |

## Scope (SC2-series)

| ID | Check | Command |
|---|---|---|
| SC2-1 | The prompt does not ask for multiple unrelated theorems | Manual review: each OB-*.md targets one focused mathematical statement |
| SC2-2 | Forbidden-paths section lists ≥ 2 explicitly prohibited shortcuts | `grep -c -i 'forbidden\|must not\|not allowed' outsource/OB-*.md` → must be ≥ 2 |
| SC2-3 | Acceptance criteria are concrete and executable (not "be convinced") | Manual review: acceptance must include runnable commands (pytest, ruff, python) |

## Re-scan rule

When a new defect class is found by a reviewer, add a new row above and
re-run ALL checks against ALL active prompts. Record the re-scan date in
`outsource/README.md`.
