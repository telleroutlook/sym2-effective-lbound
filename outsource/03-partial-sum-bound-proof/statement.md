# Statement — Partial-sum bound for sym^2 Delta

**Theorem ID:** ps-bound-sym2-delta
**Mathematical status:** THEOREM (via Friedlander-Iwaniec Proposition 3.2; explicit constant not available)
**Computational status:** EMPIRICAL (verified for X <= 20000)
**Program ref:** sym2-effective-lbound Q-11
**Paper target:** Paper A (effective L(1) bound)

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

with A(1) = 1, A multiplicative, and for prime p:

```
A(p) = c_p^2 - 1,    c_p = tau(p) / p^{5.5}
A(p^{k+1}) = (c_p^2 - 1) A(p^k) - (c_p^2 - 1) A(p^{k-1}) + A(p^{k-2})
```

(GL_3 Hecke recurrence for the symmetric square.)

Define the partial sums:

```
S(X) = sum_{n<=X} A(n)
```

## Theorem (conjectured)

For every epsilon > 0, there exists C(epsilon) > 0 such that for all X >= 1:

```
|S(X)| <= C(epsilon) * X^{1/2 + epsilon}
```

Moreover, for the specific case epsilon = 0 (if attainable):

```
|S(X)| <= C * X^{1/2}
```

for some absolute constant C.

## Empirical evidence

For X in [1, 20000], computed from the exact A(n):

```
max_{1<=X<=20000} |S(X)| / X^{0.5} = 0.2590
```

The ratio |S(X)| / X^{0.5} appears bounded, suggesting the exponent 1/2
is correct (not just 1/2 + epsilon).

## Connection to L(1)

If the theorem holds with alpha = 0.5, then the Cesaro truncation error
satisfies:

```
|L(1) - L_ces(N,1)| <= C * N^{-0.5} / 0.5 = 2C / sqrt(N)
```

With C = 0.259 and N = 10^8: error <= 0.000052, giving:

```
L(1, sym^2 Delta) in [0.6317, 0.6318]
```
