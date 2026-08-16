"""
Extended scan to N=10^7: S(X) growth + L_ces zero gap at sigma=0.9.

Computes:
  1. S(X) = sum_{n<=X} a_sym2(n) for X up to 10^7, tracks max|S(X)|/X^{2/3}
  2. L_ces(10^7, 0.9+it) minimum over t in [0, 50]
  3. Updated C_GL3 threshold at N=10^7 vs N=10^6

Expected output (extrapolated from N=10^6 data):
  max|S(X)| ~ 150  at X ~ 8*10^6
  C_GL3_empirical ~ 0.006
  threshold C_GL3 < 4.49 (relaxed from 2.63 at N=10^6)
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time

print("=== Extended scan to N=10^7 ===", flush=True)
print("Loading/computing tau and a_sym2 to N=10^7 ...", flush=True)

t0 = time.time()
from discovery._fast_tau_sieve import compute_tau_fast, compute_a_sym2

N = 10_000_000
tau_f = compute_tau_fast(N)
a_arr = compute_a_sym2(tau_f)
a = np.array([float(a_arr[i]) for i in range(N)], dtype=np.float64)
print(f"  Done in {time.time()-t0:.0f}s", flush=True)

# --- Part 1: S(X) partial sums ---
print("\n--- Part 1: S(X) = sum_{n<=X} a(n), max|S|/X^{2/3} ---", flush=True)
cum = np.cumsum(a)
xs = np.arange(1, N+1, dtype=np.float64)
ratio = np.abs(cum) / xs**(2/3)

max_idx = int(np.argmax(ratio))
max_ratio = float(ratio[max_idx])
max_S = float(cum[max_idx])
print(f"  max |S(X)|/X^{{2/3}} = {max_ratio:.6f}  at X = {max_idx+1}")
print(f"  |S|_max = {abs(max_S):.4f}")

# Report at several milestones
for k in [1e5, 1e6, 5e6, 1e7]:
    k = int(k)
    if k <= N:
        print(f"  X={k:.0e}: S={cum[k-1]:.4f}, max|S|/X^{{2/3}}(to X) = {float(np.max(ratio[:k])):.6f}")

# --- Part 2: L_ces(N, 0.9+it) minimum ---
print("\n--- Part 2: min|L_ces(10^7, 0.9+it)| for t in [0,50] ---", flush=True)

sigma = 0.9
ns = np.arange(1, N+1, dtype=np.float64)
ns_sigma = ns ** (-sigma)

# Cesaro weights
cesaro_weights = (1.0 - ns / (N + 1)) * ns_sigma

# Scan t in [0, 50] with step 0.02
t_vals = np.arange(0.0, 50.01, 0.02)
min_abs = 1e9
min_t = 0.0

for t in t_vals:
    phase = np.exp(-1j * t * np.log(ns))
    L_val = float(np.dot(a * cesaro_weights, phase.real)) + 1j * float(np.dot(a * cesaro_weights, phase.imag))
    av = abs(L_val)
    if av < min_abs:
        min_abs = av
        min_t = t

print(f"  min|L_ces(0.9+it)| = {min_abs:.6f}  at t = {min_t:.3f}")
print(f"  (at N=10^6 this was 0.449015 at t=7.070)")

# --- Part 3: Updated certification threshold ---
print("\n--- Part 3: Certification threshold at N=10^7, sigma=0.9 ---", flush=True)
sigma = 0.9
N_big = 1e7
# Tail error = C_GL3 * (7/30) * N^{-7/30} * (30/7) * sigma / (sigma - 2/3)
# = C_GL3 * sigma * N^{-7/30} / (sigma - 2/3)
tail_factor = sigma * N_big**(-7/30) / (sigma - 2/3)
finite_err = 3 * abs(float(cum[N-1])) * N_big**(-sigma)
print(f"  Tail error factor: {tail_factor:.4f}  (vs 0.154 at N=10^6)")
print(f"  Finite error: {finite_err:.2e}")
print(f"  Min|L_ces|: {min_abs:.4f}")
print(f"  C_GL3 threshold: < {(min_abs - finite_err)/tail_factor:.4f}  (vs 2.63 at N=10^6)")
print(f"  Empirical C_GL3 = {max_ratio:.4f}  (safety margin: {(min_abs-finite_err)/tail_factor/max_ratio:.0f}x)")
