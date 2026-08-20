# F-2B: Exact Euler-Factor Extraction — Proof

## Mathematical content

The goal is the exact euler factor extraction for the global Rankin–Selberg integral.

### Factorization of the global integral

The global Rankin–Selberg integral Ψ(s, W, W, Φ) unfolds to a product of local
integrals by the strong approximation theorem and the factorization of the Whittaker
function:

    Ψ(s, W, W, Φ) = ∏_v Ψ_v(s, W_v, W_v, Φ_v)

Each local integral Ψ_v(s, W_v, W_v, Φ_v) is computed separately.

### Unramified places (good primes)

For p ∤ N, the local integral at p is:

    Ψ_p(s, W_p, W_p, Φ_p) = L_p(s, π_p × π̃_p)

This is the standard Godement–Jacquet local zeta integral. For unramified π_p
with Satake parameters α_p, β_p:

    L_p(s, π_p × π̃_p) = (1 − α_p β̄_p p^{−s})^{−1} (1 − ᾱ_p β_p p^{−s})^{−1} (1 − |α_p|² p^{−s})^{−1} (1 − |β_p|² p^{−s})^{−1}

For trivial central character (|α_p β_p| = 1), this simplifies to:

    ζ_p(s) · L_p(s, π, Ad)

### Ramified places (bad primes)

For p | N, the local integral depends on the local newvector. The computation
requires:
- The local Whittaker function W_p on GL₂(Q_p)
- The local Haar measure normalization
- The local test function Φ_p

### Archimedean place

For the archimedean integral Ψ_∞, the result depends on the archimedean representation:
- Holomorphic discrete series of weight k: involves Γ_R(s+1)·Γ_C(s+k−1)
- Maass form: involves different Gamma factors

**Key point**: The archimedean factor is NOT fixed at k=11. It must be parameterized
or the theorem must be narrowed to a specific weight.

### L(s, π × π̃) = ζ(s) · L(s, π, Ad)

For GL₂ with trivial central character, the Rankin–Selberg L-function factors as:

    L(s, π × π̃) = ζ(s) · L(s, π, Ad)

This follows from:
- Unramified computation: the Satake parameters of π × π̃ are
  {α_p β̄_p, ᾱ_p β_p, 1, 1} (trivial central char gives |α_p β_p| = 1)
- The adjoint L-function has parameters {α_p β_p^{−1}, β_p α_p^{−1}, 1}
- ζ(s) contributes the pole at s = 1

## Status: [OBL]

The main obstruction is the explicit computation of ramified local factors Z_p(1)
for each bad prime p. This requires:
1. Identifying the local newvector type (Iwahori, spherical, etc.)
2. Computing the local Whittaker function explicitly
3. Evaluating the local Godement–Jacquet integral
