# M-1: Mollifier Construction — Proof v4

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

**Status**: The true reciprocal coefficients ρ_Π(n) are computable [THM].
The truncated mollifier M_X(s) is well-defined [THM].

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

where (sum variable is r, NOT s — to avoid collision with the complex variable):

    A(s) = Σ_{r ≤ T^{3/2}} a_Π(r) r^{-s} V_t(r/T^{3/2})
    B(s) = Σ_{r ≤ T^{3/2}} ā_Π(r) r^{s-1} V_t^*(r/T^{3/2})

with V_t, V_t^* t-dependent smooth cut-offs.

**Functional-equation factor (corrected normalization):**

With arithmetic conductor q_Π and standard completed L-function
Λ(s, Π) = q_Π^{s/2} L_∞(s, Π) L(s, Π):

    X_Π(s) = ε_Π · q_Π^{1/2-s} · L_∞(1-s, π̃) / L_∞(s, Π)

where ε_Π is the root number (|ε_Π| = 1). For level one (q_Π = 1):

    X_Π(s) = ε_Π · L_∞(1-s, π̃) / L_∞(s, Π)

**On the critical line** s = ½+it: |X_Π(½+it)| = 1 (unitary functional equation).

Then |M · L|² = |M · (A + X·B)|² expands into FOUR blocks:

    |M·L|² = |M·A|² + |M·X·B|² + M·A·X̄·B̄ + M̄·Ā·X·B

= I_{++} + I_{--} + I_{+-} + I_{-+}

Each block has:
- Different weight functions (V_t from A, V_t^* from B, none from M)
- The convolution structure is 4-variable: ns ≈ mr

**Gamma-phase analysis (corrected per reviewer verdict 2026-08-20):**

Since |X_Π(½+it)| = 1 on the critical line:

- **I_{++}** = |M·A|²: no gamma phase at all
- **I_{--}** = |M·X·B|² = |M|²·|B|²: the phase |X|² = 1 cancels; NO gamma oscillation
- **I_{+-}** = M·A·X̄·B̄: gamma phase X̄(t) present → oscillatory
- **I_{-+}** = M̄·Ā·X·B: gamma phase X(t) present → oscillatory

Therefore **the t-dependent gamma oscillation is concentrated in the TWO
CROSS BLOCKS I_{+-} and I_{-+}**, not in all three non-diagonal blocks.
The reviewer correctly identified that I_{--} has no gamma phase.

The single-sum "c_X(q) c̄_X(q')" formula in v2 described at most ONE of
these blocks (approximately I_{++}), NOT the complete I(T). The cross
terms I_{+-}, I_{-+} each have different convolution structures, weight
functions, and gamma-phase oscillation.

**This is the core reason D is [OBL]:** the 4-block decomposition with
weights, gamma phases, and distinct convolution structures must ALL be
analyzed simultaneously. In particular, the two cross blocks require
gamma-phase stationary-phase analysis that determines the stationary
locus — this is different from the near-diagonal geometry of I_{++}.

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
upper bounds (DLY 2024: T^{4/3+ε}; Pal IMRN 2025: T^{3/2-3/32+ε})
do not achieve the power-saving asymptotic needed here. These are
UPPER BOUND results for related (but not identical) problems — they
do not directly solve the fixed-Π t-aspect mollified moment.

### Cross-block gamma-phase analysis [OBL]

The two cross blocks I_{+-}, I_{-+} involve the gamma oscillation of
X_Π(t). The stationary-phase geometry of these blocks is DIFFERENT from
the near-diagonal geometry of I_{++}. This is [OBL].

## Step F: Explicit constants (last step, after analytic proof)

Only AFTER the analytic proof is complete:
- Compute C_{Π,θ} from the diagonal arithmetic
- Optimize θ (mollifier length exponent)
- Determine δ (power-saving exponent)

## Status: [OBL]

Steps A–C are [THM] (standard algebraic setup).
Steps D–E are [OBL] — the core GL₃ twisted moment estimate.
Step F is [OBL] — downstream computation.
