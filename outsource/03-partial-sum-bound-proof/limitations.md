# Limitations — Partial-sum bound

1. The bound |S(X)| <= C(epsilon) * X^{1/2+epsilon} is proved
   unconditionally via Friedlander-Iwaniec Proposition 3.2.

2. The explicit constant C(epsilon) is NOT available from the theorem.
   The empirical value max |S(X)|/X^{0.5} = 0.259 for X in [100, 20000]
   is discovery-tier only.

3. The exponent 1/2+epsilon is not conjecturally optimal. Friedlander-Iwaniec
   itself gives a stronger natural scale O(X^{1/3+epsilon}) for degree-3
   L-functions; 1/2+epsilon is the weaker, already unconditional bound.

4. The partial-sum bound is used to control the Cesàro truncation error
   in the L(1) computation. Without it, the L(1) certificate is
   conditional only.

5. This task does not resolve the general effective L(1) bound problem
   (Goldfeld-Hoffstein-Lieman 1994). It addresses only the specific
   instance sym^2 Delta.
