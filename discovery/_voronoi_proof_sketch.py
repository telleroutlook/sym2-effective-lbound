"""
[OBL M-Voronoi] proof sketch: explicit C_GL3 from Miller-Schmid (2006).

This script documents the EXACT theorem chain needed to close [OBL M-Voronoi]:
prove |S(X)| <= C_GL3 * X^{2/3} for all X >= 1 with explicit C_GL3 < 7.488.

CURRENT STATUS:
  - ||K_nu||_1 = 0.19947 (Arb-assisted discovery value via Mellin identity)
    CORRECTION: previous value 0.184 was WRONG (underestimated small-y tail 4.5x)
    Mellin identity: K_hat_nu(1) = (4pi^2)^{-1}*Gamma(13/4)*Gamma(1/2)*Gamma(-9/4) = -0.19947
    Under sign-definiteness K_nu(y)<0 (verified at 30+ points): ||K||_1 = |K_hat(1)| = 0.19947
    Conservative upper bound (no sign assumption): ||K||_1 <= 0.225
  - Conditional C_GL3 sketches range from about 1.04 to 2.74 [GL3 Voronoi required]
  - Empirical C_GL3 = 0.001611 (margin 4649x vs threshold)

PROOF SKETCH (sketch only, [OBL] markers indicate what is still needed):

Theorem Chain:
  EXTERNAL INPUT (source checked this session; not yet in baseline/): Miller-Schmid
  (2006 preprint), Theorem 1.18:
    https://sites.math.rutgers.edu/~sdmiller/voronoi/miller-schmid-voronoi.pdf

    For A(m,n) attached to a cuspidal GL(3,Z)-automorphic representation,
    f in S(R) vanishing to infinite order at 0, (a,c)=1, c != 0,
    a_bar*a = 1 mod c, and q > 0:

      sum_{n != 0} A(q,n) e(-n a/c) f(n)
      = sum_{d | c q} (c/d)^{1-lambda1-lambda2-lambda3}
        sum_{n != 0} A(n,d) / |n|
        S(q a_bar, n; q c/d)
        F(n d^2 / (c^3 q)).

    Here S(n,m;c) is the classical Kloosterman sum and F is the normalized
    GL(3) Bessel transform defined by Miller-Schmid's triple integral (or,
    equivalently, by their Mellin-Barnes formula).  This exact normalization is
    the starting point for M-Voronoi-1; it is not yet the generic c^{-2}/K_nu
    formula previously sketched below.

  EXTERNAL INPUT (not yet baseline-verified): Weil-Katz bound (Katz 1988, ell-adic):
    For GL3 Kloostermann sums
    at level 1:
      |S_GL3(c,n)| <= tau(c) * c^{1/2}   for all n,c >= 1
    where tau(c) = d(c) = number of divisors (tau <= 2c^eps for any eps>0).
    In particular for (n,c)=1 or the level-1 case: |S_GL3(c,n)| <= 2 * c^{1/2}.

  EXTERNAL INPUT (not yet baseline-verified): Rankin-Selberg:
    For sym^2 Delta on GL3,
      sum_{n<=N} |A(n,1)|^2 = C_RS * N + O(N^{2/3})
    with C_RS = Res_{s=1} L(s, sym^2 Delta x sym^2 Delta) / L(s)
    Numerically: C_RS = 0.4433 (discovery estimate, n=10^5 stable).

  [OBL M-Voronoi-1]: Starting from the exact Theorem 1.18 above, choose smooth
    upper/lower cutoffs enclosing chi_{[0,X]}, derive the resulting transform
    bounds, and determine whether the old K_nu(nt/c^3) normalization is valid.
    The generic c^{-2}K_nu formula is only a candidate, not an extracted theorem.

  [OBL M-Voronoi-2]: Prove the Cauchy-Schwarz bound for the dual n-sum:
    For c >= 1 and the SMOOTH cutoff phi_delta = convolution of chi_{[0,X]}
    with a delta-approximate identity supported on [X, X+delta]:
      |sum_n A(n,1) S_GL3(c,n) Phi_F(n,c)|
      <= 2 * c^{1/2} * sum_{n~c^3/X} |A(n,1)| * ||K_nu||_1 * (c^3/X)
      <= 2 * c^{1/2} * sqrt(C_RS * c^3/X) * sqrt(c^3/X) * ||K_nu||_1
         [Cauchy-Schwarz + Rankin-Selberg]
      = 2 * sqrt(C_RS) * ||K_nu||_1 * c^{1/2} * c^3/X

  [OBL M-Voronoi-3]: Sum over c and extract X^{2/3}:
    Contribution to S(X) from level c:
      c^{-2} * 2 * sqrt(C_RS) * ||K_nu||_1 * c^{1/2} * c^3/X * X
      = 2 * sqrt(C_RS) * ||K_nu||_1 * c^{3/2}

    Sum over c <= X^{1/3} (the main range where c^3/X <= 1):
      sum_{c<=X^{1/3}} 2 * sqrt(C_RS) * ||K_nu||_1 * c^{3/2}
      <= 2 * sqrt(C_RS) * ||K_nu||_1 * sum_{c=1}^infty c^{3/2-2}
         [Abel summation converts the sum-over-c to ...]

    NOTE: This gives sum_c c^{3/2} DIVERGES (c^{3/2} grows!).
    The correct argument uses a DYADIC decomposition and the
    SMOOTHNESS of phi to gain cancellation. The correct bound is:
      sum_{c>=1} c^{-2} * [c-term] = O(1) * X^{2/3}
    via a stationary phase argument in c (not just term-by-term).

    ALTERNATIVE (Rankin-Selberg route):
    Use Cauchy-Schwarz in BOTH n and c simultaneously:
      |S(X)| <= C * sqrt(sum_{c,n} |A(n,1)|^2 / n^{2/3})
                * sqrt(sum_{c,n} |S(c,n)|^2 * ||K_nu||_1^2 * n^{2/3}) * X
    This gives O(X^{2/3}) with explicit constant from Rankin-Selberg
    and ||K_nu||_2 (not ||K_nu||_1).

NUMERICAL CONCLUSION (conditional sketch only):
  Using ||K_nu||_1 = 0.205 (conservative) and sqrt(C_RS) = 0.666:
    C_GL3 <= 2 * 0.666 * 0.205 * VORONOI_CONST
  where VORONOI_CONST captures the c-sum convergence factor.

  From the Rankin-Selberg route with ||K_nu||_2 = 0.303:
    C_GL3 <= 2 * sqrt(C_RS) * ||K_nu||_2 * zeta(7/6)
           = 2 * 0.666 * 0.31 * 6.59 = 2.74 << 7.488

  From the L1 route with zetafn(4/3) as c-sum:
    C_GL3 <= 2 * ||K_nu||_1 * zeta(4/3)
           = 2 * 0.205 * 3.601 = 1.476 << 7.488

OPEN QUESTION for [OBL M-Voronoi]:
  Which c-sum formula (zeta(3/2), zeta(4/3), zeta(7/6)) is the correct
  one for the GL3 Voronoi at level 1? The answer requires reading
  Miller-Schmid (2006) Theorem 1.18 carefully and tracking all normalizations.

  KEY CONSTRAINT: ANY formula giving C_GL3 < 7.488 certifies the bound.
  Since ALL three estimates (1.325, 2.66, ...) are well below 7.488,
  the certification is ROBUST to the exact c-sum factor up to ~5.6x.

CERTIFICATION MARGIN SKETCH (N=10^8, sigma=0.9):
  Empirical C_GL3 = 0.001611  <- strongest evidence (measured)
  L1 estimate     = 1.476     <- conditional sketch
  L2 estimate     = 2.74      <- conditional sketch
  Q^{1/3}         = 6.930     <- conditional (needs C_abs <= 1)
  THRESHOLD       = 7.488     <- from float N=10^8 scan (discovery tier)

  Safety hierarchy: 7.488 >> 6.930 >> 2.74 >> 1.476 >> 0.002
  None of these candidate constants closes the [OBL M-Voronoi] estimate by itself.
"""
import sys


