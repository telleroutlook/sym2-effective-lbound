# M-2: Mean Value Estimate — Proof

## Step 1: Approximate functional equation (NOT infinite Dirichlet series)

For Re s = ½, the Dirichlet series Σ a_Π(n) n^{-s} does NOT converge absolutely.
The correct starting point is the AFE:

    L(½+it, Π) = Σ_{n ≤ T^{3/2}} a_Π(n) n^{-½-it} ψ₁(n/T^{3/2})
                + χ(Π) Σ_{n ≤ T^{3/2}} ā_Π(n) n^{-½+it} ψ₂(n/T^{3/2})

where ψ₁, ψ₂ are smooth cut-offs and χ(Π) is the root number. The length
T^{3/2} comes from the degree d = 3 and the functional equation.

## Step 2: Square and integrate

|L(½+it, Π)|² = (diagonal) + (off-diagonal)

After inserting the AFE and integrating ∫_T^{2T}:

### Diagonal (main term)

    ∫_T^{2T} |L(½+it,Π)|² dt ≈ T · Σ_{n ≤ T^{3/2}} |a_Π(n)|²/n

The sum Σ |a_Π(n)|²/n is related to the Rankin–Selberg Dirichlet series:

    D_Π(s) = Σ_{n≥1} |a_Π(n)|² n^{-s}

which has a simple pole at s = 1 with residue R_Π > 0. Therefore:

    Σ_{n ≤ X} |a_Π(n)|²/n ~ R_Π log X

giving the diagonal contribution:

    T · R_Π · log(T^{3/2}) = (3/2) R_Π T log T + O(T)

This is why the leading term is T log T, NOT T.

### Off-diagonal (error)

The off-diagonal terms involve sums of the form:

    Σ_{m ≠ n} a_Π(m) ā_Π(n) / √(mn) · ∫_T^{2T} (n/m)^{it} dt

The t-integral gives bounds like min(T, 1/|log(n/m)|). After AFE truncation,
these become GL₃ shifted-convolution sums:

    Σ_{|h| ≲ T^{1/2}} |Σ_n a_Π(n) ā_Π(n+h) / √(n(n+h))|

which must be bounded by O(T^{1-δ}).

## Step 3: Identify D_Π(s) vs L(s, Π × Π̃)

The coefficient-square series D_Π(s) is NOT equal to the Rankin–Selberg
L-function L(s, Π × Π̃). The relationship is:

    D_Π(s) = L(s, Π × Π̃) · H_Π(s)

where H_Π(s) = Π_p H_{Π,p}(s) with local factors:

For unramified p (Satake parameters α₁, α₂, α₃):
    H_{Π,p}(s) = (1 - |α₁|² p^{-s})⁻¹ · (1 - |α₂|² p^{-s})⁻¹ · (1 - |α₃|² p^{-s})⁻¹

For trivial central character (|α₁ α₂ α₃| = 1), H_Π(s) is analytic and
nonzero at s = 1. Therefore:

    Res_{s=1} D_Π(s) = Res_{s=1} L(s, Π × Π̃) · H_Π(1)

and the leading constant is:

    A_Π = (3/2) · R_Π · (archimedean factor)

## Step 4: Archimedean factor (Iwaniec–Michel 2001)

For holomorphic weight k, the correct symmetric-square archimedean L-factor is:

    L_∞(sym² f, s) = π^{-3s/2} Γ((s+1)/2) Γ((s+k-1)/2) Γ((s+k)/2)

NOT a single K_{k-1} Bessel function. This must be used in the AFE weight
computation and in the diagonal residue.

## Step 5: Explicit constants (last step)

Only after the analytic proof is complete:
- Compute A_Π from Res_{s=1} D_Π(s) and archimedean factor
- Compute B_Π from lower-order terms
- Determine δ from the shifted-convolution bound
- Verify A_Π > 0

## Status: [OBL]

The power-saving off-diagonal estimate (shifted-convolution sum for fixed Π)
is the main obstruction. This is at the GL₃ second-moment research frontier.
