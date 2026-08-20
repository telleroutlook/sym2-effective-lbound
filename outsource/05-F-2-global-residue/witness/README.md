# Witness — F-2 Global Residue Positivity (v4)

## F-2A

**Computed**: Analytic — not a computation, but a theorem citation (JS81).

**Witness**: The positive residue follows from:
1. Eisenstein series pole (JS81 §4.3 eq. (2))
2. Whittaker unfolding (JS81 §4.5 eq. (5))
3. Pole identification at s=1 (JS81 §4.6(i))
4. Norm-square positivity (|W_φ(g)|² ≥ 0, > 0 since W_φ ≠ 0)

**NOT** "Lemma 4.4 + Lemma 4.6(i)" — citation chain is §4.3(2) + §4.5(5) + §4.6(i).

**No numerical computation required** for positivity (only for the constant c_Q).

## F-2B

**Computed**: No — the Euler factor extraction is still [OBL].

**Witness**: Will require explicit computation of:
- Archimedean factor Z_∞(1) = 2^{1-k}π^{-(k+1)}Γ(k) (formula correct, derivation [OBL])
- Ramified factors Z_p(1) for each p | N_π **[BLOCKER]**
- Product formula L(s, π × π̃) = ζ(s) · L(s, π, Ad) (correct for unramified)

## F-2C

**Computed**: No — the uniformity bound is still [OBL].

**Witness**: Will require explicit computation of:
- Local corrections Z_v(1) for all places v
- Quantitative bounds |Z_v(1)| ≥ c_v > 0 for each local type
- Product bound C(F_{N_0}) = min_{f ∈ F_{N_0}} ∏_p |Z_p(1;f)| > 0

**NOT** "min over N ≤ N₀" — the minimum is over the complete target family
of forms, not over level integers.
