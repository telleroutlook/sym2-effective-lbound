# sym2-effective-lbound

**Effective lower bounds for symmetric square L-functions at s=1.**

This repository pursues Direction 1 from the GL2xGL2 Rankin-Selberg survey:
making the constant c in L(1, sym^2 f) >= c/log N **explicit and computable**,
targeting the technical gap in the Goldfeld-Hoffstein-Lieman (1994) theorem.

## Mathematical Problem

For a holomorphic Hecke eigenform f of level N with trivial nebentypus,
Goldfeld-Hoffstein-Lieman (1994) proved:

    L(1, sym^2 f) >= c / log N

for an **ineffective** constant c > 0. The ineffectivity arises from the
Siegel zero exclusion step, which uses Siegel's theorem for Dedekind zeta
functions (qualitatively ineffective).

**This project's goal:** certify explicit lower bounds via interval arithmetic,
starting with the Ramanujan Delta function (k=12, N=1).

## Proof Status

| ID  | Description                               | Status     | File                         |
|-----|-------------------------------------------|------------|------------------------------|
| F-1 | CG local Euler factor factorization       | **[THM]**  | proof/01-foundations.tex     |
| F-2 | Global residue positivity                 | **[OBL]**  | proof/02-global-residue.tex  |
| F-3 | Certified L(1, sym^2 Delta) interval      | **[THM]**  | proof/04-effective-bound.tex |
| M-1 | Mollifier construction on GL3             | **[OBL]**  | proof/03-mollifier.tex       |
| M-2 | Mean value estimate (Kuznetsov/Petersson) | **[OBL]**  | proof/03-mollifier.tex       |
| E-1 | Certified finite Euler product (Delta)    | **[OBL]**  | src/numerical_delta.py       |
| E-2 | Certified tail bound (Ramanujan-Deligne)  | **[OBL]**  | checker/check_bound.py       |

Status grammar: [THM] = proved here; [OBL] = open proof obligation;
[OUT] = deliberately outside scope. [OBL] items may NOT be used as theorems.

## Key Certified Results

- **Theorem F-1:** For alpha_p * beta_p = 1 (trivial central character),
  the local Rankin-Selberg factor satisfies
  L_p(s, f x f)^{-1} = L_p(s, sym^2 f)^{-1} * (1 - p^{-s})(1 + p^{-s}),
  with exact (1+p^{-s}) cancellation from the Clebsch-Gordan identity chi_l^2 = sum_{j=0}^l chi_{2j}.

- **Open obligation F-2:** prove the global residue formula, including every
  bad local correction factor and the adjoint input `L(1, Ad) > 0`.  The exact
  Shahidi statement is not yet source-backed; a complete pair-L-function bridge
  has not been supplied.

- **Theorem F-3:** L(1, sym^2 Delta) in [0.63179293, 0.63179298] (width 4.6e-8).
  Proved via AFE with N=3000 terms, 256-bit precision, two-point truncation
  error bound. Therefore L(1, sym^2 Delta) > 0.
  Certificate: outsource/04-gl3-afe-rigorous-computation/witness/single_point_certificate.json

## Numerical Anchor (Discovery Tier)

For the Ramanujan Delta function, known tau(p) values give:

    L(1, sym^2 Delta) ~ 0.631793  (discovery only; not a certificate)

Local factor formula:

    L_p(1, sym^2 Delta)^{-1} = (1 - 1/p) * (1 - (c_p^2 - 2)/p + 1/p^2)

where c_p = tau(p) / p^{5.5} satisfies |c_p| <= 2 (Ramanujan-Deligne / Deligne 1974).

## Repository Structure

```
sym2-effective-lbound/
  spec/SPECIFICATION.md     # Authoritative math spec (status grammar, certificate format)
  proof/
    01-foundations.tex      # [THM F-1] Clebsch-Gordan local factorization
    02-global-residue.tex   # [OBL F-2] Global residue positivity
    03-mollifier.tex        # [OBL] Mollifier construction on GL3
    04-effective-bound.tex  # [OBL] Main theorem and GHL dichotomy
    paper.tex               # Combined paper skeleton
  src/
    euler_factors.py        # chi_l, local_factor_series, local_factor_closed
    numerical_delta.py      # TAU_PRIMES, L(1,sym^2 Delta) computation
    afe_s1_arb.py           # Finite S1[N,T] Arb certificate (canonical gamma)
    afe_s1_full.py          # Infinite S1 certificate with rigorous tail bounds
    tau_sieve.py            # Exact tau(n) via eta-product recurrence
    mollifier.py            # [OBL] Mollifier coefficients (discovery tier)
  checker/
    check_bound.py          # Independent certificate verifier (no src/ imports)
    check_s1_finite.py      # Verifier for finite S1[N,T] certificates
    check_s1_full.py        # Verifier for infinite S1 certificate (no src/ imports)
  tests/
    test_euler_factors.py   # F-1 theorem tests
    test_mollifier.py       # Mollifier coefficient tests
    test_numerical.py       # L(1,sym^2 Delta) numerical tests
    test_afe_s1_arb.py      # Finite S1 certificate tests
    test_afe_s1_full.py     # Infinite S1 certificate + checker tests
  schemas/
    bound-certificate.schema.json  # JSON schema for certificates
  papers/
    survey.tex              # GL2xGL2 Rankin-Selberg pedagogical survey
  baseline/
    s1_full_certificate.json  # Reference infinite-S1 certificate (N=20000, T=8)
    REFERENCE_BASELINE.md   # Source-backed theorem ledger (no committed PDFs)
  discovery/                # UNTRUSTED explorations; never imported by src/
```

## Module Dependency (One-Way)

```
M0 foundations
  --> M1 Satake params, local factors (euler_factors.py)
    --> M2 Euler product (numerical_delta.py)
      --> M3 Mollifier (mollifier.py)  [OBL]
        --> M4 Effective bound (04-effective-bound.tex)  [OBL]

S1 certificate chain (independent of M0-M4):
  tau_sieve.py  -->  afe_s1_arb.py (finite S1[N,T])
  tau_sieve.py  -->  afe_s1_full.py (infinite S1 with tail bounds)
  checker/check_s1_finite.py  (no src/ imports)
  checker/check_s1_full.py    (no src/ imports)
```

No reverse imports. `checker/` is independent of `src/`.
`discovery/` is never imported by any other module.

## Session Start Protocol

```bash
pytest tests/ -x -q
```

All tests must pass before any work begins. Failing tests must be fixed first.

## Key References

1. Goldfeld, Hoffstein, Lieman (1994) -- GHL lower bound (ineffective c)
2. Gelbart, Jacquet (1978) -- GL3 symmetric square lift
3. Shahidi (1981) -- inspected; the exact L(1, Ad) statement remains not-found
4. Jacquet, Shalika (1981) -- unramified local integral and Euler-product convergence
5. Iwaniec, Kowalski -- Analytic Number Theory (reference for explicit formulas)

## License

Source code: MIT. Mathematical proof documents: CC BY 4.0.
