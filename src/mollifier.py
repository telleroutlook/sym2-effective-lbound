"""
mollifier.py -- Mollifier construction for sym^2 L-functions (discovery tier).

Status: [OBL] -- This module is exploratory only.
Outputs are NOT certified and may not be imported by checker/ or proof/.

See proof/03-mollifier.tex for the proof strategy.
"""

import math
from typing import Optional


def mobius(n: int) -> int:
    """Compute the Mobius function mu(n)."""
    if n == 1:
        return 1
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            temp //= d
            if temp % d == 0:
                return 0  # p^2 divides n
        d += 1
    if temp > 1:
        factors.append(temp)
    return (-1) ** len(factors)


def sym2_hecke_eigenvalue_at_prime(p: int, tau_p: int, k: int = 12) -> float:
    """
    Compute a_Pi(p) for Pi = sym^2 Delta, where Pi is the GL3 lift.

    For the Ramanujan Delta function:
      a_Pi(p) = tau(p)^2 / p^{k-1} - 1

    (This is tilde_alpha_p^2 + 1 + tilde_beta_p^2 = c^2 - 2 + 1 = c^2 - 1
    where c = tilde_alpha_p + tilde_beta_p = tau(p)/p^{(k-1)/2},
    and a_Pi(p) = tilde_alpha_p^2 + tilde_beta_p^2 + 1 = c^2 - 2 + 1 = c^2 - 1.)
    """
    c = tau_p / p**((k - 1) / 2)
    return c * c - 1.0


def mollifier_coefficients(X: int, tau_values: dict,
                             k: int = 12) -> dict:
    """
    Compute mollifier coefficients for M(s) = sum_{n<=X} mu(n) a_Pi(n) n^{-s}.

    For squarefree n = p1*...*pk:
      coefficient = mu(n) * prod_i a_Pi(pi) (multiplicative)

    Returns dict {n: (mu_n, a_Pi_n, coefficient)} for squarefree n <= X
    with mu(n) != 0.

    Note: This is a DISCOVERY-TIER function. Not certified.
    """
    # Compute a_Pi at primes up to X
    prime_a = {}
    for p, tau_p in tau_values.items():
        if p <= X:
            prime_a[p] = sym2_hecke_eigenvalue_at_prime(p, tau_p, k)

    coeffs = {}
    # Squarefree n <= X built from primes in tau_values
    # Start with n=1
    coeffs[1] = {"mu": 1, "a_Pi": 1.0, "coeff": 1.0}

    primes_in_range = sorted(p for p in prime_a if p <= X)

    def build_squarefree(current_n, current_mu, current_a, prime_idx):
        coeffs[current_n] = {
            "mu": current_mu,
            "a_Pi": current_a,
            "coeff": current_mu * current_a,
        }
        for i in range(prime_idx, len(primes_in_range)):
            p = primes_in_range[i]
            new_n = current_n * p
            if new_n > X:
                break
            build_squarefree(new_n, -current_mu, current_a * prime_a[p], i + 1)

    build_squarefree(1, 1, 1.0, 0)
    return coeffs


def mollifier_value(s: complex, X: int, tau_values: dict, k: int = 12) -> complex:
    """
    Evaluate M(s) = sum_{n<=X} mu(n) a_Pi(n) n^{-s} at a given s.

    DISCOVERY TIER ONLY -- not certified.
    """
    coeffs = mollifier_coefficients(X, tau_values, k)
    return sum(v["coeff"] * n**(-s) for n, v in coeffs.items())


if __name__ == "__main__":
    from src.numerical_delta import TAU_PRIMES
    X = 20
    s = 0.5 + 10j
    M_s = mollifier_value(s, X, TAU_PRIMES)
    print(f"M({s}) with X={X}: {M_s}  [discovery tier]")