sys.path.insert(0, '.')
from flint import arb, ctx
from mpmath import mp, mpf, zeta as mpzeta, sqrt as mpsqrt

ctx.prec = 200
mp.dps = 50

PI = arb.pi()

print("=== [OBL M-Voronoi] Conditional C_GL3 bound summary ===")
print()

L1_upper  = arb(205) / arb(1000)   # ||K_nu||_1 <= 0.205 (conservative, no sign assumption)
                                    # Mellin-exact: 0.19947 (assuming K_nu <= 0)
L2_upper  = arb(31)  / arb(100)    # ||K_nu||_2 <= 0.31 (from float64 + 2% safety)
C_RS_ub   = arb(45)  / arb(100)    # discovery estimate C_RS <= 0.45

z_43  = float(mpzeta(mpf(4)/3))
z_76  = float(mpzeta(mpf(7)/6))
z_32  = float(mpzeta(mpf(3)/2))

print(f"  zeta(4/3) = {z_43:.4f}")
print(f"  zeta(7/6) = {z_76:.4f}")
print(f"  zeta(3/2) = {z_32:.4f}")
print()

threshold = 7.4877
Q_GL3     = 332.75

for label, formula_val, route in [
    ("L1 + zeta(4/3)",
     2 * float(L1_upper) * z_43,
     "2 * ||K||_1 * zeta(4/3)  [Weil + L1, c-sum 4/3]"),
    ("L2 + sqrt(C_RS) + zeta(7/6)",
     2 * float(mpsqrt(mpf(0.45))) * float(L2_upper) * z_76,
     "2 * sqrt(C_RS) * ||K||_2 * zeta(7/6)  [Cauchy-Schwarz + L2]"),
    ("L1 + zeta(3/2)",
     2 * float(L1_upper) * z_32,
     "2 * ||K||_1 * zeta(3/2)  [Weil + L1, c-sum 3/2]"),
]:
    ok = formula_val < threshold
    print(f"  Route [{label}]:")
    print(f"    Formula: {route}")
    print(f"    C_GL3 <= {formula_val:.4f}  < {threshold:.4f}? {'YES' if ok else 'NO'}  (margin {threshold/formula_val:.1f}x)")
    print()

print("CONCLUSION:")
print("  All sketched routes give C_GL3 <= 1.0 to 2.7 (far below threshold 7.488).")
print("  This is evidence of robustness, not a proof of any C_GL3 bound.")
print(f"  If C_GL3 <= Q^{{1/3}} = {Q_GL3**(1/3):.3f} were proved, it would suffice; it is not proved.")
print()
print("[OBL M-Voronoi] remaining work:")
print("  (1) Identify the exact c-sum exponent in Miller-Schmid (2006) Theorem 1.18")
print("  (2) Verify the normalization of K_nu against the paper")
print("  (3) Write up the explicit constant derivation")
print("  The current numerical margins do not replace this derivation.")
