# M-1: Mollifier Construction — Proof v2

## Step A: True reciprocal mollifier (only option)

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

**Why NOT the squarefree proxy**: The original used μ(n)a_Π(n) as mollifier
coefficients. This is wrong because:

    Σ_{p² | m} μ(m) a_Π(m) m^{-s} L(s,Π) ≡ 0

since μ(m) = 0 whenever p² | m. So the "squarefree approximation error"
is IDENTICALLY ZERO — it measures nothing. The true error from truncating
the reciprocal series is:

    D_X(s) = Σ_{n≤X} (ρ_Π(n) - μ(n)a_Π(n)) P(...) n^{-s}

which is nonzero precisely for n with p² | n or p³ | n. A genuine
approximation lemma must bound this D_X(s), not the trivially-zero sum.

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

## Step D: AFE-based reduction — 4-variable structure

Insert the approximate functional equation for L(½+it, Π):

    L(½+it, Π) = Σ_{r ≤ T^{3/2}} a_Π(r) r^{-½-it} V_t(r/T^3)
                + X_Π(½+it) Σ_{s ≤ T^{3/2}} ā_Π(s) s^{-½+it} V_t^*(s/T^3)

where V_t, V_t^* are t-dependent smooth cut-offs (NOT fixed constants),
and X_Π(½+it) is the t-dependent functional-equation factor from the
gamma ratio:

    X_Π(s) = N^{1-2s} · L_∞(Π, 1-s) / L_∞(Π, s)

NOT a constant root number χ(Π). The factor has |X_Π| ≈ 1 but oscillates
rapidly in t.

Then |M · L|² expands into FOUR indices (m, n from mollifier; r, s from AFE):

    I(T) = Σ_{m,n,r,s} b_m b̄_n a_Π(r) ā_Π(s) / √(mn·rs)
           · ∫_T^{2T} (n·s / (m·r))^{it} dt

The true near-diagonal condition is:

    n · s ≈ m · r

NOT simply r ≈ s (unmollified) or m = n (diagonal). The convolution
structure is:

    c_X(q) = Σ_{mr = q, m ≤ X} b_m · a_Π(r)

and the moment becomes:

    I(T) = Σ_{q, q'} c_X(q) c̄_X(q') / √(qq') · ∫_T^{2T} (q'/q)^{it} dt

This is the CORRECT reduction. It has four indices coupled through the
convolution, not the two-index shifted convolution of the unmollified case.

## Step E: What must be proved [OBL]

The required analytic estimate is:

    I(T) = C_{Π,θ} · T + O(T^{1-δ})

where C_{Π,θ} > 0 is determined by the arithmetic of {b_m} and {a_Π(n)}.

For the error term, one needs bounds on the twisted moment:

    Σ_{q ≈ Q} |c_X(q)|² ≪ Q^{ε}    (convolution coefficient bound)

and the off-diagonal contribution from q ≠ q'. The relevant shift scale
is h ≪ T^{1/2} (from degree-3 AFE length T^{3/2} and time scale T).

**This is at the GL₃ second-moment research frontier.** Current best
results (DLY 2024: T^{4/3+ε} upper bound for unmollified; Pal 2025:
T^{3/2-3/32+ε}) do not achieve the power-saving asymptotic needed here.

## Step F: Explicit constants (last step, after analytic proof)

Only AFTER the analytic proof is complete:
- Compute C_{Π,θ} from the diagonal arithmetic
- Optimize θ (mollifier length exponent)
- Determine δ (power-saving exponent)

## Status: [OBL]

Steps A–C are [THM] (standard algebraic setup).
Steps D–E are [OBL] — the core GL₃ twisted moment estimate.
Step F is [OBL] — downstream computation.
