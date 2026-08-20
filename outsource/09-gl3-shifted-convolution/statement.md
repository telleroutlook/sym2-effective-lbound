# GL₃ Shifted Convolution — Statement

**Status:** [OBL] (two sub-problems, see below)

## Context

After expanding |L(½+it, Π)|² via the two-term AFE and integrating over
t ∈ [T, 2T], the off-diagonal contributions involve GL₃ shifted convolution
sums of the form

    S_W(h, N; Π) = Σ_n a_Π(n) ā_Π(n+h) W(n/N)

with smooth weight W, shift h, and summation length N.

From the degree-3 AFE structure: N ≍ T^{3/2}, and the natural shift scale
from the AFE length is h ≍ T^{1/2} = N^{1/3}.

The AFE expansion does NOT produce a single individual shifted sum; it
produces an **averaged** object:

    (T/N) · Σ_{h ≍ N/T} Σ_{n ≍ N} a_Π(n) ā_Π(n+h) W(n/N, h/(N/T))

This is the natural input for M-1 and M-2.

---

## Sub-problem 09-A: Individual shifted convolution [OBL]

**Question:** For fixed h ≍ N^{1/3}, does the individual smooth shifted sum

    S_W(h, N; Π) ≪_{Π,W,ε} N^{1-δ}

for some δ > 0?

**Note:** We do NOT presuppose a main term C_Π(h)·N. The Rankin–Selberg
L(s, Π × Π̃) controls the diagonal h = 0, not the shifted h ≠ 0 case.
Whether a main term exists for h ≠ 0 is itself an open question (it would
require analysis via the delta method or spectral expansion, not just
Rankin–Selberg).

**Status:** [OBL] — no power-saving bound for individual fixed h is known
at the critical scale h ≍ N^{1/3}.

---

## Sub-problem 09-B: Averaged shifted convolution — transfer to holomorphic Π [OBL]

**Question:** For Π = sym²π where π is a holomorphic Hecke eigenform of
weight k on SL₂(ℤ), can the DLY averaged shifted-convolution mechanism
be rigorously transferred?

### What DLY 2024 proved (Theorem 1.2)

For SL₃(ℤ) Hecke cusp forms (spherical/Maaß type):

    Σ_{n,k} λ_f(n) λ_f(n+k) W(n/N, k/H)
    ≪_{f,ε} N^{4/3+ε}/H^{1/3} + √H · N^{ε} + N^{1+ε}

This is **non-trivial** when H > N^{1/4}.

Our AFE gives H ≍ N^{1/3} > N^{1/4}, so the averaged problem already
admits non-trivial cancellation in the spherical/Maaß case.

### The transfer question

DLY's proof uses the GL₃ Voronoi formula + twisted classical Kloosterman
sums + Weil-type bounds. The archimedean place is handled via the
spherical/Maaß spectral theory.

For Π = sym²(holomorphic π), the infinity type is **cohomological**,
not spherical. The archimedean component of the Voronoi formula
involves different gamma factors and a different spectral decomposition.

**The precise research task:** Can the DLY averaged shifted-convolution
mechanism be adapted to the holomorphic symmetric-square case, accounting
for the different infinity type?

**Status:** [OBL] — the spherical/Maaß mechanism is established; the
holomorphic transfer is open.

---

## Relationship to M-1 and M-2

- M-1 (mollifier second moment) requires an averaged power-saving bound
  on the off-diagonal, which is exactly 09-B.
- M-2 (unmollified second moment) requires the same type of averaged bound.
- **09-B is NOT a necessary precondition in the logical sense** — it is a
  sufficient condition. The actual second-moment estimate may be achievable
  by other routes (e.g., direct moment methods without individual shifts).
- However, 09-B is the most natural and well-understood approach given
  current technology.
