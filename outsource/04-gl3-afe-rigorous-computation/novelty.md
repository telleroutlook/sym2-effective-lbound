# Novelty — GL_3 AFE computation

1. The GL_3 AFE is standard in the theory of automorphic L-functions.
   What is new is the RIGOROUS implementation with certified error bounds
   using Arb interval arithmetic for the specific case sym^2 Delta.

2. The connection to the effective L(1) problem: the rigorous AFE
   computation provides the zero-free region needed to bound the Cesàro
   truncation error and certify L(1).

3. The combination of exact coefficient computation (tau sieve) with
   rigorous AFE evaluation is specific to this instance and not available
   in general L-function databases (LMFDB, Lcalc, etc.).
