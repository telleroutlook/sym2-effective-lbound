# GL₃ Shifted Convolution — Proof

**Status:** RESEARCH GAP (no proof exists for either sub-problem).

## §1. What the AFE actually produces

After squaring the two-term AFE for L(½+it, Π) and integrating over
t ∈ [T, 2T], the off-diagonal contributions are NOT a single individual
shifted sum. They are **averaged** over h:

    (T/N) · Σ_{h ≍ N/T} Σ_{n ≍ N} a_Π(n) ā_Π(n+h) W(n/N, h/H)

with H = N/T ≍ N^{1/3} = T^{1/2}.

This averaging is intrinsic to the AFE squaring process — it is not
an optional smoothing. The individual shifted sum S_W(h, N; Π) for
fixed h is a related but strictly stronger object.

## §2. What DLY 2024 established

### Theorem 1.1 (second moment upper bound)

For f a Hecke–Maaß cusp form on SL₃(ℤ):

    ∫_{-T}^{T} |L(f, ½+it)|² dt ≪_{f,ε} T^{4/3+ε}

This beats the trivial T^{3/2+ε} by a genuine power saving T^{1/6-ε}.

### Theorem 1.2 (averaged shifted convolution)

For the same class of f:

    Σ_{n,k} λ_f(n) λ_f(n+k) W(n/N, k/H)
    ≪_{f,ε} N^{4/3+ε}/H^{1/3} + √H · N^{ε} + N^{1+ε}

**Non-trivial regime:** H > N^{1/4}.

At our scale H = N^{1/3} > N^{1/4}, this gives a genuine averaged
power-saving bound on the shifted convolution.

### How DLY handles Kloosterman sums

After applying GL₃ Voronoi to the shifted sum, the dual involves
**classical** Kloosterman sums S(k̄, n; c), NOT GL₃ Kloosterman sums.
DLY then uses:

1. Twisting by Hecke eigenvalues λ_f(c)
2. Weil-type bounds for classical Kloosterman sums
3. Large sieve for GL₃

The key insight is that the GL₃ Voronoi transforms the GL₃ shifted
convolution into a sum involving classical (GL₂-level) arithmetic,
where standard tools apply.

### What DLY does NOT cover

DLY's f is a Hecke–Maaß cusp form on SL₃(ℤ) (spherical/infinite-
dimensional representation at infinity).

Our Π = sym²π where π is a **holomorphic** Hecke eigenform on
SL₂(ℤ). The symmetric-square lift to GL₃ gives a cuspidal automorphic
representation with **cohomological** archimedean component (finite-
dimensional at infinity).

The GL₃ Voronoi formula has a different archimedean factor for
cohomological vs. spherical representations. The gamma factors,
the spectral expansion, and the resulting bounds may differ.

## §3. The Kloosterman situation (corrected)

### Classical Kloosterman sums (GL₂-level)

| Bound | Source | Status |
|-------|--------|--------|
| \|S(m,n;c)\| ≤ d₃(c) · c^{1/2} | Weil (1948) | Classical [THM] |
| ∑_{c≤C} \|S(m,n;c)\|² / c ≪ C^{1+ε} | Kuznetsov/standard | Classical [THM] |

These are well-understood and used by DLY.

### GL₃ Kloosterman sums

| Bound | Source | Status |
|-------|--------|--------|
| \|S₃(m,n;c)\| ≪ c^{3/2+ε} | Trivial (size of sum) | Known [BASE] |
| \|S₃(m,n;c)\| ≪ c^{(n-1)/2+ε} (GL(n)) | Blomer–Man (2023) | [THM] |
| \|S₃(m,n;c)\| power-saving for Weyl elements | Larsen, Stevens, etc. | Various [THM] |

The GL₃ Kloosterman sums DO have non-trivial bounds beyond the
trivial c^{3/2+ε} for specific element types. The package's previous
claim of "only trivial bound" was incorrect.

However, the relevant Kloosterman sums for the DLY-type approach are
**classical** (GL₂-level) sums S(k̄, n; c), not GL₃ sums. The GL₃
Voronoi formula reduces the problem to classical arithmetic.

## §4. Why the holomorphic transfer is non-trivial

The DLY proof uses:

1. **GL₃ Voronoi formula**: the cohomological archimedean factor
   changes the gamma functions in the dual expression.

2. **Spectral expansion**: DLY expands over Maaß forms; the holomorphic
   case requires expanding over holomorphic forms (cohomological
   spectral theory, which is less developed).

3. **Weil bounds for classical Kloosterman sums**: these are
   arch-independent and should transfer directly.

4. **Large sieve for GL₃**: the GL₃ large sieve of Goldfeld–Kontorovich
   may need modification for the cohomological case.

The critical question is whether steps 1–2 can be adapted without
losing the power-saving bound from step 3.

## §5. Status of each sub-problem

### 09-A: Individual S_W(h, N; Π) ≪ N^{1-δ}

**Status:** [OBL]

No power-saving bound for individual fixed h ≍ N^{1/3} is known,
for any class of GL₃ forms. This is strictly stronger than what
DLY proves (which is averaged over h).

### 09-B: Averaged shifted convolution transfer to holomorphic Π

**Status:** [OBL]

The spherical/Maaß mechanism (DLY) is established. The transfer to
cohomological/holomorphic Π is open but well-defined:
- The classical Kloosterman bounds transfer (arch-independent)
- The GL₃ Voronoi archimedean factor needs adaptation
- The spectral expansion needs cohomological theory

## §6. Dependencies

This package depends on:
- **03-partial-sum-bound**: Friedlander–Iwaniec GL₂ bound (AFE input)
- **04-gl3-afe**: GL₃ AFE structure (provides N ≍ T^{3/2}, h ≍ T^{1/2})

This package is relevant to (but NOT a logical prerequisite for):
- **06-M-1-mollifier**: averaged power-saving would suffice
- **07-M-2-mean-value**: averaged power-saving would suffice

## Status: [OBL]

Both sub-problems are open research questions. 09-B is the more
approachable and directly relevant to the project.
