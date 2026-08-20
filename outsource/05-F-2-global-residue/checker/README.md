# F-2 Checker README (v2)

## What it checks

1. **Required files**: statement.md, proof.md, dependencies.yaml, limitations.md, novelty.md
2. **[OBL] status**: No file promotes F-2 to [THM] without [OBL] tag
3. **F-2A coverage**: diagonal, norm-square, jacquet–shalika in proof-F-2A.md
4. **F-2B coverage**: euler factor, archimedean, ramified in proof-F-2B.md
5. **F-2C coverage**: uniformity, local, explicit in proof-F-2C.md
6. **Forbidden patterns** (v2):
   - "Ann. Math. 114" — wrong JS81 citation (should be Am. J. Math. 103)
   - Single-factor Adjoint (should be 3 factors)
   - Continuity→positive uniformity (should require explicit nonvanishing first)

## What it does NOT check

- Mathematical correctness of Euler factors
- Exact Γ-factor computation
- Quantitative bounds
- Whether Z_∞ has correct degree

## Version history

- v1 (2026-08-20): Initial checker
- v2 (2026-08-20): Added citation, Adjoint factor, uniformity forbidden patterns
