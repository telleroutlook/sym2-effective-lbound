"""
check_grid.py -- Independent checker for OB-04 grid values.

Spot-checks L(s) values from witness/grid_values.json using a
completely independent implementation (no imports from src/).

For Re(s) > 1: recomputes L(s) via truncated Dirichlet series.
For critical strip: recomputes via AFE weight (mpmath).

Usage:
    python3 check_grid.py [--witness PATH]

Exit code: 0 if all checks pass, 1 otherwise.
"""

import json
import math
import os
import sys

try:
    import mpmath
except ImportError:
    print("FAIL: mpmath required")
    sys.exit(1)

mp = mpmath
mp.mp.dps = 30


# ===================================================================
# Independent tau computation (same algorithm, no repo imports)
# ===================================================================

def _compute_tau(N):
    p = [0] * (N + 1)
    p[0] = 1
    for k in range(1, N + 1):
        for _ in range(24):
            for n in range(N, k - 1, -1):
                p[n] -= p[n - k]
    return [p[n - 1] for n in range(1, N + 1)]


def _compute_sym2(tau_vals):
    N = len(tau_vals)
    c = [0.0] * (N + 1)
    c[1] = 1.0
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    sp = [0] * (N + 1)
    for p in range(2, N + 1):
        if is_prime[p]:
            sp[p] = p
            cp = tau_vals[p - 1] / p ** 5.5
            c2 = cp * cp
            mk = max(1, int(math.log(N, p)) + 1)
            ap = [0.0] * (mk + 1)
            ap[0] = 1.0
            ap[1] = c2 - 1.0
            if mk >= 2:
                ap[2] = (c2 - 1) * ap[1] - (c2 - 1) * ap[0]
            for k in range(3, mk + 1):
                ap[k] = ((c2 - 1) * ap[k - 1]
                         - (c2 - 1) * ap[k - 2]
                         + ap[k - 3])
            pk = p
            k = 1
            while pk <= N:
                c[pk] = ap[k]
                pk *= p
                k += 1
            j = p * p
            while j <= N:
                is_prime[j] = False
                if sp[j] == 0:
                    sp[j] = p
                j += p
    for n in range(4, N + 1):
        if is_prime[n]:
            continue
        p = sp[n]
        m = n // p
        pk = p
        k = 1
        while m % p == 0:
            m //= p
            pk *= p
            k += 1
        if m != 1:
            c[n] = c[pk] * c[m]
    return [c[i] for i in range(1, N + 1)]


# ===================================================================
# Independent L(s) via Dirichlet series (Re(s) > 1)
# ===================================================================

def _L_dirichlet(a, N, sigma, t):
    re_s, im_s = 0.0, 0.0
    for n in range(1, N + 1):
        an = a[n - 1]
        nsigma = n ** sigma
        if t == 0:
            re_s += an / nsigma
        else:
            logn = math.log(n)
            re_s += an * math.cos(-t * logn) / nsigma
            im_s += an * math.sin(-t * logn) / nsigma
    return complex(re_s, im_s)


# ===================================================================
# Independent Gamma + AFE weight
# ===================================================================

def _gamma_r(s):
    return mp.power(mp.pi, -s / 2) * mp.gamma(s / 2)


def _gamma_c(s):
    return 2 * mp.power(2 * mp.pi, -s) * mp.gamma(s)


def _G(s):
    return _gamma_r(s) * _gamma_c(s + 11)


def _afe_weight(y, s, T=30.0, n_quad=500):
    y_mp = mp.mpf(y)
    Gs = _G(s)
    dt = 2 * T / n_quad
    integral = mp.mpc(0)
    for i in range(n_quad):
        tau = -T + (i + 0.5) * dt
        u = mp.mpc(1, tau)
        Gu = _G(s + u)
        integral += (Gu / Gs) * mp.power(y_mp, -u) * mp.exp(u * u) / u * dt
    return integral / (2 * mp.pi)


def _L_afe(a, s, X=12.0, N_terms=60):
    total = mp.mpc(0)
    for n in range(1, min(N_terms + 1, len(a) + 1)):
        an = mp.mpf(a[n - 1])
        if an == 0:
            continue
        y = mp.mpf(n) / mp.mpf(X)
        V = _afe_weight(y, s)
        total += an * mp.power(mp.mpf(n), -s) * V
    return total


# ===================================================================
# Main checker
# ===================================================================

def check(witness_path):
    with open(witness_path) as f:
        data = json.load(f)

    cert = data["certificate"]
    grid = data["grid"]

    # Recompute coefficients
    N = cert["N_terms"]
    tau = _compute_tau(N)
    a = _compute_sym2(tau)
    print(f"Recomputed A(n): A(1)={a[0]}, A(2)={a[1]:.4f}, A(3)={a[2]:.4f}")

    # Spot-check: L(2) via Dirichlet
    L2 = _L_dirichlet(a, N, 2.0, 0.0)
    L2_val = float(mp.re(L2))
    L2_expected = cert.get("spot_L2", 0.806)
    err = abs(L2_val - L2_expected)
    status = "PASS" if err < 0.01 else "FAIL"
    print(f"  L(2) = {L2_val:.6f}  (expected {L2_expected:.6f}, err={err:.6f}) [{status}]")

    if status == "FAIL":
        return False

    # Spot-check grid points
    X = cert["X"]
    all_pass = True
    n_checked = 0
    for r in grid:
        sigma, t = r["sigma"], r["t"]
        s = mp.mpc(sigma, t)

        if sigma > 1.0:
            L_recomputed = _L_dirichlet(a, N, sigma, t)
        else:
            L_recomputed = _L_afe(a, s, X=X, N_terms=min(60, N))

        mod_recomputed = float(abs(L_recomputed))
        reported = r["L_mod"]
        rel_err = abs(mod_recomputed - reported) / max(reported, 1e-10)

        if rel_err < 0.1:
            status = "PASS"
        else:
            status = "FAIL"
            all_pass = False
        n_checked += 1
        print(f"  L({sigma:.2f}+{t:.2f}i): reported={reported:.6f} "
              f"recomputed={mod_recomputed:.6f} rel_err={rel_err:.2e} [{status}]")

    print(f"\nChecked {n_checked} grid points + 1 spot-check.")
    overall = "PASS" if all_pass else "FAIL"
    print(f"OVERALL: {overall}")
    return all_pass


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", default=None)
    args = parser.parse_args()

    if args.witness is None:
        args.witness = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "witness", "grid_values.json"
        )

    ok = check(args.witness)
    sys.exit(0 if ok else 1)
