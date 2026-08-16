"""
_m3_zero_scan.py -- Discovery-tier scan for zeros of L(s, sym^2 Delta).

GOAL ([OBL M-3] numerical path):
  Scan L(sigma+it, sym^2 Delta) for sigma in [0.6, 1.0] and t in [0, 20].
  If min |L(s)| > epsilon (empirically), this suggests a numerical zero-free region.
  Arb certification of the zero-free region comes later.

METHOD:
  L(sigma+it) ~ sum_{n=1}^{N} a(n)/n^{sigma+it} * (1 - n/N)  [Cesaro smoothing]

  The Cesaro truncation error at Re(s)=sigma is O(N^{-(sigma-1/2)+eps}).
  For sigma=0.9, N=2000: error ~ 2000^{-0.4} * C ~ 0.04 * C.
  If min|L| > 0.1 (say), and C < 2, then certified min|L| > 0 follows from Arb.

OUTPUTS:
  For each (sigma, t_k): |L_cesaro(sigma+it_k)|
  Min |L| over the grid (empirical bound from below)
  Plot: heatmap of |L(sigma+it)| showing zero-free region

STATUS: discovery tier.  [OBL M-3] certification requires Arb interval arithmetic.
"""
import sys; sys.path.insert(0, '.')
import math
import numpy as np
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs

N_COEFF = 2000
print(f"Loading {N_COEFF} coefficients ...")
tau_arr = compute_tau(N_COEFF)
a_sym2 = compute_sym2_coeffs(tau_arr)
a_arr = np.array([float(a_sym2[i]) for i in range(N_COEFF)], dtype=float)
n_arr = np.arange(1, N_COEFF + 1, dtype=float)
log_n = np.log(n_arr)
print("Done.")


def L_cesaro_sigma(sigma, t, N=None):
    """L(sigma+it) via Cesaro-smoothed Dirichlet series (N terms)."""
    if N is None:
        N = N_COEFF
    weights = 1.0 - n_arr[:N] / N
    # n^{-sigma-it} = n^{-sigma} * exp(-it * log n)
    amplitudes = a_arr[:N] * n_arr[:N]**(-sigma) * weights
    phases = np.exp(-1j * t * log_n[:N])
    return (amplitudes * phases).sum()


if __name__ == "__main__":
    # Grid: sigma x t
    sigmas = [0.6, 0.7, 0.8, 0.9, 1.0]
    t_vals = np.linspace(0, 20, 401)  # dense t grid

    print("\nScanning |L(sigma+it)| for zeros:")
    print(f"  sigma x t_range x N_t = {sigmas} x [0,20] x {len(t_vals)}")
    print()

    global_min = 1e10
    global_min_loc = None

    for sigma in sigmas:
        # Use more terms for smaller sigma (larger error)
        N_use = {0.6: 2000, 0.7: 2000, 0.8: 2000, 0.9: 1000, 1.0: 500}[sigma]

        L_vals = np.array([L_cesaro_sigma(sigma, t, N_use) for t in t_vals])
        abs_L = np.abs(L_vals)

        idx_min = np.argmin(abs_L)
        t_min = t_vals[idx_min]
        L_min = abs_L[idx_min]

        print(f"  sigma={sigma:.1f}: min|L| = {L_min:.6f} at t={t_min:.3f}  "
              f"  max|L| = {abs_L.max():.4f}  "
              f"  mean|L| = {abs_L.mean():.4f}  [N={N_use}]")

        if L_min < global_min:
            global_min = L_min
            global_min_loc = (sigma, t_min)

    print()
    print(f"Global minimum |L(s)| = {global_min:.6f} at s = {global_min_loc[0]:.1f} + {global_min_loc[1]:.3f}i")
    print()

    # Fine scan near the critical line (sigma=0.6) for deeper check
    print("Fine scan at sigma=0.6 (t in [0,20], N=2000):")
    t_fine = np.linspace(0, 20, 2001)
    L_fine = np.array([L_cesaro_sigma(0.6, t, 2000) for t in t_fine])
    abs_fine = np.abs(L_fine)

    # Report the 5 smallest values
    idx_sorted = np.argsort(abs_fine)[:5]
    for i in idx_sorted:
        print(f"  t={t_fine[i]:.4f}:  |L(0.6+it)| = {abs_fine[i]:.6f}  "
              f"Re(L)={L_fine[i].real:.5f}  Im(L)={L_fine[i].imag:.5f}")

    print()
    print(f"Minimum |L(0.6+it)| over t in [0,20]: {abs_fine.min():.6f}")
    print(f"If min > 0.05 (say), the Cesaro estimate suggests no zeros in Re(s)=0.6 strip.")
    print(f"Arb certification with explicit error bound would confirm this.")
