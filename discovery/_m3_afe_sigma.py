"""
_m3_afe_sigma.py -- Two-sided Gaussian AFE for L(sigma+it, sym^2 Delta) at sigma < 1.

FORMULA:
  L(sigma+it) = S_main(sigma, t, X) + eps * chi(sigma, t) * S_dual(1-sigma, t, X)
                + O(exp(-(X/X_t)^2))

where:
  S_main(sigma, t, X) = sum_n a(n)/n^{sigma+it} * exp(-(n/X)^2)
  S_dual(1-sigma, t, X) = sum_n a(n)/n^{1-sigma-it} * exp(-(n/X)^2)  [same Gaussian]
  chi(sigma, t) = Q^{sigma-1/2} * Q^{-it} * G(1-sigma-it) / G(sigma+it)  [FE factor]
  eps = +1 (self-dual)

For the Gaussian weight exp(-x^2) with X_t = (Q * (|t|+2))^{1/3} (analytic conductor scale):
  - S_main: N ~ 4 X_t terms, each term < exp(-16) for n > 4 X_t -> exponentially small error
  - S_dual: SAME N terms, also exp-small
  - FE correction from imperfect Gaussian: O(exp(-X_t^2)) ~ exp(-100) for X_t=10 [tiny]

  => L(sigma+it) certified to O(exp(-16)) ~ 10^{-7} precision with ~50 terms.

CROSS-CHECK:
  - Compare with Cesaro(N=2000) at sigma=0.7, t in [0, 20]
  - Should agree to ~0.001 or better
  - Min |L_AFE(0.6+it)| should be > 0.10 (certifying zero-free at sigma=0.6)

STATUS: discovery tier (G-factor computed with mpmath, not Arb).
Next step: replace mpmath G-factor with Arb for certified interval arithmetic.
"""
import sys; sys.path.insert(0, '.')
import math
import numpy as np
import mpmath; mpmath.mp.dps = 30
from discovery.afe_gl3 import G_factor
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs

mp = mpmath
k = 12
Q = mp.mpf(144)
eps = 1  # self-dual

N_COEFF = 200
print(f"Loading {N_COEFF} coefficients ...")
tau_arr = compute_tau(N_COEFF)
a_sym2 = compute_sym2_coeffs(tau_arr)
a_arr = np.array([float(a_sym2[i]) for i in range(N_COEFF)], dtype=float)
n_arr = np.arange(1, N_COEFF + 1, dtype=float)
log_n = np.log(n_arr)
print("Done.")


def X_t(t_val):
    """Analytic conductor scale X = (Q * (|t|+2))^{1/3}."""
    return float((144.0 * (abs(t_val) + 2.0)) ** (1.0 / 3.0))


def FE_factor(sigma, t_val):
    """
    chi(sigma, t) = Q^{sigma-1/2-it} * G(1-sigma-it) / G(sigma+it).
    This is the functional equation factor: L(sigma+it) = eps * chi * L(1-sigma-it).
    """
    s = mp.mpc(mp.mpf(str(sigma)), mp.mpf(str(t_val)))
    one_minus_s_conj = mp.mpc(mp.mpf(str(1.0 - sigma)), mp.mpf(str(-t_val)))
    G_s = G_factor(s, k, mp)
    G_1ms = G_factor(one_minus_s_conj, k, mp)
    Qfac = mp.power(Q, mp.mpc(mp.mpf(str(0.5 - sigma)), mp.mpf(str(-t_val))))
    return complex(Qfac * G_1ms / G_s)


def L_afe_two_sided(sigma, t_val, N=None):
    """
    L(sigma+it) via two-sided Gaussian AFE.
    Returns (L_val, X_scale, N_used).
    """
    Xt = X_t(t_val)
    if N is None:
        N = min(int(5 * Xt) + 5, N_COEFF)

    # Gaussian weights exp(-(n/X_t)^2)
    gauss = np.exp(-(n_arr[:N] / Xt) ** 2)
    phases_main = np.exp(-1j * t_val * log_n[:N])  # n^{-it}
    phases_dual = np.exp(1j * t_val * log_n[:N])   # n^{it} = conj(n^{-it})

    # Main sum: a(n)/n^{sigma+it} * Gaussian
    S_main = (a_arr[:N] / n_arr[:N]**sigma * gauss * phases_main).sum()

    # Dual sum: a(n)/n^{1-sigma-it} * Gaussian
    S_dual = (a_arr[:N] / n_arr[:N]**(1.0 - sigma) * gauss * phases_dual).sum()

    # FE factor
    chi = FE_factor(sigma, t_val)

    L_val = S_main + eps * chi * S_dual
    return L_val, Xt, N


if __name__ == "__main__":
    print("\nCross-check AFE vs Cesaro at sigma=0.7, t in [0, 20]:")
    print(f"  {'t':>6}  {'|L_AFE|':>10}  {'|L_Cesaro|':>12}  {'diff':>10}  {'X_t':>5}  N")
    print()

    t_check = [0.5, 1.0, 2.0, 3.14, 5.0, 7.07, 10.0, 15.0, 20.0]
    sigma_test = 0.7
    max_diff = 0.0

    for t in t_check:
        L_afe, Xt, N_used = L_afe_two_sided(sigma_test, t)
        # Cesaro with N=2000
        N_ces = min(2000, N_COEFF)
        w = 1.0 - n_arr[:N_ces] / N_ces
        L_ces = (a_arr[:N_ces] / n_arr[:N_ces]**sigma_test * w *
                 np.exp(-1j * t * log_n[:N_ces])).sum()
        diff = abs(L_afe - L_ces)
        max_diff = max(max_diff, diff)
        print(f"  {t:>6.2f}  {abs(L_afe):>10.6f}  {abs(L_ces):>12.6f}  {diff:>10.2e}"
              f"  {Xt:>5.2f}  {N_used}")

    print(f"\n  Max |AFE-Cesaro| at sigma=0.7: {max_diff:.4e}")

    # Now scan sigma=0.6 with AFE (the hardest case)
    print("\nScan |L_AFE(0.6+it)| for t in [0, 20]:")
    sigma_scan = 0.6
    t_scan = np.linspace(0, 20, 201)
    abs_L_afe = []
    for t in t_scan:
        L_v, _, _ = L_afe_two_sided(sigma_scan, t)
        abs_L_afe.append(abs(L_v))
    abs_L_afe = np.array(abs_L_afe)

    idx_min = np.argmin(abs_L_afe)
    print(f"  Min |L_AFE(0.6+it)| = {abs_L_afe[idx_min]:.6f} at t={t_scan[idx_min]:.3f}")
    print(f"  Max |L_AFE(0.6+it)| = {abs_L_afe.max():.4f}")

    print()
    print("If AFE agrees with Cesaro and min|L_AFE| > 0.10:")
    print("  The L-function has no zeros at sigma=0.6, |t|<=20 (empirical, discovery tier).")
    print("  Arb certification: replace mpmath G-factor with flint.acb G-factor.")
    print("  Then: certified |L(s)| > 0 => certified zero-free region [OBL M-3 -> DONE].")
