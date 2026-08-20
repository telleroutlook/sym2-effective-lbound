# M-2 Checker README (v2)

## What it checks

1. **Required files**: statement.md, proof.md, dependencies.yaml, limitations.md, novelty.md
2. **[OBL] status**: No file promotes M-2 to [THM] without [OBL] tag
3. **Required concepts**: T·log T main term, AFE, diagonal decomposition
4. **Forbidden patterns**:
   - "c_Π T" / "cπ T" — wrong main term (should be T·log T)
   - "infinite double sum" — wrong starting point (Dirichlet series doesn't converge at Re s = ½)
   - "χ(Π)" / "χ(pi)" — constant root number as AFE dual factor (should be t-dependent X_Π(t))
   - "(3/2) R_Π" / "(3/2) Rπ" — wrong leading constant (should be 3R_Π)

## What it does NOT check

- Mathematical correctness of the H_{Π,p} formula
- Correctness of the shifted-convolution bound
- Whether A_Π = 3R_Π is actually proved (only checks it's not stated as (3/2)R_Π)
- Archimedean factor computation

## Version history

- v1 (2026-08-20): Initial checker
- v2 (2026-08-20): Added AFE dual factor, leading constant forbidden patterns
