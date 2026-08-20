# M-2: Mean Value Estimate — Proof v3

## Step 1: Approximate functional equation (smooth form)

For Re s = ½, the Dirichlet series Σ a_Π(n) n^{-s} does NOT converge absolutely.
The correct starting point is the smooth AFE with t-dependent dual factor:

    L(½+it, Π) = Σ_{n≥1} a_Π(n) n^{-½-it} W_t(n)
                + X_Π(½+it) Σ_{n≥1} ā_Π(n) n^{-½+it} W_t^*(n)

where W_t, W_t^* are t-dependent smooth cut-off functions satisfying:

    W_t(y) ≪ (1 + y/|t|^{3/2})^{-A}    for any A > 0

(with effective A depending on the number of derivatives used). The key
property is that W_t has effective support y ≪ |t|^{3/2}, so the dominant
contribution comes from n ≪ T^{3/2}.

**NOT a finite sum ≤ T^{3/2}:** The AFE is an identity for the full infinite
Dirichlet series with smooth weights. If truncated to n ≤ N, the truncation
error must be bounded:

    |L(½+it) - (truncated sums)| ≪ (N/|t|^{3/2})^{-A}

Choosing N = T^{3/2+ε} makes this O(T^{-B}) for any B.

The dual factor is:

    X_Π(s) = N^{1-2s} · L_∞(Π, 1-s) / L_∞(Π, s)

For level one (N=1):

    X_Π(s) = L_∞(Π, 1-s) / L_∞(Π, s)

where the archimedean L-factor (Iwaniec–Michel 2001, formula 2.22) is:

    L_∞(sym² f, s) = π^{-3s/2} Γ((s+1)/2) Γ((s+k-1)/2) Γ((s+k)/2)

**CRITICAL**: X_Π(½+it) is NOT a constant root number χ(Π). It has
|X_Π(½+it)| ≈ 1 but oscillates rapidly in t through the gamma ratios.

**Status [OBL]:** The smooth AFE identity itself is standard [THM, Iwaniec–
Kowalski §5.6]. However, the specific smooth weight W_t(y) with the above
decay property, and the explicit truncation error bound, require careful
verification for the symmetric-square case. This is standard but not
self-contained in this package.

## Step 2: Square and integrate — four terms, not two

Write L = S₁ + X·S₂ where:

    S₁ = Σ a_Π(r) r^{-½-it} W_t(r)
    S₂ = Σ ā_Π(s) s^{-½+it} W_t^*(s)

Then:

    |L|² = |S₁|² + |S₂|² + S₁·X̄·S̄₂ + S̄₁·X·S₂

= I_{++} + I_{--} + I_{+-} + I_{-+}

After integrating ∫_T^{2T} dt:

### I_{++} (primary diagonal + off-diagonal)

    I_{++} = ∫_T^{2T} |S₁|² dt
           = ∫_T^{2T} Σ_{r,r'} a_Π(r) ā_Π(r') (rr')^{-½} W_t(r) W_t(r') (r'/r)^{it} dt

Diagonal (r = r'): each gives T · Σ |a_Π(r)|²/r · W_t(r)² → R_Π · T · log T

### I_{--} (dual diagonal + off-diagonal)

Same structure as I_{++} with a_Π → ā_Π, giving another R_Π · T · log T.

### I_{+-} and I_{-+} (primary–dual cross terms)

These contain the t-dependent gamma phase X_Π(t):

    I_{+-} = ∫_T^{2T} S₁ · X̄_Π(t) · S̄₂ dt

**These cross terms MUST be shown to be o(T log T)** for the leading term
A_Π = 3R_Π to hold. If the cross terms contribute at the T log T level,
the leading constant would differ. This is [OBL].

### Total diagonal contribution

The diagonal parts of I_{++} and I_{--} together give:

    2 × (3/2) R_Π T log T = 3 R_Π T log T

**IF the cross terms I_{+-}, I_{-+} and the off-diagonal parts of I_{++}, I_{--}
are all o(T log T), then A_Π = 3R_Π.**

This is the CONDITIONAL status of the leading constant.

## Step 3: Local Euler correction H_{Π,p}

The coefficient-square series D_Π(s) = Σ |a_Π(n)|² n^{-s} is NOT equal to
the Rankin–Selberg L-function L(s, Π × Π̃). The relationship is:

    D_Π(s) = L(s, Π × Π̃) · H_Π(s)

where H_Π(s) = Π_p H_{Π,p}(s).

**Correct formula** for level-one symmetric-square with Satake parameters
z = α², 1, z⁻¹ and A_p = z + 1 + z⁻¹:

    H_{Π,p}(x) = 1 - A_p² x² + 2(A_p² - 1) x³ - A_p² x⁴ + x⁶

Verification: H_{Π,p}(0) = 1 ✓, coefficient of x is 0 ✓ (matches 1+O(x²)).

**H_{Π,p}(1/p) ≠ 0:** Since D_{Π,p}(x) > 0 for x > 0 (coefficient-square
series has nonneg coefficients) and L_p(Π×Π̃, x) > 0 for 0 < x < 1/p
(Rankin–Selberg local factor positivity), the quotient H_{Π,p}(x) =
D_{Π,p}(x)/L_p(Π×Π̃, x) is positive for 0 < x < 1/p. In particular
H_{Π,p}(1/p) > 0.

Since |A_p| ≤ 3 (Deligne), the product Π_p H_{Π,p}(p^{-s}) converges
absolutely for Re s > ½, so H_Π(s) is analytic and nonzero at s = 1.

Therefore:

    Res_{s=1} D_Π(s) = Res_{s=1} L(s, Π × Π̃) · H_Π(1) = R_Π

with H_Π(1) > 0.

## Step 4: Off-diagonal (error) [OBL]

The off-diagonal terms involve:

- Same-half shifted convolution: Σ_{r≠r'} a_Π(r) ā_Π(r') · kernel(r,r')
- Primary–dual cross terms: Σ_{r,s} a_Π(r) ā_Π(s) · X_Π(t) · kernel(r,s)

After AFE truncation, the critical shift scale is h ≪ T^{1/2}
(from degree-3 AFE length T^{3/2} and time scale T).

All off-diagonal contributions must be bounded by O(T^{1-δ}).

**This is a GL₃ shifted-convolution sum for fixed Π, at the research frontier.**

## Step 5: Archimedean factor [THM]

For holomorphic weight k, the correct symmetric-square archimedean L-factor
(Iwaniec–Michel 2001, formula 2.22):

    L_∞(sym² f, s) = π^{-3s/2} Γ((s+1)/2) Γ((s+k-1)/2) Γ((s+k)/2)

## Step 6: Explicit constants (last step)

Only after the analytic proof is complete:
- Compute A_Π = 3R_Π from the Rankin–Selberg residue (CONDITIONAL on cross terms)
- Compute B_Π from lower-order terms (including H_Π(1), archimedean constants)
- Determine δ from the shifted-convolution bound
- Verify A_Π > 0

## Status: [OBL]

Steps 1, 3, 5 are [THM] (standard algebra/known formulas).
Step 2 diagonal coefficient is [CONDITIONAL: 3R_Π if cross terms are o(T log T)].
Step 2 cross terms are [OBL].
Step 4 is [OBL] (GL₃ shifted-convolution research frontier).
Step 6 is [OBL] (downstream computation).
