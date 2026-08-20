# F-2 Global Residue Positivity — Outsource Package

**Obligation**: Global residue positivity for Rankin–Selberg convolution
**Status**: [OBL] (F-2A is [THM/REFEREED candidate], F-2B/C are [OBL])
**Restructured**: 2026-08-20 per independent review

## Restructuring

The original F-2 package contained a fundamental scaling contradiction and a
misreading of Jacquet–Shalika 1981. Per reviewer recommendation, F-2 is now
split into three sub-obligations:

### F-2A: Diagonal global residue positivity [THM/REFEREED candidate]

**Claim**: For unitary cuspidal π, same vector W, conjugate(W) ∈ W(π̃, ψ⁻¹),
Φ̂(0) > 0:

    Res_{s=1} Ψ(s, W, W, Φ) = c_Q · Φ̂(0) · |φ|² > 0

**Status**: Essentially a specialization of Jacquet–Shalika §4.2–4.6.
**Files**: `statement-F-2A.md`, `proof-F-2A.md`

### F-2B: Exact Euler-factor extraction [OBL]

**Claim**: The global integral factors as:

    Ψ(s) = L^S(s, π × π̃) · ∏_{v∈S} Z_v(s)

with L(s, π × π̃) = ζ(s) · L(s, π, Ad). All normalization explicit.

**Status**: The real technical obligation.
**Files**: `statement-F-2B.md`, `proof-F-2B.md`

### F-2C: Target-family local positivity/uniformity [OBL]

**Claim**: For the specific modular form family (fixed level, weight, nebentypus,
newvector normalization, Haar measures, archimedean vector, bad-prime type):

    Z_p(1) and Z_∞(1) computed explicitly; product bounded below uniformly.

**Status**: Interfaces with downstream (M-1, M-2, c_eff).
**Files**: `statement-F-2C.md`, `proof-F-2C.md`

## Key corrections from original F-2

1. **Integral formula**: W'(g)·conj(W(g)), NOT W̃(g)·W(g)
2. **Diagonal condition**: π' = π, NOT π̃ = π
3. **Residue source**: norm-square |φ|² > 0, NOT L(1, π, Ad) > 0
4. **Archimedean factor**: parameterized by weight k, NOT fixed at k=11
5. **Bad-place blocker**: existence of suitable local data, NOT arbitrary-data positivity

## Checker

```bash
python3 checker/check_global_residue.py <submission_dir>
```

Tests:
```bash
python3 -m pytest tests/ -v
```
