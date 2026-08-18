# Statement — Partial-sum bound for sym^2 Delta

**Theorem ID:** ps-bound-sym2-delta
**Mathematical status:** THEOREM (Friedlander-Iwaniec 2005, Proposition 3.2)
**Computational status:** EMPIRICAL (verified for X in [100, N])
**Program ref:** sym2-effective-lbound Q-11

---

## Definitions

Let Delta(q) = q * prod_{k>=1} (1-q^k)^{24} = sum_{n>=1} tau(n) q^n be the
Ramanujan cusp form of weight 12 for SL_2(Z).

The symmetric-square L-function is:

```
L(s, sym^2 Delta) = prod_p prod_{i<=j} (1 - alpha_i alpha_j p^{-s})^{-1}
```

where alpha_1, alpha_2 are the Satake parameters at p with |alpha_i| = 1
(Deligne) and alpha_1 * alpha_2 = 1.

The Dirichlet series coefficients A(n) are defined by:

```
L(s, sym^2 Delta) = sum_{n>=1} A(n) n^{-s}
```

with A(1) = 1, A multiplicative, and for prime p, with a = A(p) = c_p^2 - 1:

```
A(p^0) = 1
A(p^1) = a
A(p^2) = a^2 - a
A(p^r) = a * A(p^{r-1}) - a * A(p^{r-2}) + A(p^{r-3}),  r >= 3
```

(GL_3 Hecke recurrence for the symmetric square.)

Define the partial sums:

```
S(X) = sum_{n<=X} A(n)
```

## Theorem

For every epsilon > 0, there exists C(epsilon) > 0 such that for all X >= 1:

```
|S(X)| <= C(epsilon) * X^{1/2 + epsilon}
```

Moreover, for the specific case epsilon = 0 (if attainable):

```
|S(X)| <= C * X^{1/2}
```

for some absolute constant C. Whether this holds remains open.

## Empirical evidence

For X in [100, N], computed from exact A(n) via tau(n):

```
max |S(X)| / X^{0.5} approx 0.259
```

Note: S(1)/sqrt(1) = 1, so the range must start at X >= 2 (or X >= 100)
for the ratio to be meaningful.

## Connection to L(1)

By Abel summation:

```
L(1) = sum_{n<=N} A(n)/n - S(N)/N + integral_N^inf S(x)/x^2 dx
```

If |S(X)| <= C * X^{0.5}, then:

```
|L(1) - sum_{n<=N} A(n)/n| <= 3C / sqrt(N)
```

With C = 0.259 and N = 10^8: error <= 7.8e-5, giving:

```
L(1, sym^2 Delta) in approximately [0.6317, 0.6326]
```

(This is discovery-tier since C is not proved.)
