# GL₃ Shifted Convolution — Novelty

## What is new in this package

1. **Precise sub-problem decomposition**: Splitting the research gap into
   09-A (individual, strongest) and 09-B (averaged transfer, most relevant).

2. **Corrected dependency logic**: 09 is a sufficient condition for M-1/M-2,
   not a necessary condition. The second moment may be achievable by other
   routes.

3. **Corrected literature synthesis**: DLY's averaged mechanism already gives
   non-trivial cancellation at our scale H = N^{1/3} > N^{1/4} for spherical
   GL₃. The real question is the holomorphic transfer, not "no power saving
   exists."

4. **Corrected Kloosterman description**: The DLY approach uses classical
   Kloosterman sums (GL₂-level) after GL₃ Voronoi, not GL₃ Kloosterman
   sums. Classical sums have Weil bounds. GL₃ sums also have non-trivial
   bounds for Weyl elements (Blomer–Man 2023).

5. **Corrected C_Π(h) claim**: Deleted the unsubstantiated claim that
   Rankin–Selberg decomposition gives a main term C_Π(h)·N for h ≠ 0.
   The diagonal (h=0) is controlled by Rankin–Selberg; the shifted case
   requires separate analysis.

## What is NOT new

- The GL₃ Kuznetsov/Voronoi formula is classical
- DLY's averaged shifted convolution result is in the literature
- The difficulty of the holomorphic transfer is implicit in the literature
- The Kloosterman bounds are classical results

## Previous errors corrected

| Error | Correction |
|-------|-----------|
| "C_Π(h)N from Rankin–Selberg" | Deleted; no main term established for h ≠ 0 |
| "Large sieve gives S ≪ N^{5/6}" | Deleted; the stated bound is not valid for individual shifted sums |
| "No power saving at critical scale" | Corrected: averaged problem has non-trivial DLY bound |
| "GL₃ Kloosterman only trivial" | Corrected: Weil-type bounds exist for Weyl elements |
| "Pal is current best" | Corrected: DLY is stronger in GL₃ scope |
| "Iwaniec–Kowalski = GL₃ Kuznetsov" | Corrected: use Blomer, Goldfeld–Kontorovich |
| "09 is necessary for M-1/M-2" | Corrected: sufficient, not necessary |
