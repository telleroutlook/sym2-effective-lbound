# M-1 Checker README (v4)

## What it checks

1. **Required files**: statement.md, proof.md, dependencies.yaml, limitations.md, novelty.md
2. **[OBL] status**: No file promotes M-1 to [THM] without [OBL] tag
3. **Required concepts**: (n/m)^{it} phase, mollifier, AFE
4. **Forbidden patterns**:
   - "Hecke eigenvalue orthogonality" (wrong object — family, not fixed Π)
   - "GL3 spectral large sieve" (wrong object — family, not fixed Π)
   - "I(T) >= c₀T" bridge lemma (FALSE)
   - "deduce L(½" (normalization gap)
   - "hence L(1," (normalization gap)

## What it does NOT check

- Mathematical correctness of the proof
- Correctness of the GL₃ twisted-moment estimate
- Whether the FE factor has correct normalization (ε_Π, q_Π)
- Whether the I_{--} gamma-phase description is correct
- Whether the 4-block AFE decomposition is complete
- Whether the convolution variable notation avoids collision

**STRUCTURAL CHECKER ONLY — not a theorem certificate.**

## Version history

- v1 (2026-08-20): Initial checker
- v2 (2026-08-20): Added bridge-lemma, squarefree, normalization forbidden patterns
- v3 (2026-08-20): Fixed README drift
- v4 (2026-08-20): Added FE normalization, I_{--} gamma-phase corrections to limitations
