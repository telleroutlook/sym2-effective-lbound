# Problem OB-02 — Certified AFE dual term J for L(1, sym²Δ)

**Type:** Automorphic L-functions / explicit computation (GL₃ AFE)
**Status:** [OBL] — all results below are obligations, not theorems.

**Non-circularity:** The abc conjecture, IUT, Szpiro, and any fitted parameter
are not used. The result concerns a specific integral identity for the
Ramanujan Δ function's symmetric-square L-function.

---

## Definitions (self-contained)

### 1. Symmetric-square L-function of Δ

Let τ(n) denote Ramanujan's tau function. Define:

    A(1) = 1,  A(2) = τ(2)² / 2^{11} − 1 = −23/32

and multiplicatively at every prime p:

    A(p^k)  via the GL(3) Satake recurrence with parameters
    α_p = τ(p) / p^{11/2},  β_p = 1/α_p  (|α_p| = 1 by Ramanujan–Petersson)

The L-function:

    L(s) = Σ_{n≥1} A(n) n^{-s}  =  L(s, sym²Δ)

### 2. Gamma factors

[DEF] The completed L-function uses:

    Γ_R(s) = π^{-s/2} Γ(s/2)
    Γ_C(s) = 2 (2π)^{-s} Γ(s)
    G(s) = Γ_R(s) × Γ_C(s+11)

### 3. AFE weight function

[DEF] For the approximate functional equation at s₀ = 1:

    A(t) = G(1/2+it) / G(1)
           × 12^{-1/2+it}
           × exp((−1/2+it)²) / (−1/2+it)

The Gaussian factor e^{s²} provides super-exponential decay: |A(t)| ≤
C × e^{−t²/4} for large |t|.

### 4. The GL₃ AFE identity

[DEF] The approximate functional equation for L(1, sym²Δ) at X = √Q = √12:

    L(1) = S1 − J

where the main sum:

    S1 = Σ_{n≥1} A(n)/n × W(n/12)

with W(y) = (1/2π) ∫ Re[A(t) × y^{−1/2+it}] dt, and the dual/contour term:

    J = (1/2π) ∫_{−∞}^{∞} Re[L(1/2+it) × A(t)] dt

### 5. Certified infinite S1

[THM] (proved in `src/afe_s1_full.py`, verified by `checker/check_s1_full.py`)

For N = 20000, T = 8, M = 200000, precision = 128:

    S1 ∈ [0.548298, 0.548305]     (width ≈ 7.0 × 10⁻⁶)

This certifies the infinite main sum S1 (all n ≥ 1). It does NOT certify
the dual term J or L(1).

### 6. The dual term J — known values (discovery tier)

Numerical estimates (NOT certified):

    J ≈ −0.083    (from Cesàro averaging and direct double integration)
    L(1) = S1 − J ≈ 0.631793     (consistent across 3 independent methods)

### 7. The obstacle

The integral J = (1/2π) ∫ Re[L(1/2+it) × A(t)] dt involves L(1/2+it) on
the critical line, where L(s, sym²Δ) does NOT converge absolutely. The
Cesàro-truncated Dirichlet series L_ces(N, 1/2+it) converges conditionally;
the truncation error requires either:

(a) GL₃ Voronoi summation (Task V / OB-01) to bound the partial sums
    |Σ_{n≤X} A(n) n^{-1/2-it}| ≤ C_GL3 × X^{2/3}, or

(b) An explicit zero-free region for L(s, sym²Δ) in {Re(s) ≥ 0.9}
    (the [OBL M-3] path, partially explored in discovery/).

---

## Theorem (to be proved)

**[OBL]** Produce a certificate `J ∈ [J_lo, J_hi]` with width at most 10⁻⁶,
together with a proof of the identity and every tail bound used.

From this and the certified S1 ∈ [0.548298, 0.548305], derive:

    L(1, sym²Δ) = S1 − J ∈ [L_lo, L_hi]

with explicit certified bounds.

---

## Acceptable routes

A submission may use any fully proved route, including:

1. **Voronoi route:** Derive an absolutely convergent dual Dirichlet series from
   Miller–Schmid Theorem 1.18 and bound its tail with Arb. Requires OB-01
   (C_GL3 bound) to be completed first.

2. **Zero-free region route:** Prove a sufficiently explicit numerical
   zero-free region for L(s, sym²Δ) in {Re(s) ≥ 0.9, |Im(s)| ≤ T_max},
   then integrate with certified interval arithmetic via Abel summation.

3. **Alternative route:** Supply another rigorous functional-equation or
   modular-identity argument that gives an absolutely convergent or otherwise
   rigorously controlled expression for J.

Route selection is part of the task. The final proof must make clear why the
conditionally convergent critical-strip object has been replaced by an
absolutely convergent or otherwise rigorously controlled quantity.

---

## Numerical anchor

| Quantity | Value | Source |
|---|---|---|
| S1 (certified) | [0.548298, 0.548305] | `src/afe_s1_full.py`, N=20000, T=8 |
| J (discovery) | ≈ −0.083 | Cesàro averaging, direct integration |
| L(1) (discovery) | ≈ 0.631793 | S1 − J, three independent methods |
| min\|L_ces(0.9+it)\| | 0.392596 at t=110.020 | N=10⁸ scan |
| C_GL3 empirical | 0.001611 | N=10⁸ peak value |
| C_GL3 threshold (σ=0.9) | 7.488 | Zero-free region certification |
| Q_GL3^{1/3} | 6.930 | Analytic conductor bound |
| G(1) | Γ_R(1) × Γ_C(12) | Gamma factors at s=1 |

---

## Explicitly forbidden

1. Cesàro averaging, numpy/mpmath floats, or convergence tables as proof.
2. Interchanging a limit/integral without a dominated convergence argument.
3. Using an empirical zero-free scan or the absence of observed zeros as proof.
4. Claiming J or L(1) from the finite certificate `src/afe_s1_arb.py`:
   that file certifies only S1[N,T].
5. Using [OBL M-3] or Task V (OB-01) as if it were already proved.
6. Using `src/afe_s1_full.py` output as a bound on J: that file certifies
   only the infinite main sum S1, not the dual term.
7. Self-declaring J without running `checker/check_certified_j.py`.
8. Assuming GRH or any unproved hypothesis about zeros of L(s, sym²Δ).

---

## Required certificate fields

The JSON certificate must identify:

1. The mathematical route (Voronoi / zero-free region / alternative).
2. The exact test functions and normalisation.
3. Arb precision and all interval endpoints.
4. Every truncation length (N for Dirichlet sum, T for vertical integral, etc.).
5. An explicit proof-level tail bound for each truncated sum/integral.
6. A false `certifies_l1` field unless an independently certified S1 tail
   is also supplied.
7. A SHA-256 checksum for any exact integer coefficient vector.

---

## Acceptance criteria

Provide:

1. A complete mathematical PDF or LaTeX derivation.
2. Interval-arithmetic code (python-flint / Arb) reproducing every numerical
   constant.
3. An independent checker (`checker/check_certified_j.py`) that:
   - Does NOT import `src/`
   - Verifies the identity J = (1/2π) ∫ Re[L(1/2+it) A(t)] dt
   - Recomputes the tail bounds from stated truncation lengths
   - Rejects if `certifies_l1` is true without certified S1
4. Tamper tests: checker must reject after changing any endpoint by 1 ULP.
5. Commands:

```bash
pytest tests/test_certified_j.py -q
python checker/check_certified_j.py certificates/j_sym2_delta.json
ruff check src/ checker/ tests/
```

The reviewer will additionally run the repository-wide test suite and inspect
the source-level citation ledger before accepting the result.
