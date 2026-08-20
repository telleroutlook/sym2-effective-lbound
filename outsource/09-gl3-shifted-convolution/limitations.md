# GL₃ Shifted Convolution — Limitations

## What this package does

This package documents two sub-problems [OBL]:
- 09-A: individual shifted convolution (open research problem)
- 09-B': Wang 2026 smooth-weight transfer (technical verification)

## Literature status (corrected)

### DLY 2024 (arXiv:2407.06962)

- **Theorem 1.2 (exact):** Σ_{n,k} λ(n)λ_f(n+k) W(n/N, k/H) ≪ N^{4/3+ε}/H^{1/3} + √H·N^{1+ε}
- **Scope:** Hecke cusp forms on SL₃(ℤ) (spherical/Maaß type)
- **Proof chain:** GL₃ Voronoi → Poisson → delta symbol → norm bound → duality → twisted Kloosterman sums → Weil bounds → Gallagher hybrid character large sieve
- **NOT used:** GL₃ spectral expansion, GL₃ large sieve, Maaß spectral theory

### Wang 2026 (PRESEMA, doi:10.1017/prm.2026.10153)

- **Main result:** Averaged shifted convolution for λ_{sym²f}(n), holomorphic cusp form of even integral weight on SL₂(ℤ), non-trivial for H ≫ N^{1/4}
- **Scope:** Holomorphic symmetric-square — exactly our project's class of forms
- **Our scale:** H = N^{1/3} > N^{1/4} → covered

### Pal 2025 (arXiv:2212.14620v3, IMRN 2025)

- ∫|L|² ≪ T^{3/2 - 3/88 + ε} ≈ T^{1.466+ε} for Hecke–Maaß GL₃ cusp forms
- **Weaker than DLY** in GL₃ scope: T^{1.466} vs T^{1.333}
- Note: 3/2 - 3/88 = 132/88 - 3/88 = 129/88 ≈ 1.466 (NOT 0.406)

### Kloosterman sums

| Object | Bound | Source |
|--------|-------|--------|
| Classical S(m,n;c) | Weil: ≤ d₃(c)·c^{1/2} | Classical [THM] |
| Twisted S_χ(m,n;p) | ≤ 2p^{1/2} | DLY Lemma 2.9 [THM] |
| Twisted S_χ(m,n;p^j) | ≤ 2p^{j/2} or 2p^{j-1/2} | DLY Lemma 2.9 [THM] |
| GL₃ S₃(m,n;c) | ≪ c^{3/2+ε} (trivial) | [BASE] |
| GL(n) Weyl elements | Power-saving | Blomer–Man 2023 [THM] |

The DLY approach uses **classical twisted Kloosterman sums** (GL₂-level),
not GL₃ Kloosterman sums. The Weil-type bounds for twisted sums are
classical and well-understood.

## What is NOT achieved

### 09-A: Individual shifted convolution [OBL]

No power-saving bound S_W(h,N;Π) ≪ N^{1-δ} for individual fixed h ≍ N^{1/3}
is known for any class of GL₃ forms. The averaged results (DLY, Wang)
rely on averaging over h and do not imply individual bounds.

### 09-B': Smooth-weight transfer [OBL]

Wang 2026 proves the estimate for box cutoff. The transfer to smooth
two-variable weight W(n/N, h/H) via dyadic decomposition + partial
summation is a technical step that needs verification.

## Key clarification

**09 is NOT a necessary condition for M-1/M-2.** The second-moment
estimate may be achievable by other routes. However, the averaged
shifted-convolution approach (Wang 2026 + 09-B') is the most natural
given current technology.
