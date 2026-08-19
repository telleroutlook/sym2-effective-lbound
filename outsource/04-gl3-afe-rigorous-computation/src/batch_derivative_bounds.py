"""Batch compute |L'(s)| at all grid points needed for full overlapping disk coverage."""
import sys, time, json
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent.parent.parent
WITNESS = REPO / "outsource" / "04-gl3-afe-rigorous-computation" / "witness"
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(REPO / "src"))
from flint import acb, ctx
from afe_sym2_arb import compute_tau, compute_sym2_coeffs, _compute_weight
from heartbeat import Heartbeat

PREC = 256
ctx.prec = PREC
N_AFE = 60
X = 12.0

def compute_L(s_re, s_im, A):
    s = acb(s_re, s_im)
    main = acb(0, 0)
    dual = acb(0, 0)
    for n in range(1, N_AFE + 1):
        an = A[n - 1]
        if an == 0:
            continue
        ns = acb(n, 0) ** (-s)
        nsm1 = acb(n, 0) ** (s - acb(1, 0))
        V = _compute_weight(n / X, s, "V")
        Vt = _compute_weight(n * X, s, "V_tilde")
        main += acb(an, 0) * ns * V
        dual += acb(an, 0) * nsm1 * Vt
    return main + dual

def compute_r(s_re, s_im, A, h=0.01):
    """Compute continuity radius r = |L(s)| / |L'(s)|."""
    L = compute_L(s_re, s_im, A)
    L_mod = float(abs(L).mid())

    # Central differences for gradient
    Lph = compute_L(s_re + h, s_im, A)
    Lmh = compute_L(s_re - h, s_im, A)
    dL_dsigma = abs((Lph - Lmh) / acb(2 * h, 0))

    Lph_t = compute_L(s_re, s_im + h, A)
    Lmh_t = compute_L(s_re, s_im - h, A)
    dL_dt = abs((Lph_t - Lmh_t) / acb(2 * h, 0))

    grad = (float(dL_dsigma.mid())**2 + float(dL_dt.mid())**2)**0.5
    r = L_mod / grad if grad > 1e-15 else float('inf')
    return L_mod, grad, r

tau_vals = compute_tau(200)
A = compute_sym2_coeffs(tau_vals)

# Existing derivative bounds (from derivative_bound.py)
existing = {
    (0.6, -7.0), (0.6, -6.0), (0.6, -5.0), (0.6, -8.0), (0.6, -9.0),
    (0.7, -7.0), (0.7, -8.0),
    (0.8, -7.0), (0.8, -8.0),
    (0.9, -7.0), (0.9, -8.0), (0.9, -16.0),
    (1.0, -7.0), (1.0, -16.0), (1.0, 0.0),
    (0.6, 7.0), (0.6, 6.0), (0.6, 5.0), (0.6, 8.0), (0.6, 9.0),
    (0.7, 7.0), (0.7, 8.0),
    (0.8, 7.0), (0.8, 8.0),
    (0.9, 7.0), (0.9, 8.0), (0.9, 16.0),
    (1.0, 7.0), (1.0, 16.0),
}

# All grid points in [0.6, 1.0] x [-20, 20]
sigmas = [0.6, 0.7, 0.8, 0.9, 1.0]
ts = list(range(-20, 21))
needed = [(s, float(t)) for s in sigmas for t in ts if (s, float(t)) not in existing]

print(f"Computing derivative bounds at {len(needed)} new grid points...")
print(f"({len(existing)} already computed)")

hb = Heartbeat(interval=30)
results = {}
t_start = time.time()

for idx, (s_re, s_im) in enumerate(needed):
    t0 = time.time()
    hb.tick(f"point {idx+1}/{len(needed)} ({s_re}, {s_im})")
    L_mod, grad, r = compute_r(s_re, s_im, A)
    elapsed = time.time() - t0
    results[f"{s_re},{s_im}"] = {"L_mod": L_mod, "grad": grad, "r": r}
    if (idx + 1) % 10 == 0:
        print(f"  [{idx+1}/{len(needed)}] ({s_re}, {s_im:+.0f}): |L|={L_mod:.4f}, |L'|={grad:.4f}, r={r:.4f} ({elapsed:.1f}s)")
        # Save intermediate results
        with open(WITNESS / "derivative_bounds_batch.json", "w") as f:
            json.dump(results, f, indent=2)

hb.done()
elapsed_total = time.time() - t_start

# Save final results
with open(WITNESS / "derivative_bounds_batch.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nDone: {len(results)} points computed in {elapsed_total:.1f}s ({elapsed_total/len(results):.1f}s/point)")

# Merge with existing and verify coverage
import math
existing_r = {
    (0.6, -7.0): 0.132619, (0.6, -6.0): 1.124193, (0.6, -5.0): 1.943164,
    (0.6, -8.0): 0.890908, (0.6, -9.0): 1.091370,
    (0.7, -7.0): 0.249332, (0.7, -8.0): 1.000345,
    (0.8, -7.0): 0.393366, (0.8, -8.0): 1.139019,
    (0.9, -7.0): 0.455316, (0.9, -8.0): 1.313217, (0.9, -16.0): 1.438702,
    (1.0, -7.0): 0.529, (1.0, -16.0): 1.493555, (1.0, 0.0): 2.813740,
    (0.6, 7.0): 0.132619, (0.6, 6.0): 1.124193, (0.6, 5.0): 1.943164,
    (0.6, 8.0): 0.890908, (0.6, 9.0): 1.091370,
    (0.7, 7.0): 0.249332, (0.7, 8.0): 1.000345,
    (0.8, 7.0): 0.393366, (0.8, 8.0): 1.139019,
    (0.9, 7.0): 0.455316, (0.9, 8.0): 1.313217, (0.9, 16.0): 1.438702,
    (1.0, 7.0): 0.529, (1.0, 16.0): 1.493555,
}
for k, v in results.items():
    s, t = k.split(",")
    existing_r[(float(s), float(t))] = v["r"]

# Verify coverage
sigma_centers = [0.65, 0.75, 0.85, 0.95]
t_centers = [t + 0.5 for t in range(-20, 20)]
cell_diag = math.sqrt(0.1**2 + 1.0**2)

covered = 0
uncovered = []
for sc in sigma_centers:
    for tc in t_centers:
        found = False
        for gp, r in existing_r.items():
            d = math.sqrt((sc - gp[0])**2 + (tc - gp[1])**2)
            if d < r:
                found = True
                break
        if found:
            covered += 1
        else:
            uncovered.append((sc, tc))

print(f"\nOverlapping disk coverage: {covered}/{covered+len(uncovered)} cells")
if uncovered:
    print(f"Uncovered: {len(uncovered)} cells")
    for c in uncovered:
        print(f"  ({c[0]:.2f}, {c[1]:+.1f})")
else:
    print("ALL CELLS COVERED - zero-free region proved!")
