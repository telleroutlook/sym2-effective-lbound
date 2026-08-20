# M-1: Mollifier Construction — Proof

## Step A: Mollifier definition

### Option 1: True reciprocal mollifier

Define the reciprocal coefficients by:

    L(s, Π)⁻¹ = Σ_{n≥1} ρ_Π(n) n^{-s},    Re s > 1

For unramified primes with Satake parameters γ₁, γ₂, γ₃:

    L_p(s, Π)⁻¹ = 1 - e₁ p^{-s} + e₂ p^{-2s} - e₃ p^{-3s}

where e₁ = A_Π(p), e₂ = A_Π(p) (for trivial central char), e₃ = 1.

Set:

    M_X(s) = Σ_n ρ_Π(n) P(log(X/n) / log X) n^{-s}

where P is a smooth cutoff with P(1) = 1, P(u) = 0 for u < 0.

### Option 2: Squarefree proxy (requires approximation lemma)

If using μ(n)a_Π(n), must prove:

    |Σ_{p² | m} μ(m)a_Π(m) m^{-s} L(s,Π)| ≤ ε · Σ_{n≤X} |a_Π(n)| n^{-Re s}

uniformly in the relevant region. This is the Squarefree Approximation Lemma,
currently [OBL].

## Step B: Exact mollified moment identity

For any mollifier coefficients b_m:

    I(T) = Σ_{m,n≤X} (b_m b̄_n / √(mn)) · J_{m,n}(T)

where:

    J_{m,n}(T) = ∫_T^{2T} (n/m)^{it} |L(½+it, Π)|² dt

This is the FIRST LOAD-BEARING IDENTITY of the proof. The factor (n/m)^{it}
cannot be dropped.

## Step C: Diagonal and off-diagonal decomposition

Split I(T) = I_diag + I_off:

- **Diagonal** (m = n): J_{m,m}(T) = ∫_T^{2T} |L(½+it,Π)|² dt
- **Off-diagonal** (m ≠ n): J_{m,n}(T) involves the oscillatory factor (n/m)^{it}

The diagonal gives the main term. The off-diagonal must be bounded.

## Step D: AFE-based reduction

Insert the approximate functional equation for L(½+it, Π):

    L(½+it, Π) = Σ_{n ≤ T^{3/2}} a_Π(n) n^{-½-it} + χ(Π) Σ_{n ≤ T^{3/2}} ā_Π(n) n^{-½+it}

Then |L|² expands into:
- Diagonal terms: n = m
- Near-diagonal terms: |n - m| ≲ T^{1/2}
- Shifted convolution terms: general m, n

The core analytic estimate is:

    Σ_{|h| ≤ T^{1/2}} |Σ_n a_Π(n) ā_Π(n+h) / √(n(n+h))| ≪ T^{1-δ}

This is a GL₃ shifted-convolution sum, currently at the research frontier.

## Step E: Error control

After establishing the diagonal main term and off-diagonal bounds:

    I(T) = A_Π T log T + B_Π T + O(T^{1-δ})

where A_Π > 0 (by positivity of |a_Π(n)|² and the log growth).

The mollifier coefficients b_m are chosen to maximize A_Π while keeping
the off-diagonal error manageable.

## Step F: Explicit constants (last step)

Only AFTER the analytic proof is complete:
- Compute A_Π, B_Π explicitly
- Optimize θ (mollifier length exponent)
- Determine δ (power-saving exponent)
- Compute c₀, T₀

## Status: [OBL]

The core analytic lemma (Step D) is the main obstruction. The tools needed
(delta method, Voronoi, conductor lowering) are known but the specific GL₃
twisted moment estimate for fixed Π is not yet proved.
