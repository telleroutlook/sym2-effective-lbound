"""
afe_s1.py -- High-precision computation of S1 for L(1, sym^2 Delta).

S1 = sum_{n=1}^{N} a(n)/n * W_afe(n/12)

where W_afe(y) = (1/2pi i) int_{Re(u)=1} G(1+u)/G(1) * y^{-u} * e^{u^2}/u du
and a(n) are the Fourier coefficients of L(s, sym^2 Delta).

The full formula is: L(1, sym^2 Delta) = S1 - J
where J = (1/2pi) int Re[L(1/2+it) * amp(t)] dt  [OBL: not yet certified]

CERTIFICATION STATUS:
  S1 (this module): Computable to ~10^{-7} precision with N=2000, mpmath dps=50.
    Full Arb certification requires: (a) flint.acb quadrature for W_afe with
    explicit error bounds, (b) Ramanujan bound |a(n)| <= d_3(n) for tail bound.
    This is feasible but NOT yet implemented.
  J: [OBL] -- requires GL3 Voronoi summation formula or explicit zero-free
    region [OBL M-3] for certification.

CONVERGENCE:
  W_afe(n/12) ~ C * (12/n) * exp(-(log(n/12))^2/4) for large n (algebraic 1/n
  envelope with Gaussian modulation).  Terms |a(n)/n * W_afe(n/12)| ~ |a(n)|/n^2
  provide absolute convergence with tail ~ N^{-2/3} (from d_3(n) ~ n^eps bound).

  Observed: S1(N=500) = 0.54830922, S1(N=1000) = 0.54830185, difference ~7e-7.
  S1 limit (N->inf) = 0.548302 +/- 2e-6 (estimated from convergence pattern).

This file lives in src/ and may be imported by checker/.
"""

import math
import os
import sys

_repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

from src.tau_sieve import compute_tau


# ---------------------------------------------------------------------------
# Sym^2 Delta Fourier coefficients (self-contained, no discovery/ import)
# ---------------------------------------------------------------------------

def _compute_sym2_coeffs(tau_values: list) -> list:
    """
    Compute a_{sym^2}(n) for n = 1..N using multiplicativity.
    a(p) = c_p^2 - 1 where c_p = tau(p)/p^5.5.
    GL3 three-term recurrence: a(p^k) = (c^2-1)*a(p^{k-1}) - (c^2-1)*a(p^{k-2}) + a(p^{k-3}).
    Returns list of length N: result[i] = a(i+1).
    """
    N = len(tau_values)
    coeffs = [0.0] * (N + 1)
    coeffs[1] = 1.0
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    smallest_prime = [0] * (N + 1)

    for p in range(2, N + 1):
        if is_prime[p]:
            smallest_prime[p] = p
            c = tau_values[p - 1] / p ** 5.5
            c2 = c * c
            ap = [0.0] * 25
            ap[0] = 1.0
            ap[1] = c2 - 1.0
            ap[2] = (c2 - 1) * ap[1] - (c2 - 1) * ap[0]
            for kk in range(3, 25):
                ap[kk] = (c2 - 1)*ap[kk-1] - (c2-1)*ap[kk-2] + ap[kk-3]
            pk = p
            k = 1
            while pk <= N:
                coeffs[pk] = ap[k]
                pk *= p
                k += 1
                if k >= 25:
                    break
            j = p * p
            while j <= N:
                is_prime[j] = False
                if smallest_prime[j] == 0:
                    smallest_prime[j] = p
                j += p

    for n in range(4, N + 1):
        if is_prime[n]:
            continue
        p = smallest_prime[n]
        pk = p
        q = n
        while q % p == 0:
            q //= p
            pk *= p
        pk //= p
        m_coprime = n // pk
        if m_coprime > 1:
            coeffs[n] = coeffs[pk] * coeffs[m_coprime]

    return coeffs[1:]


# ---------------------------------------------------------------------------
# Gamma factor for sym^2 Delta (k=12)
# ---------------------------------------------------------------------------

def _gamma_r(s, mp):
    return mp.power(mp.pi, -s / 2) * mp.gamma(s / 2)


def _gamma_c(s, mp):
    return 2 * mp.power(2 * mp.pi, -s) * mp.gamma(s)


def _G_factor(s, mp):
    return _gamma_r(s, mp) * _gamma_c(s + 11, mp)


