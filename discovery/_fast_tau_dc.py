"""
Divide-and-conquer FFT sieve for tau(n) (Ramanujan delta).

Recurrence (from _fast_tau_sieve.py, 0-indexed, f[n]=tau(n+1)):
  f[n] = (-24/n) * sum_{j=0}^{n-1} sig[j] * f[n-1-j]
  where sig[j] = sigma_1(j+1).

Equivalently: f[n] = (-24/n) * sum_{k=0}^{n-1} H[n-1-k] * f[k]
  where H[m] = sig[m] = sigma_1(m+1).

This is online convolution (f[n] uses f[0..n-1]).
DC-FFT reduces O(N^2) to O(N log^2 N).

Cross contribution from f[lo..mid-1] to targets [mid..hi-1]:
  acc[n] += sum_{k=lo}^{mid-1} H[n-1-k] * f[k]
          = (np.convolve(A, H_trunc))[n-1-lo]
  where A = f[lo..mid-1], H_trunc = H[0..hi-lo-2].
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import time


def _build_H(N: int) -> np.ndarray:
    """H[m] = sigma_1(m+1) for m=0..N-2."""
    sig1 = np.zeros(N + 1, dtype=np.float64)
    for d in range(1, N + 1):
        sig1[d::d] += d
    return sig1[1:N].copy()   # length N-1, H[m]=sigma_1(m+1)


_DIRECT_BLOCK = 512   # below this size, use O(B^2) direct pass (avoids tiny-FFT overhead)


def compute_tau_dc(N: int) -> np.ndarray:
    """
    Compute f[0..N-1] where f[n] = tau(n+1), using DC-FFT online convolution.
    O(N log^2 N) time.
    Same output convention as compute_tau_fast in _fast_tau_sieve.py.
    """
    H = _build_H(N)
    f = np.zeros(N, dtype=np.float64)
    f[0] = 1.0      # tau(1) = 1
    acc = np.zeros(N, dtype=np.float64)

    def dc(lo: int, hi: int) -> None:
        if hi <= lo:
            return
        size = hi - lo
        if size <= _DIRECT_BLOCK:
            # Direct forward pass: compute f[n] then immediately push its contribution
            # to future acc positions within [lo, hi).  Avoids millions of tiny FFT calls.
            # Start at lo (not lo+1) so f[lo] (or f[0]=1) is propagated before f[lo+1] is computed.
            for n in range(lo, hi):
                if n >= 1:
                    f[n] = -24.0 * acc[n] / n
                # f[n] is now set; propagate to future slots within this block
                length = hi - n - 1
                if length > 0:
                    acc[n + 1:hi] += f[n] * H[:length]
            return

        mid = (lo + hi) // 2
        dc(lo, mid)

        # Cross: f[lo..mid-1] → acc[mid..hi-1]
        # acc[n] += (H★A)[n-1-lo]  for n in [mid..hi-1]
        # where (H★A)[m] = sum_{i=0}^{A_len-1} H[m-i]*A[i]
        # m = n-1-lo ranges from mid-lo-1 to hi-lo-2
        A = f[lo:mid].copy()
        A_len = len(A)
        h_len = hi - lo - 1          # max m+1 needed = hi-lo-2+1
        H_trunc = H[:h_len] if h_len <= len(H) else np.concatenate([H, np.zeros(h_len - len(H))])

        nfft = 1
        while nfft < A_len + h_len:
            nfft <<= 1
        C = np.fft.irfft(np.fft.rfft(A, nfft) * np.fft.rfft(H_trunc, nfft), nfft)
        # C[m] = sum_{i} A[i]*H_trunc[m-i]

        m0 = mid - lo - 1          # first m = mid-1-lo
        m1 = hi  - lo - 1          # last  m = hi-1-lo  (exclusive: hi-lo-1)
        acc[mid:hi] += C[m0:m1]

        dc(mid, hi)

    dc(0, N)
    return f


def compute_a_sym2_dc(N: int) -> np.ndarray:
    """Compute a_sym2(1..N): tau sieve + GL3 Hecke recursion."""
    tau_f = compute_tau_dc(N)
    from discovery._fast_tau_sieve import compute_a_sym2
    return compute_a_sym2(tau_f)


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000

    print(f"DC-FFT tau sieve, N={N}", flush=True)
    t0 = time.time()
    f = compute_tau_dc(N)
    dt = time.time() - t0
    print(f"  Time: {dt:.2f}s", flush=True)

    # Known tau values (1-indexed): tau(n) = f[n-1]
    known = {1:1, 2:-24, 3:252, 4:-1472, 5:4830, 6:-6048, 7:-16744, 8:84480,
             9:-113643, 10:-115920, 11:534612, 12:-370944}
    ok = True
    for n, v in known.items():
        if n <= N:
            got = f[n-1]
            if abs(got - v) > 0.5:
                print(f"  FAIL tau({n}): got {got:.0f}, expected {v}")
                ok = False
    if ok:
        print(f"  Spot-checks PASS (all {len([n for n in known if n<=N])} values correct)")
    print(f"  tau({N}) = {f[N-1]:.0f}")
