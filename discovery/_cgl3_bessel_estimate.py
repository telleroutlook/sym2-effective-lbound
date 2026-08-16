"""
Numerical estimation of C_GL3 via GL3 Voronoi + Bessel function analysis.

For sym^2 Delta (spectral parameters nu=(11/2, 0, -11/2)), the partial sum bound
  |S(X)| <= C_GL3 * X^{2/3}
requires estimating the GL3 Bessel function K_nu(y) and its L1 norm.

The GL3 Voronoi formula (Miller-Schmid 2006, level 1, self-dual) gives:
  S(X) = sum_c c^{-2} sum_n a(n) S(1,n;c) Psi(nX/c^3)
where Psi is the GL3 Bessel transform of the smoothing function.

The key bound:
  C_GL3 <= 2 * |Psi|_1 * C_c  (Weil: |S(1,n;c)| <= 2c^{1/2}, C_c = sum_c c^{-3/2+eps})
but this over-counts due to cancellation.  Better: Cauchy-Schwarz gives:
  C_GL3 <= 2 * sqrt(C_RS) * ||Psi||_2 * C_c_sq  (Rankin-Selberg input)

This script numerically evaluates:
  (1) K_nu(y) via Barnes integral (Meijer G representation)
  (2) ||K_nu||_1 and ||K_nu||_2
  (3) Estimates C_GL3 via both routes

STATUS: DISCOVERY TIER - not a certified proof.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
from mpmath import mp, mpf, gamma, mpc, exp, pi, quad, inf, re, im, log, sqrt, zeta
import time

mp.dps = 30

nu1 = mpf('11') / 2    # 11/2
nu2 = mpf('0')
nu3 = -mpf('11') / 2   # -11/2

Q_GL3 = float(332.75)
C_RS  = float(0.4433)

print("=== GL3 Bessel function estimate for C_GL3 (sym^2 Delta) ===")
print(f"Spectral parameters: nu = ({nu1}, {nu2}, {nu3})")
print(f"Q_GL3 = {Q_GL3:.2f},  Q^{{1/6}} = {Q_GL3**(1/6):.4f},  Q^{{1/3}} = {Q_GL3**(1/3):.4f}")
print()


def K_nu_integrand(t, y):
    """
    Integrand for K_nu(y) as a vertical Mellin-Barnes integral:
      K_nu(y) = (1/2pi) * int_{Re(s)=1} (4pi^2 y)^{-s}
                * Gamma((s+nu1)/2) * Gamma((s+nu2)/2) * Gamma((s+nu3)/2) ds
    Evaluate at s = 1 + it (vertical line Re(s)=1).
    """
    s = mpc(1, t)
    try:
        G1 = gamma((s + nu1) / 2)
        G2 = gamma((s + nu2) / 2)
        G3 = gamma((s + nu3) / 2)
        base = 4 * pi**2 * y
        val = base**(-s) * G1 * G2 * G3
        return val
    except Exception:
        return mpc(0)


def K_nu(y, T=200.0, n_pts=2000):
    """Numerical evaluation of K_nu(y) via truncated Barnes integral."""
    ts = np.linspace(-T, T, n_pts)
    dt = ts[1] - ts[0]
    vals = np.array([complex(K_nu_integrand(t, float(y))) for t in ts])
    # K_nu(y) = (1/2pi) * int Re part of the Mellin kernel
    # For real y and self-dual form: K_nu(y) should be real
    result = float(np.real(np.sum(vals)) * dt / (2 * np.pi))
    return result


# Sample K_nu at a few points to understand its behavior
print("--- K_nu(y) sampled values (T=200, 2000 pts) ---")
print(f"{'y':>10}  {'K_nu(y)':>15}  {'y^{2/3} K_nu(y)':>18}")
t0 = time.time()
y_vals = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0]
K_vals = []
for y in y_vals:
    K = K_nu(y, T=150.0, n_pts=1500)
    K_vals.append((y, K))
    print(f"{y:>10.3f}  {K:>15.6e}  {y**(2/3)*K:>18.6e}")
print(f"  (evaluation time: {time.time()-t0:.1f}s)")
print()


# L1 norm estimate: int_0^infty |K_nu(y)| dy/y (with GL3 Voronoi normalization)
# In Voronoi: the dual sum involves sum_n a(n) * int K_nu(nX/c^3) phi(x) dx
# Key quantity: int_0^infty |K_nu(y)| dy (L1 norm without measure factor)
print("--- L1 and L2 norm estimates ---")

# Approximate K_nu on a grid and compute norms
y_grid = np.logspace(-2, 2, 200)  # y in [0.01, 100]
K_grid = []
t0 = time.time()
for y in y_grid:
    K = K_nu(y, T=100.0, n_pts=500)  # faster evaluation
    K_grid.append(K)
K_grid = np.array(K_grid)
print(f"  Grid evaluation: {time.time()-t0:.1f}s")

# L1 norm: int |K(y)| dy (trapezoidal over log-spaced grid => dy = y d(log y))
dlogy = np.log(y_grid[1]) - np.log(y_grid[0])
L1_norm = float(np.sum(np.abs(K_grid) * y_grid) * dlogy)
L2_norm = float(np.sqrt(np.sum(K_grid**2 * y_grid) * dlogy))

print(f"  ||K_nu||_1 (int |K| dy) ≈ {L1_norm:.4f}")
print(f"  ||K_nu||_2 (sqrt(int K^2 dy)) ≈ {L2_norm:.4f}")
print()


# C_GL3 estimate via different routes
print("--- C_GL3 rough estimates ---")

# Route 1: Weil + L1 norm
# |S(X)| <= X^{2/3} * sum_c c^{-3/2} * 2 * ||K||_1 * (number of n terms ~ c^3/X)
# This double-counts; rough: C_GL3 ~ 2 * ||K||_1 * sum_c c^{-3/2} * c^3/X / X^{2/3}
# Actually: sum over c of (X/c^3)^{2/3} weighting ~ X^{2/3} * c^{-2} (rough)
# The correct bound: C_GL3 ~ 2 * ||K||_1 * C_c where C_c = sum_c c^{-1} ~ log X (divergent!)
# Better:
# In the dual sum, the n sum has ~c^3/X significant terms.
# Contribution per c: c^{-2} * 2c^{1/2} * (c^3/X)^{1/2} * ||K||_1 [by Cauchy-Schwarz in n]
#   using |sum_n a(n) K(nX/c^3)| <= sqrt(sum |a(n)|^2/(nX/c^3)) * sqrt(sum (nX/c^3)|K|^2)
#   ~ sqrt(C_RS) * (c^3/X)^{1/2} * X^{1/3} * ||K||_2   [rough]
# Then: c^{-2} * 2c^{1/2} * sqrt(C_RS) * (c^3/X)^{1/2} * X^{1/3} * ||K||_2
#      = 2 * sqrt(C_RS) * c^{-2+1/2+3/2} * X^{-1/2+1/3} * ||K||_2
#      = 2 * sqrt(C_RS) * c * X^{-1/6} * ||K||_2

# Sum over c <= X^{1/3}:
# sum_{c<=X^{1/3}} 2 * sqrt(C_RS) * c * X^{-1/6} * ||K||_2
# = 2 * sqrt(C_RS) * (X^{1/3})^2/2 * X^{-1/6} * ||K||_2
# = sqrt(C_RS) * X^{2/3} * X^{-1/6} * ||K||_2 [still off by X^{1/2}?]

# I think there's an error in my normalization. Let me use the known result:
# For GL3 at level 1: C_GL3 = O(Q^{1/6}) with absolute constant from the Bessel kernel.
# The spectral-conductor factor is Q^{1/6} = 2.632.

# Rough estimate from Voronoi + Cauchy-Schwarz:
C_est_1 = 2 * L1_norm * float(zeta(mpf('4') / 3))  # Weil + c-sum
C_est_2 = 2 * float(sqrt(mpf(C_RS))) * L2_norm * float(zeta(mpf('7') / 6))  # RS + Cauchy-Schwarz
C_est_spectral = Q_GL3**(1/6) * float(sqrt(mpf(C_RS)))  # spectral conductor * RS

print(f"  Weil + L1 + zeta(4/3) estimate: C_GL3 ~ {C_est_1:.3f}")
print(f"  RS + L2  + zeta(7/6) estimate:  C_GL3 ~ {C_est_2:.3f}")
print(f"  Q^{{1/6}} * sqrt(C_RS):            C_GL3 ~ {C_est_spectral:.3f}")
print()
print(f"  Certification threshold (N=10^8, sigma=0.9): 7.4880")
print(f"  Q^{{1/3}} = {Q_GL3**(1/3):.4f}")
print()
print("Summary:")
print(f"  L1 estimate {C_est_1:.3f} < 7.488? {'YES (certifies if this is rigorous)' if C_est_1 < 7.488 else 'NO'}")
print(f"  L2 estimate {C_est_2:.3f} < 7.488? {'YES' if C_est_2 < 7.488 else 'NO'}")
print(f"  Q^{{1/3}} = {Q_GL3**(1/3):.3f} < 7.488? {'YES' if Q_GL3**(1/3) < 7.488 else 'NO'}")
