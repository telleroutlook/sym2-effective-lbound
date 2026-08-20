# Outsource status board

Each row tracks one outsourced proof obligation.
Status key: **pending** (not yet sent), **sent** (prompt dispatched),
**returned** (answer received), **verified** (independent checker passed),
**failed** (checker rejected), **stale** (prompt superseded).

| Artifact | Status | Prompt file | Review file | Notes |
|---|---|---|---|---|
| Task V: C_GL3 from Miller–Schmid Thm 1.18 | pending | OB-01-cgl3-explicit-bound.md | — | Blocked: need full Kloosterman/Bessel extraction |
| Task J: certified AFE dual term for L(1,sym²Δ) | verified | OB-02-dual-term-certification.md | — | COMPLETED: J = S1 - L(1) route certified |
| OB-03: partial-sum bound \|S(X)\| << X^{1/2+ε} | verified | 03-partial-sum-bound-proof/ | — | COMPLETED: Friedlander-Iwaniec Thm 3.2 |
| OB-04: GL₃ AFE rigorous computation | verified | 04-gl3-afe-rigorous-computation/ | — | COMPLETED: L(1) certified [0.63179293, 0.63179298] |
| F-2: global residue positivity | verified | 05-F-2-global-residue/ | — | RESTRUCTURED: F-2A/B/C split; JS81 specialization; checker+lint pass |
| M-1: mollifier construction | verified | 06-M-1-mollifier/ | — | v2: deleted wrong bridge lemma, 4-variable convolution, T scale (not T·log T) |
| M-2: mean value estimate | verified | 07-M-2-mean-value/ | — | v2: t-dependent X_Π(t), correct H_{Π,p}, A_Π=3R_Π, Pal→IMRN 2025 |
| c_eff: general explicit lower bound | verified | 08-c_eff-explicit-bound/ | — | RESTRUCTURED: 1/log(kp+1) scope, Case 2 eliminated, HL route; checker+lint pass |

## Pre-send checklist (mandatory)

Before dispatching any outsource prompt, run `PROMPT_LINT.md` against it.
A prompt with any FAILED item must not be sent.

## Pre-flight math lint

Run `preflight_lint.py` against any package before externalizing:
```bash
python3 preflight_lint.py <package_dir>
python3 preflight_lint.py --all <base_dir>/
```
Catches: wrong main terms, wrong citations, dependency reversals, conductor confusion,
scaling errors, missing objects, checker quality issues, hardcoded paths, missing tests/manifest.

## Re-scan rule

When a new defect class is discovered (by a reviewer or during internal work),
add it to `PROMPT_LINT.md` and re-scan ALL active (pending/sent) prompts.
Record the re-scan result in this status board as a dated note.
