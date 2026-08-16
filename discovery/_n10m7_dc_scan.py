"""
N=10^7 partial sum scan using DC-FFT sieve.
Computes max|S(X)|/X^{2/3} and L_ces(0.9+7.07i, N=10^7) to tighten C_GL3 threshold.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time

N = 10_000_000
sigma = 0.90
t_vals_check = [7.07, 73.98, 110.02]  # known local minima from t-scan

print(f"=== N={N} scan via DC-FFT ===", flush=True)

t0 = time.time()
print("Computing tau via DC-FFT ...", flush=True)
from discovery._fast_tau_dc import compute_tau_dc
tau_f = compute_tau_dc(N)
print(f"  tau done in {time.time()-t0:.1f}s", flush=True)

from discovery._fast_tau_sieve import compute_a_sym2
a_arr = compute_a_sym2(tau_f)
print(f"  a_sym2 done in {time.time()-t0:.1f}s", flush=True)

a = np.array([float(a_arr[i]) for i in range(N)], dtype=np.float64)
ns = np.arange(1, N+1, dtype=np.float64)

# Partial sum S(X) = sum_{n<=X} a(n)
print("Computing partial sums S(X) ...", flush=True)
S = np.cumsum(a)
max_S_abs = np.max(np.abs(S))
max_S_loc = int(np.argmax(np.abs(S))) + 1
C_GL3_emp = max_S_abs / (max_S_loc ** (2/3))
print(f"  max|S(X)| = {max_S_abs:.4f} at X={max_S_loc}", flush=True)
print(f"  C_GL3_emp = max|S|/X^{{2/3}} = {max_S_abs / (N**(2/3)):.6f}  (at N={N})", flush=True)
print(f"  C_GL3_emp = {C_GL3_emp:.6f}  (at peak location)", flush=True)

# L_ces at several t values with sigma=0.9
print(f"\nL_ces(sigma={sigma}+it, N={N}) at key t values:", flush=True)
log_ns = np.log(ns)
cesaro = (1.0 - ns/(N+1)) * ns**(-sigma)
a_w = a * cesaro
for t in t_vals_check:
    L_r = float(np.dot(a_w, np.cos(t * log_ns)))
    L_i = float(np.dot(a_w, -np.sin(t * log_ns)))
    print(f"  t={t}: |L_ces| = {(L_r**2+L_i**2)**0.5:.6f}", flush=True)

# Quick t-scan near t=110 for new minimum
print(f"\nFine t-scan near t=110 ...", flush=True)
min_abs = 1e9; min_t = 0.0
for t in np.arange(108.0, 112.0, 0.005):
    L_r = float(np.dot(a_w, np.cos(t * log_ns)))
    L_i = float(np.dot(a_w, -np.sin(t * log_ns)))
    av = (L_r**2+L_i**2)**0.5
    if av < min_abs:
        min_abs = av; min_t = t
print(f"  min|L_ces(0.9+it)| near t=110: {min_abs:.6f} at t={min_t:.3f}", flush=True)

# Certification threshold
tail_factor = sigma / (sigma - 2/3) * N**(2/3 - sigma)
finite_err = 3 * float(abs(S[N-1])) * N**(-sigma)
print(f"\n--- Certification at N={N} ---")
print(f"tail_factor = {tail_factor:.5f}")
print(f"finite_err  = {finite_err:.2e}")
print(f"C_GL3 threshold (min near t=110): C_GL3 < {(min_abs - finite_err)/tail_factor:.4f}")
print(f"Total elapsed: {time.time()-t0:.0f}s")
