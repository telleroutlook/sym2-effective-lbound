# Problem OB-01 — Explicit C_GL3 from Miller–Schmid Theorem 1.18

**Type:** Automorphic L-functions / analytic number theory (GL₃ Voronoi)
**Status:** [OBL] — all results below are obligations, not theorems.

**Non-circularity:** The abc conjecture, IUT Corollary 3.12, Szpiro's
conjecture, and any fitted parameter K_ε are not used or assumed. The result
concerns an explicit spectral/exponential-sum constant for GL₃ Voronoi summation.

---

## Definitions (self-contained)

### 1. Setup

Let Δ(z) = q^{1/2} Σ_{n≥1} τ(n) e^{2πinz} be the weight-12 cusp form for
SL₂(ℤ), with Ramanujan tau function τ(n). The symmetric-square L-function is:

    L(s, sym²Δ) = Σ_{n≥1} A(n) n^{-s}

where A(1) = 1, and A is multiplicative with at each prime p:

    A(p) = τ(p)² / p^{11} − 1

### 2. Analytic conductor

The spectral parameters are ν = (11, 0, −11)/2 = (11/2, 0, −11/2). The
analytic conductor is:

    Q_GL3 = Π_{i<j} |ν_i − ν_j| = (11/2)² × 11 = 1331/4 = 332.75

### 3. Partial sum of symmetric-square coefficients

Define the partial sum:

    S(X) = Σ_{n≤X} A(n)

The GL₃ Voronoi summation gives the bound:

    |S(X)| ≤ C_GL3 × X^{2/3+ε}     for all X ≥ 1

where C_GL3 is an explicit constant depending on the GL₃ spectral data,
Kloosterman sum bounds, and GL₃ Bessel kernel norms.

### 4. The Miller–Schmid GL₃ Voronoi formula

[BASE] (Miller–Schmid, *Automorphic distributions, L-functions, and Voronoi
summation for GL(3)*, Ann. of Math. (2) **164** (2006), 423–488,
Theorem 1.18, pp. 427–428.)

For cuspidal GL(3,ℤ) Fourier coefficients a_{q,n}, representation parameters
(λ, δ), (a,c) = 1, c ≠ 0, and a Schwartz function φ vanishing to infinite
order at the origin:

    Σ_{n≠0} a_{q,n} e(−na/c) φ(n)
      = Σ_{d|cq} |c/d|
          Σ_{n≠0} A(n,d)/|n|
          S(q·ā, n; q·c/d)
          F(n·d²/(c³·q))

where:
- |c/d| is the normalisation factor (d | cq)
- A(n,d)/|n| are the GL₃ Fourier coefficient normalisation
- S(q·ā, n; q·c/d) is the Kloosterman sum of modulus qc/d
- F(nd²/(c³q)) is the normalized GL₃ Bessel transform

### 5. Kloosterman sum bound

[BASE] (Weil bound for GL₃ Kloosterman sums.) For modulus m ≥ 1:

    |S(a, b; m)| ≤ d₃(m) × m^{1/2}

where d₃(m) = Σ_{d₁d₂d₃=m} 1 is the trifold divisor function.

### 6. GL₃ Bessel kernel

For spectral parameter ν = (ν₁, ν₂, ν₃) with ν₁ + ν₂ + ν₃ = 0, the GL₃
Bessel kernel K_ν(y) is an oscillatory function with:

    ||K_ν||_{L¹(0,∞)} ≤ 0.225    (conservative upper bound, Arb-certified)
    ||K_ν||_{L¹(0,∞)} ≈ 0.1995   (Mellin恒等式, 60-bit precision)

The Mellin identity: K̂_ν(1) = (4π²)^{-1} × Γ(13/4) × Γ(1/2) × Γ(−9/4) ≈ −0.1995.

### 7. Rankin–Selberg density

[DEF] The Rankin–Selberg normalisation constant:

    C_RS = lim_{N→∞} (1/N) × Σ_{n≤N} |A(n)|² ≈ 0.4433

Numerical anchor: C_RS = 0.4433 (N=10³..10⁵, δ < 10⁻³).

---

## Theorem (to be proved)

**[OBL]** For the Ramanujan Δ function (weight 12, level 1), prove an explicit
constant C_GL3 such that for all X ≥ 1:

    |Σ_{n≤X} A(n)| ≤ C_GL3 × X^{2/3}

