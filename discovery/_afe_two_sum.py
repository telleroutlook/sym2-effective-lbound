"""Compute the two-sum GL3 AFE at natural scale sqrt(Q)=12."""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 25
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs
from discovery.afe_gl3 import afe_weight, G_factor

tau = compute_tau(3000)
a = compute_sym2_coeffs(tau)
mp = mpmath

def W2_weight(y, k=12, dps=25, T_max=40.0, n_quad=400):
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
N1 = min(int(6 * sqrtQ), len(a))
print(f"S1: sum a(n)/n * W_afe(n/{sqrtQ}) for n=1..{N1}")
s1 = sum(a[n-1]/n * afe_weight(n/sqrtQ, s0=1.0, k=12, dps=20, T_max=25, n_quad=200)
         for n in range(1, N1+1))
print(f"  S1 = {s1:.6f}")

N2 = min(int(12 * sqrtQ), len(a))  # go to ~12*12=144 to capture W2 tail
print(f"S2: sum a(n) * W2(n/{sqrtQ}) for n=1..{N2}")
s2_raw = sum(a[n-1] * W2_weight(n/sqrtQ, dps=20, T_max=25, n_quad=200)
             for n in range(1, N2+1))
s2 = s2_raw / sqrtQ
print(f"  S2_raw = {s2_raw:.6f}")
print(f"  S2 = {s2:.6f}")
print(f"  S1+S2 = {s1+s2:.6f}  (target L(1) ~ 0.6314)")
print(f"  Error = {s1+s2-0.6314:.5f}")
