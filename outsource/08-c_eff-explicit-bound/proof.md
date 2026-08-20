# c_eff: Explicit Lower Bound — Proof (v2, corrected)

## Stage A — Normalization

### Form setup
Let f ∈ S_k^new(Γ₀(p)) be a normalized Hecke eigenform (a_f(1) = 1).
The symmetric-square lift F = sym²π_f is a cuspidal automorphic
representation of GL₃(A_Q), since f is non-dihedral.

### Euler factors
For q ≠ p (good prime):
    L_q(s, F) = (1 − α_f(q)² q^{−s})⁻¹ (1 − q^{−s})⁻¹ (1 − β_f(q)² q^{−s})⁻¹
where α_f(q) β_f(q) = 1 (Ramanujan bound gives |α_f(q)| ≤ 1).

For q = p (bad prime, Steinberg type):
    L_p(s, F) = (1 − p^{−s−1})⁻¹
(Iwaniec–Michel 2001, §3 normalization.)

### Conductors
Arithmetic conductor: q_ar(F) = p².
(This follows from the conductor formula for sym² of a newform of prime level p.)

### Completed L-function
    Λ(s, F) = p^s · L_∞(s) · L(s, F)

with Iwaniec–Michel (2001) archimedean factor:

    L_∞(s) = π^{−3s/2} Γ((s+1)/2) Γ((s+k−1)/2) Γ((s+k)/2)

Note the factor p^s = (p²)^{s/2} = q_ar^{s/2}. The functional equation is:

    Λ(s, F) = Λ(1 − s, F)

### Analytic conductor
The archimedean shifts are approximately 1, k−1, k. At t = 0:

    Q_an(F, 0) ≍ p² · (1+1) · (1+k−1) · (1+k) ≍ p² k²

More generally:

    Q_an(F, t) ≍ p² (1 + |t|)(k + |t|)²

For |t| ≫ k this reduces to p² |t|³.

---

## Stage B — GHL generic zero-free region

### The auxiliary series
Following GHL 1994 Appendix, define:

    φ(s) = ζ(s) · L(s, F)² · L(s, F × F)

where F × F denotes the Rankin–Selberg convolution of F with its
contragredient F̃. Since F is self-contragredient (sym² of a
self-dual GL₂ form), F̃ = F.

### Factorization
By the Rankin–Selberg identity for the symmetric-square lift:

    L(s, F × F) = L(s, F) · L(s, F, V²)

where V² is the symmetric part of the exterior square ⊗² minus the
symmetric square. This gives:

    φ(s) = ζ(s) · L(s, F)³ · L(s, F, V²)

### Pole structure at s = 1
- ζ(s) has a simple pole at s = 1 (residue = 1)
- L(s, F, V²) has a simple pole at s = 1 when f is non-dihedral
  (this is the key non-degeneracy condition)
- L(s, F) is holomorphic at s = 1 (cuspidal Π has no pole)

Therefore φ(s) has a **double pole** at s = 1.

### Zero-count argument (GHL)
Suppose for contradiction that L(β, F) = 0 for some real β with

    1 − c₀/log(kp+1) < β < 1.

Then L(s, F)³ contributes a **triple zero** at s = β to φ(s).
But GHL's zero-count lemma says: a function with a double pole at s = 1,
non-negative Dirichlet coefficients, and polynomial growth, can have at
most 2 real zeros near 1 (counting multiplicity).

A triple zero at β would exceed this bound. Contradiction.

### Result
    L(s, F) ≠ 0  for  1 − c₀/log(kp+1) < s < 1

for an explicit constant c₀ > 0 depending on k and the explicit
parameters in the GHL zero-count lemma.

---

## Stage C — Hoffstein–Lockhart lower bound

### The HL function
Consider:

    A(s) = ζ(s) · L(s, F)

Properties:
1. Dirichlet coefficients a_n ≥ 0 (product of ζ and L with non-negative
   coefficients — follows from Hecke multiplicativity and positivity of
   symmetric-square coefficients)
2. Simple pole at s = 1 with residue:
   Res_{s=1} A(s) = L(1, F)
3. Polynomial growth in vertical strips (from Gamma factors)
4. No real zero in (1 − c₀/log(kp+1), 1) — from Stage B

### Application of HL Proposition 1.1
Hoffstein–Lockhart (1994), Proposition 1.1 states:
If A(s) has non-negative coefficients, a simple pole at s = 1 with
residue R, satisfies appropriate growth conditions, and has no real zero
in (1 − δ, 1), then:

    R⁻¹ ≪ log(1/δ)

Applied with δ = c₀/log(kp+1):

    L(1, F)⁻¹ ≪ log(kp+1)

Therefore:

    L(1, sym² f) = L(1, F) ≥ c₁ / log(kp+1)

where c₁ = 1/C for the implied constant C in the HL bound.

### Role separation
- **Stage B** (GHL): establishes the zero-free region (no real zero near 1)
- **Stage C** (HL Prop 1.1): converts zero-free region into L(1) lower bound

These are two distinct steps that must not be conflated.

---

## Stage D — Numerical constant extraction [OBL]

### What needs to be computed
The constant c₁ in Stage C depends on:

1. **GHL zero-free region constant c₀**: from the zero-count lemma,
   depends on Gamma function derivatives, Dirichlet series coefficients
   bound M = 1 + D · max|c_n|, and conductor D.

2. **HL Proposition 1.1 implied constant C**: from the contour integral
   representation, depends on:
   - The growth parameter B in |A(s)| ≪ |t|^B
   - The contour shift distance r (related to c₀)
   - The Dirichlet series coefficient bound M

3. **Explicit A(s) = ζ(s)L(s,F) at s = 1**: the residue is L(1,F)
   itself, so the constant extraction is bootstrapped — we get an
   inequality, not an equation.

4. **Bad Euler factor**: L_p(1, F) = (1 − p^{−2})⁻¹ ≤ p²/(p²−1)

### The final task
Show inf_{k≥2, p prime} c₁(k,p) > 0 and compute a certified
interval [a, b] with a > 0 containing this infimum (or a useful
lower bound for it).

This requires:
- Explicit bounds on Gamma derivatives at the relevant points
- Explicit M (Dirichlet coefficient bound) in terms of kp
- Explicit B (growth exponent) from the functional equation
- Contour integral estimation with explicit constants
- Arb/python-flint interval arithmetic with outward rounding

### Status: [OBL]
None of these explicit constants have been computed.

---

## Status: [OBL]

The main remaining tasks are:
1. Trace all implied constants in GHL zero-count lemma (Stage B constants)
2. Trace all implied constants in HL Proposition 1.1 (Stage C constants)
3. Combine to get explicit c₁(k,p) > 0
4. Show inf_{k,p} c₁ > 0
5. Compute interval [a,b] with a > 0 using Arb
