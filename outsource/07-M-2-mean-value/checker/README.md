# M-2 Checker README (v3)

## What it checks

1. **Required files**: statement.md, proof.md, dependencies.yaml, limitations.md, novelty.md
2. **[OBL] status**: No file promotes M-2 to [THM] without [OBL] tag
3. **Required concepts**: T·log T main term, AFE, diagonal decomposition
4. **Forbidden patterns** (v3 expanded):
   - "c_Π T" / "cπ T" — wrong main term (should be T·log T)
   - "infinite double sum" — wrong starting point
   - "χ(Π)" / "χ(pi)" — constant root number as AFE dual factor (should be t-dependent X_Π(t))
   - "(3/2) R_Π" / "(3/2) Rπ" — wrong leading constant (should be 3R_Π)
   - "r/T^3" — wrong AFE weight scale (should be T^{3/2})

## What it does NOT check

- Mathematical correctness of the H_{Π,p} formula
- Correctness of the shifted-convolution bound
- Whether the 4-term decomposition (|S₁|²+|S₂|²+cross terms) is complete
- Whether cross terms are actually o(T log T)
- Whether the AFE is the smooth version or truncated version
- Archimedean factor computation

**STRUCTURAL CHECKER ONLY — not a theorem certificate.**

## Version history

- v1 (2026-08-20): Initial checker
- v2 (2026-08-20): Added AFE dual factor, leading constant forbidden patterns
- v3 (2026-08-20): Added χ(Π), (3/2)R_Π, r/T^3 patterns; fixed README drift
