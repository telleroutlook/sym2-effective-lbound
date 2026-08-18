# Limitations — GL_3 AFE computation

1. The implementation uses mpmath floats (30 digits), not Arb interval
   arithmetic. No certified error bounds are provided. This is
   discovery-tier only.

2. The two-term AFE (main sum + dual sum) is implemented with the
   correct gamma ratio G(1-s+v)/G(s) in the dual weight. However,
   the quadrature error and truncation error are not rigorously bounded.

3. The "independent checker" recomputes the same formula with the same
   algorithm, verifying arithmetic consistency, not mathematical correctness.

4. The finite grid (45 points in the critical strip) cannot certify a
   continuous zero-free region. Points between grid locations may be zeros.

5. For large |t|, the Gamma factors grow exponentially, making the
   computation harder. The practical limit is |t| ~ 100.

6. The dual sum weight V_tilde(n*X, s) decays as ~(nX)^{-1} for large n,
   ensuring convergence. With X=12, N=60: V_tilde(720, s) ~ 4e-6.
