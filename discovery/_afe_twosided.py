"""
Two-sided AFE verification: J as an absolutely convergent series.

Derivation:
  L(1) = S1 - J
  S1 = sum_n a(n)/n * W_afe^{s0=1}(n/X)   [integral on Re(u)=1, G(1+u)]
  J = -(1/X) * sum_n a(n) * W_dual(X/n)    [functional eq + orientation reversal]

where W_dual(y) = (1/2pi i) int_{Re(v)=1} G(v)/G(1) * y^v * e^{v^2}/v dv.

Sign derivation: applying Λ(1+z) = Λ(-z) inside J integral on Re(z)=-1/2, then
v = -z (orientation reverses: upward on Re=-1/2 becomes DOWNWARD on Re=+1/2,
introducing a minus sign). After restoring upward orientation and shifting Re(v)
from 1/2 to 1 (no poles in strip):

  J = -Q^{-1/2} * (1/2pi i) int_{Re=1} (Q/X)^v G(v)/G(1) L(v) e^{v^2}/v dv
    = -(1/X) * sum_n a(n) * W_dual(X/n)

Hence  L(1) = S1 + (1/X) * sum_n a(n) * W_dual(X/n).

W_dual decay: W_dual(y) ~ C * exp(-(log y)^2/4) for y -> 0 (saddle-point on Re=1),
so W_dual(X/n) ~ exp(-(log(n/X))^2/4) decays at the same rate as W_afe(n/X).
Both sums converge absolutely in ~670 terms.
"""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 30
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs
from discovery.afe_gl3 import G_factor, afe_weight

mp = mpmath

N_max = 200
tau = compute_tau(N_max)
a_sym2 = compute_sym2_coeffs(tau)

X = mp.mpf(12)
G1 = G_factor(mp.mpf(1), 12, mp)
T_max = 50
n_quad = 800

def w_dual(y, T=T_max, n=n_quad):
    """W_dual(y) = (1/2pi) int G(1+it)/G(1) * y^{1+it} * e^{(1+it)^2} / (1+it) dt."""
    dt = 2 * T / n
    total = mp.mpf(0)
    for i in range(n):
        t = -T + (i + 0.5) * dt
        v = mp.mpc(1, t)
        Gv = G_factor(v, 12, mp)
        integrand = Gv / G1 * mp.power(y, v) * mp.exp(v**2) / v
        total += mp.re(integrand)
    return total * dt / (2 * mp.pi)

# Verify W_afe values
print("Checking W_afe^{s0=1} is consistent with earlier computation:")
for n_test, y_expected in [(1, 0.812), (12, 0.308), (72, 0.056)]:
    y = mp.mpf(n_test) / X
    w_ref = float(afe_weight(y, mp.mpf(1), 12, 30, T_max, n_quad))
    print(f"  n={n_test:3d}: afe_weight={w_ref:.5f}  expected~{y_expected}")

print()
print("W_dual(12/n) for selected n (should decay like exp(-(log(n/12))^2/4)):")
for n_test in [1, 6, 12, 24, 72, 144]:
    y = X / mp.mpf(n_test)
    w = w_dual(y)
    saddle = mp.exp(-(mp.log(mp.mpf(n_test)/X)**2)/4)
    print(f"  n={n_test:3d}: y={float(y):.3f}  W_dual={float(w):.5f}  saddle-approx~{float(saddle):.5f}")

print()
print("Computing S1, J_dual (= -sum/12), and L(1) = S1 + sum/12 for n=1..200:")
print("(J_correct = -(1/12)*sum; L(1) = S1 - J = S1 + (1/12)*sum)")

S1 = mp.mpf(0)
J_dual_sum = mp.mpf(0)  # ∑ a(n) * W_dual(12/n)

for n in range(1, N_max + 1):
    an = mp.mpf(a_sym2[n-1])
    y_fwd = mp.mpf(n) / X
    y_bwd = X / mp.mpf(n)
    w_fwd = afe_weight(y_fwd, mp.mpf(1), 12, 30, T_max, n_quad)
    w_bwd = w_dual(y_bwd)
    S1 += an / n * w_fwd
    J_dual_sum += an * w_bwd
    if n in [10, 20, 50, 100, 150, 200]:
        J = -J_dual_sum / X
        L1 = float(S1) + float(J_dual_sum / X)
        print(f"  n={n:3d}: S1={float(S1):.6f}  J=-(sum/12)={float(J):.6f}  L(1)={L1:.6f}  (target 0.6314)")

J_final = -J_dual_sum / X
L1_final = float(S1) + float(J_dual_sum / X)
print(f"\nFinal (n=1..{N_max}):")
print(f"  S1     = {float(S1):.6f}")
print(f"  J      = {float(J_final):.6f}  (expected ~-0.083)")
print(f"  L(1)   = {L1_final:.6f}  (expected ~0.6314)")
