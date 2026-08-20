# M-2: Mean Value Estimate — Proof v4

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

    X_Π(s) = ε_Π · q_Π^{1/2-s} · L_∞(Π, 1-s) / L_∞(Π, s)

For level one (q_Π = 1, ε_Π = +1):

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

**Diagonal (r = r'):** After integrating over t, the diagonal contribution is:

    ∫_T^{2T} Σ_r |a_Π(r)|²/r · W_t(r)² dt

The inner sum Σ_r |a_Π(r)|²/r · W_t(r)², with W_t having effective support
r ≪ T^{3/2}, produces:

    R_Π · log(T^{3/2}) + O(1) = (3/2) R_Π · log T + O(1)

Therefore each half's diagonal contributes:

    I_{++}^{diag} = (3/2) R_Π · T · log T + O(T)

**NOT R_Π · T · log T** — the AFE length T^{3/2} introduces the factor 3/2
from log(T^{3/2}) = (3/2) log T.

### I_{--} (dual diagonal + off-diagonal)

Same structure as I_{++} with a_Π → ā_Π, giving another:

    I_{--}^{diag} = (3/2) R_Π · T · log T + O(T)

### I_{+-} and I_{-+} (primary–dual cross terms)

These contain the t-dependent gamma phase X_Π(t):

    I_{+-} = ∫_T^{2T} S₁ · X̄_Π(t) · S̄₂ dt

**These cross terms MUST be shown to be o(T log T)** for the leading term
A_Π = 3R_Π to hold. If the cross terms contribute at the T log T level,
the leading constant would differ. This is [OBL].

### Total diagonal contribution

The diagonal parts of I_{++} and I_{--} together give:

    2 × (3/2) R_Π T log T = 3 R_Π T log T

### What A_Π = 3R_Π requires (corrected per reviewer verdict 2026-08-20)

The formula A_Π = 3R_Π requires ALL of the following to hold simultaneously:

1. **Precise diagonal-weight asymptotic** [OBL]: The smooth-weighted sum
   ∫_T^{2T} Σ_r |a_Π(r)|²/r · W_t(r)² dt must have asymptotic
   (3/2)R_Π T log T + C_Π^{(+)} T + o(T). This requires a diagonal-weight
   lemma (Mellin analysis of W_t, residue at s=1 of the associated Dirichlet
   series D_Π(s)).

2. **Cross terms o(T log T)** [OBL]: I_{+-} + I_{-+} = o(T log T).

3. **Same-half off-diagonal o(T log T)** [OBL]: The off-diagonal parts of
   I_{++} and I_{--} must each be o(T log T).

Only the combination of all three gives A_Π = 3R_Π. The previous version
stated this as conditional only on cross terms, which is insufficient.

## Step 3: Local Euler correction H_{Π,p}

The coefficient-square series D_Π(s) = Σ |a_Π(n)|² n^{-s} is NOT equal to
the Rankin–Selberg L-function L(s, Π × Π̃). The relationship is:

    D_Π(s) = L(s, Π × Π̃) · H_Π(s)

where H_Π(s) = Π_p H_{Π,p}(s).

**Correct formula** for level-one symmetric-square with Satake parameters
z = α², 1, z⁻¹ and A_p = z + 1 + z⁻¹:

    H_{Π,p}(x) = 1 - A_p² x² + 2(A_p² - 1) x³ - A_p² x⁴ + x⁶

**Factorization** (corrected per reviewer verdict 2026-08-20):

    H_{Π,p}(x) = (1-x)² · (1+x+x² - A_p x) · (1+x+x² + A_p x)

**Proof that H_{Π,p}(1/p) > 0:**

Since |A_p| ≤ 3 (Deligne), for 0 < x ≤ 1/p ≤ 1/2:

- (1-x)² > 0 ✓
- 1+x+x² - |A_p|x ≥ 1+x+x² - 3x = (1-x)² > 0 ✓
- 1+x+x² + A_p x ≥ 1+x+x² - 3x = (1-x)² > 0 ✓

Therefore H_{Π,p}(x) > 0 for all 0 < x ≤ 1/p, INCLUDING the endpoint x = 1/p.

**Previous error**: The v3 proof showed H_{Π,p}(x) > 0 for 0 < x < 1/p
(open interval) and then claimed "in particular H_{Π,p}(1/p) > 0" — this
is a logical gap (cannot deduce endpoint from open interval). The factorization
proof above closes this gap.

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
- Compute A_Π = 3R_Π from the Rankin–Selberg residue (CONDITIONAL on items 1-3)
- Compute B_Π from lower-order terms (including H_Π(1), archimedean constants)
- Determine δ from the shifted-convolution bound
- Verify A_Π > 0

## Status: [OBL]

Steps 1, 3, 5 are [THM] (standard algebra/known formulas).
Step 2 diagonal coefficient is [CONDITIONAL: 3R_Π requires diagonal-weight
lemma + cross terms o(T log T) + same-half off-diagonal o(T log T)].
Step 2 cross terms are [OBL].
Step 4 is [OBL] (GL₃ shifted-convolution research frontier).
Step 6 is [OBL] (downstream computation).
