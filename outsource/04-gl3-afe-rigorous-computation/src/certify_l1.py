"""
L(1, sym^2 Delta) computation via AFE — DISCOVERY-TIER ONLY.

Uses float coefficients from afe_sym2_arb with high-precision
V_arb/V_tilde_arb from afe_sym2_arb_single.

KNOWN LIMITATIONS:
  - N vs 2N difference is NOT a proved tail bound
  - Coefficient chain uses float, not exact rational
  - Quadrature error not bounded
  - Status was previously CERTIFIED; downgraded to DISCOVERY in v3
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent.parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_REPO / "src"))
sys.path.insert(0, str(_REPO / "outsource/04-gl3-afe-rigorous-computation/src"))

from flint import acb, arb, ctx

PREC = 256
ctx.prec = PREC

from afe_sym2_arb import compute_tau, compute_sym2_coeffs
from afe_sym2_arb_single import V_arb, V_tilde_arb

X = 12.0


def L_arb_corrected(s_re: float, s_im: float, A, N_afe: int) -> acb:
    """Compute L(s) via AFE with CORRECT A[n-1] indexing."""
    s = acb(s_re, s_im)
    main = acb(0, 0)
    dual = acb(0, 0)
    for n in range(1, N_afe + 1):
        an = A[n - 1]  # CORRECT: A is 0-indexed
        if an == 0:
            continue
        an_ball = acb(float(an))
        ns = acb(float(n)) ** (-s)
        V = V_arb(n / X, s)
        main += an_ball * ns * V

        Vt = V_tilde_arb(n * X, s)
        nsm1 = acb(float(n)) ** (s - acb(1, 0))
        dual += an_ball * nsm1 * Vt
    return main + dual


def certify_L1():
    t0 = time.time()
    print("=" * 60)
    print("L(1, sym^2 Delta) — DISCOVERY-TIER COMPUTATION")
    print("NOT a rigorous certificate (N vs 2N is not a tail bound)")
    print("=" * 60)
    print(f"Precision: {PREC} bits")
    print(f"X = {X}, T_quad = 20.0, N_quad = 2000")
    print()

    N_COEFFS = 6200
    print(f"Computing coefficients (N={N_COEFFS})...", flush=True)
    tau_vals = compute_tau(N_COEFFS)
    A = compute_sym2_coeffs(tau_vals)
    print(f"  done. A has {len(A)} elements, A[0]={A[0]:.6f}, A[1]={A[1]:.6f}", flush=True)

    # Primary at N_afe = 3000
    N_afe = 3000
    print(f"\nComputing L(1) at N_afe={N_afe}...", flush=True)
    L_N = L_arb_corrected(1.0, 0.0, A, N_afe)
    L_N_mod = abs(L_N)
    L_N_mid = float(L_N_mod.mid())
    L_N_rad = float(L_N_mod.rad())
    print(f"  L(1) = {float(L_N.real.mid()):.15f} + {float(L_N.imag.mid()):.15f}i")
    print(f"  |L(1)| = {L_N_mid:.15f} ± {L_N_rad:.2e}")

    # Secondary at N_afe = 6000 for convergence diagnostic
    N_double = 6000
    print(f"\nComputing L(1) at N_afe={N_double} (convergence diagnostic)...", flush=True)
    L_2N = L_arb_corrected(1.0, 0.0, A, N_double)
    L_2N_mod = abs(L_2N)
    L_2N_mid = float(L_2N_mod.mid())
    L_2N_rad = float(L_2N_mod.rad())
    print(f"  |L(1)| = {L_2N_mid:.15f} ± {L_2N_rad:.2e}")

    # Convergence diagnostic (NOT a proved tail bound)
    diff = L_2N - L_N
    diff_mod = abs(diff)
    diff_mid = float(diff_mod.mid())
    diff_rad = float(diff_mod.rad())
    diag_err = diff_mid + diff_rad
    print(f"\n  |L_6000 - L_3000| = {diff_mid:.2e} ± {diff_rad:.2e}")
    print(f"  Convergence diagnostic = {diag_err:.2e}")
    print(f"  NOTE: This is NOT a proved tail bound.")

    # Convergence-based interval (DISCOVERY-TIER ONLY)
    L_lo = L_N_mid - L_N_rad - diag_err
    L_hi = L_N_mid + L_N_rad + diag_err

    elapsed = time.time() - t0

    print(f"\n{'=' * 60}")
    print(f"DISCOVERY-TIER RESULT")
    print(f"{'=' * 60}")
    print(f"  L(1, sym^2 Delta) ∈ [{L_lo:.10f}, {L_hi:.10f}]")
    print(f"  Interval width = {L_hi - L_lo:.2e}")
    print(f"  L(1) > 0: {'YES (discovery)' if L_lo > 0 else 'INCONCLUSIVE'}")
    print(f"  Time: {elapsed:.1f}s")

    result = {
        "status": "DISCOVERY",
        "s": "1.0+0.0i",
        "L_center_real": float(L_N.real.mid()),
        "L_center_imag": float(L_N.imag.mid()),
        "L_radius": float(max(L_N.real.rad(), L_N.imag.rad())),
        "L_mod_mid": L_N_mid,
        "L_mod_rad": L_N_rad,
        "L_2N_mod_mid": L_2N_mid,
        "L_2N_mod_rad": L_2N_rad,
        "N_afe_primary": N_afe,
        "N_afe_secondary": N_double,
        "convergence_diag_mid": diff_mid,
        "convergence_diag_rad": diff_rad,
        "convergence_diag_bound": diag_err,
        "L_lo": L_lo,
        "L_hi": L_hi,
        "L_positive": L_lo > 0,
        "time_s": round(elapsed, 1),
        "precision_bits": PREC,
        "X": X,
        "N_quad": 2000,
        "T_quad": 20.0,
        "note": "DISCOVERY-TIER: N vs 2N difference is a convergence diagnostic, "
                "NOT a proved tail bound. Coefficient chain uses float. "
                "Quadrature error not bounded. See limitations.md."
    }

    out_path = _HERE.parent / "witness" / "single_point_certificate.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved to {out_path}")

    return result


if __name__ == "__main__":
    certify_L1()
