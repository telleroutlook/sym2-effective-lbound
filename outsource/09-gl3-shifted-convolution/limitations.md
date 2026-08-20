# GL₃ Shifted Convolution — Limitations

## What this package does

This package documents two open research problems [OBL] related to
GL₃ shifted convolution sums, with precise statements and corrected
literature references.

## What this package does NOT do

- Does NOT contain a proof
- Does NOT claim any [THM]-labelled result
- Does NOT claim that 09-A or 09-B are necessary conditions for M-1/M-2
  (they are sufficient conditions, not necessary)

## Corrected literature status

### DLY 2024 (Dasgupta–Leung–Young, arXiv:2407.06962)

- **Theorem 1.1**: ∫|L(f,½+it)|² dt ≪ T^{4/3+ε} for Hecke–Maaß GL₃ cusp forms
- **Theorem 1.2**: Averaged GL₃ shifted convolution, non-trivial when H > N^{1/4}
- **Scope**: spherical/Maaß GL₃, NOT holomorphic symmetric-square
- **Kloosterman handling**: uses classical S(k̄,n;c) + Weil bounds (NOT GL₃ sums)

### Pal 2025 (arXiv:2212.14620v3, IMRN 2025)

- ∫|L(F,½+it)|² dt ≪ T^{3/2-3/32+ε} for Hecke–Maaß GL₃ cusp forms
- **Weaker than DLY** in the GL₃ cusp form scope: T^{3/2-3/32} ≈ T^{0.406} vs T^{4/3} ≈ T^{0.333}
- Pal's result applies to a broader class of forms (not just GL₃) but is not the current best for GL₃

### Kloosterman sums (corrected)

| Object | Best known bound | Status |
|--------|-----------------|--------|
| Classical S(m,n;c) | Weil: d₃(c)·c^{1/2} | Classical [THM] |
| GL₃ S₃(m,n;c) | ≪ c^{3/2+ε} (trivial) | Known [BASE] |
| GL(n) Weyl elements | Power-saving (Blomer–Man 2023, etc.) | [THM] |

The package's previous claim of "only trivial bound for GL₃ Kloosterman sums" was
incorrect: non-trivial bounds exist for specific element types.

However, the DLY approach uses **classical** Kloosterman sums after GL₃ Voronoi,
so the GL₃ Kloosterman bounds are not directly relevant to the DLY mechanism.

## What is NOT achieved

### 09-A: Individual shifted convolution [OBL]

No power-saving bound S_W(h,N;Π) ≪ N^{1-δ} for individual fixed h ≍ N^{1/3}
is known for any class of GL₃ forms. The trivial bound is N^{1+ε}.

### 09-B: Averaged transfer to holomorphic Π [OBL]

DLY's averaged mechanism works for spherical/Maaß GL₃. The transfer to
cohomological/holomorphic Π = sym²(holomorphic π) requires:

1. Adapting the GL₃ Voronoi formula for cohomological archimedean type
2. Using cohomological spectral theory instead of Maaß spectral theory
3. Verifying that the power-saving is preserved

This is a well-defined but open research task.

## Key clarification: 09 is NOT a necessary condition for M-1/M-2

The second-moment estimate ∫|L(½+it,Π)|² dt may be achievable by other
routes (direct moment methods, hybrid bounds, etc.) without proving either
09-A or 09-B. The shifted-convolution approach is the most natural given
current technology, but it is not the only possible route.
