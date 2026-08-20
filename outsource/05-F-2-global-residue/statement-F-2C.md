# F-2C: Target-Family Local Positivity/Uniformity

## Desired Statement

For the specific modular form family needed downstream (L(1, sym² f) ≥ c/log N):

**Statement**: Fix:
- Level N (conductor of the symmetric square)
- Weight k (holomorphic weight of f)
- Nebentypus χ (if applicable)
- Newvector normalization (Petersson-normalized or Whittaker-normalized)
- Haar measures on GL₂(A_Q) (modular normalizations)
- Archimedean vector φ_∞ (holomorphic discrete series of weight k)
- Bad-prime types (spherical/Iwahori at each p | N)

Then the local corrections satisfy:

1. **Archimedean correction**: Z_∞(1) is computed explicitly in terms of k

2. **Ramified corrections**: For each p | N, Z_p(1) is computed explicitly in terms
   of the local newvector type

3. **Uniformity**: For the family of forms with level ≤ N₀, the corrections satisfy:

    min_{p | N} |Z_p(1)| ≥ c' > 0

   for some explicit constant c' depending on N₀ but not on the individual form.

## What remains

This is the final link between the abstract F-2A/F-2B and the concrete lower bound
c/log N. The key tasks are:

1. **Fix the archimedean vector**: For weight k, the holomorphic discrete series
   vector has a specific normalization. Compute Z_∞(1) explicitly.

2. **Fix the newvector type**: For each p | N, determine whether the local representation
   is spherical, Iwahori, or higher level. Compute Z_p(1) accordingly.

3. **Prove uniformity**: Show that the product ∏_v Z_v(1) is bounded below by an
   explicit constant depending only on N₀ (not on individual forms).

4. **Interface with downstream**: The constant c' from uniformity feeds directly into
   the M-1 mollifier construction and the c_eff explicit bound.

## Status: [OBL]

This is the most concrete of the three obligations and the one that directly
interfaces with the computational pipeline (checker/check_bound.py, F-3).
