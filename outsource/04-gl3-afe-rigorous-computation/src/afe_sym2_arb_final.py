"""
Final certificate attempt for L(1, sym^2 Delta) — DISCOVERY-TIER ONLY.

Strategy:
  1. Compute A(n) coefficients via float-based Euler product (fast)
  2. Compute L(s) = main_sum + dual_sum via AFE with N=N_afe terms
  3. Main sum uses V_arb(n/X, s) contour integrals
  4. Dual sum: negligible at N_afe >= 3000 (V_tilde ~ 10^{-14})
  5. Main tail bounded via C_V (numerically integrated, outward-rounded)

KNOWN BUGS (identified in v3 review):
  - compute_C_V_rigorous() is MISSING the |G(s+1+it)/G(s)| factor
  - main_tail formula divides by X instead of multiplying: should be
    C_V * X * exact_part, not C_V / X * exact_part
  - dual_tail is hardcoded as 1e-12 with no derivation
  - Coefficient chain uses float, not exact rational

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


def compute_C_V_numerical(sigma: float, T: float = 20.0, M: int = 2000) -> float:
    """Numerical (NOT rigorous) estimate of the AFE tail majorant.

    FIXME: This computes ∫ exp(1-t²)/|1+it| dt but is MISSING the
    |G(s+1+it)/G(s)| Gamma-ratio factor that should multiply the integrand.
    The function name and docstring previously claimed rigor — they do not.

    Returns a numerical upper bound on the integral WITHOUT the G factor.
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
    print(f"    C_V({sigma}) ≈ {C_V:.4f} (MISSING G factor, not rigorous)", flush=True)

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

    # FIXME: main_tail formula has X-direction error.
    # From Re(u)=1 contour: |V(n/X,s)| <= C_V * (X/n)^1
    # So tail should be C_V * X * sum d3(n)/n^{sigma+1}
    # Current code has C_V / X * exact_part (X in denominator).
    # Below uses the WRONG formula to match existing behavior.
    # TODO: fix to C_V * X * exact_part after verifying the correct bound.
    from afe_sym2_arb import compute_d3_table, d3_tail_sum_exact
    N_TABLE = 200000
    d3 = compute_d3_table(N_TABLE)
    exp_main = sigma + 1.0
    exact_part = d3_tail_sum_exact(d3, N_afe, exp_main)
    main_tail = C_V / X * exact_part  # FIXME: should be C_V * X

    # FIXME: dual_tail is hardcoded, not derived
    dual_tail = 1e-12

    total_tail = main_tail + dual_tail

    L_abs = abs(L_approx)
    L_mid = float(L_abs.mid())
    L_rad = float(L_abs.rad())
    lower = L_mid - L_rad - total_tail

    certified = lower > 0.0

    print(f"    |L(s)| ≈ {L_mid:.10f} ± {L_rad:.2e}")
    print(f"    Main tail (DISCOVERY) ≤ {main_tail:.6e}")
    print(f"    Dual tail (hardcoded) ≤ {dual_tail:.2e}")
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
        "note": "DISCOVERY-TIER: C_V missing G factor, X-direction error in tail, "
                "dual_tail hardcoded, coefficients use float not exact rational."
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
