"""
_afe_bessel.py -- GL3 Bessel function weight for the central value AFE.

KEY INSIGHT: The "proper" GL3 AFE at s=1/2 uses the Meijer G-function
  W_Bessel(y) = G_{0,3}^{3,0}(y | 0,0,0)
which decays as exp(-c * y^{2/3}) for large y -- EXPONENTIAL in y^{2/3},
not the algebraic 1/y that our previous e^{u^2} regularizer produced.

This is the GL3 analogue of the K-Bessel function in the GL2 AFE.

FORMULA: L(1/2, sym^2 Delta) = 2 * sum_n a(n)/n^{1/2} * W_GL3(n/Q^{1/3})
(or similar normalization -- see the computation below for the correct scale).

DECAY CHECK: G_{0,3}^{3,0}(y | 0,0,0) ~ C * y^{-1/3} * exp(-3 * y^{2/3} / something)
For y = n/12: decay exp(-c * (n/12)^{2/3}), need only ~30 terms for 10^{-10}.

STATUS: discovery tier.  Verifying against Tauberian value L(1) ~ 0.6314.

REFERENCES:
  - Goldfeld "Automorphic Forms and L-Functions for GL(n,R)" Ch.5, Sec.9
  - Miller-Schmid "Automorphic distributions" (2006)
  - mpmath meijerg documentation
"""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 40
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs

mp = mpmath

N_MAX = 200
tau = compute_tau(N_MAX)
a_sym2 = compute_sym2_coeffs(tau)

# ---------------------------------------------------------------------------
# GL3 Bessel function via Meijer G-function
# ---------------------------------------------------------------------------

def gl3_bessel(y):
    """
    W_Bessel(y) = G_{0,3}^{3,0}(y | (),(0,0,0))
               = (1/2pi i) int Gamma(s)^3 * y^{-s} ds

    This is the GL3 analogue of the modified Bessel function K_0.
    Decays as exp(-c * y^{2/3}) for large y.

    mpmath: meijerg([[],[]], [[0,0,0],[]], y)
    """
    return mp.meijerg([[],[]], [[0,0,0],[]], y)


def gl3_bessel_normalized(y, Q=144):
    """
    Normalized GL3 Bessel weight for sym^2 Delta with conductor Q=144.
    The AFE uses W(n/Q^{1/3}) or similar -- test different scalings.
    """
    # GL3 conductor factor: Q = 144, Q^{1/3} = 144^{1/3} ~ 5.24
    # Or Q^{1/2} = 12? Let's test both.
    Qfactor = mp.power(mp.mpf(Q), mp.mpf('1')/3)  # Q^{1/3}
    return gl3_bessel(y / Qfactor)


# ---------------------------------------------------------------------------
# Verify decay of GL3 Bessel function
# ---------------------------------------------------------------------------

print("GL3 Bessel W(y) = G_{0,3}^{3,0}(y|(),(0,0,0)) decay:")
print(f"  {'y':>8}  {'W_Bessel':>14}  {'Gaussian approx':>16}")
for y_test in [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]:
    w = gl3_bessel(mp.mpf(y_test))
    # Standard asymptotics: W ~ C * y^{-1/3} * exp(-3 * (y/4)^{1/3} * pi ... )
    # Rough: exp(-c * y^{2/3}) with c from Stirling
    approx = mp.exp(-3 * mp.power(mp.mpf(y_test), mp.mpf('2')/3) / 4)
    print(f"  {y_test:>8.3f}  {float(w):>14.6e}  {float(approx):>16.6e}")

print()

# ---------------------------------------------------------------------------
# AFE at s=1/2 using GL3 Bessel weight
# L(1/2) = 2 * sum_n a(n)/n^{1/2} * W_Bessel(n * C) for suitable scale C
# ---------------------------------------------------------------------------

# First, compute partial sums with different scaling factors to find
# which gives L(1/2, sym^2 Delta) ~ expected value.
# Expected L(1) ~ 0.631 (from Tauberian). L(1/2) is a different value.

# The correct normalization: G(s) = Gamma_R(s) * Gamma_C(s+11).
# The AFE at s=1/2: sum_n a(n)/n^{1/2} * V(n/X) where X ~ Q^{1/(2d)} with d=3.
# For GL3: d=3, so X ~ Q^{1/3} ~ 5.24 (not Q^{1/2} = 12).

print("Partial sums for L(1/2) at s0=1/2 using GL3 Bessel weight:")
print("Testing different scale factors X:")

for X_val in [5.24, 8.0, 12.0, 17.0]:
    X = mp.mpf(X_val)
    L_half = mp.mpf(0)
    for n in range(1, N_MAX + 1):
        an = mp.mpf(a_sym2[n-1])
        y = mp.mpf(n) / X
        w = gl3_bessel(y)
        L_half += an / mp.sqrt(n) * w
    print(f"  X={X_val:.2f}: L_half(N={N_MAX}) = {float(L_half):.6f}")

print()

# ---------------------------------------------------------------------------
# Convergence study for X = Q^{1/3} ~ 5.24
# ---------------------------------------------------------------------------

X = mp.power(mp.mpf(144), mp.mpf('1')/3)  # Q^{1/3}
print(f"Convergence of L_half at X = Q^{{1/3}} = {float(X):.4f}:")
print(f"  {'n':>5}  {'L_half(N=n)':>14}  {'term':>12}  {'W(n/X)':>12}")

L_half = mp.mpf(0)
for n in range(1, N_MAX + 1):
    an = mp.mpf(a_sym2[n-1])
    y = mp.mpf(n) / X
    w = gl3_bessel(y)
    term = an / mp.sqrt(n) * w
    L_half += term
    if n in [1,2,3,5,10,15,20,30,50,80,100,150,200]:
        print(f"  {n:>5}  {float(L_half):>14.8f}  {float(term):>+12.2e}  {float(w):>12.2e}")

print()
print(f"Final L_half(N={N_MAX}) = {float(L_half):.8f}")
print(f"Note: 2*L_half gives AFE estimate if formula is L(1/2) = 2*sum")
print(f"  2*L_half = {2*float(L_half):.8f}")
print()

# ---------------------------------------------------------------------------
# Cross-check: compare with standard W_afe (s0=1/2) from afe_gl3.py
# ---------------------------------------------------------------------------
# The W_afe at s0=1/2 gave slow convergence (algebraic decay ~1/y).
# The GL3 Bessel gives exp(-c*y^{2/3}) -- much faster.

print("Comparing decay rates at s0=1/2:")
print(f"  {'n':>5}  {'GL3_Bessel':>14}  {'algebraic_1/y':>14}  {'ratio':>10}")
for n in [1, 5, 10, 20, 50, 100, 200]:
    y = mp.mpf(n) / X
    w_bessel = float(gl3_bessel(y))
    w_alg = 1.0 / float(y)  # approximate algebraic decay
    if w_alg > 0:
        ratio = w_bessel / w_alg
    else:
        ratio = float('nan')
    print(f"  {n:>5}  {w_bessel:>14.4e}  {w_alg:>14.4e}  {ratio:>10.4f}")
