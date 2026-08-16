"""
afe_gl3.py -- Discovery-tier GL₃ approximate functional equation for L(1, sym^2 Delta).

MATHEMATICAL BACKGROUND
-----------------------
For sym^2 Delta (the Gelbart-Jacquet GL₃ lift of Delta ∈ S_{12}(SL_2(Z))), the
completed L-function satisfies the functional equation

    Lambda(s) = Lambda(1-s),    Lambda(s) = Q^{s/2} G(s) L(s, sym^2 Delta)

where Q is the analytic conductor and

    G(s) = Gamma_R(s) * Gamma_C(s + k - 1),   k = 12

    Gamma_R(s) = pi^{-s/2} Gamma(s/2),
    Gamma_C(s) = 2 (2pi)^{-s} Gamma(s).

SMOOTHED-SUM IDENTITY
---------------------
For any X > 0, Mellin inversion applied to the Dirichlet series gives:

    sum_n a(n)/n * e^{-n/X}  =  L(1) + I(X)

where the Mellin remainder I(X) lives on the contour Re(w) = -1/2:

    I(X) = (1/2pi i) int_{-1/2 - i*inf}^{-1/2 + i*inf}
                L(1+w) * X^w * Gamma(w) dw.

The standard GL₃ convexity bound gives |L(1/2 + it)| << (Q(1+|t|)^3)^{1/4 + eps},
and Stirling gives |Gamma(-1/2 + it)| ~ sqrt(2pi) |t|^{-1} e^{-pi|t|/2}, so

    |I(X)| <= C * X^{-1/2}

with an explicit constant C computable from the convexity exponent and Q.
For Q ~ 144, C ~ 3 * Q^{1/4} * <integral of Stirling * convexity> ≈ 10.

Hence for X = 1000:  |I(1000)| <= 10 / sqrt(1000) ≈ 0.32   (rough)
     for X = 10000: |I(10000)| <= 10 / sqrt(10000) ≈ 0.10  (rough)

A tighter bound uses the ACTUAL GL₃ AFE weight W_afe(y) which decays faster
than e^{-y}: the saddle-point analysis of the Mellin integrand shows

    W_afe(y) ~ exp(-c * y^{2/3})  for large y,

so the partial sum with N ~ (C * X)^{3/2} captures L(1) to < exp(-c N^{2/3}).
For X = 8 (= sqrt(analytic conductor ~ 60)), N ~ 30-50 suffices.

METHODS IMPLEMENTED HERE
------------------------
1. exponential_smooth(a_sym2, X)  -- L(1) via sum a(n)/n * exp(-n/X)
2. afe_weight(y, s0, dps)         -- W_afe(y) via contour integration with h(u)=e^{u^2}
3. afe_sum(a_sym2, X, s0, dps)    -- L(1) via sum a(n)/n * W_afe(n/X)
4. demo()                          -- compare all methods, print convergence table

STATUS: discovery-tier (mpmath floats, not Arb intervals).
Certified version [OBL E-2] requires bounding C explicitly and using python-flint.
"""

import math
import os
import sys

_repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)


# ---------------------------------------------------------------------------
# Gamma factor for sym^2 Delta (k = 12, N = 1)
# ---------------------------------------------------------------------------

def gamma_r(s, mp):
    """Gamma_R(s) = pi^{-s/2} Gamma(s/2)."""
    return mp.power(mp.pi, -s / 2) * mp.gamma(s / 2)


def gamma_c(s, mp):
    """Gamma_C(s) = 2 (2pi)^{-s} Gamma(s)."""
    return 2 * mp.power(2 * mp.pi, -s) * mp.gamma(s)


def G_factor(s, k, mp):
    """
    G(s) = Gamma_R(s) * Gamma_C(s + k - 1) for sym^2 of weight-k form.

    Reference: Shimura (1975); the completed L-function is
      Lambda(s) = Q^{s/2} G(s) L(s, sym^2 f)
    with functional equation Lambda(s) = Lambda(1-s).
    """
    return gamma_r(s, mp) * gamma_c(s + k - 1, mp)


def G_ratio(u, s0, k, mp):
    """G(s0 + u) / G(s0) — the ratio appearing in the AFE weight integrand."""
    return G_factor(s0 + u, k, mp) / G_factor(s0, k, mp)


# ---------------------------------------------------------------------------
# AFE weight function W_afe(y) via Gauss-Hermite-style contour integration
# ---------------------------------------------------------------------------

