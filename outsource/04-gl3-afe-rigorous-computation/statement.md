# Statement — GL_3 AFE computation for L(s, sym^2 Delta)

**Theorem ID:** gl3-afe-rigorous-sym2-delta
**Mathematical status:** METHOD-DESCRIPTION (not a theorem)
**Computational status:** DISCOVERY (discovery-tier numerical values)
**Program ref:** sym2-effective-lbound Q-11

---

## Goal

Describe a computational method for evaluating L(s, sym^2 Delta) at points
in the critical strip using the GL_3 approximate functional equation (AFE).

## Current results (discovery-tier)

Numerical evaluation using mpmath floats (30 digits) with the two-term AFE:

- L(1, sym^2 Delta) ~ 0.63179295
- S1 ~ 0.5483 (main sum, N=20000, T=8)
- J = S1 - L(1) ~ -0.0835
- Min |L(s)| ~ 0.170 on 5x41 grid in [0.6,1] x [-20,20]

**These are NOT certified values.** The error closure is not closed.

## What is NOT claimed

1. No certified L(1) interval (quadrature + tail errors not bounded)
2. No proved zero-free region (derivative bounds not rigorous)
3. No certified J value (depends on certified L(1))
4. No THM or CERTIFIED labels on any result

## Status

This batch is a METHOD-DESCRIPTION + DISCOVERY prototype. The AFE
framework is consistent with the standard derivation. All rigorous
error layers (exact coefficients, quadrature error, contour tail,
AFE tails) remain [OBL].

## v3 corrections

Previous versions incorrectly labeled some witness files as CERTIFIED.
All certificates have been downgraded to DISCOVERY. Code bugs in
C_V computation (missing G factor, X-direction error) have been
identified and documented.
