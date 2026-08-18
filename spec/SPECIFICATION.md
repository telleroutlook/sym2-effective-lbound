# Effective Lower Bounds for L(1, sym^2 f): Mathematical Specification

**Document type:** authoritative mathematical specification
**Scope:** symmetric square L-functions of primitive holomorphic Hecke eigenforms over Q
**Completion state:** F-1 [THM]; F-2, F-3, mollifier, and explicit-constant layers [OBL]

---

## 0. Logical Contract

### 0.1 Status Grammar

| Status | Meaning | Logical use |
|--------|---------|-------------|
| [DEF]  | Definition fixed by this document | May be unfolded |
| [BASE] | Standard theorem admitted as foundation | Usable with stated hypotheses |
| [THM]  | Theorem proved in this document | Usable downstream |
| [OBL]  | Proof still required | May not be used as a theorem |
| [OUT]  | Deliberately outside the certified profile | No downstream force |

### 0.2 Module Dependency

    M0 foundations
      +-> M1 local factors [THM] (proof/01)
            +-> M1 global residue [OBL] (proof/02)
            +-> M2 mollifier construction     (proof/03)            [OBL]
                  +-> M3 zero-free region     (proof/04 pt1-2)      [OBL]
                        +-> M4 explicit bound (proof/04 pt3)        [OBL]

---

## 1. Mathematical Objects

### 1.1 Holomorphic Hecke Eigenforms

[DEF] A normalized primitive holomorphic Hecke eigenform of weight k, level N, trivial
nebentypus is f in S_k(N) with Hecke eigenvalues a_f(n), a_f(1)=1, a newform.
Fourier expansion: f(z) = sum_{n>=1} a_f(n) e^{2pi i n z}.

[DEF] The normalized Satake parameters at p not dividing N:
  alpha_p + beta_p = a_f(p) p^{-(k-1)/2},   alpha_p * beta_p = 1

### 1.2 Symmetric Square L-Function

[DEF] The symmetric square L-function (degree 3):
  L(s, sym^2 f) = prod_{p not | N} [(1-alpha_p^2 p^{-s})(1-p^{-s})(1-beta_p^2 p^{-s})]^{-1}
                  * prod_{p | N} L_p^ram(s)^{-1}
converging absolutely for Re(s) > 1.

For trivial central character, L(s, sym^2 f) = L(s, f, Ad) (the adjoint L-function).

### 1.3 Rankin-Selberg L-Function

[DEF] L(s, f x fbar) = zeta(s) * L(s, sym^2 f),
arising from the dual group decomposition std (x) std^v = 1 + Ad.

For the Ramanujan Delta function, the Fourier-coefficient normalization used in
the computations satisfies the separate identity

    sum_n tau(n)^2 / n^{11+s} = [zeta(s)/zeta(2s)] * L(s, sym^2 Delta).

The factor zeta(2s)^{-1} is not optional: it comes from the local factor 1+x in
the squared spherical Whittaker series.  The earlier identity without this
denominator led to the retracted F-3 estimate below.

---

## 2. Foundation Theorems

### 2.1 Local Euler Factor Factorization

[BASE] (Casselman-Shalika formula) For unramified pi_v with parameters (a_v, b_v),
a_v * b_v = 1:
  W_{f,v}(diag(varpi_v^l, 1)) = q_v^{-l/2} chi_l(a_v, b_v)
where chi_l(a,b) = (a^{l+1} - b^{l+1})/(a-b) is the SU(2) character.
Source: Casselman-Shalika (1980), Compositio Math. 41, Theorem 5.4, p. 227,
with the GL(2) essential-vector transcription in Jacquet-Shalika (1981),
Section 2.2, p. 511.

[BASE] (Clebsch-Gordan for SU(2)) chi_l^2 = sum_{j=0}^l chi_{2j}, hence:
  sum_{j>=0} chi_{2j}(a,b) x^j = (1+x) / [(1-a^2 x)(1-b^2 x)]  (ab=1)
  sum_{l>=0} chi_l(a,b)^2 x^l = (1+x) / [(1-x)(1-a^2 x)(1-b^2 x)]

[THM] (F-1) [proved in proof/01-foundations.tex]
For unramified v with a_v * b_v = 1 and Phi_v = char(O_v^2):
  I_v(s) = 1 / [(1-q_v^{-s})^2 (1-a_v^2 q_v^{-s})(1-b_v^2 q_v^{-s})]
         = zeta_v(s) * L_v(s, pi_v, Ad)
The (1 + q_v^{-s}) factor cancels exactly via Clebsch-Gordan.

### 2.2 Global Residue Positivity

[BASE] (Jacquet-Shalika 1981, Proposition 2.3, pp. 511-512)
For generic unramified local data and the measure normalization
vol(N_v A_v K_v)=vol(K_v)=1, the local Jacquet-Shalika integral with essential
Whittaker functions equals L_v(s, pi_v x pi_v~).

