# M-2 Checker README (v4)

## What it checks

1. **Required files**: statement.md, proof.md, dependencies.yaml, limitations.md, novelty.md
2. **[OBL] status**: No file promotes M-2 to [THM] without [OBL] tag
3. **Required concepts**: T·log T main term, AFE, diagonal decomposition
4. **Forbidden patterns** (v4 context-aware):
   - Global: "c_Π T", "infinite double sum", "χ(Π)" — always forbidden
   - Proof-only: "(3/2) R_Π", "r/T^3" — forbidden in proof.md, but allowed
     in limitations.md if in negation context (describing corrected errors)

## v4 changes

- Context-aware forbidden patterns: old-error references in "corrected from"
  sections no longer trigger false positives
- Negation detection: checks surrounding 80 chars for keywords like
  "corrected", "fixed", "was wrong", "previous", "v2", "v3"

## What it does NOT check

- Mathematical correctness of the H_{Π,p} formula
- Correctness of the shifted-convolution bound
- Whether the 4-term decomposition is complete
- Whether cross terms are actually o(T log T)
- Whether the AFE is the smooth version or truncated version
- Archimedean factor computation

**STRUCTURAL CHECKER ONLY — not a theorem certificate.**

## Version history

- v1 (2026-08-20): Initial checker
- v2 (2026-08-20): Added AFE dual factor, leading constant forbidden patterns
- v3 (2026-08-20): Added χ(Π), (3/2)R_Π, r/T^3 patterns
- v4 (2026-08-20): Context-aware forbidden patterns (negation detection)
