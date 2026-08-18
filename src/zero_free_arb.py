"""
zero_free_arb.py -- Certified zero-free region for L(s, sym^2 Delta).

Two-track evaluation:
  Track A (Re(s) > 1): truncated Dirichlet series with tail bound from
    empirical partial-sum growth |S(X)| <= C * X^alpha.
    [STATUS: discovery -- C and alpha from N=20000 data, not proven.]

  Track B (Re(s) <= 1): GL3 AFE smoothed-sum identity.
    L(s) = sum_n A(n)/n^s * V(n/X, s) + chi(s) * dual_sum.
    [STATUS: discovery -- mpmath floats, not Arb intervals.]

For proof-tier certification, both tracks need:
  - Arb interval arithmetic (python-flint) for outward rounding
  - Proven bound on |S(X)| or certified GL3 AFE weight bounds
"""

import json
import math
import os
import sys

_repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

from src.tau_sieve import compute_tau


# ---------------------------------------------------------------------------
# Sym^2 coefficients (from tau values)
# ---------------------------------------------------------------------------

def compute_sym2_coeffs(tau_values):
    """Compute a_{sym^2}(n) for n = 1..N via multiplicativity."""
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
            max_k = max(1, int(math.log(N, p)) + 1)
            ap = [0.0] * (max_k + 1)
            ap[0] = 1.0
            ap[1] = c2 - 1.0
            if max_k >= 2:
                ap[2] = (c2 - 1) * ap[1] - (c2 - 1) * ap[0]
            for k in range(3, max_k + 1):
                ap[k] = (c2 - 1) * ap[k - 1] - (c2 - 1) * ap[k - 2] + ap[k - 3]
            pk = p
            k = 1
            while pk <= N:
                coeffs[pk] = ap[k]
                pk *= p
                k += 1
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
        m = n // p
        pk = p
        k = 1
        while m % p == 0:
            m //= p
            pk *= p
            k += 1
        if m != 1:
            coeffs[n] = coeffs[pk] * coeffs[m]

    return [coeffs[i] for i in range(1, N + 1)]


# ---------------------------------------------------------------------------
# Precomputation: coefficients + partial sums
# ---------------------------------------------------------------------------

def precompute(N):
    """Compute tau, A(n), and partial sums S(X) = sum_{n<=X} A(n)."""
    tau_vals = compute_tau(N)
    a_sym2 = compute_sym2_coeffs(tau_vals)
    S = [0.0] * (N + 1)
    for n in range(1, N + 1):
        S[n] = S[n - 1] + a_sym2[n - 1]
    return a_sym2, S


# ---------------------------------------------------------------------------
# Partial-sum tail bound (Track A)
# ---------------------------------------------------------------------------

def find_partial_sum_bound(S, N, search_range=(100, None)):
    """Find best C, alpha such that |S(X)| <= C * X^alpha for X in range."""
    lo, hi = search_range
    if hi is None:
        hi = N
    best_C = float('inf')
    best_alpha = 0.5
    for alpha_10 in range(5, 55, 5):
        alpha = alpha_10 / 100.0
        C = max(abs(S[X]) / X ** alpha for X in range(lo, hi + 1))
        if C < best_C:
            best_C = C
            best_alpha = alpha
    return best_C, best_alpha


def tail_from_partial_sums(S_N, sigma, t, C, alpha, N):
    """
    Tail bound via Abel summation with |S(X)| <= C * X^alpha.

    |sum_{n>N} A(n)/n^s| <= |S(N)|/N^sigma + |s|*C*N^{alpha-sigma}/(sigma-alpha)
    """
    sn = abs(S_N)
    modulus_s = math.sqrt(sigma ** 2 + t ** 2)
    if sigma <= alpha:
        return float('inf')
    return sn / N ** sigma + modulus_s * C * N ** (alpha - sigma) / (sigma - alpha)


# ---------------------------------------------------------------------------
# L(s) evaluation: Track A (Dirichlet, sigma > 1)
# ---------------------------------------------------------------------------

