# Effective Lower Bounds for L(1, sym^2 f): Mathematical Specification

**Document type:** authoritative mathematical specification
**Scope:** symmetric square L-functions of primitive holomorphic Hecke eigenforms over Q
**Completion state:** foundation layer [THM]; mollifier and explicit-constant layers [OBL]

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
      +-> M1 local factors + global residue  (proof/01, proof/02)  [THM]
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

---

## 2. Foundation Theorems [THM]

### 2.1 Local Euler Factor Factorization

[BASE] (Casselman-Shalika formula) For unramified pi_v with parameters (a_v, b_v),
a_v * b_v = 1:
  W_{f,v}(diag(varpi_v^l, 1)) = q_v^{-l/2} chi_l(a_v, b_v)
where chi_l(a,b) = (a^{l+1} - b^{l+1})/(a-b) is the SU(2) character.
Source: Casselman-Shalika (1980), Compositio Math.

[BASE] (Clebsch-Gordan for SU(2)) chi_l^2 = sum_{j=0}^l chi_{2j}, hence:
  sum_{j>=0} chi_{2j}(a,b) x^j = (1+x) / [(1-a^2 x)(1-b^2 x)]  (ab=1)
  sum_{l>=0} chi_l(a,b)^2 x^l = (1+x) / [(1-x)(1-a^2 x)(1-b^2 x)]

[THM] (F-1) [proved in proof/01-foundations.tex]
For unramified v with a_v * b_v = 1 and Phi_v = char(O_v^2):
  I_v(s) = 1 / [(1-q_v^{-s})^2 (1-a_v^2 q_v^{-s})(1-b_v^2 q_v^{-s})]
         = zeta_v(s) * L_v(s, pi_v, Ad)
The (1 + q_v^{-s}) factor cancels exactly via Clebsch-Gordan.

### 2.2 Global Residue Positivity

[BASE] (Jacquet-Shalika 1981) The Jacquet-Shalika integral factors as:
  integral_{N(A)\GL_2(A)} W_f(g) Wbar_f(g) |det g|^s dg
  = zeta_F(s) * L(s, f, Ad) * ||W_f||^2 * (local factors at bad primes)

[BASE] (Analytic Class Number Formula)
  Res_{s=1} zeta_F(s) = 2^{r1} (2pi)^{r2} h_F R_F / (w_F sqrt|D_F|) > 0.

[BASE] (Shahidi 1981) L(1, f, Ad) > 0 for any generic cuspidal automorphic pi.

[THM] (F-2) [proved in proof/02-global-residue.tex]
  Res_{s=1} <1, T^JS_{s,Phi}[W_f (x) W_fbar]>
  = Phihat(0) * Res_{s=1} zeta_F(s) * L(1, pi, Ad) * ||W_f||^2 > 0

### 2.3 Instance Certification

[THM] (F-3) [certified in src/numerical_delta.py, verified by tests/test_numerical.py]
For Delta in S_{12}(SL_2(Z)) (Ramanujan delta function, N=1):
  L(1, sym^2 Delta) in [2.405, 2.407]  (Arb interval arithmetic, 128 bits)
In particular L(1, sym^2 Delta) >= 2.405 > 0.

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
  Case 2 (Siegel zero): contradicts [THM F-2]. Excluded.

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

checker/check_bound.py verifies independently:
  1. Hecke eigenvalue relations a_f(p)^2 = a_f(p^2) + p^{k-1} for unramified p
  2. Satake parameters satisfy alpha_p * beta_p = 1
  3. Euler product tail bound is valid
  4. Interval arithmetic enclosure strictly contains L_0
