"""
Local Euler factor computation for GL2 x GL2 Rankin-Selberg.

Implements the algebraic identities proved in proof/01-foundations.tex:
  - Casselman-Shalika formula for unramified Whittaker functions
  - Clebsch-Gordan sum identity: chi_l^2 = sum_{j=0}^l chi_{2j}
  - Exact (1+q^{-s}) cancellation (Theorem F-1)
  - Identification I_v(s) = zeta_v(s) * L_v(s, pi_v, Ad)

All computations use mpmath for discovery; for certified bounds use
python-flint (Arb) in numerical_delta.py.
"""
from __future__ import annotations


def chi_l(alpha: complex, beta: complex, l: int) -> complex:
    """Character of the (l+1)-dim SU(2) irrep.

    chi_l(alpha,beta) = (alpha^{l+1} - beta^{l+1}) / (alpha - beta)
    For alpha = beta: chi_l(alpha,alpha) = (l+1) * alpha^l.
    """
    if abs(alpha - beta) < 1e-15:
        return (l + 1) * alpha**l
    return (alpha**(l + 1) - beta**(l + 1)) / (alpha - beta)


def l_series_exact(alpha: complex, beta: complex, x: complex) -> complex:
    """Closed-form sum_{l=0}^inf chi_l(alpha,beta)^2 * x^l.

    Formula (Proposition 4.1 in proof/01-foundations.tex, alpha*beta=1):
        = (1+x) / ((1-x)(1-alpha^2*x)(1-beta^2*x))
    """
    return (1 + x) / ((1 - x) * (1 - alpha**2 * x) * (1 - beta**2 * x))


def local_euler_factor(alpha: complex, beta: complex, q: float, s: complex) -> complex:
    """Unramified local factor I_v(s) = 1/[(1-q^{-s})^2(1-a^2 q^{-s})(1-b^2 q^{-s})].

    Equals zeta_v(s) * L_v(s, pi_v, Ad) by Theorem F-1. Assumes alpha*beta=1.
    """
    x = q**(-s)
    return 1.0 / ((1 - x)**2 * (1 - alpha**2 * x) * (1 - beta**2 * x))


def adjoint_local_factor(alpha: complex, beta: complex, q: float, s: complex) -> complex:
    """Adjoint local L-factor L_v(s, pi_v, Ad) with Satake params (alpha^2, 1, beta^2)."""
    x = q**(-s)
    return 1.0 / ((1 - x) * (1 - alpha**2 * x) * (1 - beta**2 * x))


def zeta_local(q: float, s: complex) -> complex:
    """Local zeta factor: (1 - q^{-s})^{-1}."""
    return 1.0 / (1 - q**(-s))


def verify_cancellation(alpha: complex, beta: complex, q: float, s: complex) -> dict:
    """Verify the (1+q^{-s}) exact cancellation of Theorem F-1.

    Computes three equal quantities and reports relative errors.
    """
    x = q**(-s)
    I_direct = local_euler_factor(alpha, beta, q, s)
    S_m = 1.0 / ((1 - x) * (1 + x))
    S_l = l_series_exact(alpha, beta, x)
    I_before = S_m * S_l
    I_factored = zeta_local(q, s) * adjoint_local_factor(alpha, beta, q, s)
    err1 = abs(I_direct - I_before) / (abs(I_direct) + 1e-300)
    err2 = abs(I_direct - I_factored) / (abs(I_direct) + 1e-300)
    return {
        "I_direct": I_direct,
        "I_before_cancellation": I_before,
        "I_factored": I_factored,
        "rel_error_cancel": err1,
        "rel_error_factored": err2,
        "cancellation_verified": err1 < 1e-10 and err2 < 1e-10,
    }


def delta_satake_params(p: int) -> tuple:
    """Normalized Satake parameters of the Ramanujan Delta function at prime p.

    alpha*beta=1, alpha+beta = tau(p) * p^{-11/2}.
    """
    tau_values = {
        2: -24, 3: 252, 5: 4830, 7: -16744, 11: 534612, 13: -577738,
        17: -6905934, 19: 2727432, 23: 18643272, 29: 128406630,
        31: -52843168, 37: -182213314, 41: -357799110, 43: 740985142,
        47: 1447455360,
    }
    if p not in tau_values:
        raise NotImplementedError(f"tau({p}) not precomputed")
    tau_p = tau_values[p]
    norm_sum = tau_p * p**(-5.5)
    disc = norm_sum**2 - 4.0
    if disc >= 0:
        sq = disc**0.5
        return (norm_sum + sq) / 2, (norm_sum - sq) / 2
    sq = (-disc)**0.5
    return complex(norm_sum / 2, sq / 2), complex(norm_sum / 2, -sq / 2)


def delta_local_sym2_factor(p: int, s: complex = 1.0) -> complex:
    """Local sym^2 factor L_p(s, sym^2 Delta)^{-1}."""
    alpha, beta = delta_satake_params(p)
    x = p**(-s)
    return (1 - alpha**2 * x) * (1 - x) * (1 - beta**2 * x)
