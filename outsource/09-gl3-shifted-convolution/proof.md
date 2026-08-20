# GL₃ Shifted Convolution — Proof

**Status:** RESEARCH GAP (no proof for 09-A; 09-B' is technical transfer).

## §1. What the AFE actually produces

After squaring the two-term AFE for L(½+it, Π) and integrating over
t ∈ [T, 2T], the off-diagonal contributions are an **averaged** object:

    (T/N) · Σ_{h ≍ N/T} Σ_{n ≍ N} a_Π(n) ā_Π(n+h) W(n/N, h/H)

with H = N/T ≍ N^{1/3} = T^{1/2}.

The individual shifted sum S_W(h, N; Π) for fixed h is a strictly
stronger object and is 09-A.

## §2. What DLY 2024 established (corrected)

### Theorem 1.1 (second moment upper bound)

For f a Hecke cusp form on SL₃(ℤ):

    ∫_{-T}^{T} |L(f, ½+it)|² dt ≪_{f,ε} T^{4/3+ε}

### Theorem 1.2 (averaged shifted convolution — exact statement)

For 1 ≤ H ≤ N^{1/2-ε} and W an X^ε-inert smooth function on (ℝ⁺)²:

    Σ_{n,k} λ_f(n)λ_f(n+k) W(n/N, k/H)
    ≪_{f,ε} N^{4/3+ε}/H^{1/3} + √H · N^{1+ε}

**Non-trivial when H > N^{1/4}.**

**Scope:** Hecke cusp forms on SL₃(ℤ) — this includes **spherical/Maaß**
representations at infinity. Our project uses **holomorphic** symmetric-square
lifts, which have a different (cohomological) archimedean type. The DLY proof
mechanism does NOT rely on spectral theory at infinity, so the archimedean
distinction does not block the method. Wang 2026 handles the holomorphic case
directly.

At our scale H = N^{1/3}:
- First term: N^{4/3-1/9+ε} = N^{11/9+ε}
- Second term: N^{1/6+1+ε} = N^{7/6+ε}
- Dominant: N^{11/9+ε}
- Saving vs NH = N^{4/3}: factor N^{1/9}
- With AFE coefficient T/N = N^{-1/3}: contribution ≈ N^{8/9} = T^{4/3} ✓

### DLY proof mechanism (corrected from previous version)

The DLY proof does NOT use GL₃ spectral expansion or GL₃ large sieve.
The actual chain is:

1. **GL₃ Voronoi summation** (Lemma 2.4, Miller–Schmid): Transforms the
   sum over λ_f(n) using GL₃ Fourier coefficients.

2. **Poisson summation** in the k-variable: Dualizes the shift.

3. **DFI delta symbol** (Lemma 2.6): Introduces arithmetic conductor c ≤ Q
   with Q² = o(N), trading arithmetic for archimedean conductor.

4. **Reduction to norm bound** (Proposition 4.8): The problem reduces to
   bounding a bilinear form involving twisted Kloosterman sums:

     𝒩(N',Q,k,Y) = max_{‖α‖=1} ∫_{yasymp Y} Σ_{casymp Q}
       |Σ_{nasymp N'} α_n S(k̄,n;c) n^{iy}|² dy

5. **Duality + Poisson** (§5): Open the square, apply Poisson in n,
   get twisted Kloosterman sums S_χ(1,1;nk).

6. **Multiplicative Fourier decomposition** (eq. 1.17–1.18): The
   exponential e_{nk}(c₂c̄₁ + c₁c̄₂) decomposes as

     Σ_{χ mod nk} Ĝ(χ) χ(c₁) χ̄(c₂)

   where Ĝ(χ) = S_χ(1,1;nk)/φ(nk).

7. **Weil bounds for twisted Kloosterman sums** (Lemma 2.9):
   |S_χ(m,n;p)| ≤ 2p^{1/2} for prime p. For prime powers p^j,
   |S_χ(m,n;p^j)| ≤ 2p^{j/2} (with conductor condition) or
   |S_χ(m,n;p^j)| ≤ 2p^{j-1/2} (without). Higher prime powers are
   sparse enough that the saving suffices.

8. **Hybrid large sieve** (Lemma 2.8, Gallagher): For Dirichlet
   characters χ mod d:

     Σ_{χ mod d} ∫_{-Y}^{Y} |Σ_{n≤N} a_n χ(n) n^{iy}|² dy ≪ (dY + N) Σ|a_n|²

This is a **Gallagher-type hybrid character large sieve**, NOT a "GL₃
spectral large sieve." The spectral theory of GL₃ is not used in the
proof.

## §3. Wang 2026 (new reference)

**You Jun Wang**, "Shifted convolution sum for the coefficients of
symmetric square L-function", *Proc. Roy. Soc. Edinburgh Sect. A*,
online 6 May 2026. doi:10.1017/prm.2026.10153.

**Main result:** For f a normalized primitive holomorphic cusp form of
even integral weight on SL₂(ℤ), and λ_{sym²f}(n) the n-th coefficient
of L(s, sym²f):

    Σ_{h≤H} Σ_{N<n≤2N} λ_{sym²f}(n) λ_{sym²f}(n+h) ≪_{f,ε} N^{?+ε}

for H ≫ N^{1/4}. The bound is non-trivial at our scale H = N^{1/3}.

**Scope:** Holomorphic cusp forms of even integral weight on the full
modular group — exactly the class of forms in our project.

**Proof method:** Uses Perron formula, symmetric square L-function
analytic properties, and shifted convolution techniques. The paper
references the same family of results (Munshi 2013, Sun 2018, Xi 2018,
Pal 2025) that DLY builds on.

## §4. What 09-B' requires

Wang 2026 proves the estimate for a **box cutoff** Σ_{h≤H} Σ_{N<n≤2N}.
Our AFE produces a **smooth two-variable weight** W(n/N, h/H).

The transfer from box to smooth weight requires:

1. **Dyadic decomposition**: Break the sum into dyadic blocks
   n ≍ N₀, h ≍ H₀.
2. **Partial summation**: Convert the box cutoff to smooth weight using
   summation by parts.
3. **Uniformity check**: Verify that Wang 2026's implied constant is
   uniform enough for the dyadic decomposition to not lose the saving.

This is a standard but non-trivial technical step. If it works, the
averaged off-diagonal for M-1/M-2 is controlled.

## §5. 09-A: Why individual fixed-h is harder

For individual fixed h, the AFE expansion does NOT average over h.
The sum S_W(h, N; Π) for fixed h ≍ N^{1/3} has:

- No averaging benefit over h
- The DLY/Wang mechanism relies on averaging over h to apply the
  large sieve / character decomposition
- Individual shifted convolutions at the critical scale remain open
  for all classes of GL₃ forms

## §6. Dependencies

This package depends on:
- **03-partial-sum-bound**: Friedlander–Iwaniec GL₂ bound (AFE input)
- **04-gl3-afe**: GL₃ AFE structure (provides N ≍ T^{3/2}, h ≍ T^{1/2})

This package is relevant to (but NOT a logical prerequisite for):
- **06-M-1-mollifier**: averaged power-saving would suffice
- **07-M-2-mean-value**: averaged power-saving would suffice

## Status: [OBL]

09-A (individual) is an open research problem.
09-B' (Wang 2026 transfer) is a technical verification pending.
