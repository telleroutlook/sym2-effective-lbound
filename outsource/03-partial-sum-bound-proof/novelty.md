# Novelty — Partial-sum bound

There is NO new theorem in this package. The universal bound
|S(X)| <<_epsilon X^{1/2+epsilon} for the symmetric-square coefficients of
Delta is an instantiation of existing literature: Friedlander-Iwaniec
(Can. J. Math. 57 (2005), Proposition 3.2, degree m = 3 specialization)
together with Iwaniec-Michel's Euler factors, Gamma factors, entireness,
and functional equation for sym^2 of a primitive holomorphic cusp form.

The package's contribution is limited to:

1. Verifying the hypotheses explicitly for the concrete instance
   (k = 12, N = 1, kappa = (1, 11, 12), D = 1) and wiring the result into
   this repository's later effective-computation framework.

2. A discovery-tier finite experiment (exact A(n), X <= 5000 measured;
   maximum |S(X)|/sqrt(X) = 0.258953 at X = 196) motivating — but not
   proving — the stronger empirical sqrt(X)-scale model.

No claim is made that the bound was previously open, and no certified L(1)
interval is claimed here; the explicit C(epsilon) and rigorous L(1) tails
remain the actual open work.
