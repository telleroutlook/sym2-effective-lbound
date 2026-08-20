# Checker — Partial-sum bound

The universal bound |S(X)| <<_epsilon X^{1/2+epsilon} is a THEOREM
(Friedlander-Iwaniec Prop. 3.2 at degree 3, applied to sym^2 Delta); no
finite checker is needed or able to verify it. What the finite checker
tests is the STRONGER EMPIRICAL model |S(X)| <= C*sqrt(X): it recomputes
S(X) via floating-point computation for X in [100, 5000] and verifies |S(X)| <= 0.26*sqrt(X) on
that range (maximum observed 0.258953 at X = 196). The constant 0.259 is a
discovery-tier candidate only, with no standing beyond the computed range.
