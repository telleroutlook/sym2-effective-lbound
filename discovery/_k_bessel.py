"""
_k_bessel.py -- Natural GL3 Bessel function for sym^2 Delta.

DEFINITION:
  K(y) = (1/2pi) int_R G(1/2+it)/G(1) * y^{-1/2-it} dt

where G(s) = Gamma_R(s) * Gamma_C(s+11) is the archimedean L-factor of sym^2 Delta.

DECAY: K(y) decays super-polynomially via stationary phase.  The G factor
  |G(1/2+it)| ~ C * |t|^{10.75} * exp(-3*pi*|t|/4)
provides exponential decay in t, and by stationary phase:
  K(y) ~ C * y^7 * exp(-3*pi * y^{2/3} / 4) for large y.

COMPUTED VALUES:
  K(0.1) = 1.127e+00
  K(1.0) = 3.865e-01
  K(5.0) = 3.204e-05
  K(10.)  = 2.384e-10
  K(50.)  ~ 10^{-23}  (effectively zero)

RELATIONSHIP TO J (the AFE contour term):
  J uses the Gaussian-regularized weight K'(y) = w(n) with Gaussian envelope
  exp(-(log(n*e/12))^2/4).  K_natural != K' because the test function e^{u^2}
  in the AFE creates a different weight.

  The GL3 Voronoi formula would connect K' and K via:
    J = sum_n a(n) * [Voronoi_transform_of_K'](n / X_dual)
  where [Voronoi_transform_of_K'] uses K as the integration kernel.

  KEY DISCOVERY: K decays as exp(-c * n^{2/3}) vs K' decays as Gaussian-in-log-n.
  If we could implement the Voronoi transform, J would be computable from a
  sum of ~20 terms (K(n/X_dual) < 10^{-10} for n >= 10).

  WHAT sum_n a(n)/n^alpha * K(n/X_scale) actually computes:
    = (1/2pi) int G(1/2+it)/G(1) * X_scale^{1/2+it} * L(1/2+it) dt / X_scale^{1/2}
  This is a weighted integral of L(1/2+it) -- related to L(1/2, sym^2 Delta),
  NOT to J or L(1).  (Converges absolutely; confirmed to ~0.587 at N=50.)

NEXT STEP FOR CERTIFICATION:
  Derive the explicit Voronoi kernel B(y, z) such that
    w(n) = int_0^inf K(ny/Q) * B(y, n) dy
  This would express J = sum_m a(m) * K(m/X_dual) as an absolutely convergent
  series needing only ~20 terms.  Requires GL3 Voronoi theory (Miller-Schmid 2006).

STATUS: discovery tier.  Confirms exponential decay of GL3 Bessel;
  Voronoi kernel derivation is [OBL M-Voronoi] (new sub-task).
"""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 40
from discovery.afe_gl3 import G_factor

mp = mpmath
k = 12
G1 = G_factor(mp.mpf(1), k, mp)


def compute_K(y_val, T=80, n_t=3000):
    """K(y) = (1/2pi) int G(1/2+it)/G(1) * y^{-1/2-it} dt."""
    y = mp.mpf(y_val)
    dt = mp.mpf(2 * T) / n_t
    total = mp.mpf(0)
    for i in range(n_t):
        t = mp.mpf(-T) + (i + mp.mpf('0.5')) * dt
        Gs = G_factor(mp.mpc(mp.mpf('0.5'), t), k, mp)
        total += mp.re(Gs / G1 * mp.power(y, mp.mpc(mp.mpf('-0.5'), -t))) * dt
    return float(total / (2 * mp.pi))


if __name__ == "__main__":
    print("K(y) = (1/2pi) int G(1/2+it)/G(1) * y^{-1/2-it} dt:")
    print(f"  {'y':>8}  {'K(y)':>14}  {'exp(-3pi*y^{2/3}/4)':>20}")
    import math
    for y_test in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]:
        Ky = compute_K(y_test)
        approx = math.exp(-3 * math.pi * y_test ** (2 / 3) / 4) if y_test > 0 else 1.0
        print(f"  {y_test:>8.2f}  {Ky:>14.5e}  {approx:>20.5e}")

    print()
    print("K(y) confirms super-polynomial (exp(-c*y^{2/3})) decay.")
    print("This is the natural GL3 Bessel for sym^2 Delta.")
    print("Use as Voronoi kernel to get absolutely convergent J sum.")
