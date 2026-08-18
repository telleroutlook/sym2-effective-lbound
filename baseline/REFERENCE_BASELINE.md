# Reference baseline ledger

This ledger records the external claims actually used by the proof and discovery
layers.  It distinguishes a source-backed claim from a bibliographic pointer.
A row below does not itself promote an obligation to `[THM]`; it only records
the current evidence level for the cited input.

Verification date: 2026-08-18.  PDFs are intentionally not committed to this
repository.  The source URLs below were downloaded for personal verification and
processed with `pdftotext` or page OCR; no paywalled content is redistributed.

## Verdict key

- `supported`: the exact used statement, including hypotheses, occurs in the cited source.
- `stronger-in-source`: the source proves at least the used statement under compatible hypotheses.
- `weaker-in-source`: the source supports only part of the used statement.
- `source-unavailable`: no primary text could be inspected; the claim must not be used for release.

## Claim table

| ID | Claim as used | Primary source checked | Verdict | Downstream impact |
|---|---|---|---|---|
| GHL-A.1 | For a non-GL(1)-lift newform `f`, its adjoint-square lift `F` satisfies `L(1,F) >= c_1/log(AN+1)` with effective absolute constants; the appendix remark extends the argument to holomorphic forms and states that there are no GL(1) lifts for prime level and trivial central character. | Goldfeld--Hoffstein--Lieman, *Appendix: An effective zero-free region*, Ann. of Math. (2) **140** (1994), 177--181, Main Theorem and following Remark, pp. 177--178. Public scan: <https://www.math.columbia.edu/~goldfeld/EffectiveZeroFreeRegion.pdf>. | supported | Validates the research target and the prime-level generic setting, but gives no explicit numerical `c_1`; M-3/E-1 remain `[OBL]`. |
| MS-V.1 | For cuspidal `GL(3,Z)`, additive twists of Schwartz functions satisfy the exact dual sum involving `S(q a_bar,n; qc/d)`, `A(n,d)`, and the normalized transform `F(nd^2/(c^3 q))` in Miller--Schmid Theorem 1.18. | Miller--Schmid, *Automorphic distributions, L-functions, and Voronoi summation for GL(3)*, Ann. of Math. (2) **164** (2006), 423--488, Theorem 1.18, esp. pp. 427--428. Public PDF: <https://annals.math.princeton.edu/wp-content/uploads/annals-v164-n2-p02.pdf>. | supported | M-Voronoi and the `C_GL3` derivation must start from this exact normalization. It does not by itself supply any explicit decay constant. |
| GJ-9.3 | A non-dihedral cuspidal automorphic representation of GL(2) has an essentially unique automorphic cuspidal adjoint lift to GL(3) with the prescribed adjoint Satake classes. | Gelbart--Jacquet, *A relation between automorphic representations of GL(2) and GL(3)*, Ann. Sci. ENS (4) **11** (1978), 471--542, Theorem (9.3), pp. 532--533. Numdam PDF: <https://www.numdam.org/item/10.24033/asens.1355.pdf>. | supported (conditional on the theorem's non-self-twist hypothesis) | Supports automorphy for non-CM/non-dihedral inputs. It does not make bad local factors or the conductor constant explicit. |
| JS-EP.1 | If `pi` and `pi'` are irreducible unitary cuspidal representations of `GL_r(A_F)` and `GL_p(A_F)`, then the incomplete Rankin--Selberg Euler product `L_S(s,pi x pi')` converges absolutely and is nonzero in `Re(s) > 1`. | Jacquet--Shalika, *On Euler products and the classification of automorphic representations I*, Amer. J. Math. **103** (1981), 499--558, Theorem (5.3), pp. 555--556 (article pp. 499--558). Public scan: <https://www.math.columbia.edu/~hj/On%20Euler%20products%20I.pdf>. | supported | This is now theorem-level evidence for absolute convergence. It does not describe the residue at `s=1`, so it does not close F-2. |
| CS-W.1 | For an unramified split reductive group, the normalized essential Whittaker function on the dominant cocharacter `a_J` is the modulus factor `delta^{1/2}(a_J)` times `Tr rho_J(A)`, where `rho_J` is the representation with highest weight `J` and `A` is the Satake class. | Casselman--Shalika, *The unramified principal series of p-adic groups II: The Whittaker function*, Compositio Math. **41** (1980), 207--231, Theorem 5.4, p. 227. Jacquet--Shalika 1981, §2.2, especially formula (2.2.2), p. 511, transcribes the same formula for `GL_r`. Public scan: <https://personal.math.ubc.ca/~cass/research/pdf/casselman-shalika.pdf>. | supported | Specializing `r=2`, `J=(l,0)`, and the standard Haar measure gives the `q_v^{-l/2} chi_l(alpha_v,beta_v)` normalization used by F-1. This closes the previous normalization mismatch at unramified places. |
| JS-LI.1 | For generic unramified `GL_r` data, the Jacquet--Shalika local integral with essential Whittaker functions and characteristic-function test vector equals `L_v(s,pi x pi')`, under the source's measure normalization. | Jacquet--Shalika, 1981, Proposition (2.3), pp. 511--512, following the formula displayed in §(2.2). Public scan: <https://www.math.columbia.edu/~hj/On%20Euler%20products%20I.pdf>. | supported | Gives the exact unramified local integral used in F-1. It does not control ramified or archimedean correction factors. |
| JS-GF.1 | The particular global factorization in proof/02, including explicit correction factors at every place in `S` and positivity of their values at `s=1`, follows from Jacquet--Shalika 1981. | Jacquet--Shalika 1981, §4.5--§4.7, pp. 550--552, gives the global integral, its Euler product for pure tensors, and Lemma (4.6) on a simple pole; §§1.5 and 3.17 give local nonvanishing. Public scan: <https://www.math.columbia.edu/~hj/On%20Euler%20products%20I.pdf>. | not-found | The source supports the global integral, pure-tensor factorization, and pole criterion, but does not state the explicit positive correction factors or residue formula asserted by F-2. A complete local positivity/normalization bridge is still required; F-2 remains `[OBL]`. |
| SH-AD.1 | `L(1,pi,Ad)` is positive for every generic cuspidal GL(2) representation. | Shahidi, *On certain L-functions*, Amer. J. Math. **103** (1981), 297--355. Author scan: <https://www.math.purdue.edu/~fshahidi/articles/Shahidi%20%5B1981,%2059pp%5D---On%20certain%20L-functions.pdf>, Theorems 5.2--5.3, pp. 352--354. | not-found | The paper is now source-backed, but the inspected theorems state nonvanishing for Jacquet--Shalika pair L-functions and for symmetric third/fourth powers; they do not verbatim establish the claimed `L(1,Ad)>0`. F-2's positivity input remains blocked until the exact theorem is located or a complete bridge is proved. |
| SH-RS.1 | The incomplete Rankin--Selberg pair Euler product `L_S(1+it,pi x pi')` is nonzero for every real `t`. | Shahidi, *On nonvanishing of L-functions*, Bull. Amer. Math. Soc. (N.S.) **2** (1980), 462--464, Theorem, p. 462. AMS PDF: <https://www.ams.org/journals/bull/1980-02-03/S0273-0979-1980-14769-2/S0273-0979-1980-14769-2.pdf>. | supported | This is a useful related input. For `pi'=pi~` and trivial central character it concerns `zeta(s)L(s,pi,Ad)`, so a zero of `L(1,Ad)` may cancel the zeta pole. It does not alone imply SH-AD.1. |
| SH-S2.1 | The symmetric-square Dirichlet series has the asserted holomorphic continuation and functional equation. | Shimura, *On the holomorphy of certain Dirichlet series*, Proc. London Math. Soc. (3) **31** (1975), 79--98. DOI: <https://doi.org/10.1112/plms/s3-31.1.79>. | source-unavailable | Not verified against primary text. For non-dihedral forms, GJ-9.3 supplies a related automorphic route, but bad-place and archimedean normalizations remain unchecked. |
| HL-SZ.1 | The preceding Hoffstein--Lockhart zero-free/exceptional-zero argument. | Hoffstein--Lockhart, *Coefficients of Maass forms and the Siegel zero*, Ann. of Math. (2) **140** (1994), 161--176. Article page: <https://annals.math.princeton.edu/1994/140-1/p04>. | source-unavailable | The GHL appendix supplies enough to state the effective generic appendix theorem, but any independent use of the preceding HL main theorem still requires its primary text. |
| DEL-R.1 | `|tau(n)| <= d(n) n^{11/2}`. | Deligne, *La conjecture de Weil I*, Publ. Math. IHES **43** (1974), 273--307. | source-unavailable | Used by `src/certified_rs.py` for upper intervals at `s>1`; before publishing that certificate, verify the normalized eigenvalue version and divisor-majorization step from the primary source. |

