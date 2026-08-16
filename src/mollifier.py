"""
Mollifier construction for symmetric square L-functions.

M(s) = sum_{n <= X} mu(n) * a_sym2(n) * n^{-s}

Status: [OBL] - mean value theorem M-2 not yet proved.
This module provides computational tools for numerical exploration.
"""
from __future__ import annotations

import math


def mobius(n: int) -> int:
    """Compute mu(n) by trial division."""
    if n == 1:
        return 1
    factors = []
    d, temp = 2, n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            temp //= d
            if temp % d == 0:
                return 0
        d += 1
    if temp > 1:
        factors.append(temp)
    return (-1) ** len(factors)


def mollifier_value(s: complex, X: int, a_sym2: dict) -> complex:
    """Evaluate M(s) = sum_{n<=X} mu(n) * a_sym2(n) * n^{-s}."""
    total = 0.0 + 0.0j
    for n in range(1, X + 1):
        mu_n = mobius(n)
        if mu_n == 0:
            continue
        a_n = a_sym2.get(n, 0.0)
        if a_n == 0.0:
            continue
        total += mu_n * a_n * n**(-s)
    return total


def optimal_mollifier_length(N: int, theta: float = 0.25) -> int:
    """Return X = N^theta. Standard choice theta=1/4. See proof/03-mollifier.tex [OBL]."""
    return max(1, int(N**theta))
