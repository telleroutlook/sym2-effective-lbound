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
| F-2: global residue positivity | pending | F-2-global-residue/ | — | Blocked: L(1,π,Ad)>0 not located |
| M-1: mollifier construction | pending | M-1-mollifier/ | — | Blocked: GL₃ mean value + large sieve explicit constants |
| M-2: mean value estimate | pending | M-2-mean-value/ | — | Blocked: archimedean integral + bad places |
| c_eff: general explicit lower bound | pending | c_eff-explicit-bound/ | — | Blocked: all above + Vinogradov-Korobov GL₃ |

## Pre-send checklist (mandatory)

Before dispatching any outsource prompt, run `PROMPT_LINT.md` against it.
A prompt with any FAILED item must not be sent.

## Re-scan rule

When a new defect class is discovered (by a reviewer or during internal work),
add it to `PROMPT_LINT.md` and re-scan ALL active (pending/sent) prompts.
Record the re-scan result in this status board as a dated note.
