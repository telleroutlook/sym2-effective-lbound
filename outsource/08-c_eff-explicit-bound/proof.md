# c_eff: Explicit Lower Bound — Proof (v4, corrected per reviewer)

## Stage A — Normalization [THM]

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

## Stage B — GHL zero-free region [THM, constants OBL]

### The auxiliary series
Following GHL 1994 Appendix, define:

    φ(s) = ζ(s) · L(s, F)² · L(s, F × F)

where F × F denotes the Rankin–Selberg convolution of F with its
contragredient F̃. Since F is self-contragredient (sym² of a
self-dual GL₂ form), F̃ = F.

### Factorization
By the Rankin–Selberg identity for the symmetric-square lift:

    L(s, F × F) = L(s, F) · L(s, F, V²)

where V² denotes the symmetric-square L-series of F (the symmetric
part of the tensor square of the standard representation of GL₃).
This gives:

    φ(s) = ζ(s) · L(s, F)³ · L(s, F, V²)

### Pole structure at s = 1
- ζ(s) has a simple pole at s = 1 (residue = 1)
- L(s, F, V²) has a simple pole at s = 1 when f is non-dihedral
  (this is the key non-degeneracy condition)
- L(s, F) is holomorphic at s = 1 (cuspidal Π has no pole)

**Crucial prerequisite**: The double-pole argument also requires L(1, F) ≠ 0.
If L(s, F) had a zero at s = 1, then L(s, F)³ would cancel the pole
of L(s, F, V²), reducing the order of the pole. Hoffstein–Lockhart (1994)
explicitly establishes L(1, F) ≠ 0 for cuspidal F = sym²f with f
non-CM/non-dihedral (this follows from the non-vanishing of L(1, sym²f)
proved by Jacquet–Shalika and standard GL₃ boundary non-vanishing).

Therefore, with L(1, F) ≠ 0 confirmed, φ(s) has a **double pole** at s = 1.

### Non-negative Dirichlet coefficients of φ
GHL explicitly establishes that φ has non-negative Dirichlet
coefficients. This is a crucial property for the zero-count argument.

**For prime level + trivial central character** (the scope of this package):
At each good prime q, the local factor of A(s) = ζ(s)L(s,F) is:

    A_q(s) = (1−q^{−s})⁻¹ · L_q(s, F)
            = (1−α_q²q^{−s})⁻¹ (1−q^{−s})⁻² (1−β_q²q^{−s})⁻¹

This has positive Dirichlet coefficients (expand each factor as a geometric
series in q^{−s}; all coefficients are positive since |α_q|, |β_q| ≤ 1).

At the bad prime p: A_p(s) = (1−p^{−s})⁻¹(1−p^{−s−1})⁻¹, also with
positive coefficients.

By multiplicativity, the full Dirichlet series ζ(s)L(s,F) has non-negative
coefficients. (Note: the previous version incorrectly stated the good-prime
local factor as (1−q^{−s})⁻¹(1−q^{−s−1})⁻¹ — this is the bad-prime factor.
The correct good-prime factor is the four-factor expression above.)

**For general level**: GHL establishes positivity of φ's coefficients
in full generality, including non-prime level. The argument is, as GHL
notes, "somewhat more subtle" in that case. We take this from GHL without
reproducing the full verification.

### Zero-count argument (GHL)
Suppose for contradiction that L(β, F) = 0 for some real β with

    1 − c_ZF/log K < β < 1

where K = kp + 1 and c_ZF > 0 is the GHL zero-free region constant.
Then L(s, F)³ contributes a **triple zero** at s = β to φ(s).
But GHL's zero-count lemma says: a function with a double pole at s = 1,
non-negative Dirichlet coefficients, and polynomial growth, can have at
most 2 real zeros near 1 (counting multiplicity).

A triple zero at β would exceed this bound. Contradiction.

### Result
    L(s, F) ≠ 0  for  1 − c_ZF/log K < s < 1

where c_ZF > 0 is an **absolute effective constant** (independent of k
and p), determined by the GHL zero-count lemma parameters.

---

## Stage C — Hoffstein–Lockhart lower bound [THM, constants OBL]

### The HL function
Consider:

    A(s) = ζ(s) · L(s, F)

Properties:
1. Dirichlet coefficients a_n ≥ 0: verified in Stage B above
   (local factors at good and bad primes all have positive coefficients;
   multiplicativity gives non-negativity of the full series)
2. Simple pole at s = 1 with residue:
   Res_{s=1} A(s) = L(1, F)
3. Polynomial growth in vertical strips (from Gamma factors)
4. No real zero in (1 − c_ZF/log K, 1) — from Stage B

