# M-2 Checker README

## What it checks

1. **Required files**: statement.md, proof.md, dependencies.yaml, limitations.md, novelty.md
2. **[OBL] status**: No file promotes M-2 to [THM] without [OBL] tag
3. **Required concepts**: T log T main term, AFE, diagonal decomposition, shifted convolution
4. **Forbidden patterns**: "c_Π T" (wrong main term), "infinite double sum" (wrong starting point)

## What it does NOT check

- Mathematical correctness of the proof
- Correctness of the shifted-convolution estimate
- Explicit constant computation
- Archimedean factor computation

## Bug fixes (2026-08-20)

- Changed from `any()` token matching to phrase-level matching
- Fixed OBL status check to require exact `[OBL]` tag
- Added forbidden pattern detection for wrong main term
