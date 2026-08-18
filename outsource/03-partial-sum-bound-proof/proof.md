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

For any degree-m Dirichlet series satisfying a functional equation with
archimedean parameters kappa_1, ..., kappa_m, and with coefficients
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

**Coefficient bound:** By Deligne's bound |tau(p)| <= 2*p^{5.5}, we have
|c_p| <= 2, so |A(p)| = |c_p^2 - 1| <= 3. By multiplicativity and the
Hecke recurrence, |A(n)| <= d_3(n) <<_epsilon n^epsilon. [THM, DEL-D.1]

**Entireness:** L(s, sym^2 Delta) is entire (no pole at s=1, since the
symmetric square of a cusp form has no exceptional spectrum). Therefore
R(X) = 0 in the Friedlander-Iwaniec formula. [THM]

## §3. Conclusion

Applying Friedlander-Iwaniec Proposition 3.2 with m=3, D=1,
kappa=(1,11,12), |A(n)| <<_epsilon n^epsilon, and R(X)=0:

```
S(X) := sum_{n<=X} A(n) = O_epsilon(X^{1/2 + epsilon})
```

**This is unconditional.** No GRH, no zero-free region, no explicit formula
over zeros is needed. [THM]

## §4. What is NOT available

1. **Explicit constant C:** Friedlander-Iwaniec proves C(epsilon) exists
   but does not give a numerical value. The empirical value
   max |S(X)|/X^{0.5} = 0.259 for X in [100, N] is discovery-tier.

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

With the empirical C = 0.259 and N = 10^8: error <= 3 * 0.259 / 10^4
= 7.8e-5, giving L(1) in approximately [0.6317, 0.6326].

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
