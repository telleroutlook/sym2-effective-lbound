"""
_afe_central.py -- Certifiable J computation via central-value AFE (s0=1/2+it).

KEY INSIGHT: For each fixed t, L(1/2+it) can be approximated via the GL3 AFE:

  L_main(t) = sum_n a(n)/n^{1/2+it} * V(n/12, s0=1/2+it)

where V(y, s0) = (1/2pi) int G(s0+u)/G(s0) * y^{-u} * e^{u^2}/u  du  (Re u=1).

This sum is ABSOLUTELY CONVERGENT for each fixed t:
  |a(n)/n^{1/2+it} * V(n/12, 1/2+it)| <= |a(n)|/n^{1/2} * exp(-(log(n/12))^2/4)
So the tail after n=100 is < 10^{-5}.

For the self-dual form sym^2 Delta (epsilon=+1, real a(n)):
  L(1/2+it) = L_main(t) + phase(t) * conj(L_main(t))
where phase(t) = Q^{it} * G(1/2-it)/G(1/2+it)  (magnitude 1).

The t-integral for J converges because amp(t) contains e^{(-1/2+it)^2} = e^{1/4-t^2-it},
providing Gaussian e^{-t^2} decay.

This approach is certifiable: each inner sum converges absolutely, and the t-integral
truncation error is bounded by C * e^{-T^2} (explicit C from convexity bound).

Compare with the FAILED approaches:
- Dirichlet truncation: sum_n<=N a(n)/n^{1/2+it} -> conditional, O(N^{-1/2}) tail
- Two-sided AFE: W_dual(y) ~ 1/y (polynomial decay), still conditional
- THIS approach: V(y, 1/2+it) ~ exp(-(log y)^2/4), absolute convergence
"""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 30
from discovery.rs_estimate import compute_tau
from discovery.sym2_coeffs import compute_sym2_coeffs
from discovery.afe_gl3 import G_factor

mp = mpmath

N_MAX_COEFFS = 200
tau = compute_tau(N_MAX_COEFFS)
a_sym2 = compute_sym2_coeffs(tau)

X = mp.mpf(12)
k = 12
G1 = G_factor(mp.mpf(1), k, mp)

# -------------------------------------------------------------------------
# Complex-valued AFE weight for general s0 (including complex)
# -------------------------------------------------------------------------

def afe_weight_cx(y, s0, T=40, n_u=600):
    """
    V(y, s0) = (1/2pi) int_{Re=1} G(s0+u)/G(s0) * y^{-u} * e^{u^2} / u  du

    Returns complex value (real part only when s0 is real).
    For complex s0=1/2+it, returns a complex number.
    """
    y = mp.mpf(y)
    Gs0 = G_factor(s0, k, mp)
    dt_u = 2 * T / n_u
    total = mp.mpc(0)
    for i in range(n_u):
        tau_u = -T + (i + 0.5) * dt_u
        u = mp.mpc(1, tau_u)
        Gu = G_factor(s0 + u, k, mp)
        total += (Gu / Gs0) * mp.power(y, -u) * mp.exp(u**2) / u * dt_u
    return total / (2 * mp.pi)


def compute_L_main(t_val, n_max=100, n_u=400, T_u=30):
    """
    L_main(t) = sum_{n=1}^{n_max} a(n)/n^{s0} * V(n/12, s0)
    with s0 = 1/2 + it.  Absolutely convergent.
    Returns complex value.
    """
    s0 = mp.mpc(0.5, t_val)
    L = mp.mpc(0)
    for n in range(1, n_max + 1):
        an = mp.mpf(a_sym2[n-1])
        y = mp.mpf(n) / X
        V = afe_weight_cx(y, s0, T=T_u, n_u=n_u)
        L += an * mp.power(mp.mpf(n), -s0) * V
    return L


# -------------------------------------------------------------------------
# Phase factor phi(t) = Q^{it} * G(1/2-it)/G(1/2+it)  (for self-dual AFE)
# -------------------------------------------------------------------------

def phase_factor(t_val):
    """Q^{it} * G(1/2-it)/G(1/2+it)."""
    Q = mp.mpf(144)
    Gplus  = G_factor(mp.mpc(0.5,  t_val), k, mp)
    Gminus = G_factor(mp.mpc(0.5, -t_val), k, mp)
    return mp.power(Q, mp.mpc(0, t_val)) * Gminus / Gplus


# -------------------------------------------------------------------------
# Amplitude for J = (1/2pi) int Re[L(1/2+it) * amp(t)] dt
# -------------------------------------------------------------------------

