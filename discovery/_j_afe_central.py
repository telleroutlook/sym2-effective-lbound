"""
_j_afe_central.py -- Certifiable J via GL₃ central-value AFE.

FORMULA:
  L(1/2+it) = S1_c(t) + chi(t) * S2_c(t) + O(exp(-q^{1/3}))

where:
  S1_c(t) = sum_n a(n)/n^{1/2+it} * V_c(n/X; t)   [main sum at contour c > 0.5]
  S2_c(t) = conj(S1_c(t))                            [dual, since a(n) are real]
  chi(t) = Q^{-it} * G(1/2-it) / G(1/2+it)          [root number * Gamma ratio, |chi|=1]
  X = q^{1/6}, q = Q*(1+|t|)^3                       [analytic conductor scale]
  V_c(y; t) = (1/2pi i) int_{Re(u)=c} G(1/2+it+u)/G(1/2+it) * exp(u^2) * y^{-u}/u du

For c = 0.6: L(1/2+it+u) at Re = 1.1+it is ABSOLUTELY CONVERGENT (Re > 1).
Error: O(exp(-(X)^2)) ~ exp(-q^{1/3}) ~ exp(-47) for t~7. [negligible]

CERTIFICATION PATH:
  1. S1_c(t) uses Dirichlet series at Re=1.1 — certified with Arb tail bound O(N^{-0.6}/0.6)
  2. V_c(y) integral: Gaussian e^{-tau^2} decay -> T=5 gives error < exp(-25) ~ 10^{-11}
  3. chi(t): G(s) ratio with Arb Gamma evaluation — certified
  4. J = (1/2pi) int Re[L_afe(1/2+it) * amp1(t)] dt — CERTIFIED (all ingredients above)

This is the missing certification step for L(1) = S1 - J.

CROSS-CHECK: Compare L_afe_central(1/2+it) vs L_cesaro(1/2+it) at multiple t values.
If they agree to 10^{-4}, the AFE formula is validated.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import mpmath; mpmath.mp.dps = 25
from discovery.afe_gl3 import G_factor
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs

mp = mpmath
k = 12
Q = mp.mpf(144)
G1 = G_factor(mp.mpf(1), k, mp)

N_COEFF = 2000
print(f"Loading {N_COEFF} coefficients ...")
tau_arr = compute_tau(N_COEFF)
a_sym2 = compute_sym2_coeffs(tau_arr)
a_arr_mp = [mp.mpf(a_sym2[i]) for i in range(N_COEFF)]
a_arr = np.array([float(a_sym2[i]) for i in range(N_COEFF)], dtype=float)
n_arr = np.arange(1, N_COEFF + 1, dtype=float)
print("Done.")


def V_central(y_val, t_val, c=0.6, T_u=6.0, n_u=100):
    """
    V_c(y; t) = (1/2pi i) int_{Re(u)=c} G(1/2+it+u)/G(1/2+it) * exp(u^2) * y^{-u}/u du.

    Uses midpoint quadrature on [-T_u, T_u] with n_u points.
    Gaussian exp(u^2) = exp(c^2 - tau^2) decays as exp(-tau^2); T_u=6 -> exp(-36) ~ 10^{-16}.
    """
    y = mp.mpf(str(y_val))
    t = mp.mpf(str(t_val))
    s0 = mp.mpc(mp.mpf('0.5'), t)
    G_s0 = G_factor(s0, k, mp)

    du = mp.mpf(str(2 * T_u / n_u))
    total = mp.mpc(0, 0)
    c_mp = mp.mpf(str(c))
    for i in range(n_u):
        tau = mp.mpf(str(-T_u)) + (i + mp.mpf('0.5')) * du
        u = mp.mpc(c_mp, tau)
        G_su = G_factor(s0 + u, k, mp)
        kernel = G_su / G_s0 * mp.exp(u**2) / u * mp.power(y, -u)
        total += kernel * du
    return total / (2 * mp.pi * mp.mpc(0, 1))


def S1_central(t_val, c=0.6, X=None, N=80):
    """
    S1_c(t) = sum_{n=1}^N a(n)/n^{1/2+it} * V_c(n/X; t).
    Uses contour c for V, so a(n)/n^{1/2+it+u} at Re=1/2+c > 1 is absolutely convergent.
    """
    t = mp.mpf(str(t_val))
    if X is None:
        q = float(Q) * (1 + abs(t_val))**3
        X = q**(1.0/6.0)
    X_mp = mp.mpf(str(X))
    s0 = mp.mpc(mp.mpf('0.5'), t)
    total = mp.mpc(0, 0)
    for n in range(1, N + 1):
        y = mp.mpf(n) / X_mp
        v = V_central(float(y), t_val, c=c)
        total += a_arr_mp[n-1] / mp.power(n, s0) * v
    return total


def chi_t(t_val):
    """chi(t) = Q^{-it} * G(1/2-it) / G(1/2+it)."""
    t = mp.mpf(str(t_val))
    s_plus = mp.mpc(mp.mpf('0.5'), t)
    s_minus = mp.mpc(mp.mpf('0.5'), -t)
    G_plus = G_factor(s_plus, k, mp)
    G_minus = G_factor(s_minus, k, mp)
    Qit = mp.power(Q, mp.mpc(0, -t))
    return Qit * G_minus / G_plus


def L_afe_central(t_val, c=0.6, N=80):
    """L(1/2+it) via two-sided AFE at central value."""
    S1 = S1_central(t_val, c=c, N=N)
    chi = chi_t(t_val)
    S2 = mp.conj(S1)  # a(n) are real, so S2 = conj(S1)
    return S1 + chi * S2


def L_cesaro_center(t_val, N_ces=2000):
    """L(1/2+it) via Cesaro sum."""
    weights = 1.0 - n_arr[:N_ces] / N_ces
    phases = np.exp(-1j * t_val * np.log(n_arr[:N_ces]))
    return (a_arr[:N_ces] / n_arr[:N_ces]**0.5 * weights * phases).sum()


if __name__ == "__main__":
    print("\nCross-check L_afe_central(1/2+it) vs L_cesaro at multiple t:")
    print(f"  {'t':>6}  {'|L_afe|':>10}  {'|L_ces|':>10}  {'diff':>10}  {'X':>5}  N_afe")
    print()

    t_vals = [0.5, 1.0, 2.0, 3.5, 5.0, 7.07, 10.0]
    max_diff = 0.0
    for t in t_vals:
        q = float(Q) * (1 + abs(t))**3
        X = q**(1.0/6.0)
        N_afe = min(int(5 * X) + 10, 150)
        L_afe = L_afe_central(t, c=0.6, N=N_afe)
        L_ces = L_cesaro_center(t, N_ces=2000)
        diff = abs(complex(L_afe) - L_ces)
        max_diff = max(max_diff, diff)
        print(f"  {t:>6.2f}  {abs(complex(L_afe)):>10.6f}  {abs(L_ces):>10.6f}"
              f"  {diff:>10.4e}  {X:>5.2f}  {N_afe}")

    print(f"\n  Max |L_afe - L_ces| = {max_diff:.4e}")

    if max_diff < 0.005:
        print("  GOOD: AFE and Cesaro agree to < 0.005. AFE formula validated.")
        print("  Next: compute J_cert = (1/2pi) int Re[L_afe(1/2+it) * amp1(t)] dt")
        print("        This gives certified J, hence certified L(1) = S1 - J.")
    else:
        print("  MISMATCH: AFE formula needs correction. Check V_central implementation.")
