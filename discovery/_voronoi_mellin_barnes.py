"""
GL3 Voronoi formula test via Mellin-Barnes integral (smooth test function).

Correct formula: for phi(n) = exp(-n/X),
  Sum_n a(n) * exp(-n/X) = Sum_n a(n) * Phi(n)   [self-dual: a*(n)=a(n)]

where the Voronoi transform Phi(n) has Mellin transform:
  Phi_hat(s) = R(s) * phi_hat(1-s)

with:
  R(s)       = Gamma_GL3(1-s) / Gamma_GL3(s)
  phi_hat(s) = X^s * Gamma(s)   (Mellin transform of exp(-n/X) is X^s * Gamma(s))

So:
  Phi_hat(s) = R(s) * X^{1-s} * Gamma(1-s)
  Phi(n)     = (1/2pi) integral R(1/2+it) * X^{1/2-it} * Gamma(1/2-it) * n^{-(1/2+it)} dt

For sym^2(Delta) with GL3 spectral parameters mu = (11, 0, -11):
  Gamma_GL3(s) = GammaR(s+11) * GammaR(s) * GammaR(s-11)
  GammaR(s)    = pi^{-s/2} * Gamma(s/2)

Test: does sum_n a(n) * Phi(n) = sum_n a(n) * exp(-n/X)?
If YES -> Voronoi formula is verified; C_GL3 can be extracted.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import mpmath
import time

mpmath.mp.dps = 25  # 25 significant digits

# --- GL3 Gamma factor machinery ---

def GammaR_mp(s):
    """GammaR(s) = pi^{-s/2} * Gamma(s/2), s complex mpmath."""
    return mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2)

def R_ratio_mp(s, mu=(11, 0, -11)):
    """
    R(s) = Gamma_GL3(1-s) / Gamma_GL3(s)
    Gamma_GL3(s) = prod_j GammaR(s+mu_j)
    """
    mu1, mu2, mu3 = mu
    num = GammaR_mp(1-s+mu1) * GammaR_mp(1-s+mu2) * GammaR_mp(1-s+mu3)
    den = GammaR_mp(s+mu1) * GammaR_mp(s+mu2) * GammaR_mp(s+mu3)
    return num / den

def integrand_Phi(t, n, X):
    """
    Integrand of Phi(n) at s = 1/2 + it:
    R(1/2+it) * X^{1/2-it} * Gamma(1/2-it) * n^{-(1/2+it)}
    (real part only — Phi is real by symmetry for self-dual forms)
    """
    s = mpmath.mpf('0.5') + mpmath.mpc(0, t)
    R = R_ratio_mp(s)
    Xfact = mpmath.power(X, 1-s)       # X^{1/2-it}
    Gfact = mpmath.gamma(1-s)          # Gamma(1/2-it)
    nfact = mpmath.power(n, -s)        # n^{-(1/2+it)}
    val = R * Xfact * Gfact * nfact
    return float(val.real)

def Phi_voronoi(n, X, T_max=20.0):
    """
    Phi(n) = (1/2pi) * integral_{-T}^{T} R(1/2+it)*X^{1/2-it}*Gamma(1/2-it)*n^{-(1/2+it)} dt
    """
    # Gamma(1/2-it) decays as exp(-pi*|t|/2) -> very fast convergence; T=20 is ample.
    val, err = mpmath.quad(lambda t: integrand_Phi(t, n, X), [-T_max, 0, T_max],
                           error=True, maxdegree=6)
    return float(val) / (2 * float(mpmath.pi))

# --- Load sym2 coefficients ---
print("Loading a_sym2 (N=500)...", flush=True)
t0 = time.time()
from discovery._fast_tau_sieve import compute_tau_fast, compute_a_sym2
N_ref = 500
tau_f = compute_tau_fast(N_ref)
a_arr = compute_a_sym2(tau_f)
a_vals = np.array([float(a_arr[i]) for i in range(N_ref)], dtype=np.float64)
print(f"  Done in {time.time()-t0:.1f}s", flush=True)

# --- Quick sanity check: R(1/2+it) magnitudes ---
print("\nSanity check: R(1/2+it) for sym^2(Delta) (mu=(11,0,-11)):")
for t_val in [0.0, 1.0, 5.0, 10.0]:
    s = mpmath.mpf('0.5') + mpmath.mpc(0, t_val)
    r = R_ratio_mp(s)
    print(f"  t={t_val:5.1f}: |R| = {abs(r):.6f},  arg = {float(mpmath.arg(r)):.4f} rad")

print()
print("Testing Voronoi formula: sum_n a(n)*exp(-n/X) vs sum_n a(n)*Phi(n,X)")
print("(Self-dual: a*(n) = a(n) for sym^2 Delta)")
print()

X_tests = [10, 50, 100]
for X in X_tests:
    # Direct sum: sum_n a(n) * exp(-n/X)
    ns = np.arange(1, N_ref+1, dtype=np.float64)
    direct = float(np.sum(a_vals * np.exp(-ns / X)))

    print(f"X = {X}")
    print(f"  Direct sum = {direct:.8f}")

    # Voronoi dual: sum_n a(n) * Phi(n, X)
    # The dominant contribution comes from n ~ X (where exp(-n/X) ~ e^{-1}).
    # Phi(n) decays fast for n >> X, so sum n=1..3X is sufficient.
    M = min(3*X + 20, N_ref)

    t_start = time.time()
    voronoi_sum = 0.0
    phi_vals = []
    for n in range(1, M+1):
        phi_n = Phi_voronoi(n, X)
        phi_vals.append(phi_n)
        voronoi_sum += a_vals[n-1] * phi_n

    elapsed = time.time() - t_start
    ratio = voronoi_sum / direct if abs(direct) > 1e-10 else float('nan')

    print(f"  Voronoi sum = {voronoi_sum:.8f}   ({elapsed:.1f}s for {M} terms)")
    print(f"  Ratio (Voronoi/Direct) = {ratio:.6f}  (target: 1.000000)")

    # Print first few Phi values for diagnostics
    print(f"  First 5 Phi values:")
    for n in range(1, min(6, M+1)):
        p = phi_vals[n-1]
        expval = np.exp(-n/X)
        print(f"    n={n}: exp(-n/X)={expval:.6f}, Phi(n)={p:.6f}, ratio={p/expval if expval>1e-10 else 'nan':.4f}")
    print()

print("="*60)
print("CONCLUSION:")
print("  ratio ~ 1 -> GL3 Voronoi formula verified (smooth test function)")
print("  ratio != 1 -> normalization or spectral parameters wrong")
