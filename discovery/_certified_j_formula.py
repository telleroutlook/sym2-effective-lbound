"""
_certified_j_formula.py -- Absolutely convergent formula for J.

THEOREM (claim, to be verified numerically):

  J = sum_n a(n)/n^{1/2} * w_new(n)

where

  w_new(n) = w_Vplus(n) - w_Vdual(n)

  w_Vplus(n) = (1/2pi) int Re[ n^{-it} * V_afe(n/X, 1/2+it) * amp1(t) ] dt

  w_Vdual(n) = (1/2pi) int Re[ n^{it} * V_dual(n, t) * amp1(t) ] dt

with

  V_afe(y, s0) = (1/2pi i) int_{Re(u)=1} G(s0+u)/G(s0) * y^{-u} * e^{u^2}/u du
  V_dual(n, t) = (1/2pi i) int_{Re(v)=1/2} (12/n)^v * G(1/2-it+v)/G(1/2+it) * e^{v^2}/v dv

DERIVATION:
  1. AFE at s0=1/2+it:  L(1/2+it) = S1_afe(t) - J_afe(t)
  2. J_afe(t) uses L on Re(s)=0. Apply GL3 functional equation to get L on Re(s)=1 (abs. convergent):
     J_afe(t) = sum_n a(n)/n^{1/2-it} * V_dual(n,t)
  3. L(1/2+it) = sum_n a(n)/n^{1/2+it} * V_afe(n/X,1/2+it) - sum_n a(n)/n^{1/2-it} * V_dual(n,t)
  4. J = (1/2pi) int Re[L(1/2+it) * amp1(t)] dt
       = sum_n a(n)/n^{1/2} * [w_Vplus(n) - w_Vdual(n)]
     (swap sum/integral by absolute convergence of double-Gaussian weights)

ABSOLUTE CONVERGENCE of the new series:
  |w_new(n)| ~ C * exp(-c*(log n)^2/4)   [Gaussian in log n]
  |a(n)| <= d_3(n) ~ (log n)^2
  => |a(n)/n^{1/2} * w_new(n)| ~ exp(-(c/4)*(log n)^2 + eps*log n)
  => sum converges absolutely with ~20 terms needed for 10^{-6} precision.

This formula requires NO zero-free region and NO Voronoi formula.
It is a consequence of the GL3 AFE applied at s0=1/2+it with functional equation.
"""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 30
from discovery.afe_gl3 import G_factor
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs

mp = mpmath
k = 12
Q = mp.mpf(144)
X = mp.mpf(12)
G1 = G_factor(mp.mpf(1), k, mp)

N_COEFF = 25
tau_arr = compute_tau(N_COEFF)
a_sym2 = compute_sym2_coeffs(tau_arr)


def amp1(t_val):
    """amp1(t) = G(1/2+it)/G(1) * X^{-1/2+it} * exp((-1/2+it)^2)/(-1/2+it)."""
    s = mp.mpc(mp.mpf('0.5'), mp.mpf(str(t_val)))
    w = s - 1
    return (G_factor(s, k, mp) / G1) * mp.power(X, w) * mp.exp(w**2) / w


def V_afe(y_val, s0_val, n_u=150, T_u=15.0):
    """
    V_afe(y, s0) = (1/2pi i) int_{Re(u)=1} G(s0+u)/G(s0) * y^{-u} * e^{u^2}/u du
    Contour Re(u)=1, parameterized as u=1+i*t_u.
    """
    y = mp.mpf(y_val)
    s0 = s0_val  # complex mpf
    Gs0 = G_factor(s0, k, mp)
    dt = mp.mpf(2 * T_u) / n_u
    total = mp.mpf(0)
    for i in range(n_u):
        t_u = mp.mpf(-T_u) + (i + mp.mpf('0.5')) * dt
        u = mp.mpc(1, t_u)
        Gsu = G_factor(s0 + u, k, mp)
        total += mp.re(Gsu / Gs0 * mp.power(y, -u) * mp.exp(u**2) / u) * dt
    return total / (2 * mp.pi)


