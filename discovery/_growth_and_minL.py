"""
_growth_and_minL.py -- Two analyses using N=10^6 partial sum data.

1. Fit growth exponent alpha from the partial sum table:
   max|S(X)| ~ C * X^alpha

2. Compute min|L_ces(0.9+it)| with N=10^6 terms (much more accurate than N=2000).
   This tightens the zero-free margin estimate for [OBL M-3].

PURPOSE: Update the certification margin after extending partial sum to N=10^6.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time

# ---- Part 1: Growth exponent fit from empirical data ----
data = [
    (7925,   13.30),
    (18806,  15.40),
    (94048,  26.10),
    (224786, 52.13),
    (811494, 63.82),
]
xs = np.array([d[0] for d in data], dtype=np.float64)
ys = np.array([d[1] for d in data], dtype=np.float64)
log_x = np.log(xs)
log_y = np.log(ys)

# Least squares: log_y = alpha * log_x + log_C
A = np.column_stack([log_x, np.ones_like(log_x)])
alpha, log_C = np.linalg.lstsq(A, log_y, rcond=None)[0]
C = np.exp(log_C)
print(f"Growth fit: max|S(X)| ≈ {C:.4f} * X^{alpha:.4f}")
print(f"Residuals: {[f'{v:.3f}' for v in (log_y - (alpha*log_x+log_C))]}")

# Extrapolation
for X_pred in [1e7, 1e8, 1e9, 1e10]:
    pred = C * X_pred**alpha
    print(f"  X={X_pred:.0e}: predicted max|S| ≈ {pred:.1f}")

# Cesaro error analysis for various N with power-law S(X) ≤ C*X^alpha
print(f"\nCesaro tail error integral for sigma=0.9, alpha={alpha:.3f}:")
print(f"  tail ~ C/(sigma-alpha) * N^(alpha-sigma)")
sigma = 0.9
coeff = C / (sigma - alpha)
for N in [1e6, 1e7, 1e8]:
    tail = coeff * N**(alpha - sigma)
    finite_err = 3 * C * N**alpha / N**sigma
    print(f"  N={N:.0e}: finite={finite_err:.2e}, tail={tail:.2e}, total≈{finite_err+tail:.2e}")

print()

# ---- Part 2: min|L_ces(0.9+it)| with N=10^6 ----
print("Computing min|L_ces(0.9+it)| with N=10^6 terms near t=7.075 ...")
print("(recomputing tau and a_sym2 from scratch)")

from discovery._fast_tau_sieve import compute_tau_fast, compute_a_sym2

N = 1_000_000
t0 = time.time()
tau_f = compute_tau_fast(N)
a = compute_a_sym2(tau_f)
print(f"  Computed tau + a_sym2 in {time.time()-t0:.1f}s")

n_arr = np.arange(1, N+1, dtype=np.float64)
log_n = np.log(n_arr)
w = 1.0 - n_arr / N  # Cesaro weights

def L_ces_large(sigma, t):
    """Cesaro sum with N=10^6 terms."""
    phase = np.exp(-1j * t * log_n)
    damp = n_arr**(-sigma)
    return (a * damp * phase * w).sum()

# Scan t in [6.5, 7.6] with fine grid (step 0.005)
t_grid = np.arange(6.5, 7.61, 0.005)
sigma = 0.9
print(f"  Scanning t in [6.5, 7.6] at sigma=0.9, step=0.005 ({len(t_grid)} points)...")
t1 = time.time()
vals = np.array([abs(L_ces_large(sigma, t)) for t in t_grid])
print(f"  Scan time: {time.time()-t1:.1f}s")

idx_min = np.argmin(vals)
print(f"\nResult at sigma={sigma}:")
print(f"  min|L_ces| = {vals[idx_min]:.6f} at t = {t_grid[idx_min]:.4f}")
top5 = np.argsort(vals)[:5]
for i in top5:
    print(f"    t={t_grid[i]:.4f}: |L|={vals[i]:.6f}")

# Final margin calculation
C_max_N = 63.82  # max|S(X)| for X <= 10^6
cesaro_err = 3 * C_max_N / N**sigma
tail_err = C / (sigma - alpha) * N**(alpha - sigma)
total_err = cesaro_err + tail_err
min_L = vals[idx_min]
margin = min_L - total_err
print(f"\nCertification margin (assuming power-law growth continues):")
print(f"  min|L_ces(0.9+7.07i, N=10^6)| = {min_L:.6f}")
print(f"  Cesaro finite error = 3*{C_max_N}/{N:.0e}^0.9 = {cesaro_err:.6f}")
print(f"  Tail error (power-law bound) = {tail_err:.6f}")
print(f"  Total error ≤ {total_err:.6f}")
print(f"  Margin = {min_L:.6f} - {total_err:.6f} = {margin:.6f}")
if margin > 0:
    print(f"  --> Zero-free region {{sigma>=0.9}} would be CERTIFIED (margin={margin:.4f})")
    print(f"  --> PROVIDED |S(X)| <= {C:.3f}*X^{alpha:.3f} is proved for all X")
else:
    print(f"  --> Margin negative: need larger N or different sigma")