### Growth bound
From the functional equation and Stirling, there exist absolute
effective constants C_* > 0, A_0, B > 0 such that:

    |A(1/2 + it)| ≤ C_* · K^{A_0} · (1 + |t|)^B

for all t ∈ R. Here K = kp + 1.

**The multiplicative constant C_* is essential for numerical extraction.**
In the existence proof, C_* can be absorbed into A_0 (since K ≥ 5, we can
take A_0' = A_0 + log C_*/log 5). But for explicit computation, C_* must
be tracked as a separate parameter. All ≪ bounds must eventually be
converted to explicit inequalities with known constants.

### Application of HL Proposition 1.1
Hoffstein–Lockhart (1994), Proposition 1.1 states:

If A(s) has non-negative coefficients, a simple pole at s = 1 with
residue R, satisfies |A(1/2+it)| ≤ M^A · (1+|t|)^B for some A, and
has no real zero in (1 − 1/log M, 1), then:

    R⁻¹ ≤ c(B) · log M

for an absolute effective constant c(B) > 0 depending only on the
growth exponent B.

**Parameter matching**: We must choose M so that:
- (a) Growth: C_* · K^{A_0} ≤ M^A (1+|t|)^B is satisfied
- (b) Zero-free: 1 − 1/log M falls within the GHL zero-free region

Set M = K^C where C ≥ max(A_0 + log C_*/log 5, c_ZF⁻¹) is an absolute
constant. (The C_* term accounts for the growth multiplicative constant.)
Then:
- Growth: C_* · K^{A_0} ≤ K^{C} · K^{A_0} ≤ K^{C+A_0} ... [requires careful
  tracking; the key point is that C_* can be absorbed into the choice of C]
- Zero-free: 1/log M = 1/(C log K) ≤ c_ZF/log K, so the interval
  (1 − 1/log M, 1) is contained in (1 − c_ZF/log K, 1).
  Thus (b) is satisfied.

### Result
Applying HL Proposition 1.1 with M = K^C:

    L(1, F)⁻¹ = R⁻¹ ≤ c(B) · log M = c(B) · C · log K

Therefore:

    L(1, sym² f) = L(1, F) ≥ 1/(c(B) · C) · 1/log(kp + 1)

Setting c_eff = 1/(c(B) · C) > 0:

    L(1, sym² f) ≥ c_eff / log(kp + 1)

### Role separation
- **Stage B** (GHL): establishes c_ZF (absolute) zero-free region
- **Stage C** (HL Prop 1.1): converts growth + zero-free into L(1) lower bound
- **M = K^C**: absolute constant C matches the two; NOT a Dirichlet coefficient bound

These are three distinct steps that must not be conflated.

---

## Stage D — Numerical constant extraction [OBL]

### What needs to be computed
The constant c_eff = 1/(c(B) · C) depends on:

1. **GHL zero-free region constant c_ZF**: from the zero-count lemma,
   depends on Gamma function derivatives and the GHL parameters.
   This is an absolute effective constant.

2. **Growth multiplicative constant C_***: from the functional equation
   and Stirling's formula for |A(1/2+it)| ≤ C_* K^{A_0}(1+|t|)^B.
   Absolute effective. Must be explicitly tracked.

3. **Growth exponents A_0, B**: from the functional equation and
   Stirling's formula. Absolute effective.

4. **Matching constant C**: any C ≥ max(A_0 + log C_*/log 5, c_ZF⁻¹) works.
   The optimal choice is C = max(A_0 + log C_*/log 5, c_ZF⁻¹).

5. **HL implied constant c(B)**: from the contour integral
   representation in HL Proposition 1.1. Depends on B.
   Absolute effective.

### Named constants (complete list)
- c_ZF: GHL zero-free region constant (absolute)
- C_*: growth multiplicative constant (absolute)
- A_0, B: growth exponents (absolute)
- C = max(A_0 + log C_*/log 5, c_ZF⁻¹): matching constant (absolute)
- c(B): HL implied constant (absolute)
- c_eff = 1/(c(B) · C): final effective constant

### Status: [OBL]
None of these absolute constants have been numerically computed.
The infimum inf_{k,p} c_eff is automatically bounded below by
1/(c(B) · C) since all quantities are absolute — no separate
infimum argument is needed.

---

## Status: [OBL]

The main remaining tasks are:
1. Compute c_ZF from GHL zero-count lemma (Stage B)
2. Compute C_*, A_0, B from functional equation (Stage C)
3. Compute c(B) from HL contour integral (Stage C)
4. Set C = max(A_0 + log C_*/log 5, c_ZF⁻¹) and c_eff = 1/(c(B)·C)
5. Certified interval [a,b] with a > 0 using Arb/python-flint
