"""
Full t-scan at N=10^7 using DC-FFT sieve.
Find global min|L_ces(0.9+it, N=10^7)| over t in [0, 200].
This determines the definitive C_GL3 threshold at N=10^7.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time

sigma = 0.90
N = 10_000_000
T_max = 200.0
dt = 0.05   # coarser step (4000 t values) for speed

print(f"Full t-scan N={N}, t in [0,{T_max}], step={dt}", flush=True)
t0 = time.time()

from discovery._fast_tau_dc import compute_tau_dc
tau_f = compute_tau_dc(N)
from discovery._fast_tau_sieve import compute_a_sym2
a_arr = compute_a_sym2(tau_f)
print(f"  Coefficients done in {time.time()-t0:.1f}s", flush=True)

a = np.array([float(a_arr[i]) for i in range(N)], dtype=np.float64)
ns = np.arange(1, N+1, dtype=np.float64)
log_ns = np.log(ns)
cesaro = (1.0 - ns/(N+1)) * ns**(-sigma)
a_w = a * cesaro
print(f"  Pre-weighted. Scanning {int(T_max/dt)+1} t values ...", flush=True)

min_abs = 1e9; min_t = 0.0
t_vals = np.arange(0.0, T_max + 0.001, dt)

for i, t in enumerate(t_vals):
    L_r = float(np.dot(a_w, np.cos(t * log_ns)))
    L_i = float(np.dot(a_w, -np.sin(t * log_ns)))
    av = (L_r*L_r + L_i*L_i)**0.5
    if av < min_abs:
        min_abs = av; min_t = t
    if (i % 400) == 399:
        print(f"  t={t:.0f}: global min = {min_abs:.6f} at t={min_t:.3f}", flush=True)

# Fine scan around the minimum
print(f"\nFine scan around t={min_t:.3f} ...", flush=True)
for t in np.arange(min_t - 1.0, min_t + 1.0, 0.005):
    L_r = float(np.dot(a_w, np.cos(t * log_ns)))
    L_i = float(np.dot(a_w, -np.sin(t * log_ns)))
    av = (L_r*L_r + L_i*L_i)**0.5
    if av < min_abs:
        min_abs = av; min_t = t

print(f"\n=== Global min|L_ces(0.9+it, N={N})| over t in [0,{T_max}] ===")
print(f"  min = {min_abs:.6f}  at t = {min_t:.4f}")

tail_factor = sigma / (sigma - 2/3) * N**(2/3 - sigma)
finite_err = 3 * abs(float(np.sum(a_arr[:N]))) * N**(-sigma)
threshold = (min_abs - finite_err) / tail_factor
print(f"  tail_factor = {tail_factor:.5f}")
print(f"  C_GL3 threshold: C_GL3 < {threshold:.4f}")
print(f"  Empirical C_GL3 = 0.003682  (margin: {threshold/0.003682:.0f}x)")
print(f"  Total elapsed: {time.time()-t0:.0f}s")
