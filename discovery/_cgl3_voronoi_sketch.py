"""
Theoretical derivation sketch: C_GL3 <= Q_GL3^{1/3} for sym^2 Delta.

CLAIM: For the GL3 symmetric square L-function L(s, sym^2 Delta), the
partial sum S(X) = sum_{n<=X} a(n) satisfies:
  |S(X)| <= C_GL3 * X^{2/3}  for all X >= 1
with C_GL3 <= Q_GL3^{1/3} = 332.75^{1/3} = 6.930.

INGREDIENTS:
  (1) GL3 Voronoi formula (Miller-Schmid 2006, Theorem 1.1)
  (2) Weil bound for GL3 Kloosterman sums at level 1
  (3) GL3 Whittaker function estimates from spectral parameters

KEY STEPS:

Step 1: Smoothed partial sum.
Let phi_delta be a smooth approximation to 1_{[0,1]} with:
  phi_delta(x) = 1 for x in [delta, 1-delta]
  phi_delta(x) = 0 for x outside [0, 1]
  |phi_delta'(x)| <= 2/delta
Then S(X) = sum_n a(n) phi_delta(n/X) + O(delta * X * max_{n~X} |a(n)|/n)

Step 2: Apply GL3 Voronoi to the smoothed sum.
By Miller-Schmid Theorem 1.1, for test function phi = phi_delta:
  sum_n A(1,n) phi(n/X) = sum_c>=1 (c^{-2}) sum_n A(n,1) S_3(1,n;c) Psi(n/(c^3 X))
where:
  - A(m,n) = A(n,m) (self-dual, since sym^2 Delta is self-dual)
  - S_3(1,n;c) is the GL3 Kloosterman sum at level 1
  - Psi = GL3 Bessel transform of phi

Step 3: GL3 Kloosterman bound at level 1.
For the trivial character (level 1), the GL3 Kloosterman sum satisfies:
  |S_3(1,n;c)| <= tau(c) * c^{1/3}   (from Weil + GL3 Gauss sum estimates)
Actually for level 1, the better bound is:
  |S_3(1,n;c)| <= d(c) * c^{2/3}     (Larsen, or from spectral theory)

Step 4: GL3 Bessel function estimate.
The GL3 Bessel function Psi_nu(y) for spectral parameters nu=(11/2, 0, -11/2):
  |Psi_nu(y)| <= C_nu * min(1, y^{-1/2})   for y > 0
The constant C_nu depends on nu through the Gamma factors:
  C_nu = O(|nu_max|^{1/3}) = O((11/2)^{1/3}) = O(1.765)
More precisely: C_nu ~ (|nu_1-nu_2| * |nu_2-nu_3| * |nu_1-nu_3|)^{1/6}
  = (11/2 * 11/2 * 11)^{1/6} = 332.75^{1/6} = 2.632

Step 5: Combine.
|sum_n a(n) phi(n/X)| <= sum_c c^{-2} * d(c) * c^{2/3} * |sum_n A(n,1) Psi(n/(c^3 X))|
<= sum_c c^{-4/3+eps} * X^{2/3} * C_nu * (Rankin-Selberg bound for A(n,1))

The Rankin-Selberg bound gives sum_{n<=Y} |A(n,1)|^2 = C_RS * Y + O(Y^theta).
By Cauchy-Schwarz:
|sum_n A(n,1) Psi(n/(c^3 X))| <= sqrt(C_RS) * (c^3 X)^{1/2} * ||Psi||_2

After careful optimization (smoothing parameter delta):
|S(X)| <= C_GL3 * X^{2/3}
with C_GL3 = C_nu * sqrt(C_RS) * zeta(4/3) * absolute_constant

NUMERICAL ESTIMATE:
  C_nu = 332.75^{1/6} = 2.632
  sqrt(C_RS) = sqrt(0.4433) = 0.6658
  zeta(4/3) = ~3.606  (WRONG if this factor appears -- see note below)

CAUTION: This rough estimate gives C_GL3 ~ 2.632 * 0.666 * 3.6 = 6.32.
This is LESS than our N=10^8 threshold of 7.49 but larger than the N=10^7
threshold of 4.38. So the rough estimate alone suffices for N=10^8.

NOTE: The zeta(4/3) factor arises from summing over c, but it may not appear
in the final bound if the Bessel function decays faster. If the GL3 Bessel
function Psi_nu(y) is actually O(y^{-1}), the sum over c converges faster
(zeta(2) ~ 1.64), giving C_GL3 ~ 2.632 * 0.666 * 1.64 = 2.87, within
the N=10^7 threshold of 4.38.

CONCLUSION:
- If C_GL3 ~ C_nu * sqrt(C_RS) * O(1) <= 7.49 (N=10^8 threshold): CERTIFIES
- The estimate C_GL3 <= Q_GL3^{1/3} = 6.93 < 7.49 is plausible and
  consistent with the rough bounds above
- For rigorous certification: need the exact value of absolute_constant from
  Miller-Schmid (2006) Theorem 1.1

Status: DISCOVERY TIER -- not a proof.
"""

import numpy as np

Q = 332.75
C_RS = 0.4433

# Key quantities
C_nu_16 = Q**(1/6)   # from Gamma factor estimates
C_nu_13 = Q**(1/3)   # weaker bound
sqrt_CRS = np.sqrt(C_RS)

import scipy.special as sp

# zeta(4/3) by direct summation
zeta_43 = sum(1/n**(4/3) for n in range(1, 10000)) + 0.5  # crude estimate
# actual zeta(4/3) ≈ 3.606
zeta_43_exact = 3.60608  # from known values

print("=== GL3 Voronoi C_GL3 rough bound ===")
print(f"Q_GL3 = {Q:.2f}")
print(f"C_nu (Q^{{1/6}}) = {C_nu_16:.4f}")
print(f"C_nu (Q^{{1/3}}) = {C_nu_13:.4f}")
print(f"sqrt(C_RS) = {sqrt_CRS:.4f}")
print(f"zeta(4/3) = {zeta_43_exact:.4f}")
print()
print("Rough estimate (optimistic, Q^{1/6} * sqrt(C_RS) * O(1)):")
print(f"  C_GL3 ~approx {C_nu_16 * sqrt_CRS:.3f} * O(1)  (O(1) from convergent c-sum)")
print(f"  With zeta(4/3): {C_nu_16 * sqrt_CRS * zeta_43_exact:.3f}")
print()
print("Rough estimate (pessimistic, Q^{1/3} * sqrt(C_RS) * O(1)):")
print(f"  C_GL3 ~approx {C_nu_13 * sqrt_CRS:.3f} * O(1)")
print(f"  With zeta(4/3): {C_nu_13 * sqrt_CRS * zeta_43_exact:.3f}")
print()
print("Certification thresholds:")
print(f"  N=10^7 threshold: 4.375")
print(f"  N=10^8 threshold: 7.488")
print(f"  Rough C_GL3 (optimistic): {C_nu_16 * sqrt_CRS * zeta_43_exact:.3f}")
print(f"  -> N=10^7 certifies if O(1) < {4.375 / (C_nu_16 * sqrt_CRS):.3f}")
print(f"  -> N=10^8 certifies if O(1) < {7.488 / (C_nu_16 * sqrt_CRS):.3f}")
