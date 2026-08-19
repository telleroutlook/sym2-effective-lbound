"""
Dense grid scan: sigma in [0.6, 1.0] step 0.1, t in [-20, 20] step 1.0.
Purpose: prove continuous zero-freeness via overlapping disks.

Updated to use N_afe=3000 for accurate truncation.
Dual sum only computed for n<=300 (V_tilde negligible beyond).
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent.parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_REPO / "src"))
sys.path.insert(0, str(_REPO / "outsource/04-gl3-afe-rigorous-computation/src"))

from flint import acb, ctx
from afe_sym2_arb import compute_tau, compute_sym2_coeffs, _compute_weight
from heartbeat import Heartbeat

PREC = 128
ctx.prec = PREC
X = 12.0
N_AFE = 3000
N_DUAL = 300
N_COEFFS = N_AFE + 200
N_QUAD = 200


def compute_L(s_re, s_im, A):
    s = acb(s_re, s_im)
    main = acb(0, 0)
    dual = acb(0, 0)
    for n in range(1, N_AFE + 1):
        an = A[n - 1]
        if an == 0:
            continue
        ns = acb(n, 0) ** (-s)
        V = _compute_weight(n / X, s, "V", T=20.0, n_quad=N_QUAD)
        main += acb(an, 0) * ns * V
        if n <= N_DUAL:
            nsm1 = acb(n, 0) ** (s - acb(1, 0))
            Vt = _compute_weight(n * X, s, "V_tilde", T=20.0, n_quad=N_QUAD)
            dual += acb(an, 0) * nsm1 * Vt
    return main + dual


def main():
    tau_vals = compute_tau(N_COEFFS)
    A = compute_sym2_coeffs(tau_vals)
    print(f"Coefficients: {sum(1 for a in A if a != 0.0)} nonzero", flush=True)

    sigmas = [0.60, 0.70, 0.80, 0.90, 1.00]
    t_step = 1.0
    t_values = [t * t_step for t in range(-20, 21)]
    n_points = len(sigmas) * len(t_values)

    print(f"Dense grid: {len(sigmas)} sigmas x {len(t_values)} t-values = {n_points} points")
    print(f"N_afe={N_AFE}, N_dual={N_DUAL}, n_quad={N_QUAD}", flush=True)
    print(f"t range: [{t_values[0]}, {t_values[-1]}], step={t_step}", flush=True)

    results = []
    min_mod = float('inf')
    min_pt = None
    t0 = time.time()
    hb = Heartbeat(interval=30)

    for i, s_re in enumerate(sigmas):
        for j, s_im in enumerate(t_values):
            L = compute_L(s_re, s_im, A)
            mod = abs(L)
            mod_mid = float(mod.mid())
            mod_rad = float(mod.rad())
            certified = (mod_mid - mod_rad) > 0
            results.append({
                "sigma": s_re, "t": s_im,
                "L_mod": mod_mid, "L_rad": mod_rad,
                "certified": certified,
            })
            if certified and (mod_mid - mod_rad) < min_mod:
                min_mod = mod_mid - mod_rad
                min_pt = {"sigma": s_re, "t": s_im}
            idx = len(results)
            hb.tick(f"grid {idx}/{n_points} ({100*idx/n_points:.0f}%) "
                    f"s={s_re:.2f}{s_im:+.1f}i  |L|={mod_mid:.4f}")
    hb.done()

    elapsed = time.time() - t0
    n_certified = sum(1 for r in results if r["certified"])

    print(f"\n{'='*60}")
    print(f"DENSE GRID RESULTS (N_afe={N_AFE})")
    print(f"{'='*60}")
    print(f"Points computed: {n_points}")
    print(f"Time: {elapsed:.1f}s ({elapsed/n_points:.2f}s/point)")
    print(f"Certified nonzero: {n_certified}/{n_points}")
    print(f"Min |L(s)| > {min_mod:.6f} at {min_pt}")

    sigma_gap = 0.10
    t_gap = t_step
    diameter = (sigma_gap**2 + t_gap**2)**0.5
    print(f"Grid diagonal: {diameter:.4f}")

    out = {
        "grid": {
            "sigmas": sigmas,
            "t_values": t_values,
            "t_step": t_step,
            "n_points": n_points,
            "N_afe": N_AFE,
            "N_quad": N_QUAD,
        },
        "summary": {
            "min_modulus_lower_bound": min_mod,
            "min_modulus_point": min_pt,
            "certified_nonzero_count": n_certified,
            "total_points": n_points,
            "elapsed_s": round(elapsed, 1),
            "grid_diagonal": diameter,
        },
        "points": results,
    }
    out_path = Path(__file__).parent.parent / "witness" / "dense_grid_values_N3000.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