with C_GL3 < 7.488 (the threshold for σ = 0.9, N = 10⁸ zero-free region
certification).

**Desired bound:** C_GL3 ≤ Q_GL3^{1/3} = 6.930 (the theoretical target from
the analytic conductor).

---

## Proof skeleton (sketch — fill in gaps)

1. Start from Miller–Schmid Theorem 1.18 with the exact normalisation:
   |c/d|, A(n,d)/|n|, modulus qc/d, argument nd²/(c³q).

2. Apply the smooth test-function φ(x) = (sin πx/(πx))² (or a smoothed variant)
   to convert the Voronoi identity into a bound on S(X).

3. On the dual side, bound the Kloosterman sums via Weil: |S(a,b;m)| ≤ d₃(m) m^{1/2}.

4. Sum over d | cq using the Rankin–Selberg density: Σ_{d≤Y} d₃(d)²/d ~ C_RS × log Y + ...

5. Bound the GL₃ Bessel kernel: ||K_ν||₁ ≤ 0.225 (conservative) or 0.1995 (Mellin).

6. Combine: C_GL3 ≤ 2 × ||K_ν||₁ × ζ(3/2) ≈ 1.042 (Mellin) or 1.176 (conservative).

7. Verify C_GL3 < 7.488 (certification threshold) and < Q_GL3^{1/3} = 6.930.

---

## Numerical anchor

| Quantity | Value | Source |
|---|---|---|
| Q_GL3 | 332.75 = (11/2)² × 11 | Spectral parameters of sym²Δ |
| Q_GL3^{1/3} | 6.930 | Cube root of Q_GL3 |
| Certification threshold (σ=0.9, N=10⁸) | 7.488 | From `discovery/_conditional_cert.py` |
| \|\|K_ν\|\|₁ (conservative) | 0.225 | Dense grid + 15% margin, Arb |
| \|\|K_ν\|\|₁ (Mellin) | 0.1995 | Mellin identity, 60-bit precision |
| C_RS | 0.4433 | N=10³..10⁵ numerical scan |
| C_GL3 (L1+ζ(3/2), Mellin) | 1.042 | 2 × 0.1995 × ζ(3/2) |
| C_GL3 (L1+ζ(3/2), conservative) | 1.176 | 2 × 0.225 × ζ(3/2) |
| C_GL3 (L2+√C_RS+ζ(7/6)) | 2.74 | 2 × √0.4433 × ||K||₂ × ζ(7/6) |
| C_GL3 empirical (N=10⁸) | 0.001611 | `discovery/_n10m8_dc_scan.py` |

---

## Explicitly forbidden

1. Replacing Miller–Schmid Theorem 1.18 by a generic c⁻²K_ν(...) expression.
2. Reporting the empirical C_GL3 = 0.001611 from a finite scan as a proof.
3. Using the threshold 7.488 or margin over it as proof.
4. Silently dropping the d | cq, c, or n tails in the Voronoi sum.
5. Treating the self-dual q=c=1 identity as a cancellation estimate.
6. Assuming [OBL F-2] (global residue positivity) in any step.
7. Using mpmath or float as certified arithmetic (only Arb/python-flint).

---

## Acceptance criteria

Provide:

1. A complete mathematical PDF or LaTeX derivation starting from
   Miller–Schmid Theorem 1.18 with exact normalisation.
2. Interval-arithmetic code (python-flint / Arb) reproducing every numerical
   constant (||K_ν||₁, C_GL3, thresholds).
3. An independent checker (`checker/check_cgl3.py`) that:
   - Does NOT import `src/`
   - Recomputes ||K_ν||₁ from the Mellin identity
   - Recomputes ζ(3/2) and the combination 2 × ||K_ν||₁ × ζ(3/2)
   - Rejects if the claimed C_GL3 ≥ 7.488
4. Tamper tests: the checker must reject after changing any constant by 1 ULP.
5. Commands:

```bash
pytest tests/test_cgl3.py -q
python checker/check_cgl3.py <certificate.json>
ruff check src/ checker/ tests/
```

The reviewer will additionally run the repository-wide test suite and inspect
the source-level citation ledger (baseline/REFERENCE_BASELINE.md) before
accepting the result.
