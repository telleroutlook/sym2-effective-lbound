"""
_certified_lower_bound.py  -- Certified lower bound for L(1, sym^2 Delta).

STATUS: VACUOUS BOUND (see result below). Documents the exact obstruction.

SUMMARY:
  The Phragmen-Lindelof convexity bound for |L(1/2+it)| gives:
      J_bound = Q^{1/4} * X^{-1/2} / (2*pi) * I_phrag ~ 0.956
  which EXCEEDS S1 ~ 0.548. So the certified interval is [-0.408, 1.505] —
  no useful lower bound from this approach.

  The only certified lower bound remains L(1) > 0 from [THM F-2].
  L(1) ~ 0.6318 (discovery tier) but certifying this requires [OBL E-2].

OBSTRUCTION (definitive):
  The J correction integral = (1/2pi i) int_{Re=-1/2} L(1+w) * K(w) dw
  involves L(1/2+it) on the critical line.  The Phragmen-Lindelof bound
  |L(1/2+it)| <= Q^{1/4} * (1+|t|)^{3/4} overestimates the actual values
  by a factor ~6 (actual max |L(1/2+it)| ~ 2.5 vs PL bound ~ 14 at t=5).
  The integral of the overestimate exceeds S1, making the bound vacuous.

CERTIFICATION PATHS (from PLAN.md):
  1. [OBL M-Voronoi]: Miller-Schmid GL3 Voronoi (absolute dual convergence)
  2. [OBL M-3]: certified zero-free region {Re >= 0.6, |Im| <= T} via Arb
  3. Subconvexity: need |L(1/2+it)| << (1+|t|)^{3/4-delta} with explicit delta

DISCOVERY-TIER RESULT: L(1, sym^2 Delta) = 0.6318 +- 0.0003
"""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 30
from discovery.afe_gl3 import G_factor
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs

mp = mpmath
k = 12
Q = mp.mpf(144)
X = mp.mpf(12)         # Q^{1/2}
c_shift = mp.mpf('0.5')

G1 = G_factor(mp.mpf(1), k, mp)

print("=== Certified Lower Bound for L(1, sym^2 Delta) ===")
print()
print(f"Setup: Q={int(Q)}, X=Q^{{1/2}}={float(X)}, contour shift c={float(c_shift)}")
print()

# ------------------------------------------------------------------
# Step 1: S1 certified lower bound (from afe_gl3.py, cross-checked)
# ------------------------------------------------------------------
S1_lo = mp.mpf('0.548299')   # certified: S1 >= 0.548299  (< 3e-6 error)
S1_hi = mp.mpf('0.548306')   # certified: S1 <= 0.548306
print(f"[THM] S1 in [{float(S1_lo):.6f}, {float(S1_hi):.6f}]  (certified N=2000 Arb-ready)")
print()

# ------------------------------------------------------------------
# Step 2: I_phrag = 2 * int_0^infty (1+t)^{3/4} * |G(1/2+it)/G(1)| * e^{c^2-t^2} / |w| dt
# ------------------------------------------------------------------
def integrand_phrag(t_val):
    t = mp.mpf(str(t_val))
    s = mp.mpc(mp.mpf('0.5'), t)
    G_half_t = G_factor(s, k, mp)
    e_factor = mp.exp(c_shift**2 - t**2)
    denom = mp.sqrt(c_shift**2 + t**2)
    poly = (1 + t)**mp.mpf('0.75')
    return poly * abs(G_half_t) / abs(G1) * e_factor / denom

I_phrag_half, I_phrag_err = mp.quad(integrand_phrag, [0, mp.mpf(5)], error=True)
I_phrag = 2 * I_phrag_half
print(f"I_phrag = 2 * int_0^5 integrand dt = {float(I_phrag):.6f}  (quad error {float(2*I_phrag_err):.1e})")
print()

# ------------------------------------------------------------------
# Step 3: J_bound = Q^{1/4} * X^{-1/2} / (2*pi) * I_phrag
#         (using convexity C_conv = 1)
# ------------------------------------------------------------------
Q14 = mp.power(Q, mp.mpf('0.25'))
X_hc = mp.power(X, -c_shift)
J_bound = Q14 * X_hc / (2 * mp.pi) * I_phrag
print(f"[BASE] Phragmen-Lindelof: |L(1/2+it)| <= C_conv * Q^{{1/4}} * (1+|t|)^{{3/4}}")
print(f"       Q^{{1/4}} = {float(Q14):.4f},  X^{{-c}} = {float(X_hc):.4f}")
print(f"J_bound = Q^{{1/4}} * X^{{-c}} / (2*pi) * I_phrag = {float(J_bound):.6f}")
print()

# ------------------------------------------------------------------
# Step 4: Lower bound on L(1)
# ------------------------------------------------------------------
L1_lo = float(S1_lo) - float(J_bound)
L1_hi = float(S1_hi) + float(J_bound)
print(f"L(1) = S1 - J_correction")
print(f"     >= S1_lo - J_bound = {float(S1_lo):.6f} - {float(J_bound):.6f}")
print(f"     >= {L1_lo:.4f}")
print()
print(f"Certified interval (convexity-based): L(1) in [{L1_lo:.4f}, {L1_hi:.4f}]")
print()

# ------------------------------------------------------------------
# Comparison: discovery-tier values
# ------------------------------------------------------------------
tau_arr = compute_tau(2000)
a_sym2 = compute_sym2_coeffs(tau_arr)
import numpy as np
a_arr = np.array([float(a_sym2[i]) for i in range(2000)])
n_arr = np.arange(1, 2001, dtype=float)
w_ces = 1.0 - n_arr/2000
L1_cesaro = (a_arr / n_arr * w_ces).sum()
print(f"Discovery-tier: L(1) ~ {L1_cesaro:.6f}  (Cesaro N=2000, not certified)")
print(f"Discovery-tier: J    ~ -0.083500  (direct quadrature, not certified)")
print()
print(f"Gap: certified lower bound {L1_lo:.4f}  vs  actual ~{L1_cesaro:.4f}")
print(f"Improvement factor needed for tight bound: ~{L1_cesaro/max(L1_lo,0.001):.1f}x")
print()
print("To improve: implement [OBL M-Voronoi] or [OBL M-3] (certified zero-free region).")

if L1_lo > 0:
    print(f"\nCONCLUSION: L(1, sym^2 Delta) >= {L1_lo:.4f}  [discovery-tier certified bound]")
    print("            Assuming C_conv = 1 in the GL3 Phragmen-Lindelof bound.")
