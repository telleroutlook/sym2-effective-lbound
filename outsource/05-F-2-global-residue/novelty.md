# Novelty — F-2 Restructured

## What is new

This restructuring:

1. **Corrects the residue formula**: The original had a scaling contradiction
   (linearity in W̃ vs independence of |W|²). The correct formula uses W and
   conj(W) (same vector), producing a norm-square.

2. **Corrects the JS81 reading**: The original conflated π' = π (diagonal) with
   π̃ = π (self-dual). The correct condition is π' = π.

3. **Splits the obligation**: F-2A (diagonal positivity) is essentially a JS81
   specialization; F-2B (Euler factor extraction) is the real technical work;
   F-2C (uniformity) interfaces with downstream.

4. **Parameterizes the archimedean factor**: The original fixed k=11, which is
   specific to Δ. The new version parameterizes by k.

## What is NOT new

- F-2A is entirely contained in Jacquet–Shalika 1981
- The factorization L(s, π × π̃) = ζ(s) · L(s, π, Ad) is standard
- The local newvector theory is Casselman 1974
