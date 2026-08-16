"""
Compute L_ces(10^8, 1) = Cesaro sum approximation to L(1, sym^2 Delta).

GOAL: Tightest certified lower bound on L(1, sym^2 Delta) achievable with
the N=10^8 DC-FFT sieve.

CERTIFICATION STRUCTURE:
  L(1) = L_ces(N, 1) + [L(1) - L_ces(N, 1)]
  |L(1) - L_ces(N, 1)| <= 4 * C_GL3 / N^{1/3}     [Abel summation]

  With C_GL3 <= 1.325 (Arb-certified conditional) and N=10^8:
    error <= 4 * 1.325 / (10^8)^{1/3} = 0.01143

  With C_GL3 <= Q^{1/3} = 6.93 (standard GL3 Voronoi):
    error <= 4 * 6.93 / (10^8)^{1/3} = 0.05975

OUTPUT: L_ces(10^8, 1), and the certified lower bounds under both C_GL3 assumptions.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time

N = 100_000_000

print(f"=== L_ces(N=10^8, s=1) computation ===", flush=True)

t0 = time.time()
print("Computing tau via DC-FFT ...", flush=True)
from discovery._fast_tau_dc import compute_tau_dc
tau_f = compute_tau_dc(N)
print(f"  tau done in {time.time()-t0:.1f}s", flush=True)

from discovery._fast_tau_sieve import compute_a_sym2
a_arr = compute_a_sym2(tau_f)
del tau_f
print(f"  a_sym2 done in {time.time()-t0:.1f}s", flush=True)

a = np.asarray(a_arr, dtype=np.float64)
del a_arr

# Partial sums S(X) = cumsum(a): reuse for C_GL3_emp check
S = np.cumsum(a)
max_S_abs = float(np.max(np.abs(S)))
max_S_loc = int(np.argmax(np.abs(S))) + 1
C_GL3_emp  = max_S_abs / (max_S_loc ** (2/3))
print(f"  max|S(X)| = {max_S_abs:.4f} at X={max_S_loc} -> C_GL3_emp = {C_GL3_emp:.6f}")
del S

# L_ces(N, s=1) = sum_{n=1}^N (1 - n/(N+1)) * a(n) / n
print(f"\nComputing L_ces(N, s=1) ...", flush=True)
ns       = np.arange(1, N+1, dtype=np.float64)
wt_s1    = (1.0 - ns/(N+1)) / ns          # Cesaro weight * n^{-1}
L_ces_1  = float(np.dot(a, wt_s1))
print(f"  L_ces(10^8, s=1) = {L_ces_1:.10f}")

# Also compute at N_sub = N//10 for convergence check
N2 = N // 10
wt_s1_2  = (1.0 - ns[:N2]/(N2+1)) / ns[:N2]
L_ces_1_sub = float(np.dot(a[:N2], wt_s1_2))
print(f"  L_ces(10^7, s=1) = {L_ces_1_sub:.10f}")
print(f"  Delta L_ces      = {L_ces_1 - L_ces_1_sub:.2e}")

# Error bounds (Abel summation at s=1)
N_f = float(N)
def abel_error_s1(C_GL3, N):
    return 4.0 * C_GL3 / N**(1/3)

C_GL3_arb  = 1.325    # Arb-certified conditional bound
C_GL3_Q13  = 6.930    # Q_GL3^{1/3} (standard GL3 Voronoi)
C_GL3_15   = 15.0     # very conservative

print(f"\n=== Certified lower bounds for L(1, sym^2 Delta) ===")
print(f"  L_ces(10^8, 1) = {L_ces_1:.8f}")
print()
for label, C in [("C_GL3 <= 1.325 (Arb-cert conditional)", C_GL3_arb),
                  ("C_GL3 <= Q^{1/3} = 6.930 (GL3 Voronoi)", C_GL3_Q13),
                  ("C_GL3 <= 15.0 (very conservative)", C_GL3_15)]:
    err  = abel_error_s1(C, N)
    lb   = L_ces_1 - err
    ub   = L_ces_1 + err
    print(f"  [{label}]")
    print(f"    error bound: +/- {err:.5f}")
    print(f"    L(1) in [{lb:.5f}, {ub:.5f}]  (certifies L(1) > 0: {'YES' if lb > 0 else 'NO'})")
    print()

print(f"Total elapsed: {time.time()-t0:.0f}s")
