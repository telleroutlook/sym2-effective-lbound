"""
_certified_j_probe.py -- Fast convergence probe for the absolutely convergent J formula.

Runs the w_new(n) series up to N=80 with reduced quadrature parameters
(mpmath dps=15, fewer integration points) to check convergence speed.

The formula J = sum_n a(n)/n^{1/2} * [w_Vplus(n) - w_Vdual(n)] is absolutely
convergent, but for n < 12 the Gaussian decay does not yet apply.
This probe checks how many terms are needed to reach J_cesaro = -0.0834.
"""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 15  # reduced for speed
from discovery.afe_gl3 import G_factor
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs

mp = mpmath
k = 12
Q = mp.mpf(144)
X = mp.mpf(12)
G1 = G_factor(mp.mpf(1), k, mp)

N_COEFF = 100
tau_arr = compute_tau(N_COEFF)
a_sym2 = compute_sym2_coeffs(tau_arr)


def amp1(t_val):
    s = mp.mpc(mp.mpf('0.5'), mp.mpf(str(t_val)))
    w = s - 1
    return (G_factor(s, k, mp) / G1) * mp.power(X, w) * mp.exp(w**2) / w


def V_afe_fast(y_val, s0_val, n_u=50, T_u=8.0):
    y = mp.mpf(y_val)
    s0 = s0_val
    Gs0 = G_factor(s0, k, mp)
    dt = mp.mpf(2 * T_u) / n_u
    total = mp.mpf(0)
    for i in range(n_u):
        t_u = mp.mpf(-T_u) + (i + mp.mpf('0.5')) * dt
        u = mp.mpc(1, t_u)
        Gsu = G_factor(s0 + u, k, mp)
        total += mp.re(Gsu / Gs0 * mp.power(y, -u) * mp.exp(u**2) / u) * dt
    return total / (2 * mp.pi)


def V_dual_fast(n_val, t_val, n_v=50, T_v=8.0):
    ratio = mp.mpf(12) / mp.mpf(n_val)
    t = mp.mpf(str(t_val))
    s0 = mp.mpc(mp.mpf('0.5'), t)
    s0_conj = mp.mpc(mp.mpf('0.5'), -t)
    Gs0 = G_factor(s0, k, mp)
    dt = mp.mpf(2 * T_v) / n_v
    total = mp.mpf(0)
    for i in range(n_v):
        t_v = mp.mpf(-T_v) + (i + mp.mpf('0.5')) * dt
        v = mp.mpc(mp.mpf('0.5'), t_v)
        Gv = G_factor(s0_conj + v, k, mp)
        total += mp.re(mp.power(ratio, v) * Gv / Gs0 * mp.exp(v**2) / v) * dt
    return total / (2 * mp.pi)


def compute_w_new_fast(n_val, T_outer=3.5, n_outer=40):
    n = mp.mpf(n_val)
    y = n / X
    dt = mp.mpf(2 * T_outer) / n_outer
    w_plus = mp.mpf(0)
    w_dual = mp.mpf(0)
    for i in range(n_outer):
        t = mp.mpf(-T_outer) + (i + mp.mpf('0.5')) * dt
        a1 = amp1(t)
        s0 = mp.mpc(mp.mpf('0.5'), t)
        nit = mp.power(n, -mp.mpc(0, t))
        nQit = mp.power(n / Q, mp.mpc(0, t))
        Vp = V_afe_fast(float(y), s0)
        Vd = V_dual_fast(n_val, float(t))
        w_plus += mp.re(nit * Vp * a1) * dt
        w_dual += mp.re(nQit * Vd * a1) * dt
    w_plus /= 2 * mp.pi
    w_dual /= 2 * mp.pi
    return float(w_plus), float(w_dual), float(w_plus - w_dual)


if __name__ == "__main__":
    S1 = 0.54830205
    J_CESARO = -0.0834

    print("n  w_Vplus     w_Vdual     w_new       term        J_cumul     J_abs_cumul")
    J_cum = 0.0
    J_abs = 0.0
    for n in range(1, N_COEFF + 1):
        an = float(a_sym2[n - 1])
        wp, wd, wn = compute_w_new_fast(n)
        term = an / n**0.5 * wn
        J_cum += term
        J_abs += abs(term)
        print(f"{n:3d}  {wp:+.5e}  {wd:+.5e}  {wn:+.5e}  {term:+.3e}  {J_cum:+.6f}  {J_abs:.6f}")
        sys.stdout.flush()

    print()
    print(f"J_new(N={N_COEFF})  = {J_cum:.7f}")
    print(f"J_cesaro        = {J_CESARO:.7f}")
    print(f"L(1) estimate   = {S1 - J_cum:.7f}  (Tauberian: 0.6314)")
