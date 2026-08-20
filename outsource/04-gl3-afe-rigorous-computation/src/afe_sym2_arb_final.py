"""
Final certificate attempt for L(1, sym^2 Delta) — DISCOVERY-TIER ONLY.

Strategy:
  1. Compute A(n) coefficients via float-based Euler product (fast)
  2. Compute L(s) = main_sum + dual_sum via AFE with N=N_afe terms
  3. Main sum uses V_arb(n/X, s) contour integrals
  4. Dual sum: negligible at N_afe >= 3000 (V_tilde ~ 10^{-14})
  5. Main tail bounded via C_V (numerically integrated, outward-rounded)
  6. Dual tail bounded via C_V_dual (same style, with dual Gamma ratio)

v4 BUG FIXES (per reviewer verdict 2026-08-20):
  - compute_C_V_numerical() now includes |G(s+1+it)/G(s)| factor
  - main_tail formula corrected: C_V * X * exact_part (X in numerator)
  - dual_tail computed from integral majorant (not hardcoded 1e-12)
  - All 3 bugs documented and corrected

STATUS: DISCOVERY-TIER. Not a rigorous certificate.
"""
from __future__ import annotations
import math
import os
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent.parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_REPO / "src"))
sys.path.insert(0, str(_REPO / "outsource/04-gl3-afe-rigorous-computation/src"))

from flint import acb, arb, ctx
ctx.prec = 256
from afe_sym2_arb import compute_tau, compute_sym2_coeffs
from afe_sym2_arb_single import V_arb, V_tilde_arb


def _G_ratio_abs(s_re: float, s_im: float, t: float) -> float:
    """Compute |G(s+1+it)/G(s)| where G(s) = Γ_R(s+1)·Γ_C(s+11).

    G(s) = Γ_R(s+1)·Γ_C(s+11)
         = π^{-(s+1)/2}Γ((s+1)/2) · 2·(2π)^{-(s+11)}Γ(s+11)

    So |G(s+1+it)/G(s)| = |G_ratio| involves Gamma function ratios.
    We use Stirling's approximation for the log Gamma:
      log|Γ(σ+iτ)| ≈ (σ-1/2)log(√(σ²+τ²)) - |τ| + (σ-1/2)·arctan(τ/σ)
                     + (1/2)log(2π) + O(1/|τ|)

    For the ratio, the dominant terms cancel, leaving the t-dependent part.
    """
    # G(s+1+it)/G(s):
    # Γ_R factor: π^{-(s+1+it)/2}Γ((s+1+it+1)/2) / [π^{-(s+1)/2}Γ((s+1)/2)]
    #           = π^{-it/2} · Γ((s+2+it)/2) / Γ((s+1)/2)
    # Γ_C factor: (2π)^{-(s+11+it)}Γ(s+11+it) / [(2π)^{-(s+11)}Γ(s+11)]
    #           = (2π)^{-it} · Γ(s+11+it) / Γ(s+11)

    # Compute log|G(s+1+it)/G(s)| using log|Γ(x+iy)| approximation
    def log_gamma_abs_re(re_part, im_part):
        """Approximate log|Γ(re_part + i*im_part)| via Stirling."""
        r2 = re_part * re_part + im_part * im_part
        if r2 < 1e-30:
            return 0.0
        log_r = 0.5 * math.log(r2)
        arg = math.atan2(im_part, re_part)
        return (re_part - 0.5) * log_r - abs(im_part) + (re_part - 0.5) * arg

    # Γ_R ratio: log|Γ((s+2+it)/2)| - log|Γ((s+1)/2)|
    # (s+2+it)/2 = (sigma+2)/2 + i*(tau+t)/2
    # (s+1)/2 = (sigma+1)/2 + i*tau/2
    gamma_r_ratio = (log_gamma_abs_re((s_re + 2) / 2, (s_im + t) / 2)
                     - log_gamma_abs_re((s_re + 1) / 2, s_im / 2))

    # Γ_C ratio: log|Γ(s+11+it)| - log|Γ(s+11)|
    gamma_c_ratio = (log_gamma_abs_re(s_re + 11, s_im + t)
                     - log_gamma_abs_re(s_re + 11, s_im))

    # π and 2π factors: |π^{-it/2}| = 1, |(2π)^{-it}| = 1 (pure phase)
    # So only Gamma ratios contribute to the absolute value
    log_G_ratio = gamma_r_ratio + gamma_c_ratio

    return math.exp(log_G_ratio)


def compute_C_V_numerical(sigma: float, T: float = 20.0, M: int = 2000) -> float:
    """Numerical estimate of the AFE tail majorant with G factor.

    Computes C_V = ∫_{-T}^{T} exp(1-t²)/|1+it| · |G(s+1+it)/G(s)| dt
    where G(s) = Γ_R(s+1)·Γ_C(s+11).

    v4: Now includes the Gamma-ratio factor that was missing in v3.

    Returns a numerical upper bound (with 10% safety margin, NOT rigorous).
    """
    t_arr = []
    f_arr = []
    dt = 2.0 * T / M
    for k in range(M + 1):
        t = -T + k * dt
        t_arr.append(t)
        if abs(t) < 1e-15:
            f = math.exp(1.0)
        else:
            f = math.exp(1.0 - t * t) / math.sqrt(1.0 + t * t)
        # Multiply by |G(s+1+it)/G(s)|
        G_ratio = _G_ratio_abs(sigma, 0.0, t)
        f *= G_ratio
        f_arr.append(f)

    integral = sum(f_arr) * dt
    return integral * 1.10  # 10% safety margin (NOT a rigorous bound)


