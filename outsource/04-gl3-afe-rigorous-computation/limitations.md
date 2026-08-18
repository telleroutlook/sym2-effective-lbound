# Limitations — GL_3 AFE computation

1. The current implementation computes ONLY the main sum of the AFE.
   The dual sum (from the functional equation) is NOT implemented.
   This means the computed values are NOT certified approximations to L(s).

2. The weight function V(y, s) is computed via mpmath floats, not Arb
   interval arithmetic. No error bounds are certified.

3. The "independent checker" recomputes the same single-sum formula,
   so it verifies arithmetic consistency, not mathematical correctness.

4. The finite grid (45 points in the critical strip) cannot certify a
   continuous zero-free region. Points between grid locations may be zero.

5. For large |t|, the Gamma factors grow exponentially, making the
   computation harder. The practical limit is |t| ~ 100.
