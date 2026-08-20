# F-2 Checker README

## Purpose

Structural checker for F-2 global residue positivity submissions.

## What it checks

1. **Required files**: statement.md, proof.md, dependencies.yaml, limitations.md, novelty.md
2. **[OBL] status**: No file promotes F-2 to [THM] without [OBL] tag
3. **F-2A coverage**: Diagonal, norm-square, Jacquet–Shalika concepts in proof-F-2A.md
4. **F-2B coverage**: Euler factor, archimedean, ramified concepts in proof-F-2B.md
5. **F-2C coverage**: Uniformity, local, explicit concepts in proof-F-2C.md

## What it does NOT check

- Mathematical correctness (requires human review)
- Exact citations (requires verification against original sources)
- Quantitative bounds (requires interval arithmetic certification)

## Usage

```bash
python3 checker/check_global_residue.py <submission_dir>
```

## Bug fixes (2026-08-20)

- Changed from `any()` token matching to phrase-level matching
- Fixed OBL status check to require exact `[OBL]` tag
- Added F-2A/F-2B/F-2C structure checks
