"""
Rankin-Selberg density for sym^2(Delta) and its relation to C_GL3.

Background:
  For a cuspidal GL3 form F, the GL3 Voronoi bound is
    |S(X)| := |Sum_{n<=X} A(1,n)| <= C_GL3 * X^{2/3}
  where (by the Cauchy-Schwarz + Voronoi + Kloosterman method):
    C_GL3 <= C_abs * sqrt(C_RS)

  C_RS = lim_{N->inf} (1/N) * Sum_{n<=N} |a(n)|^2
       = Res_{s=1} L(s, sym^2 x sym^2)   [Rankin-Selberg density]
  C_abs = absolute constant from GL3 Voronoi (level 1, from Miller-Schmid 2006)

Results (N=10^5, stable to <1e-3):
  C_RS       = 0.4433
  sqrt(C_RS) = 0.6658

Certification threshold (sigma=0.9, N=10^6 Cesaro, min|L_ces|=0.449):
  Need C_GL3 < 2.63   =>   C_abs < 2.63/0.6658 = 3.95

Empirical (X <= 10^6):
  C_GL3_empirical = max|S(X)|/X^{2/3} = 0.0064
  C_abs_empirical = 0.0064/0.6658      = 0.0096   [411x below threshold]

Conclusion: C_abs < 3.95 is extremely plausible from the theory; the empirical
C_abs ≈ 0.01 gives 411x safety margin over the certification threshold.
The explicit theoretical bound for C_abs from Miller-Schmid (2006) Theorem 1.1
is the single remaining gap.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
from discovery._fast_tau_sieve import compute_tau_fast, compute_a_sym2

N = 100000
tau_f = compute_tau_fast(N)
a_arr = compute_a_sym2(tau_f)
a = np.array([float(a_arr[i]) for i in range(N)])

cumsum_sq = np.cumsum(a**2)
ns = np.arange(1, N+1, dtype=float)

print("Rankin-Selberg density C_RS = lim (1/N) * Sum|a(n)|^2:")
for k in [1000, 5000, 10000, 50000, 100000]:
    print(f"  N={k:6d}: C_RS ~ {cumsum_sq[k-1]/k:.6f}")

c_rs = float(cumsum_sq[N-1] / N)
print(f"\nBest estimate: C_RS = {c_rs:.4f}")
print(f"sqrt(C_RS)    = {np.sqrt(c_rs):.4f}")
print(f"\nCertification threshold:")
print(f"  Need C_abs < 2.63 / sqrt(C_RS) = {2.63/np.sqrt(c_rs):.3f}")
print(f"  Empirical C_abs = {0.0064/np.sqrt(c_rs):.4f}  (headroom: {2.63/0.0064:.0f}x)")

# Verify RS linear growth
print("\nRS linear growth check (should be ~constant):")
for exp in [3, 4, 5]:
    k = 10**exp
    if k <= N:
        print(f"  (1/{10**exp}) * Sum_{{n<={10**exp}}} |a(n)|^2 = {cumsum_sq[k-1]/k:.4f}")
