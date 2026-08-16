"""
_voronoi_test.py -- Numerical test of GL3 Voronoi dual formula for J.

HYPOTHESIS: J = C * sum_n a(n)/n^{1/2} * B_dual(n)

where B_dual(n) = int_0^inf w(y) * K_natural(y * n / Q) * dy/y  (or dy)

and K_natural(z) = (1/2pi) int G(1/2+it)/G(1) * z^{-1/2-it} dt
    w(y)         = (1/2pi) int Re[(y^{-it}+phase*y^{it}) * amp(t)] dt

If this holds:
  - B_dual(n) decays as exp(-c*(n/Q)^{2/3}) -> only need ~10 terms
  - Tail sum is ABSOLUTELY CONVERGENT (|a(n)| <= d_3(n), |B_dual(n)| decreases fast)
  - This certifies J without zero-free region [OBL M-3]!

STRATEGY:
  1. Pre-compute w(y_i) for y_i in [0.05, 300] (60 log-spaced points)
  2. Pre-compute K_natural(z_j) for z_j needed
  3. For n_dual=1..10: B_dual(n) via trapezoidal rule in log-y space
  4. Find C by matching sum to J_cesaro = -0.0834
  5. Verify B_dual(n) decays as expected
"""
import sys; sys.path.insert(0, '.')
import math
import mpmath; mpmath.mp.dps = 30
from discovery.afe_gl3 import G_factor
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs

mp = mpmath
k = 12
Q = mp.mpf(144)
X = mp.mpf(12)
G1 = G_factor(mp.mpf(1), k, mp)

# ---------------------------------------------------------------------------
# Core integrands (low-precision for speed)
# ---------------------------------------------------------------------------
def amp_t(t_val):
    s = mp.mpc(mp.mpf('0.5'), mp.mpf(str(t_val)))
    w = s - 1
    return (G_factor(s, k, mp) / G1) * mp.power(X, w) * mp.exp(w**2) / w

def phase_factor(t_val):
    t = mp.mpf(str(t_val))
    Gp = G_factor(mp.mpc(mp.mpf('0.5'),  t), k, mp)
    Gm = G_factor(mp.mpc(mp.mpf('0.5'), -t), k, mp)
    return mp.power(Q, mp.mpc(0, t)) * Gm / Gp

def w_func(y_val, T=30.0, n_t=200):
    """w(y) for real y."""
    y = mp.mpf(y_val)
    dt = mp.mpf(2 * T) / n_t
    total = mp.mpf(0)
    for i in range(n_t):
        t = mp.mpf(-T) + (i + mp.mpf('0.5')) * dt
        amp = amp_t(t)
        ph = phase_factor(t)
        yit = mp.power(y, -mp.mpc(0, t))
        total += mp.re(yit * amp + ph * mp.conj(yit) * amp) * dt
    return float(total / (2 * mp.pi))

def K_natural(z_val, T=50.0, n_t=500):
    """K(z) = (1/2pi) int G(1/2+it)/G(1) * z^{-1/2-it} dt."""
    z = mp.mpf(z_val)
    dt = mp.mpf(2 * T) / n_t
    total = mp.mpf(0)
    for i in range(n_t):
        t = mp.mpf(-T) + (i + mp.mpf('0.5')) * dt
        Gs = G_factor(mp.mpc(mp.mpf('0.5'), t), k, mp)
        total += mp.re(Gs / G1 * mp.power(z, mp.mpc(mp.mpf('-0.5'), -t))) * dt
    return float(total / (2 * mp.pi))


# ---------------------------------------------------------------------------
# Step 1: Pre-compute w on log-spaced grid
# ---------------------------------------------------------------------------
print("Step 1: Computing w(y) on grid [0.1, 200] ...")
import numpy as np

# log-spaced y grid
y_grid = np.logspace(math.log10(0.1), math.log10(200.0), 50)
w_vals = []
for y in y_grid:
    wv = w_func(y)
    w_vals.append(wv)
    print(f"  w({y:.3f}) = {wv:.6e}")
w_vals = np.array(w_vals)
print()


