# Baseline References

This directory records verified theorem statements for results admitted as [BASE].

Before any [BASE] theorem is used in a proof, the exact statement must be verified
against a primary source and recorded in `REFERENCE_BASELINE.md`. "I remember
what it says" is not a pass.  Source PDFs are deliberately not committed; the
ledger records the inspected edition, URL, theorem/proposition number, page,
statement, and downstream impact.

## Currently tracked exact statements

| Ledger ID | Reference | Exact theorem used | Current verdict |
|-----------|-----------|--------------------|----------------|
| GHL-A.1 | Goldfeld--Hoffstein--Lieman, Ann. Math. 140 (1994), appendix | Main Theorem, pp. 177--178 | supported |
| MS-V.1 | Miller--Schmid, Ann. Math. 164 (2006) | Theorem 1.18, pp. 427--428 | supported |
| GJ-9.3 | Gelbart--Jacquet, Ann. Sci. ENS 11 (1978) | Theorem (9.3), pp. 532--533 | supported under non-self-twist hypothesis |
| CS-W.1 | Casselman--Shalika, Compositio Math. 41 (1980) | Theorem 5.4, p. 227 | supported |
| JS-LI.1 | Jacquet--Shalika, Amer. J. Math. 103 (1981) | Proposition (2.3), pp. 511--512 | supported |
| JS-EP.1 | Jacquet--Shalika, Amer. J. Math. 103 (1981) | Theorem (5.3), pp. 555--556 | supported |
| SH-AD.1 | Shahidi, Amer. J. Math. 103 (1981) | sought but not found | not-found |
| JS-GF.1 | Jacquet--Shalika, Amer. J. Math. 103 (1981) | sought global positive-correction bridge | not-found |

Rule: no [BASE] theorem may enter the proof chain without exact source-level
evidence in the ledger.  A `not-found` row blocks the dependent claim.