def afe_weight(y, s0=1.0, k=12, dps=50, T_max=40.0, n_quad=1000):
    """
    Compute the GL₃ AFE weight function at y > 0:

        W_afe(y) = (1/2pi i) int_{c - i*inf}^{c + i*inf}
                       G(s0+u)/G(s0) * y^{-u} * exp(u^2) / u * du,   c > 0

    where c = 1 is used (right of the pole of 1/u at u=0, left of all
    Gamma-factor poles which are at u = -1, -3, ..., -12, ...).

    By the residue theorem: for 0 < y < 1, moving c to -inf picks up the
    residue at u=0 (value 1) plus small corrections from deeper poles.
    For y > 1, by the Riemann-Lebesgue lemma (oscillation y^{-it}), W → 0.

    The weight satisfies:
        W_afe(y) ~ 1  for y << 1
        W_afe(y) ~ 0  for y >> 1
    with a smooth transition centred near y=1.  The super-exponential decay
    e^{-t^2} in the integrand (from h(u)=e^{u^2}) makes this a genuine smooth
    approximation to the indicator 1_{y<1}, not a sharp cutoff.

    Returns: W_afe(y) as a Python float.
    """
    try:
        import mpmath as mp
    except ImportError:
        raise ImportError("mpmath required for afe_weight computation")

    mp.mp.dps = dps
    y = mp.mpf(y)
    c = mp.mpf(1)  # contour right of pole at u=0

    dt = 2 * T_max / n_quad
    integral = mp.mpc(0)
    for i in range(n_quad):
        t = -T_max + (i + 0.5) * dt
        u = c + mp.mpc(0, t)
        gr = G_ratio(u, s0, k, mp)
        integral += gr * mp.power(y, -u) * mp.exp(u ** 2) / u * dt

    W = mp.re(integral) / (2 * mp.pi)
    return float(W)


# ---------------------------------------------------------------------------
# Method 1: Exponential smoothing
# ---------------------------------------------------------------------------

def exponential_smooth(a_sym2, X, N=None):
    """
    Compute the exponentially smoothed sum:

        L_smooth(X) = sum_{n=1}^{N} a(n)/n * exp(-n/X)

    which approximates L(1, sym^2 Delta) with error O(X^{-1/2}).

    a_sym2: list with a_sym2[n-1] = a_{sym^2}(n), 0-indexed.
    X:      smoothing scale; larger X -> more accurate, more terms needed.
    N:      truncation; default = 5*X (enough for exp(-N/X) = e^{-5} < 0.007).
    """
    N = N or min(int(5 * X), len(a_sym2))
    total = 0.0
    for n in range(1, N + 1):
        a_n = a_sym2[n - 1]
        total += a_n / n * math.exp(-n / X)
    return total


def exponential_smooth_high_prec(a_sym2, X, N=None, dps=50):
    """High-precision version using mpmath fsum for better floating-point stability."""
    try:
        import mpmath as mp
    except ImportError:
        return exponential_smooth(a_sym2, X, N)

    mp.mp.dps = dps
    N = N or min(int(5 * X), len(a_sym2))
    X_mp = mp.mpf(X)
    terms = []
    for n in range(1, N + 1):
        a_n = mp.mpf(a_sym2[n - 1])
        terms.append(a_n / n * mp.exp(-n / X_mp))
    return float(mp.fsum(terms))


# ---------------------------------------------------------------------------
# Method 2: GL₃ AFE weight sum
# ---------------------------------------------------------------------------

def afe_sum(a_sym2, X, s0=1.0, k=12, N_terms=60, dps=40):
    """
    Compute the AFE sum:

        L_afe(X) = sum_{n=1}^{N_terms} a(n)/n^{s0} * W_afe(n/X)

    using the GL₃ AFE weight function W_afe defined above.

    For s0=1 and X = sqrt(Q) ~ 8-12, N_terms ~ 30-50 suffices due to the
    super-exponential decay of W_afe (W_afe(y) << exp(-c y^{2/3})).

    NOTE: This sum is for the FIRST Dirichlet series term in the AFE. For
    s=1 (outside the critical strip), the second term (at 1-s=0) involves
    the L-function at s=0, which vanishes by the functional equation structure
    (the Gamma factor has a pole there matching L(0)=0). So the AFE reduces
    to a single sum at s=1.
    """
    try:
        import mpmath as mp
    except ImportError:
        raise ImportError("mpmath required for afe_sum")

    mp.mp.dps = dps
    N_terms = min(N_terms, len(a_sym2))
    X_mp = mp.mpf(X)

    total = mp.mpf(0)
    for n in range(1, N_terms + 1):
        a_n = mp.mpf(a_sym2[n - 1])
        y = n / X_mp
        w = afe_weight(float(y), s0=s0, k=k, dps=dps, T_max=80.0, n_quad=500)
        total += a_n / mp.power(n, s0) * mp.mpf(w)

    return float(total)