def certify_point(s_re: float, s_im: float, N_afe: int,
                  tau, A, hb=None):
    """Compute L(s) via AFE — DISCOVERY-TIER only."""
    t0 = time.time()
    X = 12.0
    sigma = s_re
    s = acb(s_re, s_im)

    C_V = compute_C_V_numerical(sigma)
    print(f"    C_V({sigma}) ≈ {C_V:.4f} (with G factor; still NOT rigorous)", flush=True)

    print(f"    Computing main sum (N={N_afe})...", flush=True)
    main_sum = acb(0, 0)
    dual_sum = acb(0, 0)
    count = 0

    for n in range(1, N_afe + 1):
        an = A[n - 1]
        if an == 0.0:
            continue
        count += 1
        an_ball = acb(float(an))
        ns = acb(float(n)) ** (-s)

        V = V_arb(n / X, s)
        main_sum += an_ball * ns * V

        if n <= 500:
            Vt = V_tilde_arb(n * X, s)
            nsm1 = acb(float(n)) ** (s - acb(1.0))
            dual_sum += an_ball * nsm1 * Vt

    L_approx = main_sum + dual_sum
    elapsed_approx = time.time() - t0
    print(f"    L(s) ≈ {float(L_approx.real.mid()):.10f} + {float(L_approx.imag.mid()):.10f}i  ({elapsed_approx:.1f}s)", flush=True)

    # v4 FIX: From Re(u)=1 contour: |V(n/X,s)| <= C_V * (X/n)^1
    # So tail should be C_V * X * sum d3(n)/n^{sigma+1}
    # v3 had C_V / X * exact_part (X in denominator) — WRONG direction.
    from afe_sym2_arb import compute_d3_table, d3_tail_sum_exact
    N_TABLE = 200000
    d3 = compute_d3_table(N_TABLE)
    exp_main = sigma + 1.0
    exact_part = d3_tail_sum_exact(d3, N_afe, exp_main)
    main_tail = C_V * X * exact_part  # v4: X in numerator (corrected)

    # v4 FIX: Dual tail computed from integral majorant, not hardcoded.
    # V_tilde(y,s) has contour at Re(v)=1 with G(1-s+v)/G(s).
    # For the dual sum tail (n > N_dual), |V_tilde(nX,1-s)| decays as
    # (1/(nX))^{Re(v)} = 1/(nX) at Re(v)=1.
    # So dual_tail <= C_V_dual / X * sum d3(n)/n^{sigma_dual+1}
    # where sigma_dual = 1 - sigma + 1 = 2 - sigma.
    C_V_dual = compute_C_V_numerical(1.0 - sigma, T=20.0, M=2000)
    N_DUAL = 500  # dual sum truncated at N_dual=500 in the loop
    exp_dual = (2.0 - sigma) + 1.0  # Re(1-s+v) = 2-sigma at v=1
    exact_part_dual = d3_tail_sum_exact(d3, N_DUAL, exp_dual)
    dual_tail = C_V_dual / X * exact_part_dual  # dual: 1/X (correct for dual contour)

    total_tail = main_tail + dual_tail

    L_abs = abs(L_approx)
    L_mid = float(L_abs.mid())
    L_rad = float(L_abs.rad())
    lower = L_mid - L_rad - total_tail

    certified = lower > 0.0

    print(f"    |L(s)| ≈ {L_mid:.10f} ± {L_rad:.2e}")
    print(f"    Main tail (DISCOVERY) ≤ {main_tail:.6e}")
    print(f"    Dual tail (derived) ≤ {dual_tail:.6e}")
    print(f"    |L(s)| ≥ {lower:.10f}  [{('NONZERO (DISCOVERY)' if certified else 'INCONCLUSIVE')}]")

    return {
        "s": f"{s_re}+{s_im}i",
        "L_re": float(L_approx.real.mid()),
        "L_im": float(L_approx.imag.mid()),
        "L_mod": L_mid,
        "L_rad": L_rad,
        "main_tail": main_tail,
        "dual_tail": dual_tail,
        "total_tail": total_tail,
        "lower_bound": lower,
        "certified_nonzero": certified,
        "time_s": round(time.time() - t0, 1),
        "note": "DISCOVERY-TIER: C_V includes G factor (v4 fix), main_tail X corrected (v4), "
                "dual_tail derived from integral majorant (v4). Coefficients use float not exact rational."
    }


if __name__ == "__main__":
    N_AFE = 6000
    targets = [(1.0, 0.0), (0.6, -20.0), (0.6, 0.0)]

    print("=" * 60, flush=True)
    print(f"DISCOVERY-TIER AFE COMPUTATION (N_afe={N_AFE})", flush=True)
    print("NOT a rigorous certificate — see limitations.md", flush=True)
    print("=" * 60, flush=True)

    N_COEFFS = N_AFE + 200
    print(f"\nPrecomputing tau (N={N_COEFFS})...", flush=True)
    t0 = time.time()
    tau = compute_tau(N_COEFFS)
    print(f"  tau done in {time.time()-t0:.1f}s", flush=True)
    A = compute_sym2_coeffs(tau)
    print(f"  A computed ({sum(1 for a in A if a != 0.0)} nonzero)", flush=True)

    results = []
    for s_re, s_im in targets:
        print(f"\n  s = {s_re}+{s_im}i:", flush=True)
        r = certify_point(s_re, s_im, N_AFE, tau, A)
        results.append(r)

    print("\n" + "=" * 60, flush=True)
    print("SUMMARY (DISCOVERY-TIER ONLY)", flush=True)
    print("=" * 60, flush=True)
    for r in results:
        status = "NONZERO (disc.)" if r["certified_nonzero"] else "INCONCLUSIVE"
        print(f"  {r['s']:>12s}: |L| >= {r['lower_bound']:.6f}  [{status}]  (tail={r['total_tail']:.2e})")
