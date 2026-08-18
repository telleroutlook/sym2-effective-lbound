# Limitations — Partial-sum bound

1. The bound |S(X)| <= C(epsilon) * X^{1/2+epsilon} is proved
   unconditionally via Friedlander-Iwaniec Proposition 3.2 (2005).

2. The explicit constant C(epsilon) is NOT available from the theorem.
   The empirical value max |S(X)|/X^{0.5} = 0.258953 (at X = 196) for X in [100, 5000]
   is discovery-tier only.

3. The exponent 1/2+epsilon is proved; the stronger natural scale
   X^{1/3+epsilon} appears in the Friedlander-Iwaniec paper as a
   conjecture for the automorphic form, not as a proved result.
   The unconditional result is X^{1/2+epsilon}.

4. The partial-sum bound is used to control the Abel summation truncation
   error in the L(1) computation. Without an explicit C, the L(1)
   certificate remains conditional.

5. This task does not resolve the general effective L(1) bound problem
   (Goldfeld-Hoffstein-Lieman 1994). It addresses only the specific
   instance sym^2 Delta.