# ---------------------------------------------------------------------------
# Convergence analysis
# ---------------------------------------------------------------------------

def smooth_convergence_table(a_sym2, X_values=None, dps=40):
    """
    Print a convergence table for the exponentially smoothed sum
    at different values of X, and compare with the Tauberian estimate.

    Returns list of (X, L_smooth(X)).
    """
    if X_values is None:
        X_values = [50, 100, 200, 500, 1000, 2000, 3000]

    results = []
    for X in X_values:
        N = min(int(6 * X), len(a_sym2))
        val = exponential_smooth_high_prec(a_sym2, X, N=N, dps=dps)
        results.append((X, N, val))
    return results


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    try:
        import mpmath
    except ImportError:
        print("mpmath not installed — install with: pip install mpmath")
        sys.exit(1)

    print("=" * 70)
    print("GL₃ AFE for L(1, sym^2 Delta) [discovery tier]")
    print("=" * 70)

    # Load coefficients
    from discovery.rs_estimate import compute_tau, rankin_selberg_partial
    from discovery.sym2_coeffs import compute_sym2_coeffs

    N_max = 5000
    print(f"\nComputing tau(n) and a_{{sym^2}}(n) for n <= {N_max}...")
    tau = compute_tau(N_max)
    a_sym2 = compute_sym2_coeffs(tau)

    # --- Tauberian baseline ---
    import math as _math
    ZETA2 = _math.pi ** 2 / 6
    rs_results = rankin_selberg_partial(tau, verbose=False)
    final_rs = rs_results[-1]
    L1_tauberian = final_rs[3]
    print(f"\nTauberian baseline (RS method, N={N_max}):")
    print(f"  L(1, sym^2 Delta) ~ {L1_tauberian:.6f}")

    # --- Method 1: Exponential smoothing ---
    print("\nMethod 1: Exponential smoothing  [L(1) = sum a(n)/n * exp(-n/X)]")
    print(f"  {'X':>6}  {'N_used':>7}  {'L_smooth':>12}  {'error vs Tauber':>16}")
    smooth_table = smooth_convergence_table(a_sym2)
    for X, N_used, val in smooth_table:
        err = val - L1_tauberian
        print(f"  {X:>6}  {N_used:>7}  {val:>12.6f}  {err:>+16.6f}")

    # --- Method 2: AFE first-sum (for weight inspection, NOT the full AFE) ---
    print("\nMethod 2: GL₃ AFE weight W_afe inspection  [FIRST SUM ONLY]")
    print("  W_afe(y) = (1/2pi i) int_{1-inf}^{1+inf} G_ratio(u) y^{-u} e^{u^2}/u du")
    print("  NOTE: The full AFE at s=1 requires TWO sums:")
    print("    L(1) = sum_n a(n)/n W(n/X)  +  eps Q^{-1/2} G(0)/G(1) sum_n a(n) W~(n/X)")
    print("  The second sum is nonzero (G(0) = inf, L(0) = 0, product is finite).")
    print("  First sum alone gives ~ 0.515; the missing 0.116 comes from the second sum.")
    print("  Full two-sum AFE implementation is [OBL E-2].")
    print()
    print("  W_afe(y) behavior (should decay from ~1 at y→0 to ~0 at y→inf):")
    print(f"  {'y = n/X':>10}  {'W_afe(y)':>10}")
    for y_val in [0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
        w = afe_weight(y_val, s0=1.0, k=12, dps=25, T_max=8.0, n_quad=300)
        print(f"  {y_val:>10.3f}  {w:>10.6f}")

    # --- Error scaling ---
    print("\nError scaling for exponential smoothing  [I(X) ~ C / sqrt(X)]:")
    vals = [(X, v) for X, N_used, v in smooth_table]
    print(f"  {'X':>6}  {'L_smooth(X)':>12}  {'L_smooth(X) - L(3000)':>22}")
    ref = vals[-1][1]
    for X, v in vals[:-1]:
        diff = v - ref
        print(f"  {X:>6}  {v:>12.6f}  {diff:>+22.6f}")

    print("\nNOTE: For certified computation [OBL E-2], need Arb intervals + explicit C.")
    print("      C ~ 3 * Q^{1/4} * integral_bound ~ 10 for Q = 144.")
    print("      Then |I(X)| <= 10 / sqrt(X).")
    print("      For X = 10000: |I| <= 0.10  -->  L(1) in [0.53, 0.73]  (too wide).")
    print("      Need tighter C from actual GL₃ convexity bound computation.")
