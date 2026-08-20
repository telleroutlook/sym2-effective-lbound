# c_eff Checker README

## What it checks

1. **Required files**: statement.md, proof.md, dependencies.yaml, limitations.md, novelty.md
2. **[OBL] status**: No file promotes c_eff to [THM] without [OBL] tag
3. **Required concepts**: Hoffstein–Lockhart, zero-free region, auxiliary series, explicit
4. **Forbidden patterns**: "case 2" (exceptional branch), "siegel zero" (wrong framing), "Vinogradov–Korobov" (not needed)
5. **Scope check**: Must use 1/log(kp+1) or fix k, NOT 1/log p

## What it does NOT check

- Mathematical correctness of the proof
- Numerical computation of c_*
- Correctness of the interval certification
- Replay script validity

## Bug fixes (2026-08-20)

- Changed from `any()` token matching to phrase-level matching
- Fixed OBL status check to require exact `[OBL]` tag
- Added forbidden pattern detection (case 2, Siegel zero, VK)
- Added scope check for k-dependence
