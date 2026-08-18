"""
Conditional lower-bound calculator for L(1, sym^2 Delta).

This script documents the conditional structure: what is computed, what remains
discovery-only, and what single theoretical constant is still needed.  It is
not a certificate.

STRUCTURE:
  L(1) = L_ces(N, 1) + [L(1) - L_ces(N, 1)]

where:
  (A) L_ces(N, 1) is COMPUTED EXACTLY (integer sieve + exact rational arithmetic)
  (B) |L(1) - L_ces(N, 1)| <= 4 * C_GL3 / N^{1/3}   [Abel summation bound]
      requires: |S(X)| <= C_GL3 * X^{2/3} for all X  [GL3 Voronoi -- ONE GAP]

KNOWN:
  - L_ces(10^6, 1) = 0.631793  (stable to < 3e-4 for N in [100K, 1M])
  - C_GL3_empirical = 0.001611  (from N=10^8 scan, max|S(X)|/X^{2/3} at peak)

THEORETICAL GAP:
  Need explicit constant C_GL3 < C_threshold from GL3 Voronoi (Miller-Schmid 2006).
  Once established, the lower bound follows with the formula below.

Certification window (N=10^8 scan results, 2026-08-17):
  - max|S(X)| = 331.02 at X=93,166,237
  - C_GL3_emp = 0.001611 (peak)
  - min|L_ces(0.9+it, N=10^8)| = 0.392596 at t=110.020
  - tail_factor = 0.05243
  - C_GL3 threshold = 7.4877 > Q_GL3^{1/3} = 6.9296

  sigma=0.90, N=10^8: needs C_GL3 < 7.49  (Q^{1/3}=6.93 suffices!)
  sigma=0.95, N=10^6: needs C_GL3 < 6.93  (same Q^{1/3})
"""
import sys


sys.path.insert(0, '.')

# -----------------------------------------------------------------------
# Float-scan inputs (from the N=10^8 discovery scan, 2026-08-17)
# -----------------------------------------------------------------------
L_ces_1M  = 0.631793   # L_ces(N=10^6, s=1), stable < 3e-4
min_L_09  = 0.392596   # min|L_ces(0.9+it, N=10^8)| over t in [0,200] (t=110.020)
min_L_095 = 0.487849   # min|L_ces(0.95+it, N=10^6)|
max_S_N   = 331.0210   # max|S(X)| for X <= 10^8
C_GL3_emp = 0.001611   # empirical max|S(X)|/X^{2/3} at X=93166237 (peak, N=10^8)
N         = 100_000_000
tail_factor_09 = 0.05243   # sigma/(sigma-2/3) * N^{2/3-sigma} at sigma=0.9, N=10^8

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
    finite = 3 * max|S(N)| * N^{-sigma}   (from max_S_N)
    """
    tail_factor = sigma / (sigma - 2/3) * N**(2/3 - sigma)
    finite = 3 * max_S_N * N**(-sigma)
    return C_GL3 * tail_factor + finite

# -----------------------------------------------------------------------
# Print certification table
# -----------------------------------------------------------------------
print("=" * 65)
print("CONDITIONAL LOWER-BOUND CALCULATOR: L(1, sym^2 Delta) [discovery tier]")
print("=" * 65)

print(f"\n--- Direct L(1) bound [Abel at s=1, N={N:.0e}] ---")
print(f"{'C_GL3':>8}  {'error':>10}  {'L(1) >= ':>12}  {'certifies':>12}")
print("-" * 50)
for C in [0.01, 0.10, 0.50, 1.00, 2.00, 2.63, 5.00, 7.49, 10.0, 15.8]:
    err = abel_error_s1(C, N)
    lb = L_ces_1M - err
    if lb > 0:
        cert = f"{lb:.4f}"
    else:
        cert = "FAIL"
    print(f"{C:>8.2f}  {err:>10.6f}  {L_ces_1M - err:>12.6f}  {cert}")

print(f"\n  Empirical C_GL3 = {C_GL3_emp:.5f}  (margin vs Q^{{1/3}}: {332.75**(1/3)/C_GL3_emp:.0f}x)")

print(f"\n--- Zero-free region {{sigma>=0.9}} [Abel, N={N:.0e}] ---")
sigma = 0.90
threshold = min_L_09 / tail_factor_09
print(f"sigma={sigma}, min|L_ces|={min_L_09:.6f}, tail_factor={tail_factor_09:.5f}")
print(f"C_GL3 threshold = {threshold:.4f}  (Q^{{1/3}}={332.75**(1/3):.4f}, {'CERTIFIES' if threshold>332.75**(1/3) else 'NOT CERTIFIES'})")
print(f"{'C_GL3':>8}  {'total_err':>12}  {'margin':>12}  {'certifies?':>12}")
print("-" * 52)
for C in [0.01, 1.00, 2.63, 5.00, 6.93, 7.49]:
    err = cesaro_error_sigma(C, N, sigma)
    margin = min_L_09 - err
    cert = "YES" if margin > 0 else "NO"
    print(f"{C:>8.2f}  {err:>12.6f}  {margin:>12.6f}  {cert}")

print("\n--- Zero-free region {sigma>=0.95} [Abel, N=10^6] ---")
sigma = 0.95
N6 = 1_000_000
max_S_1M_v = 63.82
def cesaro_error_sigma_v(C_GL3, N, sigma, maxS):
    tail_factor = sigma / (sigma - 2/3) * N**(2/3 - sigma)
    finite = 3 * maxS * N**(-sigma)
    return C_GL3 * tail_factor + finite
print(f"sigma={sigma}, min|L_ces|={min_L_095:.6f}")
print(f"{'C_GL3':>8}  {'total_err':>12}  {'margin':>12}  {'certifies?':>12}")
print("-" * 52)
for C in [0.01, 1.00, 3.00, 5.00, 6.93, 7.50]:
    err = cesaro_error_sigma_v(C, N6, sigma, max_S_1M_v)
    margin = min_L_095 - err
    cert = "YES" if margin > 0 else "NO"
    print(f"{C:>8.2f}  {err:>12.6f}  {margin:>12.6f}  {cert}")

print("\n" + "=" * 65)
print("SINGLE REMAINING GAP:")
print("  Prove |S(X)| <= C_GL3 * X^{2/3} for all X with explicit C_GL3.")
print(f"  A proved C_GL3 < Q^{{1/3}}={332.75**(1/3):.3f} would certify zero-free {{sigma>=0.9}} at the N=10^8 threshold {threshold:.3f}.")
print(f"  A proved C_GL3 < Q^{{1/4}}={332.75**(1/4):.3f} would certify zero-free {{sigma>=0.9}} at the N=10^7 threshold 4.375.")
print("  A proved C_GL3 < 15.8 would certify L(1,sym^2 Delta) > 0.")
print(f"  [Empirical C_GL3={C_GL3_emp:.5f}, margin vs any threshold: >4649x]")
print(f"  [Rough Voronoi estimate: C_GL3 ~ Q^{{1/6}}*sqrt(C_RS)*O(1) ~ 6.32 < {threshold:.3f}]")
print("=" * 65)
