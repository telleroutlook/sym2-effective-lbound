"""
Test Cesaro (Fejér) averaging of partial Dirichlet sums at Re(s)=1/2.

Instead of L_N(1/2+it) = sum_{n<=N} a(n)/n^{1/2+it},
use the Fejér sum:
  F_N(1/2+it) = sum_{n=1}^N a(n)/n^{1/2+it} * (1 - n/N)
             = (1/N) * sum_{k=1}^N L_k(1/2+it)

For conditionally convergent series, Fejér sums often converge O(1/N)
vs O(1/sqrt(N)) for partial sums. We test whether the oscillation in J
drops below 0.0001 with this approach.
"""
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

mp = mpmath
print("Computing G factors...", flush=True)
G1 = G_factor(mp.mpf(1), 12, mp)
G_ratio_arr = np.array([complex(G_factor(mp.mpc(0.5, float(t)), 12, mp) / G1) for t in ts])

print("Precomputing cumulative Dirichlet sums L_cumsum...", flush=True)
an_sqn = an / ns**0.5
log_ns = np.log(ns)
phases = np.outer(ts, log_ns)
L_all = an_sqn[None, :] * np.exp(-1j * phases)
L_cumsum = np.cumsum(L_all, axis=1)   # shape (n_quad, N_max)

def compute_J_fejer(NL):
    """Use Fejér (Cesaro) mean of first NL partial sums."""
    # F_N = mean of L_1, L_2, ..., L_N = cumsum up to N / N
    # L_cumsum[:, k-1] = L_k(1/2+it), so:
    # F_N = (1/NL) * sum_{k=1}^{NL} L_cumsum[:, k-1]
    #      = (1/NL) * cumsum_of_cumsum at NL
    # Equivalent: F_N[i] = sum_{n=1}^{NL} a(n)/n^{1/2+it_i} * (NL - n + 1) / NL
    #                     ≈ sum_{n=1}^{NL} a(n)/n^{1/2+it_i} * (1 - n/NL)
    weights = (NL - np.arange(NL)) / NL   # (1 - n/N) for n=1..NL, shape (NL,)
    L_vals = np.sum(L_all[:, :NL] * weights[None, :], axis=1)
    integrand = (L_vals * X**(-0.5) * X**(1j*ts) * G_ratio_arr
                 * np.exp(0.25 - ts**2) * np.exp(-1j*ts) / (-0.5 + 1j*ts))
    dt = 2*T / n_quad
    return np.sum(np.real(integrand)) * dt / (2 * np.pi)

def compute_J_partial(NL):
    """Standard partial sum L_N."""
    L_vals = L_cumsum[:, NL-1]
    integrand = (L_vals * X**(-0.5) * X**(1j*ts) * G_ratio_arr
                 * np.exp(0.25 - ts**2) * np.exp(-1j*ts) / (-0.5 + 1j*ts))
    dt = 2*T / n_quad
    return np.sum(np.real(integrand)) * dt / (2 * np.pi)

S1 = 0.548490
target = 0.6314

print(f"\n{'':>6}  {'Partial sum':>12}  {'Fejér sum':>12}")
print(f"  {'N_L':>6}  {'L(1)':>7}  {'err':>9}  {'L(1)':>7}  {'err':>9}")
for NL in [500, 1000, 2000, 3000, 5000, 7500, 10000]:
    J_p = compute_J_partial(NL)
    J_f = compute_J_fejer(NL)
    L1_p = S1 - J_p
    L1_f = S1 - J_f
    print(f"  {NL:6d}  {L1_p:7.5f}  {L1_p-target:+9.6f}  {L1_f:7.5f}  {L1_f-target:+9.6f}", flush=True)

# Also try Riesz mean of order 2: w(n) = (1 - (n/N)^2)
print(f"\nRiesz-2 mean (1-(n/N)^2) vs Fejér:")
for NL in [1000, 3000, 10000]:
    riesz_w = 1.0 - (np.arange(NL)/NL)**2
    L_riesz = np.sum(L_all[:, :NL] * riesz_w[None, :], axis=1)
    integrand_r = (L_riesz * X**(-0.5) * X**(1j*ts) * G_ratio_arr
                   * np.exp(0.25 - ts**2) * np.exp(-1j*ts) / (-0.5 + 1j*ts))
    dt = 2*T / n_quad
    J_r = np.sum(np.real(integrand_r)) * dt / (2 * np.pi)
    J_f = compute_J_fejer(NL)
    print(f"  N={NL:5d}: Riesz-2 L(1)={S1-J_r:7.5f} ({S1-J_r-target:+9.6f})  "
          f"Fejér L(1)={S1-J_f:7.5f} ({S1-J_f-target:+9.6f})", flush=True)