## Source excerpts checked

### GHL Main Theorem

OCR of the public scan, p. 177--178, gives:

> Suppose that `f` is not a lift from `GL (1)`. Then there exist effective
> constants `c_1` and `c_2` such that `L(1,F) >= c_1/log(AN+1)` and
> `|rho(1)|^2 < c_2 log(AN+1)`.

The immediately following remark says:

> As in the previous paper, all the arguments go through for holomorphic `f`
> or Maass forms with weight. In fact the above bounds can be made uniform in
> the weight, as well as the level and eigenvalue.

It also states that there are no GL(1) lifts in `SL(2,Z)` or in `Gamma_0(N)`
when `N` is prime and the central character is trivial.

### Miller--Schmid Theorem 1.18

The theorem begins with cuspidal `GL(3,Z)` Fourier coefficients `a_{n,m}`,
representation parameters `(lambda, delta)`, `(a,c)=1`, `c != 0`, and a Schwartz
function vanishing to infinite order at the origin. Its identity has the form

```text
sum_{n!=0} a_{q,n} e(-n a/c) f(n)
  = sum_{d | c q} |c/d| * sum_{n!=0}
      A(n,d) / |n| * S(q a_bar, n; q c/d)
      * F(n d^2 / (c^3 q)).
```

The source then defines the Kloosterman sum and the normalized transform `F` as
a threefold integral (or equivalently by the displayed Mellin--Bessel identity).
Any `C_GL3` derivation must retain the `A(n,d)/|n|` factor and the argument
`n d^2/(c^3 q)`.  Older heuristic `c^{-2} K_nu` estimates are not a quotation of
this theorem.

