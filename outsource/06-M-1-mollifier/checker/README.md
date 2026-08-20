# M-1 Checker README (v3)

## What it checks

1. **Required files**: statement.md, proof.md, dependencies.yaml, limitations.md, novelty.md
2. **[OBL] status**: No file promotes M-1 to [THM] without [OBL] tag
3. **Required concepts**: (n/m)^{it} phase, mollifier, AFE
4. **Forbidden patterns**:
   - "Hecke eigenvalue orthogonality" (wrong object — family, not fixed Π)
   - "GL3 spectral large sieve" (wrong object — family, not fixed Π)
   - "I(T) >= c₀T" bridge lemma (FALSE: integral cannot detect central value)
   - "deduce L(½" (wrong: normalization gap, wrong bridge)
   - "hence L(1," (wrong: normalization gap)
   - "squarefree approximation" (algebraically vacuous: μ(m)=0 when p²|m)

## What it does NOT check

- Mathematical correctness of the proof
- Correctness of the GL₃ twisted-moment estimate
- Explicit constant computation
- Whether the convolution structure is correct
- Whether the 4-block AFE decomposition is complete
- Whether the coefficient bound is weighted or unweighted
- Whether the shift scale includes the θ correction

**STRUCTURAL CHECKER ONLY — not a theorem certificate.**

## Version history

- v1 (2026-08-20): Initial checker
- v2 (2026-08-20): Added bridge-lemma, squarefree, normalization forbidden patterns
- v3 (2026-08-20): Fixed README drift; clarified structural-only scope
