# GL₃ Shifted Convolution — Statement

**Status:** [OBL] (sub-problems, see below)

## Context

After expanding |L(½+it, Π)|² via the two-term AFE and integrating over
t ∈ [T, 2T], the off-diagonal contributions are NOT a single individual
shifted sum. They are **averaged** over h:

    (T/N) · Σ_{h ≍ N/T} Σ_{n ≍ N} a_Π(n) ā_Π(n+h) W(n/N, h/H)

with H = N/T ≍ N^{1/3} = T^{1/2}.

### Known results at our scale H = N^{1/3} > N^{1/4}

- **Wang 2026** (PRESEMA, doi:10.1017/prm.2026.10153): For Π = sym²f
  with f a holomorphic cusp form of even integral weight on SL₂(ℤ),
  the averaged shifted convolution

    Σ_{h≤H} Σ_{N<n≤2N} λ_{sym²f}(n) λ_{sym²f}(n+h)

  admits a non-trivial bound for H ≫ N^{1/4}. Our scale H = N^{1/3} > N^{1/4}
  is covered.

- **DLY 2024** (arXiv:2407.06962, Theorem 1.2): For f a Hecke cusp form
  on SL₃(ℤ) (spherical/Maaß), the averaged shifted convolution with smooth
  weight W(n/N, k/H) satisfies

    Σ_{n,k} λ(n)λ_f(n+k) W(n/N, k/H) ≪_{f,ε} N^{4/3+ε}/H^{1/3} + √H·N^{1+ε}

  Non-trivial when H > N^{1/4}.

### What remains open

The results above are **averaged** over h. The following remain open:

---

## Sub-problem 09-A: Individual shifted convolution [OBL]

**Question:** For fixed h ≍ N^{1/3}, does the individual smooth shifted sum

    S_W(h, N; Π) = Σ_n a_Π(n) ā_Π(n+h) W(n/N)

satisfy S_W(h, N; Π) ≪_{Π,W,ε} N^{1-δ} for some δ > 0?

**Note:** We do NOT presuppose a main term. Rankin–Selberg L(s, Π × Π̃)
controls the diagonal h = 0 only; the shifted case h ≠ 0 requires separate
analysis via delta method or spectral expansion.

**Status:** [OBL] — no power-saving bound for individual fixed h ≍ N^{1/3}
is known for any class of GL₃ forms.

---

## Sub-problem 09-B': Wang 2026 compatibility check [OBL]

Wang 2026 proves the averaged shifted convolution bound for
λ_{sym²f}(n) with holomorphic f at our required scale. However, the
AFE expansion involves a **two-variable smooth weight** W(n/N, h/H),
not a box cutoff. The precise research task is:

**Verify that Wang 2026's estimate can be promoted from box cutoff to
smooth two-variable weight W(n/N, h/H) via dyadic decomposition and
partial summation.**

This is a technical transfer problem (not an existence gap). If the
transfer works, then 09-B' closes and the averaged off-diagonal for
M-1/M-2 is controlled.

**Status:** [OBL] — technical verification pending.

---

## Relationship to M-1 and M-2

- M-1 (mollifier second moment) requires an averaged power-saving bound
  on the off-diagonal. Wang 2026 + 09-B' transfer would provide this.
- M-2 (unmollified second moment) requires the same type of averaged bound.
- **These are sufficient conditions, not necessary.** The second moment
  may be achievable by other routes (direct moment methods, hybrid bounds).
