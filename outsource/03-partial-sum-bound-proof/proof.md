# Proof — Partial-sum bound for sym^2 Delta

**Status:** THEOREM (via Friedlander-Iwaniec; explicit constant not available).

## §1. Statement

Let A(n) be the normalized symmetric-square coefficients of the weight-12
cusp form Delta in S_12(SL_2(Z)):

```
L(s, sym^2 Delta) = sum_{n>=1} A(n) / n^s
```

with A(1) = 1, A(p) = c_p^2 - 1 where c_p = tau(p)/p^{5.5}, and A
multiplicative with the GL_3 Hecke recurrence for prime powers.

**Theorem** (Friedlander-Iwaniec 2005, Proposition 3.2):

J. B. Friedlander and H. Iwaniec, "Summation Formulae for Coefficients
of L-functions", Canadian Journal of Mathematics 57 (2005), 494–505,
Proposition 3.2.

For degree m = 3 — the specialization used here — Proposition 3.2 of
Friedlander-Iwaniec gives (the general Proposition 1.1 exponent is
D^{1/(m+1)} x^{(m-1)/(m+1)+epsilon}, which is NOT what this package
uses): for a degree-3 Dirichlet series satisfying a functional equation
with archimedean parameters kappa_1, kappa_2, kappa_3 and coefficients
a(n) <<_epsilon n^epsilon, the partial sums satisfy:

```
sum_{n<=X} a(n) = R(X) + O_epsilon(D^{1/4} X^{1/2 + epsilon})
```

where D is the conductor and R(X) = 0 when L(s) is entire.

## §2. Verification of hypotheses for sym^2 Delta

**Degree m = 3:** L(s, sym^2 Delta) is a degree-3 L-function (GL_3 automorphic
form on GL_3 x GL_1). [THM, Gelbart-Jacquet 1978]

**Conductor D = 1:** Level 1, no ramified primes. [THM]

**Archimedean parameters:** The completed L-function is

```
Lambda(s) = Gamma_R(s+1) * Gamma_C(s+11) * L(s, sym^2 Delta)
```

with functional equation Lambda(s) = Lambda(1-s). Since

```
Gamma_C(s+11) = Gamma_R(s+11) * Gamma_R(s+12)
```

the three archimedean parameters are kappa_1 = 1, kappa_2 = 11, kappa_3 = 12.
[THM, Iwaniec-Michel; standard normalization for sym^2 of weight-k form with k=12]

**Coefficient bound:** the local Satake parameters of sym^2 Delta at p
are alpha_p^2, 1, beta_p^2 with |alpha_p| = |beta_p| = 1 (Deligne), so
A(p^r) is the degree-r complete homogeneous symmetric polynomial in
three unit-modulus parameters — a sum of exactly binom(r+2,2) = d_3(p^r)
unit-modulus terms. Hence |A(p^r)| <= d_3(p^r), and multiplicativity
gives |A(n)| <= d_3(n) <<_epsilon n^epsilon. [THM, DEL-D.1; local
structure per Iwaniec-Michel]

**Entireness:** the completed symmetric-square L-function of a
primitive holomorphic cusp form is entire (Iwaniec-Michel state this
explicitly, with the s <-> 1-s functional equation). Therefore
R(X) = 0 in the Friedlander-Iwaniec formula. [THM, IM]

**Self-duality (B(s) = A(s)):** The Friedlander-Iwaniec framework
requires a dual Dirichlet series B(s) = sum b(n) n^{-s} with
|b(n)| << n^epsilon. For sym^2 Delta, the L-function is self-dual
(root number +1), so B(s) = A(s) and b(n) = A(n). The coefficient
bound |A(n)| << n^epsilon therefore verifies the FI hypothesis for
both series simultaneously.

## §3. Conclusion

Applying Friedlander-Iwaniec Proposition 3.2 with m=3, D=1,
kappa=(1,11,12), |A(n)| <<_epsilon n^epsilon, and R(X)=0:

```
S(X) := sum_{n<=X} A(n) = O_epsilon(X^{1/2 + epsilon})
```

The cited proposition gives the estimate for X > D^{1/2} = 1; the
case X = 1 follows from S(1) = 1 after enlarging the implied constant.

**This is unconditional.** No GRH, no zero-free region, no explicit formula
over zeros is needed. [THM]

## §4. What is NOT available

1. **Explicit constant C:** Friedlander-Iwaniec proves C(epsilon) exists
   but does not give a numerical value. The empirical value
   max |S(X)|/X^{0.5} = 0.258953 (at X = 196) for X in [100, 5000] is discovery-tier.

2. **Fixed exponent epsilon = 0:** The theorem gives O(X^{1/2+epsilon})
   for every epsilon > 0, not O(X^{1/2}). The question of whether
   |S(X)| <= C * X^{1/2} (with fixed C) remains open.

3. **Explicit L(1) interval:** Without an explicit C, the Abel summation
   bound gives |L(1) - partial_sum(N)| <= C(epsilon) * N^{-1/2+epsilon},
   which is non-effective for numerical certification.

## §5. Connection to L(1) (Abel summation)

If |S(X)| <= C * X^alpha with alpha < 1, Abel summation gives:

```
L(1) = sum_{n<=N} A(n)/n - S(N)/N + integral_N^inf S(x)/x^2 dx
```

Note the minus sign before S(N)/N (integration by parts).

Therefore:

```
|L(1) - sum_{n<=N} A(n)/n| <= C * (1 + 1/(1-alpha)) * N^{alpha-1}
```

For alpha = 1/2: the bound is <= 3C / sqrt(N).

If one CONJECTURALLY assumes the global bound |S(X)| <= 0.259*sqrt(X)
for all X >= N (observed only on the finite computed range), then with
N = 10^8 the truncation term would be <= 3 * 0.259 / 10^4 = 7.8e-5.
This is NOT an error bound: C = 0.259 is a discovery-tier constant,
and no numeric L(1) interval is claimed in this batch (explicit
C(epsilon) and rigorous L(1) tails belong to a dedicated batch).

## §6. References

- Friedlander-Iwaniec (2005), "Summation Formulae for Coefficients of
  L-functions", Canadian Journal of Mathematics 57, 494–505.
  Proposition 3.2, degree-3 partial sum bound.
- Gelbart-Jacquet (1978), "A relation between automorphic representations
  of GL(2) and GL(3)" — GL_3 structure, entireness.
- Iwaniec-Michel, "Derivatives of L-functions of symmetric square" —
  archimedean parameters for sym^2 of weight-k form.
- Deligne (1974), "La conjecture de Weil I" — |tau(p)| <= 2*p^{5.5}.
- Iwaniec-Kowalski (2004), "Analytic Number Theory" — Abel summation.
