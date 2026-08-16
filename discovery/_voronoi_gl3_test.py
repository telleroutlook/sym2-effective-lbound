"""
_voronoi_gl3_test.py -- Numerical test of GL3 Voronoi formula for sym^2 Delta.

For sym^2(Delta), the GL3 form comes from a weight-12 holomorphic GL2 form.
The GL3 Whittaker function factors as (Jacquet-Langlands lifting):

   W^{GL3}(y1, y2) ~ W^{GL2}(y1) * W^{GL2}(y1*y2) * (normalization)

with W^{GL2}(y) = y^{k/2} * exp(-2*pi*y) for weight-k holomorphic forms.

So W^{GL3}(1, y2) ~ y2^{k/2} * exp(-2*pi*(1 + y2))

This gives a SPECIFIC GL3 Bessel integral I(n; X) that we can compute numerically.

GL3 Voronoi formula (level-1, c=1 dominant term):
   S(X) = sum_{n<=X} a_sym2(n)
        ~ sum_n a_sym2(n) * I_GL3(n; X)

where I_GL3(n; X) = integral of W^{GL3}(1, n/x) * dx/x from 0 to X.

PURPOSE: Test whether the Voronoi formula reproduces S(X) for small X,
extract the effective constant C_GL3.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
from scipy import integrate, special
import time

k = 12  # weight
NU = k / 2  # = 6, spectral parameter

# --- GL3 Whittaker function for holomorphic sym^2 lift ---
# W^{GL3}(1, y2) = y2^{k/2} * exp(-2*pi*(1+y2)) * (normalization from GL2 factorization)
# The normalization ensures that the integral I(n; X) gives the right Voronoi formula.
# We test: does sum_n a(n) * I(n; X) reproduce S(X)?

def W_GL3(y2):
    """GL3 Whittaker function at (y1=1, y2)."""
    return (y2 ** NU) * np.exp(-2 * np.pi * (1.0 + y2))

def I_GL3(n, X):
    """Voronoi GL3 Bessel integral: integral W^{GL3}(1, n/x) dx/x from 0 to X."""
    # Change of variable: u = n/x, x = n/u, dx = -n/u^2 du
    # Limits: x=0 -> u=inf, x=X -> u=n/X
    # I = integral_{n/X}^inf W_GL3(u) * (n/u^2) * du / (n/u)
    #   = integral_{n/X}^inf W_GL3(u) / u * du
    u_lo = float(n) / X
    # W_GL3(u) = u^NU * exp(-2pi(1+u)), decays for u -> inf
    # For large u_lo, use incomplete Gamma function
    def integrand(u):
        return W_GL3(u) / u

    # Only integrate where integrand is non-negligible
    u_hi = max(u_lo + 50.0, u_lo * 3)
    if u_lo > 30:  # negligible
        return 0.0
    result, err = integrate.quad(integrand, u_lo, u_hi,
                                  limit=200, epsabs=1e-12, epsrel=1e-10)
    return result

# Load sym2 coefficients for verification
print("Loading a_sym2 (N=200)...")
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs
N_ref = 200
tau_ref = compute_tau(N_ref)
a_ref = compute_sym2_coeffs(tau_ref)
a_vals = np.array([float(a_ref[i]) for i in range(N_ref)], dtype=np.float64)

# Compute S(X) directly
n_arr = np.arange(1, N_ref + 1)
cum = np.cumsum(a_vals)

print("\nTest: Does GL3 Voronoi reproduce S(X) for small X?")
print(f"  Whittaker function: W(y2) = y2^{NU} * exp(-2pi*(1+y2))")
print(f"  Integral: I(n; X) = integral_{{n/X}}^inf W(u)/u du")
print()
print(f"{'X':>8}  {'S(X) direct':>14}  {'Voronoi sum':>14}  {'ratio':>8}  {'C_GL3 bound':>12}")
print("  " + "-"*60)

X_tests = [5, 10, 20, 50, 100, 200]
norm_factor = np.exp(2 * np.pi)  # Remove the exp(-2pi) from W(y1=1) = exp(-2pi*1)

for X in X_tests:
    # Direct S(X)
    S_X = cum[X-1] if X <= N_ref else np.nan

    # Voronoi sum: sum_{n=1}^M a(n) * I_GL3(n; X)
    # Use enough terms (say n <= 3*X since I decays for n/X >> 1)
    M = min(3 * X + 20, N_ref)
    t0 = time.time()
    voronoi_sum = 0.0
    for n in range(1, M + 1):
        I_val = I_GL3(n, X)
        if abs(I_val) < 1e-15:
            break
        voronoi_sum += a_vals[n-1] * I_val
    elapsed = time.time() - t0

    ratio = voronoi_sum / S_X if abs(S_X) > 1e-10 else float('nan')
    C_GL3 = abs(S_X) / (X**(2/3)) if abs(S_X) > 0 else 0.0

    print(f"  {X:>6}  {S_X:>14.6f}  {voronoi_sum:>14.6f}  {ratio:>8.4f}  "
          f"{C_GL3:>12.4f}  ({elapsed:.2f}s)")

print()
print("If ratio ~ 1: Voronoi formula (level-1 dominant term) reproduces S(X).")
print("If ratio != 1: higher c terms or different normalization needed.")
print()

# Additional: compute the GL3 Bessel integral explicitly for small n values
print("GL3 Bessel integral I(n; X=100) for n=1..10:")
for n in range(1, 11):
    I_val = I_GL3(n, 100)
    print(f"  n={n:2d}: I(n; 100) = {I_val:.8f}, a(n)*I = {a_vals[n-1]*I_val:.8f}")

# Normalization exploration: try different normalizations
print()
print("Exploring normalization: k_norm such that S(X) = k_norm * Voronoi_sum")
for X in [10, 20, 50]:
    S_X = cum[X-1]
    M = min(3*X+20, N_ref)
    vsum = sum(a_vals[n-1] * I_GL3(n, X) for n in range(1, M+1))
    if abs(vsum) > 1e-10:
        k_norm = S_X / vsum
        print(f"  X={X}: S={S_X:.4f}, Voronoi_raw={vsum:.4f}, k_norm={k_norm:.4f}")
