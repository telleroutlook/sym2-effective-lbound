"""
GL3 Voronoi + Kloosterman test (scipy-fast version).

J(y) uses scipy.integrate.quad + scipy.special.gamma (much faster than mpmath.quad).
Integrand decays as exp(-pi*|t|/2) so T=12 is sufficient.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
from scipy.integrate import quad
from scipy.special import gamma as sc_gamma, loggamma
from math import gcd, pi
from functools import lru_cache
import time

# --- Gamma_R(s) = pi^{-s/2} * Gamma(s/2), complex s via scipy ---
def GammaR(s):
    return pi**(-s.real/2) * abs(sc_gamma(s/2)) * np.exp(1j * np.angle(sc_gamma(s/2)))

def GammaR_complex(s):
    """GammaR as a proper complex function."""
    hs = s / 2
    g = sc_gamma(complex(hs.real, hs.imag))
    return pi**(-s.real/2) * np.exp(-1j * s.imag * np.log(pi) / 2) * g

def R_ratio_scipy(s):
    """R(s) = Gamma_GL3(1-s)/Gamma_GL3(s), mu=(11,0,-11)."""
    mu = (11, 0, -11)
    num = 1.0+0j
    den = 1.0+0j
    for m in mu:
        num *= GammaR_complex(1-s+m)
        den *= GammaR_complex(s+m)
    return num / den

def J_GL3_fast(y, T=12):
    """
    J(y) = (1/y) * (1/2pi) * integral R(0.5+it) * y^{0.5+it} * Gamma(0.5+it) dt
    """
    if y <= 0:
        return 0.0

    def re_integrand(t):
        s = 0.5 + 1j*t
        R = R_ratio_scipy(s)
        G = sc_gamma(complex(0.5, t))
        ys = y**(0.5 + 1j*t)
        val = R * G * ys
        return val.real

    result, _ = quad(re_integrand, -T, T, limit=80, epsabs=1e-8, epsrel=1e-8)
    return result / (2 * pi * y)

# Precompute J for a grid of y values
def precompute_J(y_vals):
    cache = {}
    for y in y_vals:
        key = round(float(y), 8)
        if key not in cache:
            cache[key] = J_GL3_fast(float(y))
    return cache

@lru_cache(maxsize=None)
def phi(n):
    if n == 1: return 1
    result, temp = n, n
    p = 2
    while p*p <= temp:
        if temp % p == 0:
            while temp % p == 0: temp //= p
            result -= result // p
        p += 1
    if temp > 1: result -= result // temp
    return result

@lru_cache(maxsize=None)
def mobius(n):
    if n == 1: return 1
    n0, factors = n, []
    p = 2
    while p*p <= n0:
        if n0 % p == 0:
            n0 //= p
            if n0 % p == 0: return 0
            factors.append(p)
        p += 1
    if n0 > 1: factors.append(n0)
    return (-1)**len(factors)

def ramanujan(n, c):
    """c_c(n) = mu(c/gcd(n,c)) * phi(c) // phi(c/gcd(n,c))."""
    g = gcd(n, c)
    d = c // g
    return mobius(d) * phi(c) // phi(d)

# --- First: quick J validation for a few values ---
print("J_GL3 spot check (should show oscillation for large y):")
for y in [0.01, 0.1, 0.5, 1.0, 5.0, 10.0]:
    t0 = time.time()
    jv = J_GL3_fast(y)
    print(f"  J({y:.2f}) = {jv:.6f}  ({time.time()-t0:.2f}s)")

print()

# --- Load coefficients ---
print("Loading a_sym2 (N=500)...", flush=True)
from discovery._fast_tau_sieve import compute_tau_fast, compute_a_sym2
tau_f = compute_tau_fast(500)
a_arr = compute_a_sym2(tau_f)
a_vals = np.array([float(a_arr[i]) for i in range(500)], dtype=float)
cum_a  = np.cumsum(a_vals)
print("  Done.")

# --- GL3 Voronoi sum ---
print("\n" + "="*65)
print("GL3 Voronoi: S(X) vs Sum_{c=1}^C Sum_n a(n)*c_c(n)/c^{4/3}*J(nX/c^3)")
print("="*65)

X_tests = [5, 10, 20]
C_max = 4

for X in X_tests:
    S_direct = float(cum_a[X-1])
    print(f"\nX={X}:  S(X) direct = {S_direct:.6f}  |S|/X^(2/3) = {abs(S_direct)/X**(2/3):.4f}")

    running = 0.0
    for c in range(1, C_max+1):
        cfact = c**(4/3)
        N_c = min(int(50 * c**3 / max(X,1)) + 5, 500)
        contrib = 0.0
        t0 = time.time()
        for n in range(1, N_c+1):
            y = float(n * X) / float(c**3)
            jv = J_GL3_fast(y)
            kl = ramanujan(n, c)
            contrib += a_vals[n-1] * kl * jv / cfact
        running += contrib
        elapsed = time.time() - t0
        print(f"  c={c}: contrib={contrib:.6f}  running={running:.6f}  ({elapsed:.1f}s, {N_c} terms)")

    ratio = running / S_direct if abs(S_direct) > 1e-9 else float('nan')
    print(f"  Voronoi(c=1..{C_max}) / S(X) = {ratio:.4f}  (target: 1.000)")

print("\nDone.")
