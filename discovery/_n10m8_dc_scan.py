"""
N=10^8 partial sum scan using DC-FFT sieve.

Key target: at N=10^8, tail_factor(sigma=0.9) ≈ 0.0528, so
  C_GL3 threshold ≈ 0.3926 / 0.0528 ≈ 7.44

Since Q_GL3^{1/3} = 332.75^{1/3} ≈ 6.93 < 7.44, if GL3 theory gives
C_GL3 <= Q^{1/3} (the weakest Voronoi bound), N=10^8 CERTIFIES the result.

This is the computational goal: reach N large enough that the threshold
exceeds the basic GL3 Voronoi constant Q^{1/3}.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time

N = 100_000_000
sigma = 0.90
dt_coarse = 0.10   # coarser step for speed (2001 t values)
T_max = 200.0

print(f"=== N={N} scan via DC-FFT ===", flush=True)
print(f"Expected tail_factor ~ 0.0528, threshold ~ 7.44", flush=True)
print(f"Q_GL3^{{1/3}} = {332.75**(1/3):.4f} (target: threshold > this)", flush=True)

t0 = time.time()
print("Computing tau via DC-FFT ...", flush=True)
from discovery._fast_tau_dc import compute_tau_dc
tau_f = compute_tau_dc(N)
print(f"  tau done in {time.time()-t0:.1f}s", flush=True)

from discovery._fast_tau_sieve import compute_a_sym2
a_arr = compute_a_sym2(tau_f)
del tau_f   # free memory
print(f"  a_sym2 done in {time.time()-t0:.1f}s", flush=True)

# Partial sums S(X) = cumsum(a)
a = np.asarray(a_arr, dtype=np.float64).copy()
print(f"  Array cast done in {time.time()-t0:.1f}s", flush=True)
S = np.cumsum(a)
max_S_abs = float(np.max(np.abs(S)))
max_S_loc = int(np.argmax(np.abs(S))) + 1
C_GL3_emp_peak = max_S_abs / (max_S_loc**(2/3))
C_GL3_emp_N = max_S_abs / (N**(2/3))
print(f"  max|S(X)| = {max_S_abs:.4f} at X={max_S_loc}", flush=True)
print(f"  C_GL3_emp (peak) = {C_GL3_emp_peak:.6f}", flush=True)
print(f"  C_GL3_emp (at N) = {C_GL3_emp_N:.6f}", flush=True)
del S  # free memory

# L_ces pre-weighting
ns = np.arange(1, N+1, dtype=np.float64)
log_ns = np.log(ns)
cesaro = (1.0 - ns/(N+1)) * ns**(-sigma)
a_w = a * cesaro
del a, ns, cesaro
print(f"  Pre-weighted done in {time.time()-t0:.1f}s", flush=True)

# Coarse t-scan
print(f"\nCoarse t-scan (step={dt_coarse}, {int(T_max/dt_coarse)+1} t values) ...", flush=True)
t_vals = np.arange(0.0, T_max + 0.001, dt_coarse)
min_abs = 1e9; min_t = 0.0

for i, t in enumerate(t_vals):
    L_r = float(np.dot(a_w, np.cos(t * log_ns)))
    L_i = float(np.dot(a_w, -np.sin(t * log_ns)))
    av = (L_r**2 + L_i**2)**0.5
    if av < min_abs:
        min_abs = av; min_t = t
    if (i % 200) == 199:
        print(f"  t={t:.0f}: global min = {min_abs:.6f} at t={min_t:.3f}", flush=True)

# Fine scan around minimum
print(f"\nFine scan around t={min_t:.3f} ...", flush=True)
for t in np.arange(min_t - 2.0, min_t + 2.0, 0.01):
    L_r = float(np.dot(a_w, np.cos(t * log_ns)))
    L_i = float(np.dot(a_w, -np.sin(t * log_ns)))
    av = (L_r**2 + L_i**2)**0.5
    if av < min_abs:
        min_abs = av; min_t = t

# Certification
tail_factor = sigma / (sigma - 2/3) * N**(2/3 - sigma)
finite_err = 3 * abs(float(a_arr[N-1])) * N**(-sigma)  # rough bound
threshold = (min_abs - 1e-6) / tail_factor

print(f"\n=== Certification at N={N} ===")
print(f"Global min|L_ces(0.9+it)|: {min_abs:.6f}  at t={min_t:.4f}")
print(f"tail_factor = {tail_factor:.5f}")
print(f"C_GL3 threshold: C_GL3 < {threshold:.4f}")
print(f"Q_GL3^{{1/3}} = {332.75**(1/3):.4f}")
print(f"Q_GL3^{{1/4}} = {332.75**(1/4):.4f}")
print(f"Threshold > Q^{{1/3}}? {'YES - CERTIFIES if C_GL3 <= Q^{1/3}!' if threshold > 332.75**(1/3) else 'NO'}")
print(f"Threshold > Q^{{1/4}}? {'YES' if threshold > 332.75**(1/4) else 'NO'}")
print(f"Empirical C_GL3 = {C_GL3_emp_peak:.6f}  (margin: {threshold/C_GL3_emp_peak:.0f}x)")
print(f"Total elapsed: {time.time()-t0:.0f}s")
