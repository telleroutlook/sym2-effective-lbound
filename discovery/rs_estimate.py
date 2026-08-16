"""
rs_estimate.py -- Discovery-tier computation of L(1, sym^2 Delta) via
the Rankin-Selberg method.

KEY INSIGHT (uncovered during development):

1. The correct Rankin-Selberg identity is:
     sum_n tau(n)^2 / n^{11+s} = [zeta(s) / zeta(2s)] * L(s, sym^2 Delta)

   NOT "zeta(s) * L(s)" — the zeta(2s) denominator comes from the identity
     sum_{k>=0} lambda_f(p^k)^2 z^k = (1+z) * L_p(s, sym^2)
   and prod_p (1+p^{-s}) = zeta(s)/zeta(2s).

2. The Tauberian asymptotic therefore reads:
     sum_{n<=N} tau(n)^2 / n^11 / N  ->  L(1, sym^2 Delta) / zeta(2)

3. Hence the discovery-tier estimate is:
     L(1, sym^2 Delta) = zeta(2) * lim_{N->inf} sum_{n<=N} tau(n)^2/n^11 / N
                       ~ (pi^2/6) * 0.3839 ~ 0.631

4. This is consistent with the partial Euler product (25 primes) = 0.641
   and with the Dirichlet series sum_n a_{sym^2}(n)/n^{1.01} ~ 0.634 at N=3000.

5. The naive truncated Euler product at s=1 conditionally converges (the
   terms (c_p^2-1)/p have zero Sato-Tate mean, so partial sums stay bounded),
   but its ERROR BOUND is not certified via simple 3/P tail bounds (those
   bounds assume absolute convergence which fails at s=1).
   Certified proof requires the approximate functional equation [OBL E-2].

STATUS: [OBL E-2] -- full certification requires AFE; this file provides
discovery-tier estimates.

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
    Compute partial Rankin-Selberg sums and running estimates.

    The Tauberian theorem applied to
      sum_n tau(n)^2/n^{11+s} = [zeta(s)/zeta(2s)] * L(s, sym^2 Delta)
    gives residue L(1)/zeta(2) at s=1, so:
      sum_{n<=N} tau(n)^2/n^11 / N  ->  L(1, sym^2 Delta) / zeta(2)

    Returns list of (N, partial_sum, ratio, l1_estimate) where
      ratio      = partial_sum / N  ->  L(1)/zeta(2)  ~  0.384
      l1_estimate = ratio * zeta(2)  ->  L(1)          ~  0.631
    """
    ZETA2 = math.pi ** 2 / 6  # pi^2/6 = 1.6449340668...

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
            ratio = cumsum / n if n > 0 else float('nan')
            l1_estimate = ratio * ZETA2
            results.append((n, cumsum, ratio, l1_estimate))
            if verbose:
                print(f"  N={n:6d}  partial_sum={cumsum:.6f}  "
                      f"ratio={ratio:.6f}  L(1)~{l1_estimate:.6f}")
    return results


def euler_product_partial_s1(tau_values: list, primes_only: bool = True) -> dict:
    """
    Compute the partial Euler product prod_{p<=P} L_p(1, sym^2 Delta).

    The conditional Euler product (terms ordered by prime) DOES converge to
    L(1, sym^2 Delta) ~ 0.631, because the terms (c_p^2 - 1)/p have zero
    Sato-Tate mean and the partial sums stay bounded.

    However, the simple tail bound |sum_{p>P} log L_p| <= sum_{p>P} 3/p
    DIVERGES, so this product cannot be *certified* via that tail bound.
    Certification requires the approximate functional equation [OBL E-2].
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
        "interpretation": "Converges conditionally to L(1) ~ 0.631; not certifiable via 3/P tail bound",
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

    print("\nPartial Euler product at s=1 (conditional convergence toward L(1) ~ 0.631):")
    ep = euler_product_partial_s1(tau)
    print(f"  Partial product over {ep['num_primes']} primes up to {ep['largest_prime']}: "
          f"{ep['partial_product']:.4f}")
    print(f"  ({ep['interpretation']})")

    print(f"\nRankin-Selberg Tauberian estimates:")
    print("  sum_{{n<=N}} tau(n)^2/n^11 / N  ->  L(1)/zeta(2)  ->  L(1) = zeta(2)*ratio")
    results = rankin_selberg_partial(tau, verbose=True)
    final = results[-1]
    print(f"\nAt N={N}:")
    print(f"  ratio = {final[2]:.6f}  (-> L(1)/zeta(2))")
    print(f"  L(1, sym^2 Delta) ~ zeta(2) * ratio = {final[3]:.6f}")
    print("\nNote: convergence is slow (O(1/sqrt(N))); certified bound requires AFE [OBL E-2].")
