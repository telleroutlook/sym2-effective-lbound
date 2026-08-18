"""Compute J efficiently: vectorise t-loop, sum L-partial per t in numpy."""
import sys; sys.path.insert(0, '.')
import numpy as np
import mpmath; mpmath.mp.dps = 30
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs
from discovery.afe_gl3 import G_factor

tau = compute_tau(3000)
a_sym2 = compute_sym2_coeffs(tau)
mp = mpmath

# Precompute a(n) and n arrays
N_L = 3000
ns = np.arange(1, N_L + 1, dtype=float)
an = np.array(a_sym2[:N_L], dtype=float)

# J = (1/2pi) int_{-T}^T f(t) dt   where
# f(t) = Re[ L(1/2+it) * 12^{-1/2+it} * G(1/2+it)/G(1) * e^{(-1/2+it)^2}/(-1/2+it) ]
X = 12.0
T = 5.0
n_quad = 1000
ts = np.linspace(-T + T/n_quad, T - T/n_quad, n_quad)  # midpoints

# G_factor ratio on contour: precompute G(1/2+it)/G(1) for each t
print("Computing G factors...")
G1 = G_factor(mp.mpf(1), 12, mp)
G_ratio_arr = np.zeros(n_quad, dtype=complex)
for i, t in enumerate(ts):
    w = complex(-0.5, t)
    v = 1.0 + w  # = 0.5 + it
    G_ratio_arr[i] = complex(G_factor(mp.mpc(0.5, t), 12, mp) / G1)
    if i % 100 == 0:
        print(f"  t={t:.2f}, G_ratio={G_ratio_arr[i]:.4f}")

# w^{-1} * X^w * e^{w^2}
print("Computing w factors...")
ws = -0.5 + 1j * ts
w_factor = X**ws * np.exp(ws**2) / ws  # complex array, shape (n_quad,)

print("Computing L(1/2+it) sums...")
an_sqn = an / ns**0.5                             # shape (N_L,)
log_ns = np.log(ns)                               # shape (N_L,)
phases = np.outer(ts, log_ns)                     # shape (n_quad, N_L)
L_vals = np.sum(an_sqn[None, :] * np.exp(-1j * phases), axis=1)  # shape (n_quad,)
print(f"  L(1/2+0i) [t=0 approx] = {L_vals[n_quad//2]:.4f}")

# Integrand for J
integrand = L_vals * X**(-0.5) * X**(1j*ts) * G_ratio_arr * np.exp(0.25 - ts**2) * np.exp(-1j*ts) / (-0.5 + 1j*ts)
# = L(1/2+it) * X^{-1/2+it} * G/G1 * e^{w^2} / w  (with i*dt factor from (1/2pi i)*i dt = dt/(2pi))

J_integrand = np.real(integrand)
dt = 2*T / n_quad
J = np.sum(J_integrand) * dt / (2 * np.pi)
print(f"\nJ = {J:.6f}")

S1 = 0.548490
L1 = S1 - J
print(f"S1 = {S1:.6f}")
print(f"L(1) = S1 - J = {L1:.6f}  (target 0.6314)")
print(f"Error vs 0.6314: {L1 - 0.6314:+.5f}")

# Check convergence: redo with N_L = 500, 1000, 2000
print("\nConvergence in N_L:")
for NL in [100, 200, 500, 1000, 2000, 3000]:
    an2 = an[:NL]; ns2 = ns[:NL]; log_ns2 = log_ns[:NL]
    an_sqn2 = an2 / ns2**0.5
    phases2 = np.outer(ts, log_ns2)
    L2 = np.sum(an_sqn2[None, :] * np.exp(-1j * phases2), axis=1)
    integrand2 = L2 * X**(-0.5) * X**(1j*ts) * G_ratio_arr * np.exp(0.25 - ts**2) * np.exp(-1j*ts) / (-0.5 + 1j*ts)
    J2 = np.sum(np.real(integrand2)) * dt / (2*np.pi)
    L1_2 = S1 - J2
    print(f"  N_L={NL:5d}: J={J2:.6f}  L(1)={L1_2:.6f}  err={L1_2-0.6314:+.5f}")