[BASE] (Jacquet-Shalika 1981, Lemma 4.6, pp. 550-552)
The global pure-tensor Whittaker integral is meromorphic and has a simple pole
at s=1 for pi' = pi~ and nonzero global test data.  This source does not give
the explicit positive local correction factors required below.

[BASE] (Analytic Class Number Formula)
  Res_{s=1} zeta_F(s) = 2^{r1} (2pi)^{r2} h_F R_F / (w_F sqrt|D_F|) > 0.

[OBL] (Adjoint value) L(1, f, Ad) > 0 for the intended class of pi.
  Baseline audit note: the exact adjoint statement is currently `not-found` in
  baseline/REFERENCE_BASELINE.md.  Either a primary theorem or a complete bridge
  from the pair L-function / Jacquet-Shalika pole to the adjoint factor must be
  supplied before this input is used.

[OBL] (F-2) [open in proof/02-global-residue.tex]
  Res_{s=1} <1, T^JS_{s,Phi}[W_f (x) W_fbar]>
  = Phihat(0) * Res_{s=1} zeta_F(s) * L(1, pi, Ad) * ||W_f||^2 > 0
Required additionally: compute every bad local correction, prove its sign and
normalization, and prove the adjoint-value obligation above.

### 2.3 Instance Certification [OBL]

[OBL] (F-3) Instance certification at s=1
For Delta in S_{12}(SL_2(Z)) (Ramanujan delta function, N=1), prove a certified
interval [L_lo, L_hi] for L(1, sym^2 Delta) using Arb interval arithmetic.

Discovery computations consistently indicate that L(1, sym^2 Delta) is close to
0.631793.  They do not certify this value.  The earlier claimed interval
[2.405, 2.407] is retracted: it used the wrong zeta(2s)^{-1} normalization and
an incorrect tabulated value of tau(47).  No positive lower bound for
L(1, sym^2 Delta) is currently available from this repository.

---

## 3. Proof Obligations [OBL]

### 3.1 Mollifier Construction [OBL]

Goal: M(s) = sum_{n <= X} mu(n) a_{sym^2}(n) n^{-s}  (X = N^theta, theta to optimize)
such that int_T^{2T} |M(1/2+it) L(1/2+it, sym^2 f)|^2 dt >> T.
Requires: GL3 Rankin-Selberg mean value, Hecke multiplicativity, large sieve on GL3.

### 3.2 Zero-Free Region [OBL]

Goal: Explicit delta(N) > 0 with L(s, sym^2 f) != 0 for Re(s) > 1 - delta(N).
Requires: Hadamard product for L(s, sym^2 f), explicit analytic conductor bounds.

### 3.3 Explicit Lower Bound [OBL] -- The Core Research Gap

Goal (Main Theorem): For all normalized primitive f of prime level p:
  L(1, sym^2 f) >= c_eff / log p
with explicit, computable c_eff > 0.

Proof strategy (Goldfeld-Hoffstein-Lieman):
  Case 1 (no Siegel zero): zero-free region => contour integral =>
    L(1, sym^2 f) >= c_1 / log p with c_1 explicit in terms of the zero-free radius.
  Case 2 (exceptional zero): pointwise positivity F-2 does not exclude it;
    a quantitative derivative/log-derivative bound is required [OBL].

The gap: extracting c_1 requires tracing explicit constants through the zero-free region
estimate and the contour integral. This is the core research contribution.

---

## 4. Out of Scope [OUT]

[OUT] Generalized Riemann Hypothesis for L(s, sym^2 f).
[OUT] Sublogarithmic improvement L(1, sym^2 f) >> (log N)^{-(1-delta)} unconditionally.
[OUT] Ramanujan conjecture |alpha_p| = 1 (used only in discovery/).
[OUT] Higher symmetric powers (sym^3, sym^4, ...).

---

## 5. Certificate Structure

A bound certificate for L(1, sym^2 f) >= L_0:

    {
      "form": {
        "weight": k,
        "level": N,
        "label": "...",
        "hecke_coefficients": [a(1), ..., a(P)]
      },
      "bound": L_0,
      "euler_product_cutoff": P,
      "tail_bound": { "method": "rankin-selberg", "exponent": -1.0, "constant": C },
      "euler_product_interval": [lower, upper],
      "arb_precision_bits": 128,
      "checker_version": "1.0.0"
    }

checker/check_bound.py is an independent rejection gate.  At present no proof-tier
Euler-product tail estimate at s=1 has been admitted, so it must reject the former
"3/P" Ramanujan-Deligne tail (sum_{p>P} 3/p diverges) rather than report a PASS.
When E-2 supplies a real certificate, the checker must recompute its finite data
and interval enclosure from independently generated exact inputs.
