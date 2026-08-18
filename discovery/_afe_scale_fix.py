"""
Verify two-sum AFE formula with CORRECT scale: W2(n) not W2(n/12).

Derivation:
  S1 = L(1) + J  where J = (1/2pi i) int_{(-1/2)} L(1+w) X^w G(1+w)/G(1) e^{w^2}/w dw
  Using F.E. G(1-v)L(1-v) = Q^{v-1/2} G(v)L(v) and sub w=-v:
    J = -Q^{-1/2} * (1/2pi i) int_{(1/2)} G(v)/G(1) * L(v) * e^{v^2}/v dv
      = -Q^{-1/2} * sum_n a(n) * W2(n)   [y=n, NOT y=n/12]
  So L(1) = S1 + Q^{-1/2} sum_n a(n) W2(n).
"""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 20
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs
from discovery.afe_gl3 import afe_weight, G_factor

tau = compute_tau(500)
a = compute_sym2_coeffs(tau)
mp = mpmath

def W2_direct(n, k=12, T_max=20.0, n_quad=200):
    """W2(y=n) = (1/2pi i) int_{(1/2)} G(v)/G(1) n^{-v} e^{v^2}/v dv."""
    y = mp.mpf(n); c = mp.mpf('0.5')
    dt = 2 * T_max / n_quad
    integral = mp.mpc(0)
    G1 = G_factor(mp.mpf(1), k, mp)
    for i in range(n_quad):
        t = -T_max + (i + 0.5) * dt
        v = c + mp.mpc(0, t)
        integral += G_factor(v, k, mp) / G1 * mp.power(y, -v) * mp.exp(v**2) / v * dt
    return float(mp.re(integral) / (2 * mp.pi))

print("W2(n) for n=1..15:")
w2 = {}
for n in range(1, 16):
    w2[n] = W2_direct(n)
    print(f"  n={n:2d}: W2({n}) = {w2[n]:.6f}  a(n)={a[n-1]:.4f}  contribution={(a[n-1]*w2[n]/12):.6f}")

S1 = 0.548490  # precomputed
sqrtQ = 12.0

# Build S2 with y=n
print()
s2_cum = 0.0
for n in range(1, 16):
    s2_cum += a[n-1] * w2[n]
    s2 = s2_cum / sqrtQ
    print(f"  N={n:2d}: S2={s2:.6f}  S1+S2={S1+s2:.6f}  vs 0.6314: {S1+s2-0.6314:+.5f}")

# Also check W2 decays: values for larger n
print()
print("W2(n) decay for larger n (to verify super-exponential decay):")
for n in [20, 30, 50]:
    w2n = W2_direct(n, n_quad=100)
    print(f"  n={n}: W2({n}) = {w2n:.8f}")
