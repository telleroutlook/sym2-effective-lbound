# c_eff: Explicit Lower Bound — Proof

## Stage 1: Normalization and conductor

### Form setup
Let f ∈ S_k^new(Γ₀(p)) be a normalized Hecke eigenform (a_f(1) = 1).
The symmetric-square lift Π = sym²π_f is a degree-3 automorphic representation
of GL₃(A_Q).

### Euler factors
For q ≠ p (good prime):
    L_q(s, Π) = (1 − α_f(q)² q^{-s})^{-1} (1 − q^{-s})^{-1} (1 − β_f(q)² q^{-s})^{-1}
where α_f(q), β_f(q) are Satake parameters of π_f at q, with α_f(q) β_f(q) = 1.

For q = p (bad prime, Steinberg type):
    L_p(s, Π) = (1 − p^{-s-1})^{-1} (Iwaniec–Michel 2001 normalization)

### Conductors
- Arithmetic conductor: q_ar(Π) = p²
- Analytic conductor: q_an(Π, T) = p² · max(1, T)³ approximately
  (the exact formula involves the archimedean parameters)

### Completed L-function
    Λ(s, Π) = L_∞(s) · L(s, Π)

with (Iwaniec–Michel 2001):

    L_∞(s) = π^{-3s/2} Γ((s+1)/2) Γ((s+k-1)/2) Γ((s+k)/2)

## Stage 2: Zero-free region

### For Δ (k=12, p=1): already proved
    L(s, sym²Δ) ≠ 0 for σ ∈ [0.6, 1.0], |t| ≤ 20

### For general (k, p): use existing results
The symmetric-square L-function inherits zero-free regions from:
- The GL₂ form f itself (via Rankin–Selberg)
- Direct symmetric-square zero-free results in the literature

The key parameter is σ₀ = 1 − c₃/log(kp+1) for some explicit c₃ > 0.

The special structure of sym² (from GL₂) gives stronger zero-free results
than what is available for general GL₃ automorphic representations.

## Stage 3: Hoffstein–Lockhart residue proposition

### The auxiliary Dirichlet series
Following GHL 1994, construct:

    Φ(s) = ζ(s) · L(s, Π)² · L(s, Π × Π̃)

This has non-negative Dirichlet coefficients (in the relevant range).

### Key observation: prime level + trivial character
For p prime and trivial central character:
- Π = sym²π_f is NOT a monomial / GL(1)-lift (since f is non-CM)
- The auxiliary series Φ(s) has a pole of order 2 at s = 1 (from ζ(s) and L(s,Π)²)
- There is NO additional zero from a GL(1)-lift factor

Therefore: the exceptional/monomial branch DOES NOT ARISE in this scope.

### The generic branch only
By HL Proposition 1.1 (specialized):
- Φ(s) has a pole of order 2 at s = 1
- L(s, Π) has at most a simple pole at s = 1 (actually none for cuspidal Π)
- If L(s, Π) had a real zero β near 1, then L(s, Π)² would contribute a
  double zero, making Φ(s) have order ≥ 3 zero minus order 2 pole = net zero
  at s = 1, contradicting the residue computation

This gives: L(s, Π) has no real zero in [1 − c₀/log(kp+1), 1].

### Deducing L(1) > 0
From the zero-free region + Hadamard factorization + explicit residue:

    L(1, Π) ≥ c₁ / log(kp + 1)

where c₁ depends on:
- The residue of ζ(s) L(s,Π)² L(s,Π×Π̃) at s = 1
- The zero-free region parameter σ₀
- The gamma factor constants
- The bad Euler factor at p

## Stage 4: Explicit constant extraction

### What needs to be computed
1. Residue of ζ(s) L(s,Π)² L(s,Π×Π̃) at s = 1:
   = Res_{s=1} ζ(s) · L(1,Π)² · L(1,Π×Π̃) (if L(1,Π) ≠ 0)
   = 1 · L(1,Π)² · L(1,Π×Π̃)

2. Zero-free region: σ₀ = 1 − c₃/log(kp+1) with explicit c₃

3. Gamma factor ratio at s = 1 vs s = σ₀

4. Bad Euler factor at p: L_p(1, Π) = (1 − p^{-2})^{-1}

### The final constant
    c_* = f(c₁, σ₀, gamma ratios, bad factors)

with inf_{k≥2, p prime} c_* > 0.

## Stage 5: Interval certification

### Arb/python-flint computation
For each target (k, p):
1. Compute all input constants to rigorous precision
2. Use outward rounding to get certified interval [a, b]
3. Verify a > 0

### Machine-readable witness
Output:
    c_* ∈ [a, b],  a > 0,  width < ε
with SHA-256 of inputs and replay script.

## Status: [OBL]

The main tasks are:
1. Verify prime + trivial char eliminates GL(1)-lift (Stage 3)
2. Trace HL computation with all constants explicit (Stage 4)
3. Compute interval using Arb (Stage 5)
