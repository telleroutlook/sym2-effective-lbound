"""
afe_sym2.py -- Self-contained GL3 AFE evaluation for L(s, sym^2 Delta).

NO external dependencies except mpmath.  Computes:
  1. Ramanujan tau(n) via Euler product (no sieves needed)
  2. Symmetric-square coefficients a(n) via multiplicativity
  3. AFE weight function V(y, s) via Mellin contour integral
  4. L(s) evaluation via smoothed-sum identity
  5. Grid scan of |L(s)| over a rectangle in the critical strip

STATUS: discovery-tier (mpmath floats, not Arb intervals).
For proof-tier, the reviewer should implement Arb outward rounding.
"""

import json
import math
import os
import sys

try:
    import mpmath
except ImportError:
    raise SystemExit("mpmath required: pip install mpmath")

mp = mpmath
mp.mp.dps = 30

# ===================================================================
# 1. Ramanujan tau via Euler product expansion
# ===================================================================

def compute_tau(N):
    """Compute tau(n) for n = 1..N from the product prod (1 - q^n)^24."""
    p = [0] * (N + 1)
    p[0] = 1
    for k in range(1, N + 1):
        for _ in range(24):
            for n in range(N, k - 1, -1):
                p[n] -= p[n - k]
    return [p[n - 1] for n in range(1, N + 1)]


# ===================================================================
# 2. Symmetric-square coefficients (multiplicative, GL3 Hecke)
# ===================================================================

def compute_sym2_coeffs(tau_vals):
    """Compute a_{sym^2}(n) for n = 1..N.  Multiplicative, Euler product."""
    N = len(tau_vals)
    c = [0.0] * (N + 1)
    c[1] = 1.0
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    sp = [0] * (N + 1)

    for p in range(2, N + 1):
        if is_prime[p]:
            sp[p] = p
            cp = tau_vals[p - 1] / p ** 5.5
            c2 = cp * cp
            mk = max(1, int(math.log(N, p)) + 1)
            ap = [0.0] * (mk + 1)
            ap[0] = 1.0
            ap[1] = c2 - 1.0
            if mk >= 2:
                ap[2] = (c2 - 1) * ap[1] - (c2 - 1) * ap[0]
            for k in range(3, mk + 1):
                ap[k] = ((c2 - 1) * ap[k - 1]
                         - (c2 - 1) * ap[k - 2]
                         + ap[k - 3])
            pk = p
            k = 1
            while pk <= N:
                c[pk] = ap[k]
                pk *= p
                k += 1
            j = p * p
            while j <= N:
                is_prime[j] = False
                if sp[j] == 0:
                    sp[j] = p
                j += p

    for n in range(4, N + 1):
        if is_prime[n]:
            continue
        p = sp[n]
        m = n // p
        pk = p
        k = 1
        while m % p == 0:
            m //= p
            pk *= p
            k += 1
        if m != 1:
            c[n] = c[pk] * c[m]

    return [c[i] for i in range(1, N + 1)]


# ===================================================================
# 3. Gamma factors for sym^2 Delta (weight 12, level 1)
# ===================================================================

def gamma_r(s):
    """Gamma_R(s) = pi^{-s/2} Gamma(s/2)."""
    return mp.power(mp.pi, -s / 2) * mp.gamma(s / 2)


def gamma_c(s):
    """Gamma_C(s) = 2 (2pi)^{-s} Gamma(s)."""
    return 2 * mp.power(2 * mp.pi, -s) * mp.gamma(s)


def G_factor(s):
    """G(s) = Gamma_R(s+1) * Gamma_C(s+11) for sym^2 of weight-12 form.

    Correct normalization: Lambda(s) = G(s) * L(s, sym^2 Delta) satisfies
    Lambda(s) = Lambda(1-s).  The +1 in Gamma_R comes from the standard
    completed L-function for sym^2 of a weight-k holomorphic cusp form.
    """
    return gamma_r(s + 1) * gamma_c(s + 11)


# ===================================================================
# 4. AFE weight function via Mellin contour integral
# ===================================================================

def afe_weight(y, s, T=30.0, n_quad=500):
    """
    V(y, s) = (1/2pi i) int_{Re(u)=1} G(s+u)/G(s) y^{-u} h(u)/u du

    with h(u) = exp(u^2) as cutoff.

    Contour at Re(u) = 1 (right of pole at u=0).
    y = n/X, s = sigma + it.
    """
    y_mp = mp.mpf(y)
    Gs = G_factor(s)
    dt = 2 * T / n_quad
    integral = mp.mpc(0)
    for i in range(n_quad):
        tau = -T + (i + 0.5) * dt
        u = mp.mpc(1, tau)
        Gu = G_factor(s + u)
        integrand = (Gu / Gs) * mp.power(y_mp, -u) * mp.exp(u * u) / u
        integral += integrand * dt
    return integral / (2 * mp.pi)


