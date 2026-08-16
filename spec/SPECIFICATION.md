# Effective Lower Bounds for L(1, sym² f): Mathematical Specification

**Document type:** authoritative mathematical specification  
**Scope:** symmetric square L-functions of primitive holomorphic Hecke eigenforms over Q  
**Completion state:** foundation layer complete; mollifier and explicit-constant layers are proof obligations

---

## 0. Logical Contract

### 0.1 What This Document Does

This document defines the mathematical objects and states all theorems with their proof
status. Every accepted conclusion follows from typed premises by stated theorems.
Missing constructions are explicit obligations. No missing object is treated as proved.

### 0.2 Atomic Status Grammar

| Status | Meaning | Logical use |
|--------|---------|-------------|
| **\[DEF\]** | Definition fixed by this document | May be unfolded |
| **\[BASE\]** | Standard theorem admitted as foundation | Usable with stated hypotheses |
| **\[THM\]** | Theorem proved in this document | Usable downstream |
| **\[OBL\]** | Proof still required | **May not be used as a theorem** |
| **\[OUT\]** | Deliberately outside the certified profile | No downstream force |

Composite labels are forbidden.

### 0.3 Module Dependency

```
M0 foundations (adele rings, automorphic representations, Whittaker models)
  └─► M1 local factors (Casselman-Shalika, Clebsch-Gordan, Euler factor)  [THM]
        └─► M2 global residue (Jacquet-Shalika integral, pole at s=1)     [THM]
              └─► M3 mollifier construction                                [OBL]
                    └─► M4 zero-free region for L(s,sym²f)                [OBL]
                          └─► M5 explicit lower bound constant             [OBL]
```

---

## 1. Mathematical Objects

### 1.1 Holomorphic Hecke Eigenforms

**\[DEF\]** A **normalized primitive holomorphic Hecke eigenform** of weight $k$, level $N$, and
trivial nebentypus is an element $f \in S_k(N)$ satisfying:
- $f | T_p = \lambda_f(p) f$ for all Hecke operators $T_p$ (with $\lambda_f(1) = 1$)
- $f$ transforms as weight $k$ for $\Gamma_0(N)$
- $f$ is a newform (not a lift from lower level)

Fourier expansion: $f(z) = \sum_{n=1}^\infty a_f(n) e^{2\pi i n z}$ with $a_f(1) = 1$.

**\[DEF\]** The **Satake parameters** $\tilde\alpha_p, \tilde\beta_p$ at an unramified prime $p \nmid N$
are defined by $\tilde\alpha_p + \tilde\beta_p = a_f(p) p^{-(k-1)/2}$ and $\tilde\alpha_p \tilde\beta_p = 1$.

### 1.2 Symmetric Square L-Function

**\[DEF\]** The **symmetric square L-function** of $f$ is
$$L(s, \mathrm{sym}^2 f) = \prod_{p \nmid N} \bigl[(1-\tilde\alpha_p^2 p^{-s})(1-p^{-s})(1-\tilde\beta_p^2 p^{-s})\bigr]^{-1} \cdot \prod_{p \mid N} L_p^{\mathrm{ram}}(s)^{-1}$$
converging absolutely for $\mathrm{Re}(s) > 1$. For trivial central character, $L(s, \mathrm{sym}^2 f) = L(s, f, \mathrm{Ad})$.

### 1.3 Rankin–Selberg L-Function

**\[DEF\]** $L(s, f \times \tilde f) = \zeta(s) \cdot L(s, \mathrm{sym}^2 f)$, where the $\zeta(s)$ factor
arises from the decomposition $\mathrm{std} \otimes \mathrm{std}^\vee \cong \mathbf{1} \oplus \mathrm{Ad}$.

---

## 2. Foundation Theorems

### 2.1 Local Euler Factor Factorization

**\[BASE\] (Casselman–Shalika)** For unramified $\pi_v$ with Satake parameters $(\alpha_v, \beta_v)$,
$\alpha_v \beta_v = 1$, the unramified Whittaker function satisfies
$W_{f,v}(\mathrm{diag}(\varpi_v^l, 1)) = q_v^{-l/2} \chi_l(\alpha_v, \beta_v)$
where $\chi_l = (\alpha^{l+1}-\beta^{l+1})/(\alpha-\beta)$ is the $\mathrm{SU}(2)$ character.

**\[THM\] F-1 (Local Euler Factor)** *proved in `proof/01-foundations.tex`*