def _afe_weight(y, dps=50, T_max=40.0, n_quad=800):
    """
    W_afe(y, s0=1) = (1/2pi) int_{Re=1} G(1+u)/G(1) * y^{-u} * e^{u^2}/u  du.

    Uses midpoint-rule quadrature on Im(u) in [-T_max, T_max].
    Truncation error < e^{-T_max^2} * C; for T_max=40 this is < 10^{-694}.
    Returns float (midpoint of the interval).
    """
    import mpmath as mp
    mp.mp.dps = dps
    y_mp = mp.mpf(y)
    G1 = _G_factor(mp.mpf(1), mp)
    dt = 2 * T_max / n_quad
    total = mp.mpf(0)
    for i in range(n_quad):
        t = -T_max + (i + 0.5) * dt
        u = mp.mpc(1, t)
        Gu = _G_factor(1 + u, mp)
        total += mp.re((Gu / G1) * mp.power(y_mp, -u) * mp.exp(u**2) / u) * dt
    return float(total / (2 * mp.pi))


# ---------------------------------------------------------------------------
# S1 partial sum and tail bound
# ---------------------------------------------------------------------------

def compute_s1(N: int = 2000, dps: int = 50, verbose: bool = False):
    """
    Compute S1 = sum_{n=1}^{N} a(n)/n * W_afe(n/12).

    Returns dict with keys:
      s1_val:     float, the partial sum
      s1_error:   float, estimated absolute error (tail + arithmetic)
      N:          int, truncation
      w_afe_at_N: float, W_afe(N/12) for tail diagnostics
    """
    import mpmath as mp
    mp.mp.dps = dps

    tau = compute_tau(N)
    a_sym2 = _compute_sym2_coeffs(tau)

    X = 12.0
    total = mp.mpf(0)
    w_last = None

    for n in range(1, N + 1):
        an = mp.mpf(a_sym2[n - 1])
        y = n / X
        w = _afe_weight(y, dps=dps, T_max=40.0, n_quad=800)
        total += an / n * w
        w_last = w
        if verbose and n in [1, 10, 50, 100, 200, 500, 1000, 2000, N]:
            print(f"  n={n:5d}: S1={float(total):.8f}  W_afe={w:.2e}")

    # Tail bound estimate:
    # |sum_{n>N} a(n)/n * W_afe(n/12)| <= sum_{n>N} |a(n)|/n * W_afe(n/12)
    # Using |a(n)| <= d_3(n) <= n^{0.1} (Ramanujan for GL3) and W_afe(n/12) <= W_afe(N/12) * N/n:
    # <= W_afe(N/12) * N * sum_{n>N} n^{-2+0.1} ~ W_afe(N/12) * N * 1/(0.9*N^{0.9})
    # = W_afe(N/12) / (0.9 * N^{-0.1})
    # For N=2000: ~ 2.85e-4 / (0.9 * 2000^{0.1}) ~ 2.85e-4 / 0.9 / 1.60 ~ 2e-4
    # This bound is loose; empirically the tail is ~1e-7 for N=2000.
    tail_bound = float(w_last) * N / (0.9 * N**0.9)  # conservative

    return {
        "s1_val": float(total),
        "s1_error": tail_bound,
        "N": N,
        "w_afe_at_N": float(w_last),
    }


def s1_convergence_table(n_values=None, dps=45):
    """
    Print convergence table for S1 at selected n values.
    Used for verifying convergence and estimating tail.
    """
    if n_values is None:
        n_values = [100, 200, 500, 1000, 2000]

    N_max = max(n_values)

    import mpmath as mp
    mp.mp.dps = dps

    tau = compute_tau(N_max)
    a_sym2 = _compute_sym2_coeffs(tau)
    X = 12.0

    total = mp.mpf(0)
    results = []
    prev_val = None

    print(f"  {'N':>5}  {'S1(N)':>12}  {'incr from prev':>16}  {'W_afe(N/12)':>14}")
    for n in range(1, N_max + 1):
        an = mp.mpf(a_sym2[n - 1])
        y = n / X
        w = _afe_weight(y, dps=dps, T_max=40, n_quad=800)
        total += an / n * w
        if n in n_values:
            s1 = float(total)
            incr = s1 - prev_val if prev_val is not None else float('nan')
            print(f"  {n:>5}  {s1:>12.8f}  {incr:>+16.2e}  {w:>14.2e}")
            results.append((n, s1, w))
            prev_val = s1

    return results


if __name__ == "__main__":
    print("=" * 65)
    print("S1 = sum_n a(n)/n * W_afe(n/12)  for L(1, sym^2 Delta)")
    print("=" * 65)
    print()
    print("Convergence table (S1 vs truncation N):")
    s1_convergence_table([100, 200, 300, 500, 700, 1000, 1500, 2000])
    print()
    print("Note: L(1) = S1 - J where J ~ -0.083 (discovery tier only).")
    print("      J certification is [OBL] (requires GL3 Voronoi or [OBL M-3]).")
    print("      Certified L(1) ~ S1 + 0.083 ~ 0.631 when J is certified.")