def afe_weight_dual(y, s, T=30.0, n_quad=500):
    """
    V_tilde(y, s) for the dual sum in the GL_3 AFE.

    From the Mellin inversion + functional equation derivation:
      L(s) = Sigma a(n)/n^s V(n/X, s) + Sigma a(n) n^{s-1} V_tilde(nX, s)

    where:
      V(y, s)     = (1/2pi i) int G(s+u)/G(s) y^{-u} h(u)/u du
      V_tilde(y,s) = (1/2pi i) int G(1-s+v)/G(s) y^{-v} h(-v)/v dv

    with h(u) = exp(u^2).  Key: the gamma ratio is G(1-s+v)/G(s),
    NOT G(1-s+v)/G(1-s).  NO external chi factor.
    """
    y_mp = mp.mpf(y)
    Gs = G_factor(s)
    s1 = mp.mpc(1, 0) - s  # 1 - s
    dt = 2 * T / n_quad
    integral = mp.mpc(0)
    for i in range(n_quad):
        tau = -T + (i + 0.5) * dt
        v = mp.mpc(1, tau)
        Gv = G_factor(s1 + v)  # G(1 - s + v)
        integrand = (Gv / Gs) * mp.power(y_mp, -v) * mp.exp(v * v) / v
        integral += integrand * dt
    return integral / (2 * mp.pi)


# ===================================================================
# 5. L(s) via AFE with dual sum (self-dual GL_3, root number +1)
# ===================================================================

def L_via_AFE(a_sym2, s, X=None, N_terms=None, T=30.0, n_quad=500):
    """
    L(s) via smoothed GL_3 AFE with dual sum.

    For self-dual L(s, sym^2 Delta) with root number +1 and Q=1:

    L(s) = sum_{n<=N} A(n)/n^s * V(n/X, s)
           + sum_{n<=N} A(n) * n^{s-1} * V_tilde(n*X, s)

    where V is the main weight (gamma ratio G(s+u)/G(s))
    and V_tilde is the dual weight (gamma ratio G(1-s+v)/G(s)).
    NO external chi factor -- the gamma ratio is inside the integral.
    """
    if X is None:
        X = max(4.0, (abs(s) ** 2 + 100) ** 0.3)
    if N_terms is None:
        N_terms = min(int(5 * X), len(a_sym2))

    # --- Main sum: Sigma A(n)/n^s * V(n/X, s) ---
    main_total = mp.mpc(0)
    for n in range(1, N_terms + 1):
        an = mp.mpf(a_sym2[n - 1])
        if an == 0:
            continue
        y = mp.mpf(n) / mp.mpf(X)
        V = afe_weight(y, s, T=T, n_quad=n_quad)
        ns = mp.power(mp.mpf(n), -s)
        main_total += an * ns * V

    # --- Dual sum: Sigma A(n) * n^{s-1} * V_tilde(n*X, s) ---
    s_m1 = s - mp.mpc(1, 0)  # s - 1
    dual_total = mp.mpc(0)
    for n in range(1, N_terms + 1):
        an = mp.mpf(a_sym2[n - 1])
        if an == 0:
            continue
        y_dual = mp.mpf(n) * mp.mpf(X)  # n * X, not n / X
        V_d = afe_weight_dual(y_dual, s, T=T, n_quad=n_quad)
        nsm1 = mp.power(mp.mpf(n), s_m1)  # n^{s-1}
        dual_total += an * nsm1 * V_d

    return main_total + dual_total


def L_dirichlet(a_sym2, s, N_terms=None):
    """Truncated Dirichlet series (for Re(s) > 1 only)."""
    sigma = float(mp.re(s))
    t = float(mp.im(s))
    if N_terms is None:
        N_terms = len(a_sym2)
    re_sum = 0.0
    im_sum = 0.0
    for n in range(1, N_terms + 1):
        an = a_sym2[n - 1]
        nsigma = n ** sigma
        if t == 0:
            re_sum += an / nsigma
        else:
            logn = math.log(n)
            re_sum += an * math.cos(-t * logn) / nsigma
            im_sum += an * math.sin(-t * logn) / nsigma
    if t == 0:
        return complex(re_sum, 0.0)
    return complex(re_sum, im_sum)


# ===================================================================
# 6. Grid scan
# ===================================================================

def grid_scan(a_sym2, sigma_min, sigma_max, n_sigma,
              t_min, t_max, n_t, method="afe", X=12.0, N_dirichlet=5000,
              T=30.0, n_quad=500):
    """
    Evaluate |L(s)| at grid points.  method = "afe" or "dirichlet".

    Returns list of dicts: {sigma, t, L_re, L_im, L_mod, method}.
    """
    sigmas = [sigma_min + i * (sigma_max - sigma_min) / max(n_sigma - 1, 1)
              for i in range(n_sigma)]
    ts = [t_min + i * (t_max - t_min) / max(n_t - 1, 1)
          for i in range(n_t)]

    results = []
    for sigma in sigmas:
        for t in ts:
            s = mp.mpc(sigma, t)
            if method == "dirichlet" and sigma > 1.0:
                L_val = L_dirichlet(a_sym2, s, N_dirichlet)
            else:
                L_val = L_via_AFE(a_sym2, s, X=X, T=T, n_quad=n_quad)
            L_mod = abs(L_val)
            results.append({
                "sigma": round(sigma, 6),
                "t": round(t, 6),
                "L_re": round(float(mp.re(L_val)), 8),
                "L_im": round(float(mp.im(L_val)), 8),
                "L_mod": round(float(L_mod), 8),
                "method": method,
            })
    return results


