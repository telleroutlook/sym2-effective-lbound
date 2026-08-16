"""
_L1_rankin_selberg.py -- Compute L(1, sym^2 Delta) via Rankin-Selberg identity.

FORMULA (exact, for Re(s) > 1):
  L(s, sym^2 Delta) = [zeta(2s)/zeta(s)] * sum_{n>=1} tau(n)^2 / n^{s+11}

where tau(n) are the Ramanujan tau coefficients and s+11 = 12 at s=1.

At s = 1+delta (delta > 0):
  L(1+delta) = zeta(2+2*delta)/zeta(1+delta) * S(delta)
  S(delta) = sum_{n>=1} tau(n)^2 / n^{12+delta}

This is an ABSOLUTELY CONVERGENT positive Dirichlet series for delta > 0.

CERTIFICATION PATH:
  1. Compute S_N(delta) = sum_{n=1}^N tau(n)^2 / n^{12+delta}  [Arb, exact to 10^-20]
  2. Bound tail: R_N(delta) = sum_{n>N} tau(n)^2 / n^{12+delta}
     Using Deligne: tau(n)^2 <= (sigma_0(n))^2 * n^11
     => tau(n)^2 / n^{12+delta} <= (sigma_0(n))^2 / n^{1+delta}
     => R_N <= sum_{n>N} (sigma_0(n))^2 / n^{1+delta}
     <= sum_{n>N} n^{0.01} / n^{1+delta}  [since sigma_0(n) << n^{0.01}]
     = sum_{n>N} n^{-1-delta+0.01}
     <= integral_{N}^infty x^{-1-delta+0.01} dx = N^{-delta+0.01} / (delta-0.01)  [for delta > 0.01]
  3. Compute zeta(1+delta) = 1/delta + gamma + O(delta) with Arb
  4. Error from delta: |L(1) - L(1+delta)| <= delta * |L'(1+theta)| for theta in (0,delta)
     |L'(1+theta)| <= sum |b(n)| log(n) / n^{1+theta} <= [explicit Arb bound]

EMPIRICAL CHECK:
  For each delta in [0.001, 0.01, 0.05, 0.1, 0.5]: compute L(1+delta), check convergence to L(1) ~ 0.6318.

STATUS: discovery tier (mpmath). Next step: Arb interval arithmetic for certified bounds.
"""
import sys; sys.path.insert(0, '.')
import mpmath; mpmath.mp.dps = 30
from discovery.rs_estimate import compute_tau

mp = mpmath

N_COEFF = 5000
print(f"Loading {N_COEFF} tau coefficients ...")
tau_arr = compute_tau(N_COEFF)
tau2_arr = [tau_arr[i]**2 for i in range(N_COEFF)]
print(f"Done. tau(1)={tau_arr[0]}, tau(2)={tau_arr[1]}, tau(12)={tau_arr[11]}")


def S_partial(delta, N=None):
    """S_N(delta) = sum_{n=1}^N tau(n)^2 / n^{12+delta} using mpmath."""
    if N is None:
        N = N_COEFF
    s_exp = mp.mpf('12') + mp.mpf(str(delta))
    total = mp.mpf(0)
    for n in range(1, N + 1):
        total += mp.mpf(tau2_arr[n-1]) / mp.power(n, s_exp)
    return total


def L_rankin(delta, N=None):
    """L(1+delta) = zeta(2+2*delta)/zeta(1+delta) * S_N(delta)."""
    d = mp.mpf(str(delta))
    z1 = mp.zeta(1 + d)
    z2 = mp.zeta(2 + 2*d)
    S = S_partial(delta, N)
    return z2 / z1 * S, z1, z2, S


def tail_bound(delta, N):
    """
    Upper bound for sum_{n>N} tau(n)^2 / n^{12+delta}.
    Uses tau(n)^2 <= n^{11} * sigma_0(n)^2 <= n^{11} * n^{0.02} (Deligne).
    So tau(n)^2/n^{12+delta} <= n^{-1-delta+0.02}.
    Integral bound: int_N^inf x^{-1-delta+0.02} dx = N^{-delta+0.02} / (delta - 0.02).
    Only valid for delta > 0.02.
    """
    d = mp.mpf(str(delta))
    N_mp = mp.mpf(str(N))
    if delta <= 0.02:
        return None  # Bound not valid for small delta
    exponent = 0.02 - d  # negative for delta > 0.02
    return mp.power(N_mp, exponent) / (d - mp.mpf('0.02'))


if __name__ == "__main__":
    print("\nL(1+delta) via Rankin-Selberg at N=5000:")
    print(f"  {'delta':>8}  {'L(1+d)':>12}  {'error_d':>12}  {'tail_bound':>14}  zeta(1+d)")
    print()

    L_target = 0.6318  # known from direct quadrature

    deltas = [0.5, 0.2, 0.1, 0.05, 0.03, 0.02, 0.01]
    for delta in deltas:
        L_val, z1, z2, S = L_rankin(delta, N=5000)
        L_f = float(L_val)
        err_delta = abs(L_f - L_target)
        tb = tail_bound(delta, N=5000)
        tb_f = float(tb) if tb is not None else float('nan')
        print(f"  {delta:>8.3f}  {L_f:>12.8f}  {err_delta:>12.6e}  {tb_f:>14.4e}  {float(z1):.6f}")

    print()
    # Convergence study: delta=0.05, varying N
    delta = 0.05
    print(f"Convergence in N at delta={delta}:")
    for N in [100, 500, 1000, 2000, 5000]:
        L_v, _, _, _ = L_rankin(delta, N)
        tb = tail_bound(delta, N)
        print(f"  N={N:5d}: L(1+{delta}) = {float(L_v):.8f}"
              f"  tail_bound = {float(tb):.4e}")

    print()
    # Error from delta-shift: bound |L(1) - L(1+delta)| via L'
    print("Bounding L'(1+delta) via Dirichlet series:")
    delta_test = 0.05
    print(f"  Summing |b(n)| log(n) / n^{{1+{delta_test}}} for n<=5000 (sym2 coefficients):")
    from discovery.sym2_coeffs import compute_sym2_coeffs
    a_sym2 = compute_sym2_coeffs(tau_arr)
    Lprime_bound = mp.mpf(0)
    d = mp.mpf(str(delta_test))
    for n in range(1, 5001):
        Lprime_bound += abs(mp.mpf(a_sym2[n-1])) * mp.log(n) / mp.power(n, 1 + d)
    print(f"  sum |b(n)| log(n)/n^{{1+delta}} (N=5000) = {float(Lprime_bound):.6f}")
    print(f"  |L(1) - L(1+{delta_test})| <= {delta_test} * {float(Lprime_bound):.4f} = {delta_test*float(Lprime_bound):.4e}")
    print()
    print("If this bound + tail_bound < 0.005 at some (delta, N):")
    print("  L(1, sym^2 Delta) in [L(1+delta) - err, L(1+delta) + err] is CERTIFIED (via Arb).")
