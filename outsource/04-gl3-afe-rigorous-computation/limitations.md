# Limitations — GL_3 AFE computation

1. The weight function V(y, s) is computed via Mellin inversion, which
   requires bounding the tail of the Gamma-factor integral. This bound
   depends on the convexity exponent for L(s) in the critical strip,
   which is not optimal (the Lindelof hypothesis would give a better bound).

2. The computation uses mpmath floats (discovery tier). A proof-tier
   version requires python-flint (Arb) with outward rounding, which is
   significantly slower.

3. The grid resolution (sigma steps, t steps) determines the certified
   zero-free region. Finer grids give better regions but cost more time.

4. The method evaluates L(s) at specific points. It does not directly
   prove the partial-sum bound |S(X)| << X^{1/2}; that requires an
   additional step (zero-free region -> explicit formula -> partial sums).

5. For large |t|, the Gamma factors grow exponentially, making the
   computation harder. The practical limit is |t| ~ 100 with current tools.
