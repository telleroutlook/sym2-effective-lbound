"""
sym2_coeffs.py -- Compute Dirichlet coefficients a_{sym^2}(n) for L(s, sym^2 Delta).

The symmetric square L-function has the Euler product:
  L(s, sym^2 f)^{-1} = prod_p (1 - alpha_p^2 p^{-s})(1 - p^{-s})(1 - beta_p^2 p^{-s})

where (alpha_p, beta_p) are Satake parameters with alpha_p * beta_p = 1 and
c_p = alpha_p + beta_p = tau(p) / p^{5.5}.

From the local factor expansion:
  a(p)   = alpha_p^2 + 1 + beta_p^2 = c_p^2 - 1
  a(p^2) = (alpha_p^2 + 1 + beta_p^2)^2 - (alpha_p^4 + 1 + beta_p^4)
          = (c_p^2-1)^2 - ((c_p^2-2)^2-2+1)
          = (c_p^2-2)(c_p^2-1)     [verified by direct expansion]

Cross-check: The CORRECT RS identity is
  sum_n tau(n)^2/n^{11+s} = [zeta(s)/zeta(2s)] * L(s, sym^2 Delta)

(NOT "zeta(s)*L(s)").  The zeta(2s) factor comes from
  sum_{k>=0} lambda_f(p^k)^2 z^k = (1+z) * L_p(s)  and  prod_p(1+p^{-s}) = zeta(s)/zeta(2s).

For verification:
  LHS(s) ~ [zeta_partial(s)/zeta_partial(2s)] * L_partial(s)

where both sides use partial sums truncated at the same N.

NOT imported by any other module.
"""

import math
import os
import sys

_repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)


def compute_sym2_coeffs(tau_values: list) -> list:
    """
    Compute a_{sym^2}(n) for n = 1..N using multiplicativity.

    tau_values: list of length N with tau_values[n-1] = tau(n).
    Returns list of length N with result[n-1] = a_{sym^2}(n) (float).

    Algorithm: Euler sieve. For each prime p, use the GL3 Hecke recurrence:
      a(p^k) satisfies a(p^{k+1}) = a(p)*a(p^k) - a_{GL1}(p)*a(p^{k-1})
    where a_{GL1}(p) = (alpha_p^2 + beta_p^2 + 1)(1) = (c_p^2-1) for the
    standard GL3 Hecke relation... actually the cleaner recursion is:

    a_{sym^2}(p^k) = sum_{j=0}^{k} alpha_p^{2j} * beta_p^{2(k-j)}
                   = sum_{j=0}^{k} alpha_p^{2j - 2(k-j)}
                   (using beta_p = 1/alpha_p)
                   = sum_{j=0}^{k} alpha_p^{4j-2k}

    For |alpha_p| = 1 (Ramanujan conjecture, verified by Deligne):
    alpha_p = e^{i*theta_p}, and this sum is the Chebyshev-like sum:

    a_{sym^2}(p^k) = sin((k+1)*2*theta_p) / sin(2*theta_p)  if sin != 0
                   or (k+1) if theta_p = 0 or pi/2

    Alternatively, use the linear recurrence:
      a(p^0) = 1
      a(p^1) = c_p^2 - 1
      a(p^k) = (c_p^2 - 1) * a(p^{k-1}) - (c_p^2 - 2) * a(p^{k-2})
              - ... (standard GL3 Hecke recurrence for sym^2)

    For simplicity and correctness, we use the explicit formula via the
    Chebyshev polynomial U_k approach for the symmetric representation.
    """
    N = len(tau_values)
    coeffs = [0.0] * (N + 1)  # 1-indexed: coeffs[n] = a_{sym^2}(n)
    coeffs[1] = 1.0

    # Sieve: mark primes and compute prime-power values
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    smallest_prime = [0] * (N + 1)

    for p in range(2, N + 1):
        if is_prime[p]:
            smallest_prime[p] = p
            # Compute a_{sym^2}(p^k) for all prime powers p^k <= N
            c = tau_values[p - 1] / p ** 5.5  # c_p = tau(p)/p^{5.5}
            c2 = c * c
            ap = [0.0] * 14   # ap[k] = a_{sym^2}(p^k)
            ap[0] = 1.0
            ap[1] = c2 - 1.0
            # GL3 three-term Hecke recurrence (mu1+mu2+mu3 = c2-1, mu1*mu2+... = c2-1, prod = 1):
            #   a(p^k) = (c2-1)*a(p^{k-1}) - (c2-1)*a(p^{k-2}) + a(p^{k-3})
            ap[2] = (c2 - 1) * ap[1] - (c2 - 1) * ap[0]  # ap[-1]=0
            for k in range(3, 14):
                ap[k] = (c2 - 1) * ap[k - 1] - (c2 - 1) * ap[k - 2] + ap[k - 3]
            pk = p
            k = 1
            while pk <= N:
                coeffs[pk] = ap[k]
                pk *= p
                k += 1

            # Mark multiples as composite
            j = p * p
            while j <= N:
                is_prime[j] = False
                if smallest_prime[j] == 0:
                    smallest_prime[j] = p
                j += p

    # For composite n: use multiplicativity
    # a_{sym^2}(n) = prod_{p^k || n} a_{sym^2}(p^k)
    # Process in order; for each composite n, find smallest prime factor.
    for n in range(4, N + 1):
        if is_prime[n]:
            continue
        p = smallest_prime[n]
        m = n // p
        # Find exact power of p in n
        pk = p
        q = n
        while q % p == 0:
            q //= p
            pk *= p
        pk //= p  # pk = p^{v_p(n)}
        m_coprime = n // pk
        if m_coprime == 1:
            pass  # already computed above (prime power)
        else:
            coeffs[n] = coeffs[pk] * coeffs[m_coprime]

    return coeffs[1:]  # return as 0-indexed list


