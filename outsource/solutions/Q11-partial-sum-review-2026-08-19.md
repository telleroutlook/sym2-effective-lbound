# External review — Batch 03 partial-sum bound (Q-11), returned 2026-08-19

**Verdict: PASS WITH MINOR REVISIONS. Core mathematical theorem CONFIRMED.**

S(X) = sum_{n<=X} A(n) = O_eps(X^{1/2+eps}) unconditionally: Friedlander–
Iwaniec Prop. 3.2 at degree m=3 gives sum a(n) = R(x) + O(D^{1/4} x^{1/2+eps})
with constants depending only on (eps, kappa_1, kappa_2, kappa_3); Iwaniec–
Michel supply the sym^2 Euler factors, three Gamma factors at infinity,
entireness, and the s<->1-s functional equation; for (k=12, N=1) this
matches the bundle's kappa=(1,11,12), D=1. No GRH, no zero-free region, no
circularity. Reviewer's independent empirical maximum |S(X)|/sqrt(X) =
0.258952873686... at X=196 over 100<=X<=5000, cross-checked exactly to
X=500 with rational A(n).

Required revisions (nine):
1. proof.md FI statement over-general — the D^{1/4}X^{1/2+eps} exponent is
   the m=3 specialization; general Prop 1.1 is D^{1/(m+1)}x^{(m-1)/(m+1)+eps}.
   Write "For degree m=3, Proposition 3.2 gives ...".
2. d_3(n) bound reasoning too quick — use local Satake parameters
   alpha_p^2, 1, beta_p^2 (|.|=1): A(p^r) is a degree-r complete
   homogeneous symmetric polynomial in three unit-modulus parameters with
   binom(r+2,2) = d_3(p^r) terms, so |A(p^r)| <= d_3(p^r); multiplicativity.
3. Entireness justification — cite Iwaniec–Michel's completed sym^2
   L-function entire directly, not "no exceptional spectrum".
4. novelty.md badly stale — "can it be proved unconditionally" is answered
   by this very package; "certified L(1) interval" conflicts with
   limitations. Reposition: instantiation of existing theorems for the
   concrete Delta instance, wired into later effective-computation work.
5. checker/README.md contradicts the proof ("mathematical conjecture, not a
   theorem") — the universal X^{1/2+eps} bound IS a theorem; the finite
   checker only tests the stronger empirical X^{1/2} model.
6. Computed range honesty: tests reach X=5000 (not 20000) and assert
   0.26 (not 0.259) — align README/witness claims or extend the checker.
7. Self-containment: witness/README references src/zero_free_arb.py and
   baseline/zero_free_scan.json which are not in the bundle — remove the
   references or ship the files.
8. C=0.259 must be conjectural beyond the computed range; the
   error <= 7.8e-5 line at N=10^8 must be prefixed "if one conjecturally
   assumes the global bound ...".
9. S1 interval [0.548298,0.548305] vs L(1,sym^2 Delta) ~ 0.6317–0.6326
   conflict: remove the specific L(1) numeric intervals from this batch;
   leave effective-L(1) to a dedicated batch.

Final positioning: an instantiation of literature theorems, not a new
theorem; mark the Q-11 math gate CLOSED/THEOREM; keep 0.259 as
discovery-tier only; next resources to explicit C(eps) or other rigorous
L(1) tail methods.