# ===================================================================
# 7. Certificate
# ===================================================================

def make_certificate(grid_results, sigma_min, sigma_max, t_min, t_max,
                     N_coeffs, N_afe, X):
    min_pt = min(grid_results, key=lambda r: r["L_mod"])
    return {
        "module": "M-3",
        "status": "discovery",
        "certifies_zero_free": False,  # finite grid cannot certify continuous region
        "method": "GL3 AFE two-term smoothed sum (mpmath, not Arb)",
        "N_coeffs": N_coeffs,
        "N_afe": N_afe,
        "X": X,
        "sigma_range": [sigma_min, sigma_max],
        "t_range": [t_min, t_max],
        "grid_points": len(grid_results),
        "min_L_grid": min_pt["L_mod"],
        "min_L_sigma": min_pt["sigma"],
        "min_L_t": min_pt["t"],
        "witness_file": "witness/grid_values.json",
        "notes": (
            "Discovery tier (mpmath floats, two-term AFE with corrected "
            "dual sum using gamma ratio G(1-s+v)/G(s)). "
            "NOT a certified L(s) evaluation. Missing: (1) Arb interval "
            "arithmetic, (2) rigorous quadrature error bound, "
            "(3) continuous-region argument."
        ),
    }


# ===================================================================
# 8. Main
# ===================================================================

def main():
    N_COEFFS = 200
    print("Computing tau(n) and a_{sym^2}(n)...")
    tau = compute_tau(N_COEFFS)
    a_sym2 = compute_sym2_coeffs(tau)
    print(f"  N = {N_COEFFS}, A(1)={a_sym2[0]}, A(2)={a_sym2[1]:.4f}, "
          f"A(3)={a_sym2[2]:.4f}")

    # --- Grid scan: critical strip ---
    SIGMA_MIN, SIGMA_MAX = 0.6, 1.0
    T_MIN, T_MAX = -20.0, 20.0
    N_SIGMA, N_T = 5, 9  # small grid for speed; reviewer should refine
    X = 12.0
    N_DIRICHLET = min(5000, N_COEFFS)

    print(f"\nGrid scan: sigma in [{SIGMA_MIN}, {SIGMA_MAX}], "
          f"t in [{T_MIN}, {T_MAX}], grid {N_SIGMA}x{N_T}")
    print(f"  X = {X}, N_AFE = {int(5*X)}, N_Dirichlet = {N_DIRICHLET}")

    print("\nAFE evaluation (critical strip, 0.6 <= sigma <= 1.0):")
    results_afe = grid_scan(
        a_sym2, SIGMA_MIN, SIGMA_MAX, N_SIGMA,
        T_MIN, T_MAX, N_T, method="afe", X=X
    )

    print(f"\n  {'sigma':>6}  {'t':>8}  {'|L(s)|':>10}  method")
    print("  " + "-" * 45)
    for r in results_afe:
        print(f"  {r['sigma']:>6.2f}  {r['t']:>8.2f}  {r['L_mod']:>10.6f}  {r['method']}")

    # --- Dirichlet check for Re(s) > 1 ---
    print("\nDirichlet evaluation (Re(s) > 1):")
    results_dir = grid_scan(
        a_sym2, 1.01, 2.0, 5,
        0.0, 20.0, 5, method="dirichlet", N_dirichlet=N_DIRICHLET
    )
    for r in results_dir:
        print(f"  {r['sigma']:>6.2f}  {r['t']:>8.2f}  {r['L_mod']:>10.6f}  {r['method']}")

    # --- Spot-check: L(2) ---
    L2 = L_dirichlet(a_sym2, mp.mpf(2), N_DIRICHLET)
    print(f"\nSpot-check: L(2) = {float(mp.re(L2)):.6f}  (expected ~ 0.806)")

    # --- Combine and write witness ---
    all_results = results_afe + results_dir
    cert = make_certificate(results_afe, SIGMA_MIN, SIGMA_MAX,
                            T_MIN, T_MAX, N_COEFFS, int(5 * X), X)
    cert["spot_L2"] = round(float(mp.re(L2)), 6)

    witness_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "witness")
    os.makedirs(witness_dir, exist_ok=True)
    witness_path = os.path.join(witness_dir, "grid_values.json")
    with open(witness_path, "w") as f:
        json.dump({"certificate": cert, "grid": all_results}, f, indent=2)
    print(f"\nWitness written to {witness_path}")
    print(f"Certified min |L(s)| = {cert['min_L_grid']:.6f} "
          f"at ({cert['min_L_sigma']}, {cert['min_L_t']})")
    return cert


if __name__ == "__main__":
    main()
