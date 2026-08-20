# Restructuring Notes — v3 (2026-08-20)

## Major corrections from v2 (per independent review)

### 1. Stage C parameter chain wrong (CRITICAL)
v2 wrote δ = c₀/log(kp+1) then R⁻¹ ≪ log(1/δ), then somehow got
O(log(kp+1)). This is wrong: log(1/δ) = log(log(kp+1)) + O(1),
which is a much stronger conclusion and internally inconsistent with
the final O(log(kp)) result.

**Fix**: Rewritten with M = K^C matching. Set M = (kp+1)^C with
C ≥ max(A_0, c_ZF⁻¹). Then 1/log M ≤ c_ZF/log K, so the GHL
zero-free region covers HL Proposition 1.1's requirement. HL gives
R⁻¹ ≤ c(B)·log M = c(B)·C·log K. c_eff = 1/(c(B)·C).

### 2. Positivity reason wrong (ERROR)
v2 claimed non-negative coefficients "follows from Hecke multiplicativity
and positivity of symmetric-square coefficients." L(sym²f) coefficients
are NOT generally non-negative.

**Fix**: For A(s) = ζ(s)L(s,F), each local factor
(1−q^{−s})⁻¹(1−q^{−s−1})⁻¹ has all positive coefficients in q^{−s}.
By multiplicativity, the full Dirichlet series has non-negative coefficients.
GHL establishes this in general; for prime level + trivial character the
argument is especially clean.

### 3. V² description wrong (ERROR)
v2 wrote "symmetric part of the exterior square ⊗² minus the symmetric
square" — misleading and not how GHL describes it.

**Fix**: V² is the symmetric-square L-series of F. GHL calls it
"symmetric-square (L)-series of (F)."

### 4. c₀ not "depending on k" (ERROR)
v2 wrote c₀ "depending on k and the explicit parameters."
GHL states the zero-free region constant is absolute effective.

**Fix**: c_ZF is absolute effective (independent of k and p).

### 5. witness/README.md wrong (ERROR)
v2 claimed "c₀ ≤ 0.63179293 is a valid upper bound for the universal
constant." The correct relation is c_eff ≤ L(1,sym²Δ)·log(13) ≈ 1.62052.
Also Δ is level 1, outside prime-level scope.

**Fix**: Deleted the wrong claim. Added correct upper bound derivation.

### 6. Bibliography wrong (ERROR)
v2 cited HL as "Annals 140(1), pp. 1–42" (actually 161–181) and
Iwaniec–Michel as "JAMS 14, pp. 705–751" (actually Ann. Acad. Sci. Fenn.
26, pp. 465–482).

**Fix**: All citations corrected.

### 7. Stage D unnecessarily complex
v2 argued inf_{k,p} c₁(k,p) > 0 as a separate step. Since all constants
are absolute, c_eff = 1/(c(B)·C) is already a universal lower bound.

**Fix**: Simplified. No infimum argument needed.

### 8. MANIFEST included cache files
v2 MANIFEST included .pytest_cache/__pycache__ files not in the ZIP.

**Fix**: Regenerated with only stable source files.

### 9. Checker false positives
v2 checker checked for "q_ar" string presence as a proxy for correct
completed function. Also only checked statement.md for analytic conductor
(which is in proof.md).

**Fix**: Rewritten with M=K^C check, false positive fixes, proof.md checks.

## Previous corrections from v1

1. L(1/2) vs L(1) confusion — deleted L(1/2) entirely
2. Missing p^s in completed function — added
3. Analytic conductor k³ vs k² — corrected
4. Stage 3 factorization wrong — rewritten
5. Zero multiplicity wrong — rewritten as triple-zero/double-pole
6. HL Proposition 1.1 misapplied — separated into Stage B and Stage C
7. Stage 4 residue formula wrong — deleted
8. HL year wrong — corrected to 1994
9. Deleted Δ numerical dependency
