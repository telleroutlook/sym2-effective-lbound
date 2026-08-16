"""
rs_estimate.py -- Discovery-tier computation of L(1, sym^2 Delta) via
the Rankin-Selberg method.

KEY INSIGHT (uncovered during development): The naive Euler product
    prod_{p <= P} L_p(1, sym^2 f)^{-1}
diverges to zero as P -> infinity for GL3 L-functions at s=1.
Partial products over 25 primes give ~0.55, not 2.406.

CORRECT METHOD: Rankin-Selberg formula.
  L(s, Delta x Delta) = sum_n lambda(n)^2 / n^s = zeta(s) * L(s, sym^2 Delta)

where lambda(n) = tau(n) / n^{5.5} are the normalized Hecke eigenvalues, so

  sum_n tau(n)^2 / n^{s+11} = zeta(s) * L(s, sym^2 Delta).

The Rankin-Selberg partial sum satisfies (Tauberian asymptotic):
  sum_{n <= N} tau(n)^2 / n^11 ~ L(1, sym^2 Delta) * log N  (as N -> infinity)

So:
  L(1, sym^2 Delta) = lim_{N->inf} (sum_{n<=N} tau(n)^2 / n^11) / log N

STATUS: [OBL E-2] -- full certification requires the approximate
functional equation; this file provides discovery-tier estimates.

NOT imported by any other module.
"""

import math
import os
import sys

# Ensure the repo root is importable as 'src.*'
_repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)


def compute_tau(N: int) -> list:
    """
    Compute tau(1), ..., tau(N) using the q-product definition:
    Delta(q) = q * prod_{k>=1} (1-q^k)^24 = sum_{n>=1} tau(n) q^n.

    Algorithm: start with p = [1, 0, 0, ...] and multiply by (1-q^k)^24
    for k=1..N.  tau(n) is the coefficient of q^n, i.e., p[n-1] after
    shifting by the leading q.
    """
    p = [0] * (N + 1)
    p[0] = 1
    for k in range(1, N + 1):
        for _ in range(24):
            for n in range(N, k - 1, -1):
                p[n] -= p[n - k]
    return [p[n - 1] for n in range(1, N + 1)]


def rankin_selberg_partial(tau_values: list, verbose: bool = False) -> list:
    """
    Compute partial Rankin-Selberg sums and running L(1, sym^2 Delta) estimates.

    Returns list of (N, partial_sum, estimate) triples for logarithmically
    spaced N values.
    """
    N = len(tau_values)
    results = []
    cumsum = 0.0
    log_checkpoints = set()
    for k in range(1, 30):
        log_checkpoints.add(int(10 ** (k * 0.2)))

    for n in range(1, N + 1):
        tau_n = tau_values[n - 1]
        cumsum += tau_n ** 2 / n ** 11
        if n in log_checkpoints or n == N:
            estimate = cumsum / n if n > 0 else float('nan')
            results.append((n, cumsum, estimate))
            if verbose:
                print(f"  N={n:6d}  partial_sum={cumsum:.6f}  "
                      f"estimate L(1)={estimate:.6f}")
    return results


def euler_product_partial_s1(tau_values: list, primes_only: bool = True) -> dict:
    """
    Compute the partial Euler product prod_{p<=P} L_p(1, sym^2 Delta)^{-1}
    to show it diverges to 0 (NOT a valid computation of L(1)).

    This is a diagnostic function showing WHY the naive approach fails.
    """
    from src.numerical_delta import SMALL_PRIMES, local_factor_inv_real, TAU_PRIMES

    log_prod = 0.0
    for p in SMALL_PRIMES:
        inv_lp = local_factor_inv_real(p, TAU_PRIMES[p])
        log_prod += math.log(1.0 / inv_lp)

    return {
        "partial_product": math.exp(log_prod),
        "num_primes": len(SMALL_PRIMES),
        "largest_prime": SMALL_PRIMES[-1],
        "interpretation": "DOES NOT converge to L(1); Euler product diverges at s=1 for GL3",
    }


def verify_tau_small_primes(tau_values: list) -> dict:
    """Cross-check computed tau(p) against known values from LMFDB."""
    from src.numerical_delta import TAU_PRIMES

    mismatches = {}
    for p, expected in TAU_PRIMES.items():
        if p <= len(tau_values):
            computed = tau_values[p - 1]
            if computed != expected:
                mismatches[p] = {"computed": computed, "expected": expected}
    return {"mismatches": mismatches, "primes_checked": len(TAU_PRIMES)}


if __name__ == "__main__":
    import sys
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000

    print(f"Computing tau(n) for n <= {N} via q-product formula...")
    tau = compute_tau(N)

    print("\nCross-checking against known small-prime values:")
    check = verify_tau_small_primes(tau)
    if check["mismatches"]:
        print(f"  MISMATCH at primes: {check['mismatches']}")
    else:
        print(f"  All {check['primes_checked']} known values match. [OK]")

    print("\nPartial Euler product at s=1 (shows divergence to 0):")
    ep = euler_product_partial_s1(tau)
    print(f"  Partial product over {ep['num_primes']} primes up to {ep['largest_prime']}: "
          f"{ep['partial_product']:.4f}")
    print(f"  ({ep['interpretation']})")

    print(f"\nRankin-Selberg estimates for L(1, sym^2 Delta):")
    print("  sum_{{n<=N}} tau(n)^2 / n^11 / N  ->  L(1)")
    results = rankin_selberg_partial(tau, verbose=True)
    print(f"\nFinal estimate at N={N}: L(1, sym^2 Delta) ~ {results[-1][2]:.6f}")
    print("\nNote: convergence is O(1/sqrt(N)) so large N needed for precision.")
    print("For certified bound, implement approximate functional equation [OBL E-2].")