def V_dual(n_val, t_val, n_v=150, T_v=15.0):
    """
    V_dual(n, t) = (1/2pi i) int_{Re(v)=1/2} (12/n)^v * G(1/2-it+v)/G(1/2+it) * e^{v^2}/v dv
    Contour Re(v)=1/2, parameterized as v=1/2+i*t_v.
    """
    ratio = mp.mpf(12) / mp.mpf(n_val)
    t = mp.mpf(str(t_val))
    s0 = mp.mpc(mp.mpf('0.5'), t)       # G at s0 = 1/2+it (denominator)
    s0_conj = mp.mpc(mp.mpf('0.5'), -t) # G at 1/2-it (used with shift v)
    Gs0 = G_factor(s0, k, mp)
    dt = mp.mpf(2 * T_v) / n_v
    total = mp.mpf(0)
    for i in range(n_v):
        t_v = mp.mpf(-T_v) + (i + mp.mpf('0.5')) * dt
        v = mp.mpc(mp.mpf('0.5'), t_v)
        Gv = G_factor(s0_conj + v, k, mp)  # G(1/2-it+v)
        total += mp.re(mp.power(ratio, v) * Gv / Gs0 * mp.exp(v**2) / v) * dt
    return total / (2 * mp.pi)


def compute_w_new(n_val, T_outer=5.0, n_outer=80, n_inner=100, T_inner=10.0):
    """
    J = sum_n a(n)/n^{1/2} * w_new(n)  with  w_new = w_Vplus - w_Vdual.

    From the AFE at s0=1/2+it, after applying the GL3 functional equation to J_afe:
      L(1/2+it) = S1_afe(t) - J_afe_FE(t)
    where
      S1_afe(t)   = sum_n a(n)/n^{1/2+it} * V_afe(n/X, 1/2+it)
      J_afe_FE(t) = Q^{-it} * sum_n a(n)/n^{1/2-it} * V_dual(n, t)

    So J = int Re[L(1/2+it)*amp1(t)]dt/2pi
         = sum_n a(n)/n^{1/2} * [w_Vplus(n) - w_Vdual(n)]

    w_Vplus(n)  = (1/2pi) int Re[ n^{-it}          * V_afe(n/X, 1/2+it) * amp1(t) ] dt
    w_Vdual(n)  = (1/2pi) int Re[ Q^{-it} * n^{it} * V_dual(n, t)       * amp1(t) ] dt
                = (1/2pi) int Re[ (n/Q)^{it}         * V_dual(n, t)       * amp1(t) ] dt
    """
    n = mp.mpf(n_val)
    y = n / X  # argument for V_afe: n/X = n/12
    dt = mp.mpf(2 * T_outer) / n_outer
    w_plus = mp.mpf(0)
    w_dual = mp.mpf(0)

    for i in range(n_outer):
        t = mp.mpf(-T_outer) + (i + mp.mpf('0.5')) * dt
        a1 = amp1(t)
        s0 = mp.mpc(mp.mpf('0.5'), t)
        nit = mp.power(n, -mp.mpc(0, t))        # n^{-it}
        nQit = mp.power(n / Q, mp.mpc(0, t))    # (n/Q)^{it} = n^{it}/Q^{it}

        # V_afe at this t (inner Mellin integral at Re(u)=1)
        Vp = V_afe(float(y), s0, n_u=n_inner, T_u=T_inner)
        # V_dual at this t (inner Mellin integral at Re(v)=1/2, includes FE factors)
        Vd = V_dual(n_val, float(t), n_v=n_inner, T_v=T_inner)

        w_plus += mp.re(nit * Vp * a1) * dt
        w_dual += mp.re(nQit * Vd * a1) * dt    # (n/Q)^{it} from J_afe_FE formula

    w_plus /= 2 * mp.pi
    w_dual /= 2 * mp.pi
    return float(w_plus), float(w_dual), float(w_plus - w_dual)


if __name__ == "__main__":
    S1_N2000 = 0.54830205
    J_CESARO = -0.0834

    print("Computing w_new(n) = w_Vplus(n) - w_Vdual(n) for n=1..15")
    print(f"  {'n':>4}  {'a(n)':>10}  {'w_Vplus':>12}  {'w_Vdual':>12}  {'w_new':>12}  {'term':>12}")

    J_new = 0.0
    for n in range(1, 16):
        an = float(a_sym2[n - 1])
        wp, wd, wn = compute_w_new(n)
        term = an / n**0.5 * wn
        J_new += term
        print(f"  {n:>4}  {an:>+10.4f}  {wp:>+12.6f}  {wd:>+12.6f}  {wn:>+12.6f}  {term:>+12.6e}")

    print()
    print(f"J_new (N=15) = {J_new:.7f}")
    print(f"J_cesaro     = {J_CESARO:.7f}")
    print(f"Difference   = {J_new - J_CESARO:.4e}")
    print()
    L1_new = S1_N2000 - J_new
    print(f"L(1) = S1 - J_new = {S1_N2000} - ({J_new:.7f}) = {L1_new:.7f}")
    print(f"L(1) Tauberian  = 0.6314")
