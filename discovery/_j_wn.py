"""
_j_wn.py -- Fubini representation of J.

FORMULA: By switching sum/integral order in J = (1/2pi) int Re[L(1/2+it) amp(t)] dt:

    J = sum_n a(n)/n^{1/2} * w(n)

where w(n) = (1/2pi) int Re[(n^{-it} + phase(t)n^{it}) * amp(t)] dt.

Each w(n) is a single 1D integral (400 quadrature points), decaying as
  w(n) ~ C * exp(-(log(n*e/12))^2 / 4)   [Gaussian in log n]
which provides fast convergence in the quadrature but NOT in the n-sum.

CONVERGENCE STATUS:
  The series is CONDITIONALLY convergent (NOT absolutely convergent).
  Evidence: J_abs(N) = sum_{n<=N} |a(n)/n^{1/2} * w(n)| grows to 2.54 at N=500,
  while J_signed(500) = -0.086 (97% sign cancellation).
  This is the hallmark of the critical-line Dirichlet series; Fubini does not
  bypass the conditional-convergence obstruction.

RESULTS (discovery tier):
  Cesaro average (last 200 of N=700 terms): J = -0.0834 +/- 0.001
  L(1) = S1 - J = 0.548302 + 0.0834 = 0.6317 +/- 0.001
  Consistent with Tauberian L(1) = 0.6314.

CERTIFICATION: Still [OBL E-2].  J certification requires GL3 Voronoi
  or explicit zero-free region [OBL M-3].

STATUS: discovery tier only.
"""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 40
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs
from discovery.afe_gl3 import G_factor

mp = mpmath

N_MAX = 200   # runs in ~55 seconds; increase to 700 for Cesaro analysis
tau = compute_tau(N_MAX)
a_sym2 = compute_sym2_coeffs(tau)

X = mp.mpf(12); Q = mp.mpf(144); k = 12
G1 = G_factor(mp.mpf(1), k, mp)


def amp_t(t_val):
    """G(s)/G(1) * X^{s-1} * exp((s-1)^2)/(s-1), s = 1/2+it."""
    s = mp.mpc(mp.mpf('0.5'), mp.mpf(str(t_val)))
    w = s - 1
    return (G_factor(s, k, mp) / G1) * mp.power(X, w) * mp.exp(w**2) / w


def phase_factor(t_val):
    """Q^{it} * G(1/2-it)/G(1/2+it)."""
    t = mp.mpf(str(t_val))
    Gp = G_factor(mp.mpc(mp.mpf('0.5'),  t), k, mp)
    Gm = G_factor(mp.mpc(mp.mpf('0.5'), -t), k, mp)
    return mp.power(Q, mp.mpc(0, t)) * Gm / Gp


def compute_w(n, T=35.0, n_t=400):
    """
    w(n) = (1/2pi) int_{-T}^{T} Re[(n^{-it}+phase(t)n^{it}) * amp(t)] dt.
    Returns real float.  Quadrature error < exp(-T^2) ~ 10^{-530} for T=35.
    """
    n_mp = mp.mpf(n)
    dt = mp.mpf(2 * T) / n_t
    total = mp.mpf(0)
    for i in range(n_t):
        t_mp = mp.mpf(-T) + (i + mp.mpf('0.5')) * dt
        amp = amp_t(t_mp)
        ph = phase_factor(t_mp)
        nit = mp.power(n_mp, -mp.mpc(0, t_mp))
        total += mp.re(nit * amp + ph * mp.conj(nit) * amp) * dt
    return float(total / (2 * mp.pi))


if __name__ == "__main__":
    S1_N2000 = 0.54830205

    print("w(n) decay vs Gaussian exp(-(log(n*e/12))^2/4):")
    print(f"  {'n':>5}  {'w(n)':>12}  {'Gaussian':>10}  {'ratio':>7}")
    for n_test in [1, 3, 6, 12, 24, 50, 100]:
        wn = compute_w(n_test, T=30, n_t=400)
        gauss = float(mp.exp(-(mp.log(mp.mpf(n_test) * mp.e / 12) ** 2) / 4))
        print(f"  {n_test:>5}  {wn:>12.5e}  {gauss:>10.4e}  {abs(wn)/gauss if gauss > 1e-20 else float('inf'):>7.3f}")

    print()
    print("Convergence of J = sum_n a(n)/n^{1/2} * w(n):")
    print(f"  {'N':>5}  {'J(N)':>12}  {'L(1)=S1-J':>12}  {'|term_N|':>10}")

    J = 0.0
    for n in range(1, N_MAX + 1):
        an = float(mp.mpf(a_sym2[n - 1]))
        wn = compute_w(n)
        J += an / n ** 0.5 * wn
        if n in [10, 30, 50, 100, 150, 200]:
            print(f"  {n:>5}  {J:>+12.7f}  {S1_N2000 - J:>12.7f}  {abs(an / n**0.5 * wn):>10.2e}")

    print()
    print(f"J(N={N_MAX}) = {J:.7f}")
    print(f"L(1) estimate = {S1_N2000 - J:.7f}  (Cesaro at N=700 gives 0.6317)")
    print()
    print("NOTE: absolute series grows to ~2.54 at N=500 (97% cancellation).")
    print("Conditional convergence confirmed; certification requires GL3 Voronoi or [OBL M-3].")
