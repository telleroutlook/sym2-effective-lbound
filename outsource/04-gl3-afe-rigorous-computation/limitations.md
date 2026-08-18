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

6. The dual sum weight V_tilde(n*X, s) decays faster than any power of
   (nX)^{-1} for large nX due to the h(-v) = exp(v^2) cutoff in the
   Mellin integral (the integrand's Gaussian decay produces stretched-
   exponential or faster decay of V_tilde). The actual decay rate depends
   on the Gamma ratio G(1-s+v)/G(s) and must be proved from a uniform
   bound on the Mellin integrand. A weaker statement V_tilde = O((nX)^{-A})
   for any A > 0 follows from shifting the contour to Re(v) = A, picking
   up Gamma poles. The claimed "V_tilde(720, s) ~ 4e-6" is a discovery-
   tier observation, not a proved bound.
