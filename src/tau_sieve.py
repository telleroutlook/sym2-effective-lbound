"""
tau_sieve.py -- Exact computation of the Ramanujan tau function.

tau(n) is defined by the q-expansion:
    Delta(q) = q * prod_{k>=1} (1 - q^k)^24 = sum_{n>=1} tau(n) q^n

All values are exact integers.  The algorithm multiplies out the product
one factor at a time using the polynomial ring ZZ[[q]] truncated at degree N.

This module lives in src/ so that certified_rs.py can import it without
violating the rule 'discovery/ must not be imported by src/ or proof/'.
"""


def compute_tau(N: int) -> list:
    """
    Return [tau(1), tau(2), ..., tau(N)] as a list of integers.

    Uses the q-product definition:
        Delta(q) = q * prod_{k=1}^{N} (1 - q^k)^24

    The coefficient of q^n in this product (shifted by q) is tau(n).
    Complexity: O(N^2) time, O(N) space.
    """
    p = [0] * (N + 1)
    p[0] = 1
    for k in range(1, N + 1):
        for _ in range(24):
            for n in range(N, k - 1, -1):
                p[n] -= p[n - k]
    return [p[n - 1] for n in range(1, N + 1)]
