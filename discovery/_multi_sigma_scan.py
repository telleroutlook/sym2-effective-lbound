"""
_multi_sigma_scan.py -- Multi-sigma zero-free scan with N=10^6 Cesaro terms.

For each sigma in {0.7, 0.8, 0.85, 0.9, 0.95}, compute:
  - min|L_ces(sigma+it)| for t in [0, 20] (finer grid near known minimum t~7.07)
  - GL3 Voronoi certification threshold: max C_GL3 such that certification works
  - Effective PNT bound needed

KEY FORMULA (GL3 Voronoi):
  Cesaro tail error <= C_GL3 * integral(x^(2/3) / x^(sigma+1), N, inf)
                    = C_GL3 * N^(2/3-sigma) / (sigma - 2/3)
  Certification requires: C_GL3 < min|L_ces(sigma)| * (sigma - 2/3) / N^(2/3-sigma)

PURPOSE: Find optimal sigma for the GL3 Voronoi certification path [OBL M-3].
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time

# --- Load N=10^6 coefficients ---
print("Loading N=10^6 coefficients (tau + a_sym2)...")
t0 = time.time()
from discovery._fast_tau_sieve import compute_tau_fast, compute_a_sym2
N = 1_000_000
tau_f = compute_tau_fast(N)
a = compute_a_sym2(tau_f)
print(f"  Done in {time.time()-t0:.1f}s")

n_arr = np.arange(1, N+1, dtype=np.float64)
log_n = np.log(n_arr)
w = 1.0 - n_arr / N  # Cesaro weights

def L_ces(sigma, t):
    phase = np.exp(-1j * t * log_n)
    damp = n_arr**(-sigma)
    return (a * damp * phase * w).sum()

# Grid: coarse over [0,20], fine near 7.07
t_coarse = np.linspace(0, 20, 401)   # step 0.05
t_fine   = np.linspace(6.5, 7.6, 221)  # step 0.005

sigmas = [0.70, 0.80, 0.85, 0.90, 0.95]
C_max_N = 63.82   # max|S(X)| for X <= 10^6

print()
print(f"{'sigma':>6}  {'min|L|':>10}  {'t_min':>7}  {'finite_err':>12}  {'C_GL3_thresh':>14}  {'margin(PL fit)':>16}")
print("  " + "-"*80)

results = {}
for sigma in sigmas:
    # Coarse scan first
    vals_c = np.array([abs(L_ces(sigma, t)) for t in t_coarse])
    idx_c = np.argmin(vals_c)
    t_approx = t_coarse[idx_c]

    # Fine scan around minimum
    if 6.5 <= t_approx <= 7.6:
        t_scan = t_fine
    else:
        t_lo = max(0, t_approx - 0.5)
        t_hi = t_approx + 0.5
        t_scan = np.linspace(t_lo, t_hi, 201)

    vals_f = np.array([abs(L_ces(sigma, t)) for t in t_scan])
    idx_f = np.argmin(vals_f)
    min_L = vals_f[idx_f]
    t_min = t_scan[idx_f]

    # GL3 Voronoi certification threshold
    # Tail error = C_GL3 * N^(2/3-sigma) / (sigma - 2/3)
    if sigma > 2/3:
        voronoi_unit = N**(2/3 - sigma) / (sigma - 2/3)
        C_GL3_thresh = min_L / voronoi_unit
    else:
        voronoi_unit = float('inf')
        C_GL3_thresh = 0.0

    # Finite Cesaro error (using computed max|S(X)| for X <= N)
    finite_err = 3.0 * C_max_N / N**sigma

    # Margin using empirical power-law fit: |S(X)| <= 0.445 * X^0.369
    alpha_emp = 0.3692
    C_emp = 0.4446
    if sigma > alpha_emp:
        tail_emp = C_emp * N**(alpha_emp - sigma) / (sigma - alpha_emp)
        margin_emp = min_L - finite_err - tail_emp
    else:
        tail_emp = float('inf')
        margin_emp = float('-inf')

    results[sigma] = {'min_L': min_L, 't_min': t_min, 'finite_err': finite_err,
                      'C_GL3_thresh': C_GL3_thresh, 'margin_emp': margin_emp,
                      'voronoi_unit': voronoi_unit}

    print(f"  {sigma:>5.2f}  {min_L:>10.6f}  {t_min:>7.4f}  {finite_err:>12.6f}  "
          f"{C_GL3_thresh:>14.4f}  {margin_emp:>16.6f}")

print()
print("Summary: GL3 Voronoi C_GL3 threshold at various sigma (N=10^6):")
print("  (certification works if the actual GL3 Voronoi constant < threshold)")
for sigma, r in results.items():
    if sigma > 2/3:
        print(f"  sigma={sigma:.2f}: need C_GL3 < {r['C_GL3_thresh']:.3f}")

print()
print("Note: empirical max|S(X)|/X^(2/3) at X=10^6 = "
      f"{C_max_N / N**(2/3):.4f}")
print("Note: empirical max|S(X)|/X^(2/3) at X=811494 = "
      f"{C_max_N / 811494**(2/3):.4f}")
