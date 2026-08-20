# M-2: Mean Value Estimate — Proof v2

## Step 1: Approximate functional equation (correct form)

For Re s = ½, the Dirichlet series Σ a_Π(n) n^{-s} does NOT converge absolutely.
The correct starting point is the AFE with t-dependent dual factor:

    L(½+it, Π) = Σ_{r ≤ T^{3/2}} a_Π(r) r^{-½-it} V_t(r/T^3)
                + X_Π(½+it) Σ_{s ≤ T^{3/2}} ā_Π(s) s^{-½+it} V_t^*(s/T^3)

where V_t, V_t^* are t-dependent smooth cut-offs, and X_Π(s) is the
functional-equation factor:

    X_Π(s) = N^{1-2s} · L_∞(Π, 1-s) / L_∞(Π, s)

For level one (N=1):

    X_Π(s) = L_∞(Π, 1-s) / L_∞(Π, s)

where the archimedean L-factor (Iwaniec–Michel 2001, formula 2.22) is:

    L_∞(sym² f, s) = π^{-3s/2} Γ((s+1)/2) Γ((s+k-1)/2) Γ((s+k)/2)

**CRITICAL**: X_Π(½+it) is NOT a constant root number χ(Π). It has
|X_Π(½+it)| ≈ 1 but oscillates rapidly in t through the gamma ratios.
The global sign for level-one symmetric-square is +1, but this does NOT
eliminate the t-dependent phase.

## Step 2: Square and integrate — diagonal main term

|L(½+it, Π)|² = (diagonal) + (off-diagonal)

After inserting the AFE and integrating ∫_T^{2T}:

### Diagonal from each AFE half

Each half (primary and dual) contributes:

    T · Σ_{n ≤ T^{3/2}} |a_Π(n)|²/n

The sum Σ |a_Π(n)|²/n is related to the Rankin–Selberg Dirichlet series:

    D_Π(s) = Σ_{n≥1} |a_Π(n)|² n^{-s}

which has a simple pole at s = 1 with residue R_Π > 0. Therefore:

    Σ_{n ≤ X} |a_Π(n)|²/n ~ R_Π log X

Each half gives diagonal contribution: R_Π · log(T^{3/2}) = (3/2) R_Π log T.

### Both halves together

Since the AFE has TWO halves (primary + dual), the total diagonal is:

    2 × (3/2) R_Π T log T = 3 R_Π T log T + O(T)

**Therefore the leading constant is A_Π = 3R_Π, NOT (3/2)R_Π.**

The original missed this factor of 2 by only counting one AFE half.

## Step 3: Local Euler correction H_{Π,p}

The coefficient-square series D_Π(s) is NOT equal to the Rankin–Selberg
L-function L(s, Π × Π̃). The relationship is:

    D_Π(s) = L(s, Π × Π̃) · H_Π(s)

where H_Π(s) = Π_p H_{Π,p}(s).

**Wrong formula** (v1): H_{Π,p}(x) = Π_i (1 - |α_i|²x)⁻¹

This gives 1 + 3x + O(x²), contradicting the necessary condition
H_{Π,p}(x) = 1 + O(x²) (since D_{Π,p} and L_p(Π×Π̃) agree at order x¹).

**Correct formula** for level-one symmetric-square with Satake parameters
z = α², 1, z⁻¹ and A_p = z + 1 + z⁻¹:

    H_{Π,p}(x) = 1 - A_p² x² + 2(A_p² - 1) x³ - A_p² x⁴ + x⁶

Verification: H_{Π,p}(0) = 1 ✓, coefficient of x is 0 ✓ (matches 1+O(x²)).

Since |A_p| ≤ 3 (Deligne), the product Π_p H_{Π,p}(p^{-s}) converges
absolutely for Re s > ½, so H_Π(s) is analytic and nonzero at s = 1.

Therefore:

    Res_{s=1} D_Π(s) = Res_{s=1} L(s, Π × Π̃) · H_Π(1) = R_Π

and the leading constant is:

    A_Π = 3 · R_Π

(Three, from two AFE halves × (3/2) from the log coefficient.)

## Step 4: Off-diagonal (error) [OBL]

The off-diagonal terms involve:

    Σ_{m ≠ n} a_Π(m) ā_Π(n) / √(mn) · ∫_T^{2T} (n/m)^{it} dt

After AFE truncation, the critical shift scale is h ≪ T^{1/2}
(from degree-3 AFE length T^{3/2} and time scale T).

The off-diagonal must be bounded by O(T^{1-δ}).

This is a GL₃ shifted-convolution sum for fixed Π, at the research frontier.

## Step 5: Archimedean factor [THM]

For holomorphic weight k, the correct symmetric-square archimedean L-factor
(Iwaniec–Michel 2001, formula 2.22):

    L_∞(sym² f, s) = π^{-3s/2} Γ((s+1)/2) Γ((s+k-1)/2) Γ((s+k)/2)

This is correct in v1 and v2. It must be used in the AFE weight computation.

## Step 6: Explicit constants (last step)

Only after the analytic proof is complete:
- Compute A_Π = 3R_Π from the Rankin–Selberg residue
- Compute B_Π from lower-order terms (including H_Π(1), archimedean constants)
- Determine δ from the shifted-convolution bound
- Verify A_Π > 0

## Status: [OBL]

Steps 1–3, 5 are [THM] (standard algebra/known formulas).
Step 4 is [OBL] (GL₃ shifted-convolution research frontier).
Step 6 is [OBL] (downstream computation).
