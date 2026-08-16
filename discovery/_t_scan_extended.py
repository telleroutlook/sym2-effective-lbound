"""
Extended t-scan: min|L_ces(0.9+it, N=10^6)| for t in [0, 200].

The t in [0,50] scan (from _multi_sigma_scan.py) found min = 0.449015 at t=7.070.
This script extends to t in [0, 200] with step 0.02.

For certification of the zero-free region {sigma>=0.9}, we need
min|L_ces(0.9+it)| > total_error = C_GL3 * tail_factor + finite_error.

At N=10^6, sigma=0.9: total_error = C_GL3 * 0.154 + 0.000762.
The minimum over ALL t gives the tightest C_GL3 threshold.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time

sigma = 0.90
N = 1_000_000
T_max = 200.0
dt = 0.02

print(f"Extended t-scan: sigma={sigma}, N={N}, t in [0, {T_max}], step={dt}")
print("Loading a(n) coefficients ...", flush=True)
t0 = time.time()

from discovery._fast_tau_sieve import compute_tau_fast, compute_a_sym2
tau_f = compute_tau_fast(N)
a_arr = compute_a_sym2(tau_f)
a = np.array([float(a_arr[i]) for i in range(N)], dtype=np.float64)
ns = np.arange(1, N+1, dtype=np.float64)

# Cesaro weights (sigma part, t-independent)
cesaro = (1.0 - ns / (N + 1)) * ns**(-sigma)
a_w = a * cesaro  # pre-weighted

print(f"  Done in {time.time()-t0:.0f}s", flush=True)
print(f"Scanning {int(T_max/dt)+1} t values ...", flush=True)

t_vals = np.arange(0.0, T_max + 0.001, dt)
min_abs = 1e9
min_t = 0.0
min_abs_50 = 1e9
min_t_50 = 0.0

log_ns = np.log(ns)

results_top10 = []

for i, t in enumerate(t_vals):
    phase_r = np.cos(t * log_ns)
    phase_i = -np.sin(t * log_ns)
    L_r = float(np.dot(a_w, phase_r))
    L_i = float(np.dot(a_w, phase_i))
    av = (L_r*L_r + L_i*L_i)**0.5
    if av < min_abs:
        min_abs = av
        min_t = t
    if t <= 50.0 and av < min_abs_50:
        min_abs_50 = av
        min_t_50 = t
    results_top10.append((av, t))
    if (i % 1000) == 999:
        print(f"  t={t:.1f}: current global min = {min_abs:.6f} at t={min_t:.3f}", flush=True)

# Sort and show the 10 smallest
results_top10.sort()
print(f"\n=== Results: sigma={sigma}, N={N} ===")
print(f"Global min|L_ces|: {min_abs:.6f}  at t = {min_t:.3f}  (t in [0, {T_max}])")
print(f"Min for t<=50:     {min_abs_50:.6f}  at t = {min_t_50:.3f}  (was 0.449015)")
print(f"\n10 smallest |L_ces| values:")
for av, t in results_top10[:10]:
    print(f"  t={t:8.3f}: |L_ces| = {av:.6f}")

# Certification thresholds
tail_factor = sigma * N**(-7/30) / (sigma - 2/3)
finite_err = 3 * abs(float(np.sum(a_arr[:N]))) * N**(-sigma)
print(f"\nTail factor at N={N}: {tail_factor:.4f}")
print(f"Finite error: {finite_err:.2e}")
print(f"C_GL3 threshold for zero-free sigma>={sigma} (t in [0, {T_max}]):")
print(f"  C_GL3 < {(min_abs - finite_err)/tail_factor:.4f}  (prev: 2.63 for t in [0,50])")
