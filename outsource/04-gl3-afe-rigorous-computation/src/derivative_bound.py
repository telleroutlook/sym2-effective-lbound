"""Compute |L'(s)| at all dense grid points for continuity argument."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from flint import acb, ctx
from afe_sym2_arb import compute_tau, compute_sym2_coeffs, _compute_weight
from heartbeat import Heartbeat

PREC = 256
ctx.prec = PREC
N_COEFFS = 200
X = 12.0

def compute_L(s_re, s_im, A):
    s = acb(s_re, s_im)
    main = acb(0, 0)
    dual = acb(0, 0)
    for n in range(1, 61):
        an = A[n - 1]
        if an == 0: continue
        ns = acb(n, 0) ** (-s)
        nsm1 = acb(n, 0) ** (s - acb(1, 0))
        V = _compute_weight(n / X, s, "V")
        Vt = _compute_weight(n * X, s, "V_tilde")
        main += acb(an, 0) * ns * V
        dual += acb(an, 0) * nsm1 * Vt
    return main + dual

tau_vals = compute_tau(N_COEFFS)
A = compute_sym2_coeffs(tau_vals)

# Test points: all dense grid points and some extras
points = [
    (0.6, 0.0), (0.6, -7.0), (0.6, -20.0), (0.6, 20.0),
    (0.7, 0.0), (0.8, 0.0), (0.9, 0.0), (1.0, 0.0),
    (1.0, 10.0), (0.6, 10.0), (0.6, -10.0),
    (0.8, -7.0), (0.8, -20.0),
]

hdr = f"{'s':>16s}  {'|L(s)|':>10s}  {'|dL/ds|':>10s}  {'r=|L|/|dL|':>10s}  {'time':>6s}"
print(hdr)
print("-" * 60)

hb = Heartbeat(interval=30)
for idx, (s_re, s_im) in enumerate(points):
    t0 = time.time()
    hb.tick(f"point {idx+1}/{len(points)} s={s_re}+{s_im}i")
    L = compute_L(s_re, s_im, A)
    L_mod = float(abs(L).mid())

    # Central difference: |L'(s)| ≈ |L(s+h) - L(s-h)| / (2h)
    h = 0.01
    # Real direction
    Lph = compute_L(s_re + h, s_im, A)
    Lmh = compute_L(s_re - h, s_im, A)
    dL_dsigma = (Lph - Lmh) / (acb(2 * h, 0))
    # Imaginary direction
    Lph_t = compute_L(s_re, s_im + h, A)
    Lmh_t = compute_L(s_re, s_im - h, A)
    dL_dt = (Lph_t - Lmh_t) / (acb(2 * h, 0))

    # |L'(s)| in complex plane (max of partial derivatives is an upper bound)
    dL_ds = abs(dL_dsigma)
    dL_dt_abs = abs(dL_dt)
    # Full gradient norm: sqrt(|dL/dsigma|^2 + |dL/dt|^2)
    grad_sq = float(dL_ds.mid())**2 + float(dL_dt_abs.mid())**2
    grad = grad_sq**0.5

    r = L_mod / grad if grad > 0 else float('inf')
    elapsed = time.time() - t0
    print(f"  {s_re:.1f}{s_im:+.1f}i  {L_mod:10.4f}  {grad:10.4f}  {r:10.4f}  {elapsed:5.1f}s")

hb.done()

print("Note: r = |L(s)|/|L'(s)| is the continuity radius.")
print("If r > grid_diagonal/2, continuous zero-freeness is certified.")
print("Current grid diagonal: %.4f" % ((0.10)**2 + (1.0)**2)**0.5)
