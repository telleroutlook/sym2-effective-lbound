# Checker — GL_3 AFE computation

The checker recomputes L(s) at a few spot-check points using the truncated
Dirichlet series (for Re(s) > 1) and verifies agreement with the AFE
computation. It does not verify the analytic error bounds — that requires
the reviewer.

For Re(s) > 1, the Dirichlet series converges absolutely and provides an
independent check of the AFE values.
