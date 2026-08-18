# Outsource status board

Each row tracks one outsourced proof obligation.
Status key: **pending** (not yet sent), **sent** (prompt dispatched),
**returned** (answer received), **verified** (independent checker passed),
**failed** (checker rejected), **stale** (prompt superseded).

| Artifact | Status | Prompt file | Review file | Notes |
|---|---|---|---|---|
| Task V: C_GL3 from Miller–Schmid Thm 1.18 | pending | OB-01-cgl3-explicit-bound.md | — | Blocked: need full Kloosterman/Bessel extraction |
| Task J: certified AFE dual term for L(1,sym²Δ) | pending | OB-02-dual-term-certification.md | — | Blocked: depends on Task V or [OBL M-3] |

## Pre-send checklist (mandatory)

Before dispatching any outsource prompt, run `PROMPT_LINT.md` against it.
A prompt with any FAILED item must not be sent.

## Re-scan rule

When a new defect class is discovered (by a reviewer or during internal work),
add it to `PROMPT_LINT.md` and re-scan ALL active (pending/sent) prompts.
Record the re-scan result in this status board as a dated note.
