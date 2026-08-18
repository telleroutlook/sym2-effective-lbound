# PAPER_LINT.md — Pre-submission lint for sym² L-function paper(s)

Two-layer architecture: **Reactive** (P1–P20, grep-based specific checks) and
**Proactive** (S1–S5, structural completeness per theorem). Run both before
every arXiv push or journal submission.

## Precedent

Adapted from the abc-conjecture-verification project's PAPER_LINT.md
(P1–P38 reactive + S1–S5 proactive), specialised for the sym² effective
lower bound paper(s).

---

## Part I: Gate checks (run once per paper)

### P1 — No [OBL] items promoted to [THM]

```bash
grep -n '\[OBL\]' proof/paper.tex proof/04-effective-bound.tex
```

Must return 0 matches. Any [OBL] in a theorem statement blocks submission.

### P2 — Status labels are present on all major claims

```bash
grep -cE '\[(THM|OBL|DEF|BASE|OUT)\]' proof/paper.tex
```

Must be ≥ 5 (at least F-1 [THM], F-2 [OBL], F-3 [OBL], plus definitions).

### P3 — No discovery/ imports in proof/

```bash
grep -rn 'discovery/' proof/
```

Must return empty.

### P4 — No mpmath/float used as certified arithmetic in proof/

```bash
grep -iE 'mpmath|float\(\)|numpy' proof/paper.tex
```

Must return empty.

### P5 — No reference to [OBL M-3] or [OBL E-2] as if proved

```bash
grep -n 'M-3\|E-2' proof/paper.tex | grep -v '\[OBL\]'
```

Must return empty (every M-3/E-2 mention must carry [OBL]).

---

## Part II: Per-theorem structural audit

### S1 — Definition completeness

For every theorem/lemma/proposition, verify that all symbols are defined
before use. Check:

```bash
grep -n '\\begin{theorem}\|\\begin{lemma}\|\\begin{proposition}' proof/paper.tex
```

For each match, trace backwards to confirm every symbol has a [DEF] or [BASE].

### S2 — Citation completeness

For every cited result, verify a matching row in baseline/REFERENCE_BASELINE.md:

```bash
grep -oP 'cite\{[^}]+\}' proof/paper.tex | sort -u
```

Cross-check each citation key against REFERENCE_BASELINE.md IDs.

### S3 — No untagged claims

```bash
grep -n '\\newcommand\|\\renewcommand' proof/paper.tex
```

Ensure no custom commands hide status tags.

### S4 — Abstract consistency

The abstract must not claim more than the body proves. Check:

```bash
grep -A5 'abstract' proof/paper.tex
```

Verify: no "we prove" for [OBL] items; no numerical values without "discovery-tier".

### S5 — Table of contents consistency

Verify every \section, \subsection appears and has a matching status tag.

---

## Part III: Technical content sweeps

### P6 — No unqualified "L(1) > 0" claims

```bash
grep -n 'L(1.*> *0\|L(1.*positive' proof/paper.tex
```

Must return empty unless tagged [THM] with a valid proof.

### P7 — No unretracted F-3 old claims

```bash
grep -n '2\.405\|2\.407' proof/paper.tex
```

Must return empty (the old [2.405, 2.407] interval is retracted).

### P8 — Rankin–Selberg identity includes ζ(2s) denominator

```bash
grep -n 'zeta(2s)\|ζ(2s)' proof/paper.tex
```

Must return ≥ 1 match (the ζ(2s)^{-1} factor is mandatory).

### P9 — Gamma factor convention matches spec

```bash
grep -n 'Gamma_R\|Gamma_C\|Γ_R\|Γ_C' proof/paper.tex
```

Must use Γ_R(s) = π^{-s/2}Γ(s/2) and Γ_C(s) = 2(2π)^{-s}Γ(s), and
G(s) = Γ_R(s) × Γ_C(s+11).

### P10 — C_GL3 not claimed without [OBL]

```bash
grep -n 'C_GL3\|C_{GL3}' proof/paper.tex | grep -v '\[OBL\]'
```

Must return empty unless a complete proof is provided.

### P11 — S1 certificate width stated

```bash
grep -n '0\.548' proof/paper.tex
```

If S1 values appear, the interval width (≈ 7.0 × 10⁻⁶) must be stated.

### P12 — No "approximately" for certified values

```bash
grep -iE 'approximately|roughly|about' proof/paper.tex | grep -v 'discovery\|numerical anchor'
```

Must return empty or only in discovery-tier context.

---

## Part IV: Citation and reference checks

### P13 — All bibtex keys resolve

```bash
grep -oP '@\w+\{[^,]+' proof/paper.tex | awk -F'{' '{print $2}' | sort -u
```

Cross-check against bib file entries.

### P14 — GHL citation includes exact theorem number

```bash
grep -n 'Goldfeld.*Hoffstein\|GHL' proof/paper.tex
```

Every GHL mention must reference "Ann. of Math. (2) 140 (1994), 177–181".

### P15 — Miller–Schmid citation includes Theorem 1.18

```bash
grep -n 'Miller.*Schmid' proof/paper.tex
```

Must reference "Ann. of Math. (2) 164 (2006), 423–488, Theorem 1.18".

### P16 — Casselman–Shalika citation includes Theorem 5.4

```bash
grep -n 'Casselman.*Shalika' proof/paper.tex
```

Must reference "Compositio Math. 41 (1980), 207–231, Theorem 5.4".

### P17 — Jacquet–Shalika citation includes Proposition 2.3

```bash
grep -n 'Jacquet.*Shalika' proof/paper.tex
```

Must reference "Amer. J. Math. 103 (1981), 499–558, Proposition 2.3".

### P18 — No fabricated references

```bash
grep -oP '@\w+\{[^}]+' proof/paper.tex | sort -u
```

Every entry must be a real publication. Cross-check with REFERENCE_BASELINE.md.

---

## Part V: Forbidden patterns

### P19 — No composite status labels

```bash
grep -E '\[[A-Z]+ +[A-Z]+\]' proof/paper.tex
```

Must return empty.

### P20 — No self-declared lower bounds

```bash
grep -n '≥.*c.*log\|≥.*effectiv\|L(1.*≥' proof/paper.tex | grep -v '\[OBL\]'
```

Must return empty unless the bound has a complete [THM] proof.

---

## Workflow

1. **Part I gate checks (P1–P5):** all must PASS. A FAIL blocks submission.
2. **Part II structural (S1–S5):** per-theorem audit. Record findings.
3. **Part III technical (P6–P12):** content sweeps. Fix any FAIL.
4. **Part IV citation (P13–P18):** reference verification.
5. **Part V forbidden (P19–P20):** final guard.
6. Record output in `papers/paper_lint_output.md` with date.
