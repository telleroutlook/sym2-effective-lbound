# Novelty — GL_3 AFE computation

## What is new

A two-term AFE implementation for L(s, sym^2 Delta) using the correct
gamma ratio G(1-s+v)/G(s) in the dual weight, with self-duality
B(s) = A(s) correctly identified.

## Honest status after 2026-08-20 review (FAIL/BLOCKED)

Discovery-tier numerical prototype. The AFE structure is consistent with
the standard Mellin-shift derivation. Every rigorous layer is still open:

1. Exact coefficient chain (float -> rational) [OBL]
2. Quadrature error bound [OBL]
3. Contour tail bound [OBL]
4. AFE tail bound [OBL]
5. Zero-free region [OBL]

The recommended next step is to close the single-point s=1 error budget
before attempting grid or zero-free region certification.
