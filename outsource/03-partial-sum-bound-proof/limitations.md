# Limitations — Partial-sum bound

1. The conjectured bound |S(X)| <= C * X^{1/2} is not proven. All current
   evidence is computational (X <= 20000).

2. The exponent 1/2 is conjecturally optimal (related to GRH for
   L(s, sym^2 Delta)). Without GRH, the best unconditional exponent
   may be larger (e.g., 2/3 or 3/4).

3. The constant C = 0.259 is empirical. The true constant may be larger
   (but the exponent is the critical quantity).

4. The partial-sum bound is used to control the Cesàro truncation error
   in the L(1) computation. Without it, the L(1) certificate is
   conditional only.

5. This task does not resolve the general effective L(1) bound problem
   (Goldfeld-Hoffstein-Lieman 1994). It addresses only the specific
   instance sym^2 Delta.
