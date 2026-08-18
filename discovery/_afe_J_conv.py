"""Convergence study for J with N_L up to 10000."""
import sys; sys.path.insert(0, '.')
import numpy as np
import mpmath; mpmath.mp.dps = 25
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs
from discovery.afe_gl3 import G_factor

N_max = 10000
tau = compute_tau(N_max)
a_sym2 = compute_sym2_coeffs(tau)

ns = np.arange(1, N_max + 1, dtype=float)
an = np.array(a_sym2[:N_max], dtype=float)

X = 12.0
T = 5.0
n_quad = 1000
ts = np.linspace(-T + T/n_quad, T - T/n_quad, n_quad)

# Precompute G factors (done once)
print("Computing G factors...", flush=True)
mp = mpmath
G1 = G_factor(mp.mpf(1), 12, mp)
G_ratio_arr = np.array([complex(G_factor(mp.mpc(0.5, float(t)), 12, mp) / G1) for t in ts])

# Precompute L(1/2+it) for all n_quad t values and n=1..N_max
print("Precomputing L partial sums...", flush=True)
an_sqn = an / ns**0.5
log_ns = np.log(ns)
phases = np.outer(ts, log_ns)         # (n_quad, N_max)
L_all = an_sqn[None, :] * np.exp(-1j * phases)  # (n_quad, N_max)
# L_cumsum[i, n] = sum_{k=1}^{n} a(k)/k^{1/2+i ts[i]}
L_cumsum = np.cumsum(L_all, axis=1)   # (n_quad, N_max)

# For each N_L, compute J
def compute_J_from_Lcumsum(NL):
    L_vals = L_cumsum[:, NL-1]   # shape (n_quad,)
    integrand = (L_vals * X**(-0.5) * X**(1j*ts) * G_ratio_arr
                 * np.exp(0.25 - ts**2) * np.exp(-1j*ts) / (-0.5 + 1j*ts))
    dt = 2*T / n_quad
    return np.sum(np.real(integrand)) * dt / (2 * np.pi)

S1 = 0.548490
print(f"\nConvergence of J and L(1) = S1-J vs N_L:")
print(f"  {'N_L':>6}  {'J':>10}  {'L(1)':>10}  {'err vs 0.6314':>14}")
for NL in [100, 200, 500, 1000, 2000, 3000, 5000, 7500, 10000]:
    J = compute_J_from_Lcumsum(NL)
    L1 = S1 - J
    print(f"  {NL:6d}  {J:10.6f}  {L1:10.6f}  {L1-0.6314:+14.6f}", flush=True)

# Check the effective Gaussian weight for large n:
print("\nEffective Gaussian weight |Â_A(log(ne/12))| ~ exp(-(log(ne/12))^2/4):")
for n in [500, 1000, 2000, 3000, 5000, 7500, 10000]:
    lognX = np.log(n * np.e / X)
    weight = np.exp(-lognX**2 / 4)
    print(f"  n={n:6d}: log(ne/X)={lognX:.3f}  Gaussian weight={weight:.2e}")
