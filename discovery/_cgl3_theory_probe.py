"""
Theoretical bound on C_GL3 from GL3 Rankin-Selberg + explicit constants.

GOAL: Show C_GL3 < 4.375 without reading Miller-Schmid (2006).

We try two approaches:
  (A) Rankin-Selberg + Cauchy-Schwarz (trivial, gives C_GL3 ≤ 0.666*X^{1/3} = O(X^{1/3}))
  (B) Dyadic decomposition + Rankin-Selberg on blocks (gives C_GL3 = O(X^0) if RS error is small)
  (C) Empirical growth rate extrapolation with Richardson-type confidence interval

None of these can replace GL3 Voronoi, but (C) gives a "discovery-tier" upper bound.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time

print("=== C_GL3 bound analysis ===\n")

# Data from N=10^7 scan
data = [
    # (N_max, max_S, X_peak)
    (10_000,     13.3,      7_925),
    (20_000,     15.4,     18_806),
    (100_000,    26.1,     94_048),
    (500_000,    52.13,   224_786),
    (1_000_000,  63.82,   811_494),
    (7_642_126, 142.8421, 7_642_126),  # N=10^7 peak
]

print("Empirical max|S(X)|/X^{2/3} at each scale:")
print(f"  {'X_peak':>12}  {'max_S':>10}  {'C_GL3_emp':>12}  {'growth exp α'}")
exponents = []
for i, (N, S, X) in enumerate(data):
    C = S / X**(2/3)
    if i > 0:
        _, S0, X0 = data[i-1]
        α = np.log(S/S0) / np.log(X/X0) if S > S0 else 0
        exponents.append(α)
    else:
        α = float('nan')
    print(f"  {X:>12}  {S:>10.4f}  {C:>12.6f}  {'---' if np.isnan(α) else f'{α:.4f}'}")

# Fit S(X) ~ c * X^alpha to find the empirical growth law
Xs = np.array([d[2] for d in data], dtype=float)
Ss = np.array([d[1] for d in data], dtype=float)
log_X = np.log(Xs)
log_S = np.log(Ss)
alpha_fit, log_c_fit = np.polyfit(log_X, log_S, 1)
c_fit = np.exp(log_c_fit)
print(f"\nBest fit: max|S(X)| ≈ {c_fit:.4f} × X^{alpha_fit:.4f}")
print(f"GL3 theory bound: X^{2/3:.4f}")
print(f"Empirical exponent {alpha_fit:.4f} << 2/3 = {2/3:.4f}")

# For C_GL3 bound: IF max|S(X)|/X^{2/3} is bounded for all X, estimate C_GL3
# Empirical max: c_fit * X^alpha / X^{2/3} = c_fit * X^{alpha - 2/3}
# Since alpha < 2/3, this goes to 0 as X -> inf. So C_GL3_emp -> 0.
# Upper bound question: what is max over ALL X in [1, inf)?

# At small X: check our data
C_vals = Ss / Xs**(2/3)
print(f"\nMax C_GL3_emp over all measured X: {np.max(C_vals):.6f}")
print(f"Occurs at X = {Xs[np.argmax(C_vals)]:.0f}")

# Upper bound for X > N_max: IF alpha < 2/3, the ratio decreases for large X.
# Need theoretical guarantee for X > 10^7.
# By GL3 theory (unconditional): C_GL3 = O(1). Need the O(1) constant.

print(f"\n--- GL3 theory bound estimate ---")
# From spectral parameters of sym^2 Delta:
# nu = (11, 0, -11)/2, so T = max|nu_i| = 11/2 = 5.5
# GL3 conductor: Q_GL3 ≈ prod(|nu_i - nu_j|) = (11/2)^2 * 11 = 332.75
# Estimate: C_GL3 ≤ Q_GL3^{1/6} ≈ 332.75^{1/6}
Q_GL3_est = (11/2)**2 * 11   # product of spectral gaps
print(f"Spectral conductor estimate Q_GL3 ~ {Q_GL3_est:.2f}")
print(f"Q_GL3^{{1/6}} = {Q_GL3_est**(1/6):.4f}")
print(f"Q_GL3^{{1/4}} = {Q_GL3_est**(1/4):.4f}")

# Rankin-Selberg: C_GL3 <= sqrt(C_RS) * C_abs, need C_abs.
C_RS = 0.4433
print(f"\nRankin-Selberg bound: C_GL3 ≤ sqrt(C_RS) * C_abs = {C_RS**0.5:.4f} * C_abs")
print(f"Need: C_abs < 4.375 / {C_RS**0.5:.4f} = {4.375/C_RS**0.5:.3f}")

print(f"\n--- Summary ---")
print(f"Empirical C_GL3: {np.max(C_vals):.6f} (over X ≤ 10^7)")
print(f"Required threshold: < 4.375 (N=10^7) or < 2.557 (N=10^6)")
print(f"GL3 theory guarantee: O(1) — explicit constant needs Miller-Schmid (2006)")
print(f"Remaining gap factor: 4.375 / {np.max(C_vals):.6f} = {4.375/np.max(C_vals):.0f}×")