# ---------------------------------------------------------------------------
# Step 2: Compute B_dual(n) for n=1..8
# ---------------------------------------------------------------------------
# B_dual(n) = int_0^inf w(y) * K_natural(y * n / Q) * dy/y   [Mellin-style]
# or         = int_0^inf w(y) * K_natural(y * n / Q) * dy    [L1-style]
#
# We try BOTH and see which gives J = C * sum a(n)/n^{1/2} * B_dual(n)

N_MAX_COEFF = 30
tau_arr = compute_tau(N_MAX_COEFF)
a_sym2 = compute_sym2_coeffs(tau_arr)

J_CESARO = -0.0834  # from _j_wn.py Cesaro average
S1_N2000 = 0.548302

print("Step 2: Computing B_dual(n) = int w(y) K(yn/Q) dy/y for n=1..8")
print()

Q_float = 144.0

B_dual_mellin = []  # using dy/y (Mellin measure)
B_dual_L1     = []  # using dy (L^1 measure)
B_dual_sqrt   = []  # using sqrt(y) dy (testing)

for n_dual in range(1, 9):
    z_vals = y_grid * n_dual / Q_float
    K_vals = np.array([K_natural(float(z)) for z in z_vals])

    # Trapezoidal rule in log(y): int f(y) dy/y = int f(exp(t)) dt
    log_y = np.log(y_grid)
    integrand_mellin = w_vals * K_vals  # f(y) dy/y -> f(y) d(log y)
    integrand_L1     = w_vals * K_vals * y_grid  # f(y) dy -> f(y) * y * d(log y)
    integrand_sqrt   = w_vals * K_vals * np.sqrt(y_grid)

    # Trapezoidal integration in log space
    B_m = float(np.trapezoid(integrand_mellin, log_y))
    B_l = float(np.trapezoid(integrand_L1, log_y))
    B_s = float(np.trapezoid(integrand_sqrt, log_y))

    B_dual_mellin.append(B_m)
    B_dual_L1.append(B_l)
    B_dual_sqrt.append(B_s)
    print(f"  n={n_dual}: B_dual/y={B_m:.5e}  B_dual_dy={B_l:.5e}  B_dual_sdy={B_s:.5e}")

print()

# ---------------------------------------------------------------------------
# Step 3: Sum J_voronoi = C * sum a(n)/n^{1/2} * B_dual(n)
# ---------------------------------------------------------------------------
print("Step 3: Computing J_voronoi sums (trying to match J_cesaro = -0.0834)")
print()

# Compute a(n)/n^{1/2} for n=1..8
an_over_sqrtn = [float(a_sym2[n-1]) / math.sqrt(n) for n in range(1, 9)]

for label, B_list in [("dy/y", B_dual_mellin), ("dy", B_dual_L1), ("sqrt(y)dy", B_dual_sqrt)]:
    partial_sum = sum(an_over_sqrtn[i] * B_list[i] for i in range(8))
    if abs(partial_sum) > 1e-12:
        C_empirical = J_CESARO / partial_sum
    else:
        C_empirical = float('nan')
    print(f"  Measure {label:12s}: sum_n an/sqrtn * B_dual(n) = {partial_sum:.6f}")
    print(f"    -> C to match J_cesaro: {C_empirical:.6f}")
    print(f"    -> J_voronoi with C=1: {partial_sum:.6f} (J_cesaro = {J_CESARO})")
    print()

# ---------------------------------------------------------------------------
# Step 4: Decay of B_dual(n) -- does it go as exp(-c*(n/Q)^{2/3})?
# ---------------------------------------------------------------------------
print("Step 4: Decay check of B_dual(n) (Mellin measure):")
print(f"  {'n':>4}  {'B_dual(n)':>14}  {'|B_dual|':>14}  {'ratio n+1/n':>12}")
prev = None
for i, (n, B) in enumerate(zip(range(1, 9), B_dual_mellin)):
    if prev is not None and abs(prev) > 1e-20:
        ratio = abs(B) / abs(prev)
    else:
        ratio = float('nan')
    print(f"  {n:>4}  {B:>14.5e}  {abs(B):>14.5e}  {ratio:>12.6f}")
    prev = B

print()
print("If B_dual(n) decays as exp(-c*n^{2/3}), ratio should decrease rapidly.")
print("If decay is superpolynomial, only 5-10 terms needed for certified J.")