### Gelbart--Jacquet Theorem (9.3)

The theorem assumes a unitary irreducible automorphic cuspidal representation
`sigma` of `GL(2,A)` such that `sigma` and `sigma tensor chi` are inequivalent
for every nontrivial character `chi`. It concludes that the relevant degree-three
`L`-functions are entire, local lifts exist, their restricted tensor product is
automorphic cuspidal, and the listed complementary-series components do not occur.

### Jacquet--Shalika exact statements

OCR of the JSTOR scan gives the following theorem-level statements.

The unramified Whittaker normalization in §2.2, p. 511, says that for the
essential vector `W`,

```text
W(a_J) = delta^{1/2}(a_J) Tr(rho_J(A))
```

for `J in T_+(r)`, and `W(a_J)=0` otherwise.  Proposition (2.3), pp. 511--512,
then states that the local integral with both essential Whittaker functions and
the characteristic function of `R^r` equals `L_v(s,pi x pi')` (source notation
`L_s(s,pi x pi')`).  The measures are normalized by `vol(N R K)=vol(K)=1`.

Theorem (5.3), pp. 555--556, states that for irreducible unitary cuspidal
representations `pi` and `pi'`, the product `L_S(s,pi x pi')` is absolutely
convergent in `Re(s)>1`; in particular it is nonzero there.

Section 4.5--4.7, pp. 550--552, defines the global Whittaker integral, factors
it as a product of local integrals for pure tensors, and proves Lemma (4.6):
it is meromorphic, holomorphic for `Re(s)>1`, has a simple pole at `s=1` when
`pi'=pi~`, the global test function has nonzero Fourier transform at zero, and
the Whittaker vector is nonzero; conversely such a pole forces `pi'=pi~`.
These are strong inputs, but the paper does not supply the explicit local
correction factors or their positivity asserted in the current F-2 formula.

### Shahidi Theorems 5.2 and 5.3

OCR of pp. 353--354 gives:

> **Theorem 5.2.** Let `pi` and `pi'` be irreducible admissible cuspidal
> non-degenerate representations... Then for every real `t`,
> `L_S(1+it,pi x pi')` is non-zero.

> **Theorem 5.3.** Let `pi` be an irreducible cuspidal representation of
> `PGL_2(A)`. Suppose `pi` is not monomial. Then the L-functions
> `L_S(s,pi,Sym^3(rho_2))` and `L_S(s,pi,Sym^4(rho_2))` do not vanish on
> `Re(s)=1`, except for the second L-function and possibly only at `s=1`, in
> which case the zero is at most simple.

Neither statement is the exact positivity input used by proof/02.  Passing from
Theorem 5.2 to the adjoint factor at `t=0` encounters the zeta pole and is not
an immediate substitution.  This is a substantive baseline mismatch, not a
formatting issue.

## Consequences

1. The source-backed research inputs include the GHL appendix theorem,
   Miller--Schmid Theorem 1.18, Gelbart--Jacquet Theorem 9.3, and Shahidi's
   pair-nonvanishing theorem.  As transcribed here, none gives an explicit
   numerical constant for this repository's effective bound.
2. F-1's external Casselman--Shalika input is now source-backed at theorem
   level.  F-2 remains `[OBL]`: SH-AD.1 is still `not-found`, and JS-GF.1's
   explicit positive local correction/residue bridge has not been supplied.
3. `src/certified_rs.py` internally checks arithmetic, but its Deligne input is
   not yet source-backed.  Its `s>1` intervals should be called provisional in
   any external report until DEL-R.1 is verified.
