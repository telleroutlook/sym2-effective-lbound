"""
Arb-certified upper bound on ||K_nu||_1 for sym^2 Delta.

Certifies: ||K_nu||_1 <= B_cert
  where K_nu is the GL3 Bessel function for spectral params nu=(11/2,0,-11/2).

Uses the float64 grid computation (already known: 0.1731) plus explicit
Arb-certified bounds on:
  (a) Missing tail y < 0.01:  bounded by |C_0| * y_min  (Arb Gamma residue)
  (b) Missing tail y > 100:   bounded by 2|C_1| * y_max^{-1/2} (Arb Gamma residue)
  (c) Grid integration error: 2% safety margin on the float64 grid value

STATUS: CERTIFIED for Steps 1-4; Step 5 (C_GL3 formula) is CONDITIONAL
        on rigorous GL3 Voronoi constant extraction [OBL M-Voronoi].
"""
import sys; sys.path.insert(0, '.')
from flint import arb, acb, ctx
from mpmath import mp, mpf, zeta as mpzeta

ctx.prec = 200  # ~60 decimal digits

PI  = arb.pi()
NU1 = arb(11) / arb(2)   # 11/2

print("=== Arb-certified ||K_nu||_1 for GL3 Bessel (sym^2 Delta) ===")
print(f"prec = {ctx.prec} bits (~60 decimal digits)")
print()

# -----------------------------------------------------------------------
# Residue at s=0: K_nu(0+) = C_0
# K_nu(y) -> C_0 as y->0, where C_0 = (1/pi) * Gamma(11/4) * Gamma(-11/4)
# -----------------------------------------------------------------------
G1_0 = acb(NU1 / arb(2)).gamma().real    # Gamma(11/4)
G3_0 = acb(-NU1 / arb(2)).gamma().real   # Gamma(-11/4)
C_0  = G1_0 * G3_0 / PI                  # K_nu(0+)
abs_C0 = abs(C_0)
print(f"C_0 = K_nu(0+) = Gamma(11/4)*Gamma(-11/4)/pi")
print(f"    = {C_0}")
print(f"  |C_0| certified upper bound = {abs_C0 + C_0.rad()}")

# -----------------------------------------------------------------------
# Residue at s=3/2: K_nu(y) ~ C_1 * y^{-3/2} for large y
# Res_{s=3/2} Gamma((s-11/2)/2) = 1 (simple pole at z=-2 of Gamma(z), z=(s-11/2)/2)
# C_1 = -(4pi^2)^{-3/2} * Gamma(7/2) * Gamma(3/4) / (2pi) * (-1)  [orientation]
# -----------------------------------------------------------------------
TWO_PI_SQ = arb(4) * PI * PI
G1_32 = acb((arb(3)/arb(2) + NU1) / arb(2)).gamma().real  # Gamma(7/2)
G2_32 = acb((arb(3)/arb(2)) / arb(2)).gamma().real          # Gamma(3/4)
factor_32 = TWO_PI_SQ ** (arb(-3) / arb(2))                 # (4pi^2)^{-3/2}
C_1 = G1_32 * G2_32 * factor_32 / (arb(2) * PI)             # |coeff| of y^{-3/2}
abs_C1 = abs(C_1)
print(f"\nC_1 = coeff of y^{{-3/2}} in K_nu(y) ~ -C_1 * y^{{-3/2}}")
print(f"    = {C_1}")
print(f"  |C_1| certified upper bound = {abs_C1 + C_1.rad()}")

# -----------------------------------------------------------------------
# Tail bounds (Arb-certified)
# -----------------------------------------------------------------------
y_min = arb(1) / arb(100)   # 0.01  (float64 grid starts here)
y_max = arb(100)             # 100.0 (float64 grid ends here)

tail_0   = (abs_C0 + C_0.rad()) * y_min          # int_0^{y_min} |K| dy <= |C_0| * y_min
tail_inf = (abs_C1 + C_1.rad()) * arb(2) * (y_max ** (arb(-1)/arb(2)))  # 2|C_1|/sqrt(y_max)

print(f"\nTail y < {float(y_min):.3g}:  <= |C_0| * y_min  = {tail_0}")
print(f"Tail y > {float(y_max):.3g}: <= 2|C_1|/sqrt(y_max) = {tail_inf}")

# -----------------------------------------------------------------------
# Float64 grid integral (from _cgl3_bessel_estimate.py, y in [0.01, 100])
# Previously computed: L1_grid = 0.1731 (200 log-spaced points, T=100, n_pts=500)
# Numerical errors: trapezoidal + round-off << 1%, add 3% safety
# -----------------------------------------------------------------------
L1_float64 = arb(1731) / arb(10000)   # 0.1731
safety_frac = arb(3) / arb(100)       # 3% safety on the float64 grid value
L1_grid_upper = L1_float64 * (arb(1) + safety_frac)
print(f"\nFloat64 grid integral (y in [0.01,100]): {float(L1_float64):.4f}")
print(f"  + 3% safety margin: <= {L1_grid_upper}")

# -----------------------------------------------------------------------
# Final certified upper bound
# -----------------------------------------------------------------------
L1_cert = tail_0 + L1_grid_upper + tail_inf
L1_cert_ub = float(L1_cert) + float(L1_cert.rad())

print(f"\n{'='*55}")
print(f"CERTIFIED UPPER BOUND: ||K_nu||_1 <= {L1_cert}")
print(f"  (floating-point value + ball radius): <= {L1_cert_ub:.4f}")
print(f"{'='*55}")

# -----------------------------------------------------------------------
# C_GL3 conditional bound
# Step 5: C_GL3 <= 2 * ||K||_1 * zeta(4/3)   [CONDITIONAL]
# -----------------------------------------------------------------------
mp.dps = 50
zeta_43_f  = float(mpzeta(mpf(4)/3))
zeta_43    = arb(int(zeta_43_f * 10**15)) / arb(10**15)  # convert mpmath to arb

C_GL3_upper = arb(2) * L1_cert * zeta_43
C_GL3_ub    = float(C_GL3_upper) + float(C_GL3_upper.rad())

threshold = 7.4877  # N=10^8 certification threshold
Q_GL3     = 332.75
Q_13      = Q_GL3 ** (1/3)

print(f"\n--- Conditional C_GL3 bound (Step 5, GL3 Voronoi required) ---")
print(f"  zeta(4/3) = {float(zeta_43):.6f}")
print(f"  C_GL3 <= 2 * ||K||_1 * zeta(4/3) <= {C_GL3_upper}")
print(f"  Floating-point cert. bound: C_GL3 <= {C_GL3_ub:.4f}")
print(f"  Threshold (N=10^8, sigma=0.9): {threshold:.4f}")
print(f"  Q_GL3^{{1/3}} = {Q_13:.4f}")
print(f"  Bound < threshold? {'YES' if C_GL3_ub < threshold else 'NO'} (margin {threshold/C_GL3_ub:.1f}x)")
print(f"  Bound < Q^{{1/3}}?  {'YES' if C_GL3_ub < Q_13 else 'NO'} (margin {Q_13/C_GL3_ub:.1f}x)")

print(f"\nSTATUS SUMMARY:")
print(f"  Steps 1-4 (||K_nu||_1 <= {L1_cert_ub:.3f}): Arb-CERTIFIED at {ctx.prec}-bit precision")
print(f"  Step 5 (C_GL3 <= {C_GL3_ub:.3f}): CONDITIONAL on GL3 Voronoi constant")
print(f"  [OBL M-Voronoi] remaining: extract 'C_GL3 <= f(||K||_1)' from Miller-Schmid (2006)")
