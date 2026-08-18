"""Diagnose convergence of S1+S2 as function of N2."""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 20
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs, l_at_s
from discovery.afe_gl3 import afe_weight, G_factor

tau = compute_tau(3000)
a = compute_sym2_coeffs(tau)
mp = mpmath

def W2_weight_fast(y, k=12, T_max=15.0, n_quad=40):
    """Fast W2 with fewer quadrature points (for convergence testing)."""
    y = mp.mpf(y); c = mp.mpf('0.5')
    dt = 2 * T_max / n_quad
    integral = mp.mpc(0)
    G1 = G_factor(mp.mpf(1), k, mp)
    for i in range(n_quad):
        t = -T_max + (i + 0.5) * dt
        v = c + mp.mpc(0, t)
        integral += G_factor(v, k, mp) / G1 * mp.power(y, -v) * mp.exp(v**2) / v * dt
    return float(mp.re(integral) / (2 * mp.pi))

sqrtQ = 12.0

# S1 fixed (already computed)
S1 = 0.548490
print(f"S1 (fixed) = {S1:.6f}")

# Reference: Tauberian L(1) estimate
L1_tauberian = l_at_s(a, 1.01)  # near s=1
print(f"L partial sum at s=1.01, N=3000: {L1_tauberian:.6f}")
print(f"L partial sum at s=1.001, N=3000: {l_at_s(a, 1.001):.6f}")
print()

# Precompute W2 for n=1..400 (fast, n_quad=40)
print("Precomputing W2(n/12) for n=1..400...")
w2_vals = {}
for n in range(1, 401):
    w2_vals[n] = W2_weight_fast(n / sqrtQ, T_max=15.0, n_quad=40)
    if n % 50 == 0:
        print(f"  n={n:3d}: W2({n/sqrtQ:.3f}) = {w2_vals[n]:.6f}")

print()
print("Convergence of S2 = (1/12) * sum a(n)*W2(n/12):")
print(f"  {'N2':>5}  {'S2':>10}  {'S1+S2':>10}  {'vs 0.6314':>10}")
S2_cumul = 0.0
for n in range(1, 401):
    S2_cumul += a[n-1] * w2_vals[n]
    if n in [10, 20, 50, 100, 144, 200, 300, 400]:
        S2 = S2_cumul / sqrtQ
        print(f"  {n:5d}  {S2:10.6f}  {S1+S2:10.6f}  {S1+S2-0.6314:+10.5f}")

print()
# Also compute S1+S2 with the exact S1 recomputed fresh (to check S1 itself)
print("Recomputing S1 with fresh quad for verification...")
S1_new = sum(a[n-1]/n * afe_weight(n/sqrtQ, s0=1.0, k=12, dps=15, T_max=20, n_quad=100)
             for n in range(1, 73))
print(f"  S1 (fresh) = {S1_new:.6f}")
S2_at_144 = sum(a[n-1] * w2_vals.get(n, 0) for n in range(1, 145)) / sqrtQ
print(f"  S2 (N=144) = {S2_at_144:.6f}")
print(f"  S1+S2      = {S1_new+S2_at_144:.6f}")
