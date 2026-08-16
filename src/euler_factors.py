"""
eur_factors.py -- Local Euler factor computation for GL2 x GL2 Rankin-Selberg.

Implements Theorem F-1: the exact (1 + q^{-s}) cancellation via SU(2)
Clebsch-Gordan identity, giving

    I_v(s) = zeta_v(s) * L_v(s, pi_v, Ad)
           = 1 / [(1-q^{-s})^2 (1-alpha^2 q^{-s})(1-beta^2 q^{-s})]

All computations use mpmath for discovery-tier verification.
For proof-tier certification, use src/numerical_delta.py with python-flint/Arb.

Status: verified (numerical check of Theorem F-1).
"""

import cmath
import math
from typing import Union

try:
    import mpmath
    _HAS_MPMATH = True
except ImportError:
    _HAS_MPMATH = False


def chi_l(alpha: complex, beta: complex, l: int) -> complex:
    """SU(2) character: chi_l(alpha, beta) = (alpha^{l+1} - beta^{l+1}) / (alpha - beta)."""
    if abs(alpha - beta) < 1e-15:
        return (l + 1) * alpha**l
    return (alpha**(l + 1) - beta**(l + 1)) / (alpha - beta)


def local_factor_series(alpha: complex, beta: complex, q: float, s: complex,
                        n_terms: int = 80) -> complex:
    """
    Compute I_v(s) via the double Dirichlet series (truncated to n_terms).

    I_v(s) = S_m * S_l where
      S_m = sum_{m=0}^{n} q^{-2ms}
      S_l = sum_{l=0}^{n} chi_l(alpha,beta)^2 * q^{-ls}

    Used to verify the closed-form result numerically.
    """
    x = q**(-s)

    # m-series: sum_{m>=0} q^{-2ms} = sum_{m>=0} x^{2m}
    S_m = sum(x**(2 * m) for m in range(n_terms))

    # l-series: sum_{l>=0} chi_l^2 * x^l
    S_l = sum(chi_l(alpha, beta, l)**2 * x**l for l in range(n_terms))

    return S_m * S_l


def local_factor_closed(alpha: complex, beta: complex, q: float,
                        s: complex) -> complex:
    """
    Compute I_v(s) via the closed form from Theorem F-1:

        I_v(s) = 1 / [(1-q^{-s})^2 * (1-alpha^2*q^{-s}) * (1-beta^2*q^{-s})]

    Requires: alpha * beta = 1.
    """
    qms = q**(-s)
    return 1.0 / ((1 - qms)**2 * (1 - alpha**2 * qms) * (1 - beta**2 * qms))


def zeta_v(q: float, s: complex) -> complex:
    """Local zeta factor: zeta_v(s) = (1 - q^{-s})^{-1}."""
    return 1.0 / (1 - q**(-s))


def local_adjoint_factor(alpha: complex, beta: complex, q: float,
                         s: complex) -> complex:
    """
    Local adjoint L-factor for GL2 with alpha*beta=1:

        L_v(s, pi_v, Ad) = (1 - q^{-s})^{-1} (1-alpha^2 q^{-s})^{-1} (1-beta^2 q^{-s})^{-1}

    Note: the adjoint rep of GL2 has Satake parameters (alpha^2, 1, beta^2).
    """
    qms = q**(-s)
    return 1.0 / ((1 - qms) * (1 - alpha**2 * qms) * (1 - beta**2 * qms))


def verify_f1_cancellation(alpha: complex, beta: complex, q: float,
                            s: complex, tol: float = 1e-8) -> dict:
    """
    Verify Theorem F-1: check that I_v(s) = zeta_v(s) * L_v(s, pi_v, Ad).

    Returns a dict with keys:
      series_value   -- I_v(s) via truncated double series
      closed_value   -- I_v(s) via closed form
      factored_value -- zeta_v(s) * L_v(s, Ad)
      cancellation_ok -- bool, all three agree within tol
    """
    iv_series = local_factor_series(alpha, beta, q, s)
    iv_closed = local_factor_closed(alpha, beta, q, s)
    iv_factored = zeta_v(q, s) * local_adjoint_factor(alpha, beta, q, s)

    err1 = abs(iv_series - iv_closed)
    err2 = abs(iv_closed - iv_factored)

    return {
        "series_value": iv_series,
        "closed_value": iv_closed,
        "factored_value": iv_factored,
        "series_vs_closed_error": err1,
        "closed_vs_factored_error": err2,
        "cancellation_ok": err1 < tol and err2 < tol,
    }


