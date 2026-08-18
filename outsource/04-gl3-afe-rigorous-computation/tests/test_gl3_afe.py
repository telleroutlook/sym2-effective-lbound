"""Tests for the GL_3 AFE computation (outsource batch 04)."""
import math
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)


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
                ap[k] = (c2 - 1) * ap[k - 1] - (c2 - 1) * ap[k - 2] + ap[k - 3]
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


def test_L_at_sigma2():
    """L(2) should be ~ 0.806 via truncated Dirichlet series."""
    N = 5000
    tau = _compute_tau(N)
    a = _compute_sym2(tau)
    L2 = sum(a[n - 1] / n ** 2.0 for n in range(1, N + 1))
    assert abs(L2 - 0.806) < 0.01, f"L(2) = {L2:.6f}"


def test_L_positive_real():
    """L(sigma) > 0 for real sigma > 1 (Euler product)."""
    N = 2000
    tau = _compute_tau(N)
    a = _compute_sym2(tau)
    for sigma in [1.5, 2.0, 3.0]:
        Ls = sum(a[n - 1] / n ** sigma for n in range(1, N + 1))
        assert Ls > 0, f"L({sigma}) = {Ls:.6f} <= 0"


def test_sym2_A1():
    """A(1) = 1 by definition."""
    tau = _compute_tau(10)
    a = _compute_sym2(tau)
    assert a[0] == 1.0


def test_sym2_A2():
    """A(2) = c_2^2 - 1 where c_2 = tau(2)/2^{5.5}."""
    tau = _compute_tau(10)
    a = _compute_sym2(tau)
    c2 = tau[1] / (2 ** 5.5)
    expected = c2 * c2 - 1
    assert abs(a[1] - expected) < 1e-6, f"A(2) = {a[1]}, expected {expected}"


def test_afe_weight_decays():
    """V(y, s) should decay for large y (Gaussian decay)."""
    import os
    import sys
    _src = os.path.join(os.path.dirname(__file__), "..", "src")
    if _src not in sys.path:
        sys.path.insert(0, _src)
    from afe_sym2 import afe_weight, mp
    s = mp.mpc(1.0, 0.0)
    V_small = abs(afe_weight(0.5, s, T=20, n_quad=200))
    V_large = abs(afe_weight(5.0, s, T=20, n_quad=200))
    assert V_small > V_large, f"V(0.5)={V_small:.4f} should > V(5.0)={V_large:.4f}"


def test_afe_L2_matches_dirichlet():
    """L(1.0) via AFE should be positive and in reasonable range."""
    import os
    import sys
    _src = os.path.join(os.path.dirname(__file__), "..", "src")
    if _src not in sys.path:
        sys.path.insert(0, _src)
    from afe_sym2 import L_via_AFE, mp, compute_tau, compute_sym2_coeffs
    N = 200
    tau = compute_tau(N)
    a = compute_sym2_coeffs(tau)
    s = mp.mpc(1.0, 0.0)
    L_a = float(mp.re(L_via_AFE(a, s, X=12.0, N_terms=60)))
    assert L_a > 0, f"L(1.0) via AFE = {L_a:.6f} <= 0"
    assert 0.4 < L_a < 0.8, f"L(1.0) via AFE = {L_a:.6f} outside [0.4, 0.8]"
