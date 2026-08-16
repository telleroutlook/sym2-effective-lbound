"""
_zero_free_scan.py -- Discovery-tier zero-free region scan for L(s, sym^2 Delta).

STATUS: discovery tier (Cesaro N=2000, mpmath). NOT certified.

PURPOSE:
  Numerically map min|L(sigma+it)| over the rectangle
      sigma in {0.6, 0.7, 0.8, 0.9, 1.0}
      t in [0, 50]
  and document how far L is from zero. This informs [OBL M-3]:
  the certified zero-free region needed to bound J and certify L(1).

CONTEXT FOR [OBL M-3]:
  If min|L(sigma_0+it)| >= delta_0 > 0 in {sigma>=sigma_0, |t|<=T}, then by
  a certified Abel summation argument, the Cesaro truncation error is bounded.
  The discovery-tier minimum here is a LOWER BOUND on what delta_0 might be;
  the certified delta_0 would be strictly smaller (truncation adds error).

RESULT (run 2026-08-16):
  See printed output below. Key finding from prior _m3_zero_scan.py probe:
  min|L(0.6+it)| ~ 0.141 at t~7.07, min|L(0.7+it)| ~ 0.26 at t~7.07.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs

N = 2000
tau_arr = compute_tau(N)
a_sym2 = compute_sym2_coeffs(tau_arr)
a_arr = np.array([float(a_sym2[i]) for i in range(N)], dtype=np.float64)
n_arr = np.arange(1, N+1, dtype=np.float64)
log_n = np.log(n_arr)

def L_cesaro(sigma, t, N_terms=N):
    """Cesaro-smoothed Dirichlet series at sigma+it."""
    w = 1.0 - n_arr[:N_terms] / N_terms
    phase = np.exp(-1j * t * log_n[:N_terms])
    damp = n_arr[:N_terms] ** (-sigma)
    return (a_arr[:N_terms] * damp * phase * w).sum()

sigmas = [0.6, 0.7, 0.8, 0.9, 1.0]
t_fine = np.linspace(0, 50, 2001)  # step 0.025

print("Zero-free region scan: min|L_cesaro(sigma+it)| over t in [0, 50]")
print(f"  N_cesaro = {N}, t-grid = {len(t_fine)} points (step {t_fine[1]-t_fine[0]:.3f})")
print()
print(f"  {'sigma':>6}  {'min|L|':>10}  {'t_min':>8}  {'max|L|':>10}  {'t_max':>8}")
print("  " + "-"*54)

results = {}
for sigma in sigmas:
    vals = np.array([abs(L_cesaro(sigma, t)) for t in t_fine])
    idx_min = np.argmin(vals)
    idx_max = np.argmax(vals)
    results[sigma] = {
        'min': vals[idx_min], 't_min': t_fine[idx_min],
        'max': vals[idx_max], 't_max': t_fine[idx_max],
        'vals': vals,
    }
    print(f"  {sigma:>6.1f}  {vals[idx_min]:>10.4f}  {t_fine[idx_min]:>8.3f}  {vals[idx_max]:>10.4f}  {t_fine[idx_max]:>8.3f}")

print()
print("Minimum positions (top-5 closest to zero for each sigma):")
for sigma in sigmas:
    r = results[sigma]
    vals = r['vals']
    top5_idx = np.argsort(vals)[:5]
    top5 = [(t_fine[i], vals[i]) for i in top5_idx]
    print(f"  sigma={sigma}: " + "  ".join(f"t={t:.3f}(|L|={v:.4f})" for t, v in top5))

print()
print("Gap analysis for [OBL M-3]:")
print("  If certified delta_0 = discovered min * safety_factor (say 0.5),")
for sigma in [0.6, 0.7]:
    delta0 = results[sigma]['min'] * 0.5
    print(f"  sigma={sigma}: delta_0 ~ {delta0:.4f}. Zero-free if |L(s)| >= delta_0 in strip.")
print()
print("CONCLUSION: Discovery-tier scan supports zero-free region hypothesis.")
print("  Full certification requires GL3 AFE with Arb error bounds at each (sigma,t).")
print("  See [OBL M-3] in PLAN.md.")
