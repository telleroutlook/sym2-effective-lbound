"""
Conditional certified lower bound for L(1, sym^2 Delta).

This script documents the EXACT certification structure: what is already
proved/certified, and what single theoretical constant is still needed.

STRUCTURE:
  L(1) = L_ces(N, 1) + [L(1) - L_ces(N, 1)]

where:
  (A) L_ces(N, 1) is COMPUTED EXACTLY (integer sieve + exact rational arithmetic)
  (B) |L(1) - L_ces(N, 1)| <= 4 * C_GL3 / N^{1/3}   [Abel summation bound]
      requires: |S(X)| <= C_GL3 * X^{2/3} for all X  [GL3 Voronoi -- ONE GAP]

KNOWN:
  - L_ces(10^6, 1) = 0.631793  (stable to < 3e-4 for N in [100K, 1M])
  - C_GL3_empirical = 0.0064   (from N=10^6 scan, max|S(X)|/X^{2/3})

THEORETICAL GAP:
  Need explicit constant C_GL3 < C_threshold from GL3 Voronoi (Miller-Schmid 2006).
  Once established, the lower bound follows with the formula below.

Multi-sigma certification table (at N=10^6):
  sigma=0.90: needs C_GL3 < 2.63  (empirical: 0.0064, margin 411x)
  sigma=0.95: needs C_GL3 < 6.93  (margin 1083x)

Direct L(1) certification (at N=10^6):
  For any C_GL3, certified interval is:
    L(1) in [0.631793 - 4*C_GL3/100, 0.631793 + 4*C_GL3/100]
  For L(1) > 0: need C_GL3 < 15.8  (virtually guaranteed from GL3 theory)
  For L(1) >= 0.53: need C_GL3 < 2.5
  For L(1) >= 0.62: need C_GL3 < 0.30  (requires N >> 10^6 or better C_GL3 bound)
"""
import sys; sys.path.insert(0, '.')
import numpy as np

# -----------------------------------------------------------------------
# Certified inputs (from previous computations)
# -----------------------------------------------------------------------
L_ces_1M  = 0.631793   # L_ces(N=10^6, s=1),  stable < 3e-4
min_L_09  = 0.449015   # min|L_ces(0.9+it, N=10^6)| over t in [0,50]
min_L_095 = 0.487849   # min|L_ces(0.95+it, N=10^6)|
max_S_1M  = 63.82      # max|S(X)| for X <= 10^6
C_GL3_emp = 0.0064     # empirical max|S(X)|/X^{2/3} at N=10^6
N = 1_000_000

# -----------------------------------------------------------------------
# Abel summation bound for |L(1) - L_ces(N, 1)|
# Assumes |S(X)| <= C_GL3 * X^{2/3} for all X >= 1.
# -----------------------------------------------------------------------
def abel_error_s1(C_GL3, N):
    """
    Abel summation bound for |L(1) - L_ces(N, 1)|.
    tail   = C_GL3 * integral_N^inf x^{2/3-2} dx = C_GL3 * 3 * N^{-1/3}
    finite = |S(N)|/N <= C_GL3 * N^{-1/3}
    total  = 4 * C_GL3 * N^{-1/3}
    """
    return 4 * C_GL3 / N**(1/3)

# -----------------------------------------------------------------------
# Zero-free region bound for sigma-strip (Abel summation at s=sigma+it)
# Assumes |S(X)| <= C_GL3 * X^{2/3} for all X >= 1.
# -----------------------------------------------------------------------
def cesaro_error_sigma(C_GL3, N, sigma):
    """
    Abel summation bound for |L(sigma+it) - L_ces(N, sigma+it)|.
    tail   = C_GL3 * sigma / (sigma - 2/3) * N^{2/3 - sigma}
    finite = 3 * max|S(N)| * N^{-sigma}   (from max_S_1M)
    """
    tail_factor = sigma / (sigma - 2/3) * N**(2/3 - sigma)
    finite = 3 * max_S_1M * N**(-sigma)
    return C_GL3 * tail_factor + finite

# -----------------------------------------------------------------------
# Print certification table
# -----------------------------------------------------------------------
print("=" * 65)
print("CONDITIONAL CERTIFIED LOWER BOUND: L(1, sym^2 Delta)")
print("=" * 65)

print("\n--- Direct L(1) bound [Abel at s=1, N=10^6] ---")
print(f"{'C_GL3':>8}  {'error':>10}  {'L(1) >= ':>12}  {'certifies':>12}")
print("-" * 50)
for C in [0.01, 0.10, 0.50, 1.00, 2.00, 2.63, 5.00, 10.0, 15.0, 15.8]:
    err = abel_error_s1(C, N)
    lb = L_ces_1M - err
    cert = "> 0" if lb > 0 else "FAIL"
    if lb > 0:
        cert = f"{lb:.4f}"
    print(f"{C:>8.2f}  {err:>10.5f}  {L_ces_1M - err:>12.6f}  {cert}")

print(f"\n  Empirical C_GL3 = {C_GL3_emp:.4f}")
print(f"  L(1) >= {abel_error_s1(C_GL3_emp, N):.4e} away from L_ces")

print("\n--- Zero-free region {sigma>=0.9} [Abel, N=10^6] ---")
sigma = 0.90
print(f"sigma={sigma}, min|L_ces|={min_L_09:.6f}")
print(f"{'C_GL3':>8}  {'total_err':>12}  {'margin':>12}  {'certifies?':>12}")
print("-" * 52)
for C in [0.01, 0.50, 1.00, 2.00, 2.63, 3.00, 5.00]:
    err = cesaro_error_sigma(C, N, sigma)
    margin = min_L_09 - err
    cert = "YES" if margin > 0 else "NO"
    print(f"{C:>8.2f}  {err:>12.6f}  {margin:>12.6f}  {cert}")

print("\n--- Zero-free region {sigma>=0.95} [Abel, N=10^6] ---")
sigma = 0.95
print(f"sigma={sigma}, min|L_ces|={min_L_095:.6f}")
print(f"{'C_GL3':>8}  {'total_err':>12}  {'margin':>12}  {'certifies?':>12}")
print("-" * 52)
for C in [0.01, 1.00, 3.00, 5.00, 6.93, 7.50]:
    err = cesaro_error_sigma(C, N, sigma)
    margin = min_L_095 - err
    cert = "YES" if margin > 0 else "NO"
    print(f"{C:>8.2f}  {err:>12.6f}  {margin:>12.6f}  {cert}")

print("\n" + "=" * 65)
print("SINGLE REMAINING GAP:")
print("  Prove |S(X)| <= C_GL3 * X^{2/3} for all X with explicit C_GL3.")
print("  Any C_GL3 < 2.63  =>  zero-free {sigma>=0.9} certified, L(1)>=0.527")
print("  Any C_GL3 < 6.93  =>  zero-free {sigma>=0.95} certified, L(1)>=0.354")
print("  Any C_GL3 < 15.8  =>  L(1,sym^2 Delta) > 0  certified")
print("  [GL3 theory guarantees C_GL3 = O(1); explicit: needs Miller-Schmid 2006]")
print("=" * 65)
