# M-1 Checker README

## What it checks

1. **Required files**: statement.md, proof.md, dependencies.yaml, limitations.md, novelty.md
2. **[OBL] status**: No file promotes M-1 to [THM] without [OBL] tag
3. **Required concepts**: (n/m)^{it} phase, mollifier, shifted convolution, AFE, diagonal decomposition
4. **Forbidden patterns**: "Hecke eigenvalue orthogonality", "GL3 spectral large sieve" (wrong objects)

## What it does NOT check

- Mathematical correctness of the proof
- Correctness of the GL₃ shifted-convolution estimate
- Explicit constant computation
- Downstream bridge lemma to c_eff

## Bug fixes (2026-08-20)

- Changed from `any()` token matching to phrase-level matching
- Fixed OBL status check to require exact `[OBL]` tag
- Added forbidden pattern detection
