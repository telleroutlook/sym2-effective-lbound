# F-2C: Target-Family Local Positivity/Uniformity — Proof

## Mathematical content

### Archimedean correction Z_∞(1)

For a holomorphic newform of weight k, the archimedean representation π_∞ is a
discrete series representation with Harish-Chandra parameter (k−1)/2. The local
Rankin–Selberg integral at ∞ involves:

    Ψ_∞(s, W_∞, W_∞, Φ_∞) = ∫_{N(R)\GL₂(R)} W_∞(g) · conj(W_∞(g)) · Φ_∞(g) · |det g|^s dg

For the standard holomorphic vector (highest weight vector of the discrete series),
this evaluates to (up to normalization):

    Z_∞(s) = Γ_R(s + 1) · Γ_C(s + k − 1)

where:
- Γ_R(s) = π^{−s/2} Γ(s/2) (completed real gamma factor)
- Γ_C(s) = 2(2π)^{−s} Γ(s) (completed complex gamma factor)

**At s = 1**: Z_∞(1) = Γ_R(1) · Γ_C(k) = 1 · 2(2π)^{−k} Γ(k)

This depends on k (NOT fixed at k = 11).

### Ramified corrections Z_p(1)

For p | N, the local representation π_p may be:
- **Spherical** (newform): Z_p(s) involves the local L-factor L_p(s, π_p × π̃_p)
- **Iwahori level**: Additional local correction from the Iwahori-fixed vector
- **Higher level**: More complex local computation

The computation requires:
1. Identifying the local type (via the conductor)
2. Computing the local Whittaker function (Casselman's formula for Iwahori)
3. Evaluating the local Godement–Jacquet integral

### Uniformity for level ≤ N₀

The product ∏_{p|N} Z_p(1) must be bounded below uniformly for all N ≤ N₀.
The key insight is that:

1. **Finitely many bad primes**: For N ≤ N₀, the set of possible bad primes is finite.
2. **Local factors are continuous**: Z_p(1) varies continuously in the local representation.
3. **Compactness**: The set of local representations at each p is compact (up to
   normalization), so Z_p(1) achieves a minimum.

The explicit constant c' = min_{N ≤ N₀} ∏_{p|N} |Z_p(1)| is then well-defined
and computable.

### Interface with downstream

The constant c' feeds into:
- **M-1**: The mollifier construction uses c' to normalize the integral
- **M-2**: The mean value estimate uses c' to control the error
- **c_eff**: The explicit bound is proportional to c'

## Status: [OBL]

The main tasks are:
1. Explicit computation of Z_∞(1) for weight k
2. Explicit computation of Z_p(1) for each local type
3. Explicit lower bound c' for the uniform product
