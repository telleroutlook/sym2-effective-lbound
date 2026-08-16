"""
_fast_tau_sieve.py -- Extended partial sum analysis of a_sym2(n) for sym^2 Delta.

tau(n): computed via log-derivative recurrence (O(N^2) with numpy dot, ~20x faster
than the q-product implementation in rs_estimate.py).

a_sym2(n): computed by multiplicative sieve + GL3 Hecke recursion at prime powers.
  a(p) = (tau(p)/p^{11/2})^2 - 1
  a(p^k) = A*a(p^{k-1}) - A*a(p^{k-2}) + a(p^{k-3}),  A=a(p),  for k>=3
  a(p^0)=1, a(p^1)=A, a(p^2)=A(A-1)
  a(mn) = a(m)*a(n) for gcd(m,n)=1

PURPOSE: extend the partial sum S(X) = sum_{n<=X} a_sym2(n) analysis beyond N=10000
to bound the GL3 truncation error for [OBL M-3] certification.
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time


def compute_tau_fast(N: int) -> np.ndarray:
    """Return tau(1), ..., tau(N) as float64 using log-derivative recurrence.

    n*f[n] = -24 * sum_{k=1}^n sigma_1(k) * f[n-k],  f[0]=tau(1)=1.

    Float64 suffices for n<=10^5: |tau(n)| <= 2*n^{5.5} <= 2*(10^5)^{5.5} ~ 6e27,
    well within float64 range (max ~1.8e308), with 15-digit relative precision.
    """
    sig1 = np.zeros(N + 1, dtype=np.float64)
    for d in range(1, N + 1):
        sig1[d::d] += d          # sigma_1 sieve, O(N log N)
    sig = sig1[1:].copy()        # sig[k] = sigma_1(k+1)

    f = np.zeros(N, dtype=np.float64)
    f[0] = 1.0
    for n in range(1, N):        # O(N^2) with numpy dot
        s = np.dot(sig[:n], f[n-1::-1])
        f[n] = -24.0 * s / n
    return f


def compute_a_sym2(tau_f: np.ndarray) -> np.ndarray:
    """Return a_sym2(1), ..., a_sym2(N) from float tau values."""
    N = len(tau_f)

    # Smallest prime factor sieve
    spf = list(range(N + 1))
    for p in range(2, int(N**0.5) + 1):
        if spf[p] == p:
            for m in range(p * p, N + 1, p):
                if spf[m] == m:
                    spf[m] = p

    # GL3 Hecke local coefficient at prime power p^k
    def a_pk(p: int, k: int) -> float:
        A = tau_f[p - 1] ** 2 / p ** 11 - 1.0  # a(p)
        if k == 0: return 1.0
        if k == 1: return A
        if k == 2: return A * (A - 1.0)
        a3, a2, a1 = 1.0, A, A * (A - 1.0)
        for _ in range(k - 2):
            a3, a2, a1 = a2, a1, A * a1 - A * a2 + a3
        return a1

    a = np.ones(N, dtype=np.float64)  # a[n-1] = a_sym2(n)
    for n in range(2, N + 1):
        m, val = n, 1.0
        while m > 1:
            p = spf[m]
            k = 0
            while m % p == 0:
                m //= p
                k += 1
            val *= a_pk(p, k)
        a[n - 1] = val
    return a


if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000

    t0 = time.time()
    tau_f = compute_tau_fast(N)
    print(f"compute_tau_fast({N}): {time.time()-t0:.2f}s")

    # Cross-check
    known = {2: -24, 3: 252, 5: 4830, 7: -16744, 11: 534612, 13: -577738}
    for p, v in known.items():
        if p <= N:
            got = round(tau_f[p-1])
            if got != v:
                print(f"  MISMATCH tau({p}): got {got}, expected {v}")
    print("  tau cross-check done.")

    t0 = time.time()
    a = compute_a_sym2(tau_f)
    print(f"compute_a_sym2({N}): {time.time()-t0:.2f}s")

    # Verify first few a_sym2 against existing data
    from discovery.rs_estimate import compute_tau
    from discovery.sym2_coeffs import compute_sym2_coeffs
    tau_ref = compute_tau(min(N, 200))
    a_ref = compute_sym2_coeffs(tau_ref)
    for i in range(min(10, N)):
        ref = float(a_ref[i])
        got = a[i]
        if abs(got - ref) > 1e-6:
            print(f"  MISMATCH a_sym2({i+1}): got {got:.6f}, expected {ref:.6f}")
    print("  a_sym2 cross-check done (first 10).")

    # Partial sum analysis
    cumsum = np.cumsum(a)
    abs_cs = np.abs(cumsum)
    idx = np.argmax(abs_cs)
    C_max = abs_cs[idx]
    print(f"\nPartial sum S(X) = sum_{{n<=X}} a_sym2(n)  [N={N}]:")
    print(f"  max|S(X)| = {C_max:.4f} at X={idx+1}")
    print(f"  S({N}) = {cumsum[-1]:.4f}")
    top5 = np.argsort(abs_cs)[-5:][::-1]
    for i in top5:
        print(f"    X={i+1:7d}: |S|={abs_cs[i]:.4f}")

    # Cesaro error bounds
    print(f"\nCesaro error bound (sigma=0.9):  3*C_max / N^0.9 = {3*C_max/N**0.9:.6f}")
    print(f"  min|L_ces(0.9+7.075i, N={N})| ~ (extrapolate from N=10000: 0.4467)")
    print(f"  Gap estimate: ~{0.4467 - 3*C_max/N**0.9:.4f}")
