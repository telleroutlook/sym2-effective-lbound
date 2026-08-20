# M-1: Mollifier Construction — Proof v3

## Step A: Canonical exact-reciprocal mollifier

Define the reciprocal coefficients by:

    L(s, Π)⁻¹ = Σ_{n≥1} ρ_Π(n) n^{-s},    Re s > 1

For SL₂(Z) (level one, all primes unramified), the local inverse is:

    L_p(s, Π)⁻¹ = 1 - A_Π(p) p^{-s} + A_Π(p) p^{-2s} - p^{-3s}

where A_Π(p) = a_Π(p) is the Hecke eigenvalue of Π at p. The three-term
structure (with e₁ = e₂ = A_Π(p), e₃ = 1) comes from the symmetric-square
Satake parameters α², 1, α⁻² with product 1.

Set:

    M_X(s) = Σ_{m≤X} ρ_Π(m) P(log(X/m) / log X) m^{-s}

where P is a smooth cutoff with P(1) = 1, P(u) = 0 for u < 0, and X = T^θ.

**Why the exact reciprocal (canonical choice)**: The original used μ(n)a_Π(n)
as mollifier coefficients. This is wrong because:

    Σ_{p² | m} μ(m) a_Π(m) m^{-s} L(s,Π) ≡ 0

since μ(m) = 0 whenever p² | m. So the "squarefree approximation error"
is IDENTICALLY ZERO — it measures nothing.

The true difference between exact reciprocal and squarefree proxy is:

    D_X(s) = Σ_{n≤X} (ρ_Π(n) - μ(n)a_Π(n)) P(...) n^{-s}

This measures the coefficient-level difference between the two — it is
NONZERO precisely for n with p² | n (but NOT every such n: the reciprocal
local polynomial terminates at p³, so p⁴ terms may vanish on both sides,
and certain A_Π(p) values may cause additional cancellation). A genuine
approximation lemma must bound this D_X(s).

**Note:** The exact reciprocal mollifier is a canonical natural choice, but
NOT the only possible mollifier. Squarefree mollifiers, optimized Dirichlet
polynomials, and Selberg/Levinson type mollifiers are also legitimate
research objects. The original v2 error was the algebraically vacuous
"squarefree approximation" sum, not the choice of mollifier type itself.

**Status**: The true reciprocal coefficients ρ_Π(n) are computable
[THM]. The truncated mollifier M_X(s) is well-defined [THM].
The approximation lemma bounding D_X is [OBL].

## Step B: Exact mollified moment identity

For any mollifier coefficients b_m:

    I(T) = Σ_{m,n≤X} (b_m b̄_n / √(mn)) · J_{m,n}(T)

where:

    J_{m,n}(T) = ∫_T^{2T} (n/m)^{it} |L(½+it, Π)|² dt

This is the FIRST LOAD-BEARING IDENTITY of the proof. The factor (n/m)^{it}
cannot be dropped — it is the entire reason mollifier analysis is nontrivial.

## Step C: Diagonal/off-diagonal — but NOT "m = n dominates"

Split I(T) = I_{m=n} + I_{m≠n}:

- **Diagonal** (m = n): J_{m,m}(T) = ∫_T^{2T} |L(½+it,Π)|² dt
- **Off-diagonal** (m ≠ n): J_{m,n}(T) involves the oscillatory factor (n/m)^{it}

**CRITICAL**: The diagonal CANNOT simply be declared the main term with
I_{m≠n} = O(T^{1-δ}). The entire purpose of a reciprocal mollifier is to
produce massive cancellation between the two AFE halves, making M·L ≈ 1.
If M = L⁻¹ exactly, then I(T) = T with ALL contributions canceling.

Therefore the diagonal/off-diagonal split is a bookkeeping device, not a
size separation. The true main term must emerge from the FULL double sum
after exploiting the arithmetic of the mollifier coefficients b_m and their
interaction with a_Π(n) via the AFE.

## Step D: AFE-based reduction — 4 blocks, NOT a single quadratic form

Insert the approximate functional equation for L(½+it, Π):

    L(½+it, Π) = A(½+it) + X_Π(½+it) · B(½+it)

where:

    A(s) = Σ_{r ≤ T^{3/2}} a_Π(r) r^{-s} V_t(r/T^{3/2})
    B(s) = Σ_{s ≤ T^{3/2}} ā_Π(s) s^{s-1} V_t^*(s/T^{3/2})

with V_t, V_t^* t-dependent smooth cut-offs (NOT fixed constants),
and X_Π(s) = N^{1-2s} · L_∞(Π, 1-s) / L_∞(Π, s) is the t-dependent
functional-equation factor (NOT a constant root number).

Then |M · L|² = |M · (A + X·B)|² expands into FOUR blocks:

    |M·L|² = |M·A|² + |M·X·B|² + M·A·X̄·B̄ + M̄·Ā·X·B

= I_{++} + I_{--} + I_{+-} + I_{-+}

Each block has:
- Different weight functions (V_t from A, V_t^* from B, none from M)
- The t-dependent gamma phase X_Π(t) appears in I_{+-}, I_{-+} and I_{--}
- The convolution structure is ns ≈ mr (4 variables), not r ≈ s (2 variables)

The single-sum "c_X(q) c̄_X(q')" formula in v2 described at most ONE of
these blocks (approximately I_{++}), NOT the complete I(T). The cross
terms I_{+-}, I_{-+} and the dual block I_{--} each have different
convolution structures and weight functions.

**This is the core reason D is [OBL]:** the 4-block decomposition with
weights, gamma phases, and distinct convolution structures must ALL be
analyzed simultaneously. The v2 single-formula reduction was incomplete.

## Step E: What must be proved [OBL]

The required analytic estimate is:

    I(T) = C_{Π,θ} · T + O(T^{1-δ})

where C_{Π,θ} > 0 is determined by the arithmetic of {b_m} and {a_Π(n)}.

### Coefficient bound (corrected scale)

For the diagonal block I_{++}, the relevant quantity is the WEIGHTED
convolution coefficient sum:

    Σ_{q ≈ Q} |c_X(q)|² / q ≪ Q^ε    (weighted)

NOT the unweighted sum Σ|c_X(q)|² ≪ Q^ε, which would be a factor of Q
too small (since c_X(q) ≈ a_Π(q) for prime q > X, the unweighted sum
grows like Q^{1+ε}).

### Shift geometry (corrected scale)

The shift scale depends on the convolution length Q:

    Q ≈ X · T^{3/2} = T^{3/2+θ}

The near-diagonal condition q' ≈ q with |q'-q| ≲ Q/T gives:

    H ≲ T^{1/2+θ}

This is LARGER than the unmollified shift h ≲ T^{1/2} by the factor T^θ.
Mollification expands the shifted-convolution geometry, not just adds
short coefficients to an unmollified moment.

**This is at the GL₃ second-moment research frontier.** Current best
results (DLY 2024: T^{4/3+ε} upper bound for unmollified; Pal IMRN 2025:
T^{3/2-3/32+ε}) do not achieve the power-saving asymptotic needed here.
The CKLT2026 result (PGL₃ Dirichlet-twist family) does not specialize
to fixed Π, t-aspect.

## Step F: Explicit constants (last step, after analytic proof)

Only AFTER the analytic proof is complete:
- Compute C_{Π,θ} from the diagonal arithmetic
- Optimize θ (mollifier length exponent)
- Determine δ (power-saving exponent)

## Status: [OBL]

Steps A–C are [THM] (standard algebraic setup).
Steps D–E are [OBL] — the core GL₃ twisted moment estimate.
Step F is [OBL] — downstream computation.
