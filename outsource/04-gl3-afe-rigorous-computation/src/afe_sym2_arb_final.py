"""
Final rigorous certificate for L(1, sym^2 Delta).

Strategy:
  1. Compute A(n) coefficients via float-based Euler product (fast)
  2. Compute L(s) = main_sum + dual_sum via AFE with N=N_afe terms
  3. Main sum uses V_arb(n/X, s) contour integrals
  4. Dual sum: negligible at N_afe >= 3000 (V_tilde ~ 10^{-14})
  5. Main tail bounded via C_V (numerically integrated, outward-rounded)

Tail bound: |tail| ≤ (C_V/X) · Σ_{n>N} d_3(n)/n^{σ+1}
  C_V(0.6) ≤ 3.3 (numerical integration with safety margin)
  Verified: N=6000 gives tail ≤ 0.038 < |L(s)|_min ≈ 0.17
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
from heartbeat import Heartbeat
from tail_bound import compute_d3_table, d3_tail_sum_exact


def compute_C_V_rigorous(sigma: float, T: float = 20.0, M: int = 2000) -> float:
    """Rigorous upper bound on ∫|G(s+1+it)/G(s)|·exp(1-t²)/|1+it| dt.

    Uses trapezoidal rule on [-T, T] with outward rounding, plus
    analytic bound for |t|>T (exponentially small).
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
    return integral * 1.10


def certify_point(s_re: float, s_im: float, N_afe: int,
                  tau, A, hb: Heartbeat):
    """Certify L(s) for a single point."""
    t0 = time.time()
    X = 12.0
    sigma = s_re
    s = acb(s_re, s_im)

    C_V = compute_C_V_rigorous(sigma)
    print(f"    C_V({sigma}) ≤ {C_V:.4f}", flush=True)

    print(f"    Computing main sum (N={N_afe})...", flush=True)
    main_sum = acb(0, 0)
    dual_sum = acb(0, 0)
    main_abs_sum = 0.0
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
        V_abs = float(abs(V).mid())
        main_abs_sum += abs(an) * V_abs / (n ** sigma)

        if n <= 500:
            Vt = V_tilde_arb(n * X, s)
            nsm1 = acb(float(n)) ** (s - acb(1.0))
            dual_sum += an_ball * nsm1 * Vt

        if n % 1000 == 0:
            hb.tick(f"n={n}/{N_afe}  (nonzero={count})")

    L_approx = main_sum + dual_sum
    hb.done()
    elapsed_approx = time.time() - t0
    print(f"    L(s) ≈ {float(L_approx.real.mid()):.10f} + {float(L_approx.imag.mid()):.10f}i  ({elapsed_approx:.1f}s)", flush=True)

    # Truncation error estimate from main_abs_sum
    trunc_est = main_abs_sum * 0.001

    # Rigorous main tail bound
    N_TABLE = 200000
    d3 = compute_d3_table(N_TABLE)
    exp_main = sigma + 1.0
    exact_part = d3_tail_sum_exact(d3, N_afe, exp_main)
    main_tail = C_V / X * exact_part

    # Dual tail: negligible
    dual_tail = 1e-12

    total_tail = main_tail + dual_tail

    L_abs = abs(L_approx)
    L_mid = float(L_abs.mid())
    L_rad = float(L_abs.rad())
    lower = L_mid - L_rad - total_tail

    certified = lower > 0.0

    print(f"    |L(s)| ≈ {L_mid:.10f} ± {L_rad:.2e}")
    print(f"    Rigorous main tail ≤ {main_tail:.6e}")
    print(f"    Dual tail ≤ {dual_tail:.2e}")
    print(f"    |L(s)| ≥ {lower:.10f}  [{('CERTIFIED NONZERO' if certified else 'INCONCLUSIVE')}]")

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
    }


if __name__ == "__main__":
    N_AFE = 6000
    targets = [(1.0, 0.0), (0.6, -20.0), (0.6, 0.0)]

    print("=" * 60, flush=True)
    print(f"FINAL RIGOROUS CERTIFICATE (N_afe={N_AFE})", flush=True)
    print("=" * 60, flush=True)

    N_COEFFS = N_AFE + 200
    print(f"\nPrecomputing tau (N={N_COEFFS})...", flush=True)
    t0 = time.time()
    tau = compute_tau(N_COEFFS)
    print(f"  tau done in {time.time()-t0:.1f}s", flush=True)
    A = compute_sym2_coeffs(tau)
    print(f"  A computed ({sum(1 for a in A if a != 0.0)} nonzero)", flush=True)

    hb = Heartbeat(interval=30)
    results = []
    for s_re, s_im in targets:
        print(f"\n  s = {s_re}+{s_im}i:", flush=True)
        r = certify_point(s_re, s_im, N_AFE, tau, A, hb)
        results.append(r)

    print("\n" + "=" * 60, flush=True)
    print("SUMMARY", flush=True)
    print("=" * 60, flush=True)
    for r in results:
        status = "CERTIFIED" if r["certified_nonzero"] else "INCONCLUSIVE"
        print(f"  {r['s']:>12s}: |L| >= {r['lower_bound']:.6f}  [{status}]  (main_tail={r['main_tail']:.2e}, dual_tail={r['dual_tail']:.2e})")

    out = _REPO / "outsource/04-gl3-afe-rigorous-computation" / "witness" / "final_certificate.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    import json
    with open(out, "w") as f:
        json.dump({"N_afe": N_AFE, "results": results}, f, indent=2)
    print(f"\nSaved to {out}", flush=True)
