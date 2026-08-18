# Novelty — GL(3) AFE computation

The current contribution is a DISCOVERY-TIER PROTOTYPE implementing a
two-term AFE for L(s, sym^2 Delta) (mpmath floats; no Arb, no certified
error bounds). Rigorous Arb certification, proved truncation lengths,
tail bounds, and continuous zero-free verification remain FUTURE
OBLIGATIONS and are explicitly NOT claimed. The batch does not provide
the zero-free region and cannot serve as a premise downstream.

After the 2026-08-19 external review (FAIL), the honest status is:
discovery-tier numerical experiment program whose AFE structure is
consistent with the standard Mellin-shift derivation, with every
rigorous layer still open (see the repo roadmap: single-point Arb
certificate first, grid and zero-free region last).