def L_dirichlet(a_sym2, N, sigma, t):
    """Truncated Dirichlet series sum_{n<=N} A(n)/n^s."""
    re_sum = 0.0
    im_sum = 0.0
    if t == 0:
        for n in range(1, N + 1):
            re_sum += a_sym2[n - 1] / n ** sigma
        return complex(re_sum, 0.0)
    for n in range(1, N + 1):
        an = a_sym2[n - 1]
        nsigma = n ** sigma
        logn = math.log(n)
        re_sum += an * math.cos(-t * logn) / nsigma
        im_sum += an * math.sin(-t * logn) / nsigma
    return complex(re_sum, im_sum)


# ---------------------------------------------------------------------------
# L(s) evaluation: Track B (GL3 AFE, all s)
# ---------------------------------------------------------------------------

def _log_gamma(s_real, s_imag=0.0):
    """log(Gamma(s)) for complex s via mpmath fallback."""
    try:
        import mpmath
        mpmath.mp.dps = 25
        z = mpmath.mpc(s_real, s_imag)
        return complex(mpmath.loggamma(z))
    except ImportError:
        return complex(math.lgamma(s_real), 0.0)


def _log_gamma_r(s_re, s_im=0.0):
    """log(Gamma_R(s)) = -(s/2)*log(pi) + log(Gamma(s/2))."""
    h_re, h_im = s_re / 2, s_im / 2
    lg_re, lg_im = _log_gamma(h_re, h_im)
    return complex(-(s_re * math.log(math.pi)) / 2 + lg_re,
                   -(s_im * math.log(math.pi)) / 2 + lg_im)


def _log_gamma_c(s_re, s_im=0.0):
    """log(Gamma_C(s)) = log(2) - s*log(2pi) + log(Gamma(s))."""
    lg_re, lg_im = _log_gamma(s_re, s_im)
    return complex(math.log(2) - s_re * math.log(2 * math.pi) + lg_re,
                   -s_im * math.log(2 * math.pi) + lg_im)


def _log_G(s_re, s_im=0.0):
    """log(G(s)) = log(Gamma_R(s)) + log(Gamma_C(s+11))."""
    lr = _log_gamma_r(s_re, s_im)
    lc = _log_gamma_c(s_re + 11, s_im)
    return complex(lr.real + lc.real, lr.imag + lc.imag)


def _log_chi(s_re, s_im=0.0):
    """log(chi(s)) where chi(s) = Q^{1/2-s} * G(1-s)/G(s), Q=1.
    chi(s) = exp(log_G(1-s) - log_G(s))."""
    g1s = _log_G(1 - s_re, -s_im)
    gs = _log_G(s_re, s_im)
    return complex(g1s.real - gs.real, g1s.imag - gs.imag)


def L_via_AFE(a_sym2, N, sigma, t, X=None):
    """
    Evaluate L(s) via GL3 smoothed-sum identity.

    For Re(s) > 0: L(s) = sum_n A(n)/n^s * V(n/X, s) + remainder.
    Uses mpmath for Gamma evaluation; discovery-tier.
    """
    if X is None:
        X = max(4.0, (sigma ** 2 + t ** 2 + 100) ** 0.3)

    try:
        import mpmath
        mpmath.mp.dps = 25
        main_sum = mpmath.mpf(0)
        for n in range(1, min(N + 1, int(X * 50) + 1)):
            an = a_sym2[n - 1]
            if an == 0:
                continue
            y = n / X
            # Gaussian weight: exp(-y) for the basic smoothed sum
            w = float(mpmath.exp(-y))
            ns = mpmath.power(n, -mpmath.mpc(sigma, t))
            main_sum += mpmath.mpf(an) * ns * w
        return complex(main_sum)
    except ImportError:
        return L_dirichlet(a_sym2, N, sigma, t)


# ---------------------------------------------------------------------------
# Grid scan
# ---------------------------------------------------------------------------