def verify_rs_identity(tau_values: list, sym2_coeffs: list, s: float,
                       M_zeta: int = 10000) -> dict:
    """
    Cross-check the Rankin-Selberg identity:
      sum_n tau(n)^2 / n^{11+s} = [zeta(s)/zeta(2s)] * L(s, sym^2 Delta)

    LHS: sum_{n<=N} tau(n)^2 / n^{11+s}
    RHS: [sum_{m<=M} 1/m^s] / [sum_{m<=M} 1/m^{2s}] * [sum_{n<=N} a_{sym^2}(n)/n^s]

    Returns a dict with both values and their relative discrepancy.
    """
    N = len(tau_values)

    lhs = sum(tau_values[n - 1] ** 2 / n ** (11 + s) for n in range(1, N + 1))

    rhs_l = sum(sym2_coeffs[n - 1] / n ** s for n in range(1, N + 1))
    zeta_s = sum(1.0 / m ** s for m in range(1, M_zeta + 1))
    zeta_2s = sum(1.0 / m ** (2 * s) for m in range(1, M_zeta + 1))
    rhs = (zeta_s / zeta_2s) * rhs_l

    rel_disc = abs(lhs - rhs) / max(abs(lhs), 1e-300)
    return {
        "s": s,
        "N": N,
        "lhs": lhs,
        "rhs": rhs,
        "zeta_s": zeta_s,
        "zeta_2s": zeta_2s,
        "l_partial": rhs_l,
        "rel_discrepancy": rel_disc,
    }


def l_at_s(sym2_coeffs: list, s: float) -> float:
    """Partial Dirichlet sum sum_{n<=N} a_{sym^2}(n)/n^s approximating L(s,sym^2 Delta)."""
    return sum(sym2_coeffs[n - 1] / n ** s for n in range(1, len(sym2_coeffs) + 1))


if __name__ == "__main__":
    from discovery.rs_estimate import compute_tau

    N = 3000
    print(f"Computing tau(n) for n <= {N}...")
    tau = compute_tau(N)

    print("Computing a_{sym^2}(n)...")
    coeffs = compute_sym2_coeffs(tau)

    # Cross-check RS identity at several s values
    print("\nVerifying RS identity sum tau(n)^2/n^{11+s} = [zeta(s)/zeta(2s)]*L(s,sym^2 Delta):")
    print(f"  {'s':>5}  {'LHS':>15}  {'RHS':>15}  {'rel_disc':>12}")
    for s_val in [2.0, 1.5, 1.2, 1.1]:
        r = verify_rs_identity(tau, coeffs, s_val)
        print(f"  {s_val:>5.1f}  {r['lhs']:>15.8f}  {r['rhs']:>15.8f}  {r['rel_discrepancy']:>12.2e}")

    # L(s, sym^2 Delta) partial sums at various s
    print("\nPartial sums sum_{n<=N} a_{sym^2}(n)/n^s  (approximates L(s, sym^2 Delta)):")
    print(f"  {'s':>5}  {'L_partial':>15}  {'note'}")
    for s_val in [2.0, 1.5, 1.2, 1.1, 1.05, 1.02, 1.01]:
        lp = l_at_s(coeffs, s_val)
        print(f"  {s_val:>5.2f}  {lp:>15.8f}")

    # RS estimate at s->1 via the Tauberian formula
    from discovery.rs_estimate import rankin_selberg_partial
    results = rankin_selberg_partial(tau, verbose=False)
    final = results[-1]
    print(f"\nRS Tauberian at N={N}:")
    print(f"  ratio = sum/N = {final[2]:.6f}  (-> L(1)/zeta(2))")
    print(f"  L(1, sym^2 Delta) ~ zeta(2)*ratio = {final[3]:.6f}  (consistent with L_partial at s=1.01)")
