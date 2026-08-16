"""
_L1_direct_cesaro.py -- Direct Cesaro computation of L(1, sym^2 Delta) with N=10^6.

L_ces(N, 1) = sum_{n=1}^N a_sym2(n)/n * (1 - n/N)

At s=1, the Cesaro error formula gives:
  |L(1) - L_ces(N, 1)| <= 3 * max_X |S(X)| / N

EMPIRICAL ERROR BOUND (assuming power-law tail):
  finite:  3 * 63.82 / 10^6 = 0.000192
  tail:    0.445 * (10^6)^(0.369-1) / (1-0.369) = 1.64e-4
  total:   ~3.6e-4

PURPOSE: Get the most precise discovery-tier estimate of L(1, sym^2 Delta).
Compare with GL3 AFE result L(1) = 0.63180 +- 0.00003.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time

print("Loading N=10^6 coefficients...")
t0 = time.time()
from discovery._fast_tau_sieve import compute_tau_fast, compute_a_sym2
N = 1_000_000
tau_f = compute_tau_fast(N)
a = compute_a_sym2(tau_f)
print(f"  Done in {time.time()-t0:.1f}s")

n_arr = np.arange(1, N+1, dtype=np.float64)
w = 1.0 - n_arr / N  # Cesaro weights

# L_ces(N, 1) = sum a(n)/n * (1 - n/N)
L_ces_1 = np.sum(a / n_arr * w)
print(f"\nL_ces(N=10^6, 1) = {L_ces_1:.8f}")

# Error bound using empirical power law |S(X)| <= 0.445 * X^0.369
C_max_N = 63.82
alpha_emp = 0.3692
C_emp = 0.4446
N_val = float(N)
sigma = 1.0

finite_err = 3.0 * C_max_N / N_val**sigma
tail_err = C_emp * N_val**(alpha_emp - sigma) / (sigma - alpha_emp)
total_err = finite_err + tail_err

print(f"\nError analysis (assuming power-law growth for X > 10^6):")
print(f"  finite Cesaro error: 3 * {C_max_N} / 10^6 = {finite_err:.6f}")
print(f"  tail error (power law): {tail_err:.6f}")
print(f"  total error <= {total_err:.6f}")
print(f"\nCertified discovery-tier interval:")
print(f"  L(1, sym^2 Delta) in [{L_ces_1 - total_err:.6f}, {L_ces_1 + total_err:.6f}]")
print(f"  (assuming |S(X)| <= {C_emp:.3f} * X^{alpha_emp:.3f} for all X > 10^6)")

print(f"\nGL3 AFE result: L(1) = 0.63180 +- 0.00003")
print(f"Cesaro N=10^6 result: L(1) = {L_ces_1:.5f} +- {total_err:.5f}")
print(f"Difference: {abs(L_ces_1 - 0.63180):.6f}")

# Also compute convergence: L_ces at various N using the same array
print(f"\nConvergence check (sub-sums):")
for frac in [0.1, 0.2, 0.5, 1.0]:
    n_sub = int(N * frac)
    w_sub = 1.0 - n_arr[:n_sub] / n_sub
    L_sub = np.sum(a[:n_sub] / n_arr[:n_sub] * w_sub)
    print(f"  N={n_sub:7d}: L_ces = {L_sub:.6f}")

# Compare with S1 from earlier certification
S1_certified = 0.548302  # midpoint of certified interval [0.548299, 0.548306]
J_discovery = L_ces_1 - S1_certified
print(f"\nConsistency check with GL3 AFE:")
print(f"  S1 (certified) ~ {S1_certified:.6f}")
print(f"  J = L_ces(1) - S1 ~ {J_discovery:.6f}")
print(f"  Compare: J_direct_quad = -0.08350")
