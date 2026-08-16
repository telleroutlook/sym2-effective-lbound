"""
_j_direct_quad.py -- Direct quadrature for J via L(1/2+it) Cesaro sum.

METHOD:
  J = (1/2pi) int Re[L(1/2+it) * amp1(t)] dt

  For each t_k: L(1/2+it_k) ~ sum_{n=1}^N a(n)/n^{1/2+it_k} * (1 - n/N)  [Cesaro]

  amp1(t) = G(1/2+it)/G(1) * 12^{-1/2+it} * exp((-1/2+it)^2)/(-1/2+it)

  J_quad = (dt/2pi) * sum_k Re[L_cesaro(1/2+it_k) * amp1(t_k)]

  Verification: should reproduce J_cesaro = -0.0834 from _j_wn.py.
  Two independent routes => cross-check of the w(n) method.

ADVANTAGE over w(n) route:
  - Fubini sum (w(n) route) needs N~700 terms and Cesaro averaging
  - Direct quadrature: N_coeff * N_t evaluations of a(n)/n^{1/2+it}
  - For N=1000, N_t=200: 200,000 fast complex exponential evaluations
"""
import sys; sys.path.insert(0, '.')
import math
import numpy as np
import mpmath; mpmath.mp.dps = 25
from discovery.afe_gl3 import G_factor
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs

mp = mpmath
k = 12
Q = mp.mpf(144)
X = mp.mpf(12)
G1 = G_factor(mp.mpf(1), k, mp)

N_COEFF = 2000
print(f"Loading {N_COEFF} coefficients ...")
tau_arr = compute_tau(N_COEFF)
a_sym2 = compute_sym2_coeffs(tau_arr)
a_arr = np.array([float(a_sym2[i]) for i in range(N_COEFF)], dtype=float)
n_arr = np.arange(1, N_COEFF + 1, dtype=float)
print("Done.")


def amp1_mp(t_val):
    """amp1(t) = G(1/2+it)/G(1) * 12^{-1/2+it} * exp((-1/2+it)^2)/(-1/2+it)."""
    s = mp.mpc(mp.mpf('0.5'), mp.mpf(str(t_val)))
    w = s - 1
    return complex(G_factor(s, k, mp) / G1 * mp.power(X, w) * mp.exp(w**2) / w)


def L_cesaro(t_val, N=None):
    """L(1/2+it) via Cesaro-smoothed Dirichlet series."""
    if N is None:
        N = N_COEFF
    weights = 1.0 - n_arr[:N] / N  # Cesaro weight (1-n/N)
    phases = np.exp(-1j * t_val * np.log(n_arr[:N]))  # n^{-it}
    terms = a_arr[:N] / n_arr[:N]**0.5 * weights * phases
    return terms.sum()


if __name__ == "__main__":
    S1_N2000 = 0.54830205
    J_CESARO = -0.0834

    # Quadrature nodes: [-T, T] with N_t points
    T_outer = 5.0
    N_t = 200
    t_nodes = np.linspace(-T_outer, T_outer, N_t + 1)
    dt = t_nodes[1] - t_nodes[0]

    print(f"\nComputing amp1(t) at {N_t+1} nodes ...")
    amp1_vals = np.array([amp1_mp(t) for t in t_nodes], dtype=complex)
    print("Done.")

    # Cesaro at N=2000
    print("\nDirect quadrature J with Cesaro(N=2000):")
    J_vals = []
    for N_ces in [200, 500, 1000, 2000]:
        integrand = np.array([L_cesaro(t, N_ces) for t in t_nodes]) * amp1_vals
        J_q = np.trapezoid(np.real(integrand), t_nodes) / (2 * math.pi)
        J_vals.append(J_q)
        L1 = S1_N2000 - J_q
        print(f"  N_cesaro={N_ces:5d}: J = {J_q:+.7f}  L(1) = {L1:.7f}")

    print()
    print(f"J_cesaro (from _j_wn.py) = {J_CESARO}")
    print(f"Convergence of J as N_cesaro increases:")
    for i in range(len(J_vals) - 1):
        print(f"  J({[200,500,1000,2000][i+1]}) - J({[200,500,1000,2000][i]}) = {J_vals[i+1]-J_vals[i]:+.6f}")
    print()

    # Sensitivity: check with different T_outer
    print("J sensitivity to T_outer (N_cesaro=2000):")
    for T_test in [3.0, 4.0, 5.0, 6.0]:
        t_grid = np.linspace(-T_test, T_test, 201)
        amp_grid = np.array([amp1_mp(t) for t in t_grid], dtype=complex)
        integrand = np.array([L_cesaro(t, 2000) for t in t_grid]) * amp_grid
        J_t = np.trapezoid(np.real(integrand), t_grid) / (2 * math.pi)
        print(f"  T={T_test}: J = {J_t:+.7f}  L(1) = {S1_N2000 - J_t:.7f}")

    print(f"\nFinal: J_direct = {J_vals[-1]:+.7f}  L(1) = {S1_N2000 - J_vals[-1]:.7f}")
    print(f"Reference: J_cesaro = {J_CESARO}, L(1)_Tauberian = 0.6314")