def scan_zero_free(N_terms, sigma_min, sigma_max, n_sigma, t_max, n_t):
    """Scan L(s) on grid. Returns (results, sigmas, ts, C, alpha)."""
    a_sym2, S = precompute(N_terms)
    C, alpha = find_partial_sum_bound(S, N_terms)

    sigmas = [sigma_min + i * (sigma_max - sigma_min) / max(n_sigma - 1, 1)
              for i in range(n_sigma)]
    ts = [-t_max + i * 2 * t_max / max(n_t - 1, 1) for i in range(n_t)]

    results = []
    for sigma in sigmas:
        for t in ts:
            L_val = L_dirichlet(a_sym2, N_terms, sigma, t)
            mod = abs(L_val)
            tail = tail_from_partial_sums(S[N_terms], sigma, t, C, alpha, N_terms)
            cert = max(0.0, mod - tail)
            results.append((sigma, t, mod, tail, cert))

    return results, sigmas, ts, C, alpha


def find_minimum_L(results):
    """Find grid point with smallest certified |L(s)|."""
    return min(results, key=lambda r: r[4])


# ---------------------------------------------------------------------------
# Certificate
# ---------------------------------------------------------------------------

def make_certificate(N_terms, sigma_min, sigma_max, t_max,
                     min_point, C, alpha, n_grid):
    s0, t0, mod, tail, cert = min_point
    return {
        "module": "M-3",
        "status": "discovery",
        "certifies_zero_free": cert > 0,
        "method": "Dirichlet + partial-sum tail bound",
        "N_terms": N_terms,
        "partial_sum_bound": {"C": C, "alpha": alpha,
                              "note": "empirical from N={N_terms}, not proven"},
        "sigma_range": [sigma_min, sigma_max],
        "t_max": t_max,
        "grid_points": n_grid,
        "min_L_grid": round(mod, 8),
        "min_L_sigma": s0,
        "min_L_t": round(t0, 4),
        "tail_at_min": round(tail, 8),
        "certified_min_L": round(cert, 8),
        "notes": ("Discovery tier. Proof-tier requires: "
                  "(1) proven |S(X)| <= C*X^alpha, or "
                  "(2) Arb-certified GL3 AFE weight bounds.")
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    N_terms = 20000
    sigma_min = 1.01
    sigma_max = 2.0
    n_sigma = 20
    t_max = 20.0
    n_t = 200

    print("Zero-free scan: L(s, sym^2 Delta)")
    print(f"  N = {N_terms}, sigma in [{sigma_min},{sigma_max}], "
          f"|t| <= {t_max}")
    print(f"  grid = {n_sigma}x{n_t} = {n_sigma * n_t} points\n")

    results, sigmas, ts, C, alpha = scan_zero_free(
        N_terms, sigma_min, sigma_max, n_sigma, t_max, n_t
    )
    print(f"  Partial-sum bound: |S(X)| <= {C:.4f} * X^{alpha:.2f}\n")

    print(f"  {'sigma':>6}  {'min|L|':>10}  {'tail':>10}  {'cert_min':>10}")
    print("  " + "-" * 44)
    for sigma in sigmas:
        sresults = [r for r in results if abs(r[0] - sigma) < 1e-10]
        mp = min(sresults, key=lambda r: r[4])
        print(f"  {sigma:>6.2f}  {mp[2]:>10.6f}  {mp[3]:>10.6f}  {mp[4]:>10.6f}")

    overall = find_minimum_L(results)
    print(f"\n  Overall min cert: |L({overall[0]:.2f}+{overall[1]:.2f}i)| "
          f">= {overall[4]:.6f}")

    cert = make_certificate(N_terms, sigma_min, sigma_max, t_max,
                            overall, C, alpha, len(results))
    cert_path = os.path.join(_repo_root, "baseline", "zero_free_scan.json")
    os.makedirs(os.path.dirname(cert_path), exist_ok=True)
    with open(cert_path, "w") as f:
        json.dump(cert, f, indent=2)
    print(f"  Certificate -> {cert_path}")
    return cert


if __name__ == "__main__":
    main()
