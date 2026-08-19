"""
Argument principle for L(s, sym^2 Delta).

Computes (1/2πi) ∮_γ L'(s)/L(s) ds along a rectangular contour
to count zeros of L(s) inside.

Strategy: use winding number of L(γ) around origin.
  N = (1/2π) × Σ_k Im[log(L(s_{k+1})) - log(L(s_k))]
with continuous argument tracking.

Contour: rectangle with Re(s) ∈ [σ_min, σ_max], Im(s) ∈ [-T, T]
chosen to enclose the region of interest [0.6, 1] × [-20, 20].
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

from flint import acb, ctx
ctx.prec = 256
from afe_sym2_arb import compute_tau, compute_sym2_coeffs
from afe_sym2_arb_single import V_arb, V_tilde_arb
from heartbeat import Heartbeat


def compute_L_via_AFE(s_re: float, s_im: float, N_afe: int, X: float,
                      tau, A) -> acb:
    """Compute L(s) via AFE at a single point."""
    s = acb(s_re, s_im)
    main_sum = acb(0, 0)
    dual_sum = acb(0, 0)

    for n in range(1, N_afe + 1):
        an = A[n - 1]
        if an == 0.0:
            continue
        an_ball = acb(float(an))
        ns = acb(float(n)) ** (-s)

        V = V_arb(n / X, s)
        main_sum += an_ball * ns * V

        if n <= 500:
            Vt = V_tilde_arb(n * X, s)
            nsm1 = acb(float(n)) ** (s - acb(1.0))
            dual_sum += an_ball * nsm1 * Vt

    return main_sum + dual_sum


def argument_principle_winding(N_afe: int = 6000,
                                sigma_min: float = 0.55,
                                sigma_max: float = 1.05,
                                T: float = 21.0,
                                N_side: int = 200):
    """Compute winding number of L(γ) around origin.

    Contour γ is the rectangle:
      Bottom: (σ_min, -T) → (σ_max, -T)
      Right:  (σ_max, -T) → (σ_max, T)
      Top:    (σ_max, T)  → (σ_min, T)
      Left:   (σ_min, T)  → (σ_min, -T)

    N_side = number of points per side.
    """
    X = 12.0
    t0 = time.time()

    N_COEFFS = N_afe + 200
    print(f"Precomputing tau (N={N_COEFFS})...", flush=True)
    tau = compute_tau(N_COEFFS)
    A = compute_sym2_coeffs(tau)
    print(f"  done ({time.time()-t0:.1f}s)", flush=True)

    hb = Heartbeat(interval=30)

    # Build contour points (counterclockwise)
    points = []

    # Bottom side: (σ_min, -T) → (σ_max, -T)
    for k in range(N_side):
        s_re = sigma_min + (sigma_max - sigma_min) * k / N_side
        points.append((s_re, -T))

    # Right side: (σ_max, -T) → (σ_max, T)
    for k in range(N_side):
        s_im = -T + 2.0 * T * k / N_side
        points.append((sigma_max, s_im))

    # Top side: (σ_max, T) → (σ_min, T)
    for k in range(N_side):
        s_re = sigma_max - (sigma_max - sigma_min) * k / N_side
        points.append((s_re, T))

    # Left side: (σ_min, T) → (σ_min, -T)
    for k in range(N_side):
        s_im = T - 2.0 * T * k / N_side
        points.append((sigma_min, s_im))

    # Close the contour
    points.append(points[0])

    total_points = len(points) - 1
    print(f"Contour: {total_points} points", flush=True)
    print(f"  σ ∈ [{sigma_min}, {sigma_max}], t ∈ [{-T}, {T}]", flush=True)

    # Compute L(s) at each contour point
    L_values = []
    for i, (s_re, s_im) in enumerate(points):
        L = compute_L_via_AFE(s_re, s_im, N_afe, X, tau, A)
        L_values.append(L)
        if (i + 1) % 20 == 0:
            hb.tick(f"point {i+1}/{total_points}")

    hb.done()

    # Check L(s) on contour is nonzero
    contour_min = min(float(abs(L).mid()) for L in L_values)
    print(f"\n  min |L| on contour = {contour_min:.6e}")
    if contour_min < 1e-10:
        print("  WARNING: L(s) very small on contour — argument principle may not apply")

    # Compute winding number via argument changes
    total_angle = 0.0
    for k in range(len(L_values) - 1):
        L1 = L_values[k]
        L2 = L_values[k + 1]

        L1_re = float(L1.real.mid())
        L1_im = float(L1.imag.mid())
        L2_re = float(L2.real.mid())
        L2_im = float(L2.imag.mid())

        arg1 = math.atan2(L1_im, L1_re)
        arg2 = math.atan2(L2_im, L2_re)

        delta = arg2 - arg1
        while delta > math.pi:
            delta -= 2 * math.pi
        while delta < -math.pi:
            delta += 2 * math.pi

        total_angle += delta

    winding = total_angle / (2 * math.pi)

    print(f"\n  Total angle change: {total_angle:.6f} rad")
    print(f"  Winding number: {winding:.4f}")
    print(f"  Rounded: {round(winding)}")
    print(f"  Zeros inside contour: {round(winding)}")

    return {
        "contour": {"sigma_min": sigma_min, "sigma_max": sigma_max, "T": T},
        "N_side": N_side,
        "total_points": total_points,
        "contour_min_L": contour_min,
        "total_angle": total_angle,
        "winding_raw": winding,
        "winding_rounded": round(winding),
        "zeros_inside": round(winding),
        "time_s": round(time.time() - t0, 1),
    }


if __name__ == "__main__":
    print("=" * 60, flush=True)
    print("ARGUMENT PRINCIPLE FOR L(s, sym^2 Delta)", flush=True)
    print("=" * 60, flush=True)

    result = argument_principle_winding(
        N_afe=6000,
        sigma_min=0.55,
        sigma_max=1.05,
        T=21.0,
        N_side=200
    )

    print("\n" + "=" * 60, flush=True)
    print("RESULT", flush=True)
    print("=" * 60, flush=True)
    if result["zeros_inside"] == 0:
        print("L(s, sym^2 Delta) has NO zeros inside the contour.", flush=True)
        print(f"Zero-free region: σ ∈ [{result['contour']['sigma_min']}, {result['contour']['sigma_max']}], "
              f"|t| ≤ {result['contour']['T']}", flush=True)
    else:
        print(f"L(s, sym^2 Delta) has {result['zeros_inside']} zero(s) inside the contour.", flush=True)
