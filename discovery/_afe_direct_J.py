"""
Compute J = (1/2pi i) int_{(-1/2)} L(1+w) X^w G(1+w)/G(1) e^{w^2}/w dw
DIRECTLY on the contour Re(w)=-1/2 by summing L(1/2+it) as a partial Dirichlet series.

This avoids the invalid termwise interchange that breaks the formula at Re(v)=1/2.

Then: L(1) = S1 - J, which we verify against Tauberian estimate 0.6314.
"""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 25
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs
from discovery.afe_gl3 import afe_weight, G_factor

tau = compute_tau(3000)
a = compute_sym2_coeffs(tau)
mp = mpmath

# S1 = sum a(n)/n W_afe(n/X)
sqrtQ = mp.mpf(12)
N1 = 72

print("Computing S1 (precomputed for speed)...")
S1 = mp.mpf('0.548490')
print(f"  S1 = {float(S1):.6f}")

# L(1/2 + it) via partial Dirichlet series (N terms)
def L_partial(t, N=200, s0=mp.mpf('0.5')):
    """L(1/2+it, sym2Delta) as partial sum sum a(n)/n^(1/2+it)."""
    s = s0 + mp.mpc(0, t)
    total = mp.mpc(0)
    for n in range(1, N+1):
        if a[n-1] != 0:
            total += mp.mpf(a[n-1]) / mp.power(n, s)
    return total

# J = (1/2pi) int_{-T}^T L(1/2+it) * X^{-1/2+it} * G(1/2+it)/G(1) * e^{(-1/2+it)^2} / (-1/2+it) dt
# Note: the integral formula with w=-1/2+it, dw=i dt, 1/(2pi i) factor:
# J = (1/2pi) int_{-T}^T L(1/2+it) * X^(-1/2+it) * G(1/2+it)/G(1) * e^{w^2}/w dt
# where w=-1/2+it.

def compute_J(X=12, T=4.0, n_quad=200, N_L=150):
    """Compute J on Re(w)=-1/2 directly."""
    dt = 2*T / n_quad
    G1 = G_factor(mp.mpf(1), 12, mp)
    integral = mp.mpf(0)
    for i in range(n_quad):
        t = -T + (i + 0.5) * dt
        t_mp = mp.mpf(t)
        w = mp.mpc(-mp.mpf('0.5'), t_mp)
        X_mp = mp.mpf(X)
        L_val = L_partial(t_mp, N=N_L)
        G_val = G_factor(mp.mpf(1) + w, 12, mp)
        integrand = L_val * mp.power(X_mp, w) * G_val / G1 * mp.exp(w**2) / w
        # (1/2pi i) * i * dt = dt/(2pi)
        integral += mp.re(integrand) * dt
    return float(integral / (2 * mp.pi))

print("\nComputing J = (1/2pi i) int_{(-1/2)} L(1+w) X^w G(1+w)/G(1) e^{w^2}/w dw ...")
print("(With L evaluated as partial Dirichlet sum at Re(s)=1/2)")
J = compute_J(X=12, T=4.0, n_quad=300, N_L=200)
print(f"  J = {J:.6f}")
print(f"  L(1) = S1 - J = {float(S1) - J:.6f}  (target 0.6314)")
print(f"  Error vs 0.6314: {float(S1) - J - 0.6314:+.5f}")

# Verify convergence: try N_L=50, 100, 200
print("\nConvergence in N_L (partial sum length):")
for N_L in [30, 50, 100, 150, 200]:
    J_n = compute_J(X=12, T=4.0, n_quad=200, N_L=N_L)
    L1 = float(S1) - J_n
    print(f"  N_L={N_L:4d}: J={J_n:.6f}  L(1)={L1:.6f}  err={L1-0.6314:+.5f}")
