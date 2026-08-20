# Novelty — M-2 Rewritten v3

## What is new in v3 (correcting v2)

7. **Fixed AFE weight scale**: V_t(r/T^3) → W_t(r) with support r ≪ T^{3/2}.
   The T^3 was inconsistent with degree-3 AFE length.

8. **Added 4-term decomposition**: |S₁+XS_2|² = |S₁|²+|S₂|²+S₁·X̄·S̄₂+S̄₁·X·S₂.
   v2 only described diagonal, missing cross terms with gamma phase.

9. **Downgraded Step 1**: Smooth AFE with truncation error is [OBL], not [THM].

10. **Made A_Π=3R_Π conditional**: Requires cross terms to be o(T log T).

11. **Added H_Π(1)≠0 justification**: From positivity of D_{Π,p} and L_p.

12. **Fixed checker**: Added χ(Π), (3/2)R_Π, r/T^3 forbidden patterns.
    v2 README claimed these checks but code didn't implement them.

## What is new in v2 (correcting v1)

1. **Deleted wrong main term**: c_Π T → A_Π T log T (Rankin–Selberg pole).
2. **Deleted wrong dual factor**: χ(Π) → X_Π(t) (t-dependent gamma ratio).
3. **Fixed H_{Π,p} formula**: Corrected to 1+O(x²) matching.
4. **Fixed leading constant**: A_Π = 3R_Π (both AFE halves contribute).
5. **Deleted bad-prime limitation**: Level-one forms have no bad primes.

## What is NOT new

- The AFE-based second moment approach is classical
- The diagonal calculation giving R_Π log T per half is standard
- The identification of GL₃ shifted-convolution as the obstruction is known
