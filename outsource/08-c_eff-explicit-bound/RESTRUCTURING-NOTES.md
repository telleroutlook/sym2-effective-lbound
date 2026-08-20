# Restructuring Notes — v2 (2026-08-20)

## Major corrections from v1 (per independent review)

### 1. L(1/2) vs L(1) confusion (CRITICAL)
v1 stated L(½, sym² f) ≥ c_*/log(kp+1) and claimed equivalence with L(1).
This is wrong. GHL/HL gives a lower bound at s=1, not s=1/2.
These are completely different values.

**Fix**: Deleted L(1/2) entirely. Only L(1) bound is retained.

### 2. Missing p^s in completed function (CRITICAL)
v1 wrote Λ(s,Π) = L_∞(s) L(s,Π).
Correct: Λ(s,Π) = p^s L_∞(s) L(s,Π) because q_ar = p².

**Fix**: Added p^s to all completed function statements.

### 3. Analytic conductor k³ vs k² (ERROR)
v1 stated Q_an ≈ p²k³.
Correct: archimedean shifts are ≈1, k−1, k, giving Q_an ≈ p²k².

**Fix**: Corrected to k² everywhere.

### 4. Stage 3 factorization wrong (CRITICAL)
v1 claimed poles from ζ(s) and L(s,Π)².
Correct: poles from ζ(s) and L(s,F,V²); L(s,F) is holomorphic at s=1.

**Fix**: Complete rewrite of Stage B with correct factorization
φ(s) = ζ(s) L(s,F)³ L(s,F,V²).

### 5. Zero multiplicity wrong (ERROR)
v1 argued "double zero minus double pole = net zero".
Correct: triple zero at β, double pole at 1 — different points,
cannot subtract orders. GHL zero-count lemma gives contradiction.

**Fix**: Rewritten as triple-zero / double-pole contradiction.

### 6. HL Proposition 1.1 misapplied (CRITICAL)
v1 applied HL to Φ(s) = ζ·L²·L(Π×Π̃).
Correct: HL Prop 1.1 applies to A(s) = ζ(s)L(s,F), whose residue is L(1,F).
Stage B and Stage C are separate steps.

**Fix**: Separated into Stage B (GHL zero-free) and Stage C (HL residue).

### 7. Stage 4 residue formula wrong (CRITICAL)
v1 wrote Res ζ·L²·L(Π×Π̃) = L(1,Π)² L(1,Π×Π̃).
This is wrong: L(Π×Π̃) has a simple pole at s=1, so L(1,Π×Π̃) is not finite.

**Fix**: Deleted entirely. Stage D is now about explicit constant extraction,
not a residue formula.

### 8. HL year wrong
v1 referenced "Hoffstein–Lockhart (1997)".
Correct: Hoffstein–Lockhart (1994), Annals of Mathematics 140(1), pp. 1–42.

**Fix**: All references corrected to 1994.

### 9. Deleted Δ numerical dependency
v1 included L(s,sym²Δ) ≠ 0 as a dependency. This is unrelated to the
general proof and should not be in this package.

**Fix**: Removed. Δ-specific computation is in F-3 (separate package).

### 10. Checker improvements (per reviewer feedback)
- check_scope(): fixed operator precedence bug, now requires log(kp)
- Removed Case 2 string ban (it's correct to say "Case 2 is absent")
- Added checks for p^s, k², L(1/2), HL year

### 11. MANIFEST.sha256
v1 MANIFEST included .pytest_cache and __pycache__ files not in the ZIP.

**Fix**: Regenerated with only stable source/certificate files.