For $\alpha_v \beta_v = 1$ and $\Phi_v = \chi_{\mathcal{O}_v^2}$, using the Clebsch–Gordan sum
$\chi_l^2 = \sum_{j=0}^l \chi_{2j}$ and the identity
$\sum_{j=0}^\infty \chi_{2j} x^j = (1+x)/[(1-x)(1-\alpha_v^2 x)(1-\beta_v^2 x)]$:
$$I_v(s) = \frac{1}{(1-q_v^{-s})^2(1-\alpha_v^2 q_v^{-s})(1-\beta_v^2 q_v^{-s})} = \zeta_v(s) \cdot L_v(s, \pi_v, \mathrm{Ad})$$
The $(1+q_v^{-s})$ factor from the $m$-series cancels exactly against the numerator of the $l$-series.

### 2.2 Global Residue Positivity

**\[BASE\] (Jacquet–Shalika 1981)** The global Rankin–Selberg integral factors as
$\hat\Phi(0) \cdot \zeta_F(s) \cdot L(s, f, \mathrm{Ad}) \cdot \|W_f\|^2$ (up to local factors at finitely many places).

**\[BASE\] (Analytic Class Number Formula)** $\mathrm{Res}_{s=1} \zeta_F(s) > 0$.

**\[BASE\] (Shahidi 1981)** $L(1, f, \mathrm{Ad}) > 0$ for any generic cuspidal $\pi$.

**\[THM\] F-2 (Global Residue Positivity)** *proved in `proof/02-global-residue.tex`*
$$\mathrm{Res}_{s=1} \langle 1, \mathcal{T}_{s,\Phi}^{\mathrm{JS}}[W_f \otimes W_{\bar f}]\rangle = \hat\Phi(0) \cdot \mathrm{Res}_{s=1}\zeta_F(s) \cdot L(1, f, \mathrm{Ad}) \cdot \|W_f\|^2 > 0$$

### 2.3 Instance Certification

**\[THM\] F-3 (Delta Function)** *certified in `src/numerical_delta.py`*

For $\Delta \in S_{12}(SL_2(\mathbb{Z}))$: $L(1, \mathrm{sym}^2 \Delta) \in [2.405, 2.407]$ (Arb, 128-bit precision).

---

## 3. Proof Obligations

### 3.1 Mollifier Construction [OBL]

Construct $M(s) = \sum_{n \leq X} \mu(n) a_{\mathrm{sym}^2}(n) n^{-s}$ such that
$\int_T^{2T} |M(\tfrac12+it) L(\tfrac12+it, \mathrm{sym}^2 f)|^2 dt \gg T$ with explicit constant.

Requires: GL₃ Rankin–Selberg mean value, Hecke multiplicativity for sym², GL₃ large sieve.

### 3.2 Zero-Free Region [OBL]

Find explicit computable $\delta(N) > 0$ such that $L(s, \mathrm{sym}^2 f) \neq 0$ for
$\mathrm{Re}(s) \in [1-\delta(N), 1]$, $|\mathrm{Im}(s)| \leq 1$.

### 3.3 Explicit Lower Bound [OBL]

**Main Theorem (goal):** $L(1, \mathrm{sym}^2 f) \geq c_{\mathrm{eff}} / \log p$ for all
primitive $f$ of prime level $p$, with explicit computable $c_{\mathrm{eff}} > 0$.

Proof strategy: Case 1 (no Siegel zero) yields $c_1/\log p$ via contour integral with $c_1$
computable from the zero-free radius. Case 2 (Siegel zero) is excluded by [THM F-2].
The gap is making $c_1$ explicit — this is the core technical contribution.

---

## 4. Out-of-Scope

**\[OUT\]** GRH for $L(s, \mathrm{sym}^2 f)$.  
**\[OUT\]** Sublogarithmic improvement unconditionally.  
**\[OUT\]** Ramanujan conjecture $|\tilde\alpha_p| = 1$.  
**\[OUT\]** Higher symmetric power lifts.

---

## 5. Certificate Structure

```json
{
  "form": { "weight": 12, "level": 1, "label": "1.12.1.a", "coefficients": [1, -24, 252] },
  "bound": 2.405,
  "euler_product_cutoff": 500,
  "tail_bound": { "method": "rankin-selberg", "exponent": -1.0 },
  "euler_product_interval": [2.4050, 2.4070],
  "arb_precision_bits": 128,
  "checker_version": "1.0.0"
}
```

The checker verifies: Hecke relations, Satake normalization, tail bound, and interval enclosure of the claimed $L_0$.