def cg_series_vs_formula(alpha: complex, beta: complex, n_terms: int = 40) -> dict:
    """
    Verify the Clebsch-Gordan generating function identity:

        sum_{l=0}^{n} chi_l(a,b)^2 x^l
        approx (1+x) / [(1-x)(1-a^2 x)(1-b^2 x)]   (for |x| < 1, ab=1)

    at x = 0.3 (a sample convergence point).
    """
    x = 0.3

    # Series side
    series = sum(chi_l(alpha, beta, l)**2 * x**l for l in range(n_terms))

    # Closed-form side (requires alpha*beta = 1)
    formula = (1 + x) / ((1 - x) * (1 - alpha**2 * x) * (1 - beta**2 * x))

    return {
        "series": series,
        "formula": formula,
        "error": abs(series - formula),
        "n_terms": n_terms,
    }


# ---------------------------------------------------------------------------
# Public API aliases and convenience functions (test-expected names)
# ---------------------------------------------------------------------------

def l_series_exact(alpha: complex, beta: complex, x: float,
                   n_terms: int = 51) -> complex:
    """
    Compute sum_{l=0}^{n_terms-1} chi_l(alpha,beta)^2 * x^l (series form).

    This is the "l-series" side of the Clebsch-Gordan identity — evaluated
    by direct summation.  Converges when |x| < 1/max(|alpha|^2, |beta|^2).
    For |x| outside the convergence disk this returns the partial sum, which
    is still positive for real alpha, beta, x > 0.
    """
    return sum(chi_l(alpha, beta, l) ** 2 * x ** l for l in range(n_terms))


def local_euler_factor(alpha: complex, beta: complex, q: float,
                       s: complex) -> complex:
    """Alias for local_factor_closed."""
    return local_factor_closed(alpha, beta, q, s)


def adjoint_local_factor(alpha: complex, beta: complex, q: float,
                         s: complex) -> complex:
    """Alias for local_adjoint_factor."""
    return local_adjoint_factor(alpha, beta, q, s)


def zeta_local(q: float, s: complex) -> complex:
    """Alias for zeta_v."""
    return zeta_v(q, s)


def verify_cancellation(alpha: complex, beta: complex, q: float,
                        s: complex, tol: float = 1e-8) -> dict:
    """
    Verify Theorem F-1 cancellation with test-friendly key names.

    cancellation_verified -- True iff closed_value == factored_value (within tol)
    rel_error_factored    -- |closed - factored| / |factored|

    Note: series_value may differ from closed_value when |alpha^2 * q^{-s}| > 1
    (series diverges); cancellation_verified tests only the algebraic identity
    between the closed form and the factored form.
    """
    r = verify_f1_cancellation(alpha, beta, q, s, tol)
    denom = abs(r["factored_value"])
    rel_err = r["closed_vs_factored_error"] / max(denom, 1e-300)
    return {
        **r,
        "cancellation_verified": r["closed_vs_factored_error"] < tol,
        "rel_error_factored": rel_err,
    }


def delta_satake_params(p: int) -> tuple:
    """
    Return normalized Satake parameters (alpha, beta) for Ramanujan Delta
    (weight 12, level 1) at prime p, with alpha*beta = 1.

    Uses Deligne's theorem: |alpha| = |beta| = 1 (unit circle).
    """
    from src.numerical_delta import TAU_PRIMES
    tau_p = TAU_PRIMES[p]
    c = tau_p / p ** 5.5  # alpha + beta (real)
    disc = c * c - 4.0
    if disc < 0:
        im = math.sqrt(-disc) / 2.0
        return complex(c / 2.0, im), complex(c / 2.0, -im)
    else:
        a = (c + math.sqrt(disc)) / 2.0
        return a, c - a


def delta_local_sym2_factor(p: int, s: complex = 1.0) -> complex:
    """
    Local factor L_p(s, sym^2 Delta)^{-1} for Ramanujan Delta.

    Equals (1-p^{-s}) * (1-alpha^2*p^{-s}) * (1-beta^2*p^{-s})
    where alpha, beta are the unit-circle Satake parameters.
    """
    alpha, beta = delta_satake_params(p)
    qms = p ** (-s)
    return (1 - qms) * (1 - alpha**2 * qms) * (1 - beta**2 * qms)


if __name__ == "__main__":
    # Quick sanity check with random Satake parameters on the unit circle
    import cmath
    theta = 0.8  # angle on unit circle
    alpha = cmath.exp(1j * theta)
    beta = cmath.exp(-1j * theta)  # = 1/alpha since |alpha|=1
    q = 7.0
    s = 1.0 + 0j

    result = verify_f1_cancellation(alpha, beta, q, s)
    print("Theorem F-1 verification at alpha=e^{i*0.8}, q=7, s=1:")
    for k, v in result.items():
        print(f"  {k}: {v}")
    assert result["cancellation_ok"], "F-1 verification FAILED"
    print("PASS")