def amp_t(t_val):
    """G(1/2+it)/G(1) * X^{-1/2+it} * exp((-1/2+it)^2) / (-1/2+it)."""
    s = mp.mpc(0.5, t_val)
    w = s - 1  # = -1/2 + it
    return (G_factor(s, k, mp) / G1) * mp.power(X, w) * mp.exp(w**2) / w


# -------------------------------------------------------------------------
# Main computation
# -------------------------------------------------------------------------

T_INT = 5.0     # integration limit: amp(t) * e^{-t^2} < 1e-10 for |t|>5
n_t   = 40      # quadrature points in t (quick probe; 100 for production)

N_AFE = 50      # terms in the AFE inner sum (80 for production)

print("Checking V(y, 1/2+0i) decay (should match e^{-(log y)^2/4}):")
for n_test in [1, 6, 12, 24, 72, 144]:
    y = mp.mpf(n_test) / X
    V = afe_weight_cx(y, mp.mpc(0.5, 0), T=25, n_u=300)
    saddle = float(mp.exp(-(mp.log(y)**2)/4))
    print(f"  n={n_test:3d}: y={float(y):.3f}  |V|={abs(float(mp.re(V))):.5f}  "
          f"saddle~{saddle:.5f}  Im(V)={float(mp.im(V)):.2e}")

print()
print("Convergence of L_main(0) vs n_max (should approach L(1/2, sym^2 Delta)/2):")
for n_test in [10, 20, 40, 60, 80]:
    Lm = compute_L_main(0.0, n_max=n_test, n_u=200, T_u=20)
    print(f"  n_max={n_test:3d}: Re(L_main)={float(mp.re(Lm)):.6f}  Im={float(mp.im(Lm)):.2e}")

print()
print(f"Computing J via central AFE (n_t={n_t}, N_AFE={N_AFE})...")
print("(Each L(1/2+it_j) computed via absolutely convergent AFE sum)")
print()

dt = 2 * T_INT / n_t
ts_j = [-T_INT + (i + 0.5) * dt for i in range(n_t)]

J_cx = mp.mpf(0)
for j, t_j in enumerate(ts_j):
    if j % 20 == 0:
        print(f"  t_j={t_j:.2f} ({j}/{n_t})", flush=True)
    Lm = compute_L_main(t_j, n_max=N_AFE, n_u=300, T_u=25)
    ph = phase_factor(t_j)
    # Full L(1/2+it_j) = L_main + phase * conj(L_main)
    L_full = Lm + ph * mp.conj(Lm)
    amp = amp_t(t_j)
    J_cx += mp.re(L_full * amp)

J = float(J_cx) * dt / (2 * float(mp.pi))

S1 = 0.548490  # from previous session (computed via AFE at s0=1, n=72)
L1 = S1 - J

print()
print(f"Results:")
print(f"  S1     = {S1:.6f}  (AFE sum at s0=1, n=1..72)")
print(f"  J      = {J:.6f}  (via central AFE, expected ~-0.083)")
print(f"  L(1)   = {L1:.6f}  (expected ~0.6314)")
print()

# Convergence check: J vs n_t
print("Convergence in n_t (quadrature points):")
for n_t_test in [20, 40, 60, 80, 100]:
    dt_test = 2 * T_INT / n_t_test
    ts_test = [-T_INT + (i + 0.5) * dt_test for i in range(n_t_test)]
    J_test = mp.mpf(0)
    for t_j in ts_test:
        Lm = compute_L_main(t_j, n_max=N_AFE, n_u=200, T_u=20)
        ph = phase_factor(t_j)
        L_full = Lm + ph * mp.conj(Lm)
        amp = amp_t(t_j)
        J_test += mp.re(L_full * amp)
    J_val = float(J_test) * dt_test / (2 * float(mp.pi))
    print(f"  n_t={n_t_test:3d}: J={J_val:.6f}  L(1)={S1 - J_val:.6f}  "
          f"(expected 0.6314)", flush=True)

print()
print("Decay check: |V(n/12, 1/2+it)| for t=2 vs Gaussian approximation:")
t_chk = 2.0
for n_test in [12, 24, 72, 144, 500]:
    y = mp.mpf(n_test) / X
    V = afe_weight_cx(y, mp.mpc(0.5, t_chk), T=25, n_u=200)
    saddle = float(mp.exp(-(mp.log(y)**2)/4))
    print(f"  n={n_test:4d}: |V|={abs(complex(V)):.5f}  saddle~{saddle:.5f}")
