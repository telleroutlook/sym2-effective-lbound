#!/usr/bin/env python3
"""
preflight_lint.py — Pre-flight mathematical lint for outsource packages.

Catches error categories identified in review cycles:
1. Scaling/homogeneity contradictions
2. Wrong main terms (e.g. cT vs T log T)
3. Missing mathematical objects (e.g. phase factors)
4. Wrong literature attribution
5. Wrong proof architecture (dependency direction)
6. False-positive checker detection
7. Conductor confusion (arithmetic vs analytic)
8. Scope errors (missing parameters)
9. Status label integrity
10. Reference verification
11. Package-specific required mathematical objects (OBJ-004)
12. Mathematical formula structural checks (MATH-001..003)

Usage:
    python3 preflight_lint.py <package_dir>
    python3 preflight_lint.py --all /tmp/obl-packages/
"""
import sys
import os
import re
import subprocess
from pathlib import Path


# ============================================================================
# Category 1: Scaling / homogeneity contradictions
# ============================================================================

SCALING_PATTERNS = [
    {
        "id": "SCALING-001",
        "desc": "Residue formula with independent W̃ and |W|² — scaling contradiction",
        "pattern": r"res.*\|W\|.*2",
        "context_hint": "W̃",  # If W̃ appears elsewhere, flag
        "severity": "FATAL",
        "fix": "Use W and conj(W) (same vector), not independent W̃",
    },
    {
        "id": "SCALING-002",
        "desc": "Integral linear in W̃ but RHS independent of W̃",
        "pattern": r"W[~̃].*res",
        "context_hint": "|W|",
        "severity": "FATAL",
        "fix": "RHS must depend on W̃ if integral does, or use conj(W)",
    },
]


# ============================================================================
# Category 2: Wrong main terms
# ============================================================================

MAIN_TERM_PATTERNS = [
    {
        "id": "MAIN-001",
        "desc": "GL₃ second moment main term cT (should be T log T for cuspidal)",
        "pattern": r"(?:main\s+term|equals?|gives?|is)\s*c[_\s]*(π|Π|pi)\s*\*?\s*\bt\b",
        "exclude_if": r"\blog\s*T|\bwrong\b|\bincorrect\b|\bis\s+not\b|\bclaimed\b|\boriginal\b|\bshould\s+be\b|\bactually\b|\bforbidden\b",
        "severity": "FATAL",
        "fix": "Rankin–Selberg pole at s=1 gives Σ|a(n)|²/n ~ R log X, so main term is T log T",
    },
    {
        "id": "MAIN-002",
        "desc": "Second moment claimed as cT + O(T^{1-δ}) without log factor",
        "pattern": r"∫.*\|L\|.*2.*=\s*c.*T\s*\+\s*O",
        "severity": "FATAL",
        "fix": "Main term for cuspidal GL₃ is A·T·log T + B·T + O(T^{1-δ})",
    },
]


# ============================================================================
# Category 3: Missing mathematical objects
# ============================================================================

MISSING_OBJECT_PATTERNS = [
    {
        "id": "OBJ-001",
        "desc": "Mollified moment squared without (n/m)^{it} phase",
        "pattern": r"\|M.*L\|.*2.*=.*∑.*b_m.*b.*n.*∫.*\|L\|.*2",
        "missing": r"\(n/m\)\^?\{?it\}?",
        "severity": "FATAL",
        "fix": "|M(½+it)L(½+it)|² produces (n/m)^{it} phase; cannot factor out ∫|L|²",
    },
    {
        "id": "OBJ-002",
        "desc": "Infinite Dirichlet series at Re s = ½ (doesn't converge absolutely)",
        "pattern": r"∑.*a[_\s]*Π.*\(n\).*n\^\{-s\}.*∑.*ā.*n\).*n\^\{.*s\}",
        "context_at": r"Re\s*s\s*=?\s*½|σ\s*=?\s*½",
        "severity": "FATAL",
        "fix": "Use approximate functional equation, not infinite Dirichlet series",
    },
    {
        "id": "OBJ-003",
        "desc": "Coefficient-square series equated to RS L-function without correction factors",
        "pattern": r"D[_\s]*Π.*=.*L.*Π.*×.*Π[~̃]",
        "severity": "ERROR",
        "fix": "D_Π(s) = L(s,Π×Π̃)·H_Π(s) with prime-specific H_{Π,p}(s)",
    },
]


# ============================================================================
# Category 4: Wrong literature attribution
# ============================================================================

WRONG_CITATION_PATTERNS = [
    {
        "id": "CITE-001",
        "desc": "Luo–Rudnick–Sarnak 1995 cited for GL₃ second moment (wrong paper)",
        "pattern": r"[Ll]uo.*[Rr]udnick.*[Ss]arnak.*(second|moment|asymptotic)",
        "exclude_if": r"\bnot\b|\bcorrect\b|\bwrong\b|\bfix\b|\brefuted\b|\bunsupported\b|\bremove\b",
        "severity": "ERROR",
        "fix": "LRS 1995 is 'On Selberg's eigenvalue conjecture' (GAFA), not second moment",
    },
    {
        "id": "CITE-002",
        "desc": "Iwaniec–Sarnak page numbers wrong",
        "pattern": r"Iwaniec.*Sarnak.*1039.*1065",
        "exclude_if": r"\bnot\b|\bcorrect\b|\bwrong\b|\bfix\b|\brefuted\b|\bcorrect\b",
        "severity": "ERROR",
        "fix": "Correct pages: GAFA 2000 Special Vol, pp. 705–741",
    },
    {
        "id": "CITE-003",
        "desc": "GL₃ spectral large sieve cited for fixed-form twisted moment",
        "pattern": r"large.sieve.*fixed|fixed.*large.sieve",
        "exclude_if": r"\bnot\b|\bcorrect\b|\bwrong\b|\bfix\b|\brefuted\b|\bforbidden\b|\bfamily\b|\bapplies.to\b",
        "severity": "ERROR",
        "fix": "GL₃ spectral large sieve applies to families, not fixed-Π twisted moments",
    },
    {
        "id": "CITE-004",
        "desc": "Hecke eigenvalue orthogonality for fixed Π (wrong object)",
        "pattern": r"[Hh]ecke.*orthogonal.*fixed|fixed.*[Hh]ecke.*orthogonal",
        "exclude_if": r"\bnot\b|\bcorrect\b|\bwrong\b|\bfix\b|\brefuted\b|\bforbidden\b|\bfamily\b|\bapplies.to\b",
        "severity": "ERROR",
        "fix": "Hecke orthogonality is for families; fixed Π uses t-integration",
    },
    {
        "id": "CITE-005",
        "desc": "GHL described as using mollifier strategy (they don't)",
        "pattern": r"GHL.*mollif|mollif.*GHL|Goldfeld.*Hoffstein.*mollif",
        "exclude_if": r"\bnot\b|\bcorrect\b|\bwrong\b|\bfix\b|\brefuted\b|\bunsupported\b|\bremove\b|\bdon.t\b",
        "severity": "WARNING",
        "fix": "GHL uses auxiliary Dirichlet series with non-negative coefficients, not mollifiers",
    },
    {
        "id": "CITE-006",
        "desc": "Jacquet–Shalika 1981 cited as Ann. Math. 114 (wrong journal)",
        "pattern": r"[Aa]nn\.?\s*[Mm]ath\.?\s*\.?\s*114.*1981|[Aa]nn\.?\s*[Mm]ath\.?\s*\.?\s*114.*459",
        "exclude_if": r"\bnot\b|\bwrong\b|\bfix\b|\bincorrect\b|\bsee\s+limitations\b|\bcorrected\b",
        "severity": "FATAL",
        "fix": "JS81 is Am. J. Math. 103(3) (1981), 499–558, NOT Ann. Math. 114",
    },
]


# ============================================================================
# Category 5: Wrong proof architecture
# ============================================================================

ARCHITECTURE_PATTERNS = [
    {
        "id": "ARCH-001",
        "desc": "Dependency direction reversed (needing output as input)",
        "pattern": r"l\(1.*ad\).*>.*0.*(implies|gives).*res",
        "exclude_if": r"\bnot\b|\bcorrect\b|\bwrong\b|\bfix\b|\brefuted\b|\breverse\b|\bbackward\b",
        "severity": "ERROR",
        "fix": "Residue positivity → identify L(1,Ad), not the reverse",
    },
    {
        "id": "ARCH-002",
        "desc": "Case 2 (exceptional zero) included for prime/trivial-char scope",
        "pattern": r"[Cc]ase\s*2.*exceptional|[Ee]xceptional.*[Cc]ase\s*2",
        "context_scope": r"prime.*trivial|trivial.*prime",
        "exclude_if": r"\bnot\b|\beliminat\b|\bremov\b|\bdoes.not\b|\bavoid\b|\bexclude\b|\babsent\b",
        "severity": "ERROR",
        "fix": "Prime level + trivial char eliminates GL(1)-lift; remove exceptional branch",
    },
    {
        "id": "ARCH-003",
        "desc": "Ordinary second moment + large sieve claimed sufficient for mollified moment",
        "pattern": r"ordinary.*second.*moment.*large.sieve|second.moment.*large.sieve",
        "exclude_if": r"\bnot\b|\bcorrect\b|\bwrong\b|\bfix\b|\brefuted\b|\binsufficient\b|\bresearch.frontier\b",
        "severity": "ERROR",
        "fix": "Mollified moment requires twisted/shifted-convolution analysis, not ordinary second moment",
    },
]


# ============================================================================
# Category 6: Conductor confusion
# ============================================================================

CONDUCTOR_PATTERNS = [
    {
        "id": "COND-001",
        "desc": "p² called 'analytic conductor' (it's arithmetic)",
        "pattern": r"p\^?2.*analytic.conductor|analytic.conductor.*p\^?2",
        "severity": "ERROR",
        "fix": "p² is arithmetic conductor; analytic conductor also depends on weight k",
    },
    {
        "id": "COND-002",
        "desc": "1/log p claimed independent of weight k",
        "pattern": r"1.*log\s*p(?!\s*\+\s*1)|c.*/log\s*p(?!\s*\+\s*1)",
        "exclude_if": r"kp|k\s*\*\s*p|weight.*fix|fix.*weight",
        "severity": "ERROR",
        "fix": "Use 1/log(kp+1) or fix k and allow constant to depend on k",
    },
]


# ============================================================================
# Category 7: Checker quality
# ============================================================================

CHECKER_PATTERNS = [
    {
        "id": "CHK-001",
        "desc": "Checker uses any() for concept matching (false-positive prone)",
        "pattern": r"any\(kw\s+in\s+content\s+for\s+kw\s+in",
        "severity": "ERROR",
        "fix": "Use phrase-level matching: 'phrase in _normalize(content)'",
    },
    {
        "id": "CHK-002",
        "desc": "Checker checks substring 'OBL' instead of exact '[OBL]' tag",
        "pattern": r'"OBL"\s+not\s+in\s+content|not\s+.*"OBL"',
        "severity": "WARNING",
        "fix": "Check for exact '[OBL]' tag, not substring 'OBL'",
    },
]


# ============================================================================
# Category 8: Forbidden content
# ============================================================================

FORBIDDEN_CONTENT = [
    {
        "id": "FORB-001",
        "desc": "Hardcoded internal paths or company names",
        "pattern": r"/Users/|/home/|sap\.corp|SAP",
        "severity": "ERROR",
        "fix": "Use relative paths or environment variables",
    },
    {
        "id": "FORB-002",
        "desc": "Self-declared PASS without checker verification",
        "pattern": r"self.declared.*PASS|PASS.*self.declared",
        "severity": "WARNING",
        "fix": "No PASS self-report; checker output is sole authority",
    },
]


# ============================================================================
# All patterns combined
# ============================================================================

ALL_PATTERNS = (
    SCALING_PATTERNS
    + MAIN_TERM_PATTERNS
    + MISSING_OBJECT_PATTERNS
    + WRONG_CITATION_PATTERNS
    + ARCHITECTURE_PATTERNS
    + CONDUCTOR_PATTERNS
    + CHECKER_PATTERNS
    + FORBIDDEN_CONTENT
)


# ============================================================================
# Category 10: Key mathematical object presence (package-specific)
# ============================================================================

# Maps package name prefix -> required objects (at least one must appear in proof files)
REQUIRED_OBJECTS = {
    "F-2": {
        "F-2A": [
            {"id": "OBJ-004a", "pattern": r"N\(A\).*GL", "desc": "Integral over N(A)\\GL₂(A)", "severity": "ERROR",
             "fix": "F-2A integral must be over N(A)\\GL₂(A), not N(A)G(Q)\\G(A)"},
            {"id": "OBJ-004b", "pattern": r"[Φφ].*e.?[2₂]\s*g", "desc": "Test function Φ(e₂g)", "severity": "ERROR",
             "fix": "Unfolded integral uses Φ(e₂g), not Φ(g)"},
            {"id": "OBJ-004c", "pattern": r"[Jj]acquet.*[Ss]halika|[Ss]halika.*[Jj]acquet", "desc": "Jacquet–Shalika attribution", "severity": "WARNING",
             "fix": "F-2A is a specialization of JS81; must cite it"},
        ],
        "F-2B": [
            {"id": "OBJ-004d", "pattern": r"[Pp]ure.?tensor|[Dd]ecomposable|[⊗⊕]\s*v", "desc": "Pure-tensor hypothesis", "severity": "ERROR",
             "fix": "Factorization ∏_v requires W = ⊗_v W_v"},
            {"id": "OBJ-004e", "pattern": r"[Aa]dj|adjoint", "desc": "Adjoint representation mentioned", "severity": "WARNING",
             "fix": "F-2B must discuss the Adjoint L-function"},
        ],
        "F-2C": [
            {"id": "OBJ-004f", "pattern": r"Γ_R\(2\)|π\^\{?-1\}?|π⁻¹|π\*\*\{-1\}", "desc": "Γ_R(2) = π⁻¹ correction", "severity": "ERROR",
             "fix": "Z_∞(1) must include Γ_R(2) = π⁻¹ factor"},
            {"id": "OBJ-004g", "pattern": r"[Nn]onvanish|explicit.*formula|direct.*comput", "desc": "Nonvanishing from explicit formulas", "severity": "WARNING",
             "fix": "Uniformity: min>0 requires explicit nonvanishing first"},
        ],
    },
    "M-1": [
        {"id": "OBJ-004h", "pattern": r"4.?variable|quadruple|convolution", "desc": "4-variable convolution structure", "severity": "ERROR",
         "fix": "M-1 must describe 4-variable convolution (ns≈mr)"},
        {"id": "OBJ-004i", "pattern": r"mollif", "desc": "Mollifier concept", "severity": "WARNING",
         "fix": "M-1 is the mollifier construction"},
    ],
    "M-2": [
        {"id": "OBJ-004j", "pattern": r"[Xx]_\{?.Π\}?.*\([st]\)|[Xx]_Π\([st]\)", "desc": "t-dependent dual factor X_Π(s/t)", "severity": "ERROR",
         "fix": "M-2 must use t-dependent X_Π(t/s), not constant χ(Π)"},
        {"id": "OBJ-004k", "pattern": r"H_\{?.Π.*p\}|H_Π", "desc": "Prime-specific H_{Π,p} factor", "severity": "ERROR",
         "fix": "M-2 must define H_{Π,p}(x) per prime"},
    ],
    "c_eff": [
        {"id": "OBJ-004l", "pattern": r"1.*log\(.*k.*p.*\+.*1\)|1.*log\(kp\+1\)", "desc": "Correct 1/log(kp+1) scope", "severity": "ERROR",
         "fix": "c_eff uses 1/log(kp+1), not 1/log p"},
        {"id": "OBJ-004m", "pattern": r"[Hh]offstein.*[Ll]ockhart|HL\s*1994", "desc": "Hoffstein–Lockhart route attribution", "severity": "WARNING",
         "fix": "c_eff follows HL1994 mollifier route"},
    ],
}


# ============================================================================
# Category 11: Mathematical formula correctness (structural checks)
# ============================================================================

FORMULA_CHECKS = [
    {
        "id": "MATH-001",
        "desc": "Adjoint L-function: single factor (should be 3 factors for GL₂)",
        "pattern": r"adjoint.*=.*\(1\s*[-−]\s*\w+\s*\w*\s*p\^\{-?s\}\)\^\{-?1\}\s*$",
        "context_hint": r"adjoint",
        "severity": "WARNING",
        "fix": "GL₂ adjoint has degree 3: [(1-x)(1-αβ⁻¹x)(1-βα⁻¹x)]⁻¹. Single factor is incomplete.",
    },
    {
        "id": "MATH-002",
        "desc": "Archimedean factor degree 3 (should be 4 for Rankin–Selberg)",
        "pattern": r"degree\s*:?\s*3.*rankin|z_∞.*degree\s*:?\s*3",
        "severity": "WARNING",
        "fix": "L(s,π×π̃) has degree 4 for GL₂. Z_∞ must include ζ_∞ factor.",
    },
    {
        "id": "MATH-003",
        "desc": "Continuity+compactness claimed to give min>0 without nonvanishing",
        "pattern": r"continuity.*compact.*min.*>|compact.*continuity.*positive|achieves?\s+min.*>.*0",
        "exclude_if": r"nonvanish|non.?zero|explicit.*formula|direct.*comput|known.*nonzero",
        "severity": "WARNING",
        "fix": "Continuity+compactness gives min≥0. To get min>0, must first prove nonvanishing.",
    },
]


def scan_file(filepath, patterns):
    """Scan a single file against all patterns."""
    if not os.path.exists(filepath):
        return []
    basename = os.path.basename(filepath)
    # Skip checker files — they legitimately contain forbidden patterns
    if basename.startswith("check_") and basename.endswith(".py"):
        return []
    content = open(filepath).read()
    content_lower = content.lower()
    findings = []
    for pat in patterns:
        if re.search(pat["pattern"], content_lower):
            # Check exclusions
            if "exclude_if" in pat and re.search(pat["exclude_if"], content_lower):
                continue
            # Check context hints
            if "context_hint" in pat:
                if pat["context_hint"].lower() not in content_lower:
                    continue
            if "context_scope" in pat:
                if pat["context_scope"].lower() not in content_lower:
                    continue
            findings.append({
                "id": pat["id"],
                "severity": pat["severity"],
                "desc": pat["desc"],
                "fix": pat["fix"],
                "file": os.path.basename(filepath),
            })
    return findings


def scan_required_objects(pkg_dir, pkg_name):
    """Check that key mathematical objects appear in proof files."""
    findings = []
    # Match package name prefix (e.g. "F-2" from "F-2-global-residue")
    matched_key = None
    for key in REQUIRED_OBJECTS:
        if pkg_name.startswith(key):
            matched_key = key
            break
    if matched_key is None:
        return findings

    entries = REQUIRED_OBJECTS[matched_key]
    # If entries is a dict (sub-packages like F-2A/F-2B/F-2C), iterate each
    if isinstance(entries, dict):
        for sub_key, required in entries.items():
            # Find matching proof/statement files
            proof_file = os.path.join(pkg_dir, f"proof-{sub_key}.md")
            stmt_file = os.path.join(pkg_dir, f"statement-{sub_key}.md")
            targets = []
            if os.path.exists(proof_file):
                targets.append(proof_file)
            if os.path.exists(stmt_file):
                targets.append(stmt_file)
            if not targets:
                # No sub-package files found; skip
                continue
            # Use RAW content (not .lower()) to preserve Unicode subscripts/symbols
            combined = " ".join(open(f).read() for f in targets)
            for req in required:
                if not re.search(req["pattern"], combined, re.IGNORECASE):
                    findings.append({
                        "id": req["id"],
                        "severity": req["severity"],
                        "desc": req["desc"],
                        "fix": req["fix"],
                        "file": f"{sub_key} (statement/proof)",
                    })
    else:
        # Flat list (e.g. M-1, M-2, c_eff)
        # Check all .md files in the package
        md_files = list(Path(pkg_dir).glob("*.md"))
        combined = " ".join(open(f).read() for f in md_files)
        for req in entries:
            if not re.search(req["pattern"], combined, re.IGNORECASE):
                findings.append({
                    "id": req["id"],
                    "severity": req["severity"],
                    "desc": req["desc"],
                    "fix": req["fix"],
                    "file": f"{pkg_name} (*.md)",
                })
    return findings


def scan_package(pkg_dir):
    """Scan all files in a package."""
    findings = []
    md_files = list(Path(pkg_dir).rglob("*.md"))
    py_files = list(Path(pkg_dir).rglob("*.py"))
    yaml_files = list(Path(pkg_dir).rglob("*.yaml"))

    for f in md_files + py_files + yaml_files:
        findings.extend(scan_file(str(f), ALL_PATTERNS + FORMULA_CHECKS))
    return findings


def check_checker_quality(pkg_dir):
    """Verify the package's own checker is not false-positive prone."""
    findings = []
    checker_files = list(Path(pkg_dir).rglob("check_*.py"))
    for cf in checker_files:
        content = open(cf).read()
        if "any(kw in" in content:
            findings.append({
                "id": "CHK-001",
                "severity": "ERROR",
                "desc": f"Checker {cf.name} uses any() — false-positive prone",
                "fix": "Use phrase-level matching",
                "file": cf.name,
            })
        if '"OBL" not in content' and "[OBL]" not in content:
            pass  # OK if checking for [OBL]
        if re.search(r'"OBL"\s+not\s+in\s+content', content):
            findings.append({
                "id": "CHK-002",
                "severity": "WARNING",
                "desc": f"Checker {cf.name} checks substring 'OBL' not exact '[OBL]'",
                "fix": "Check for exact '[OBL]' tag",
                "file": cf.name,
            })
    return findings


def check_test_coverage(pkg_dir):
    """Verify tests exist and cover key scenarios."""
    findings = []
    test_files = list(Path(pkg_dir).rglob("test_*.py"))
    if not test_files:
        findings.append({
            "id": "TEST-001",
            "severity": "WARNING",
            "desc": "No test files found",
            "fix": "Add tests/test_checker.py",
            "file": "tests/",
        })
        return findings

    for tf in test_files:
        content = open(tf).read()
        # Check for adversarial test (trivial content should fail)
        if "trivial" not in content.lower() and "adversarial" not in content.lower():
            findings.append({
                "id": "TEST-002",
                "severity": "WARNING",
                "desc": f"{tf.name}: No adversarial/trivial-content test",
                "fix": "Add test that trivial content FAILS the checker",
                "file": tf.name,
            })
        # Check for negative test (known-bad content should fail)
        if "assert code == 1" not in content and "assert code != 0" not in content:
            findings.append({
                "id": "TEST-003",
                "severity": "WARNING",
                "desc": f"{tf.name}: No negative test (known-bad → FAIL)",
                "fix": "Add test verifying known-bad input is rejected",
                "file": tf.name,
            })
    return findings


def check_manifest(pkg_dir):
    """Verify MANIFEST.sha256 exists and is non-empty."""
    manifest = os.path.join(pkg_dir, "MANIFEST.sha256")
    if not os.path.exists(manifest):
        return [{
            "id": "MANIFEST-001",
            "severity": "ERROR",
            "desc": "MANIFEST.sha256 missing",
            "fix": "Generate with: find . -type f | xargs sha256sum > MANIFEST.sha256",
            "file": "MANIFEST.sha256",
        }]
    if os.path.getsize(manifest) == 0:
        return [{
            "id": "MANIFEST-002",
            "severity": "ERROR",
            "desc": "MANIFEST.sha256 is empty",
            "fix": "Regenerate manifest",
            "file": "MANIFEST.sha256",
        }]
    return []


def print_report(pkg_name, findings):
    """Print structured lint report."""
    if not findings:
        print(f"\n{'='*60}")
        print(f"  {pkg_name}: CLEAN — no issues found")
        print(f"{'='*60}")
        return True

    fatal = [f for f in findings if f["severity"] == "FATAL"]
    errors = [f for f in findings if f["severity"] == "ERROR"]
    warnings = [f for f in findings if f["severity"] == "WARNING"]

    print(f"\n{'='*60}")
    print(f"  {pkg_name}: {len(findings)} issues "
          f"({len(fatal)} FATAL, {len(errors)} ERROR, {len(warnings)} WARNING)")
    print(f"{'='*60}")

    for f in findings:
        icon = {"FATAL": "🔴", "ERROR": "🟠", "WARNING": "🟡"}[f["severity"]]
        print(f"\n  {icon} [{f['id']}] {f['severity']}: {f['desc']}")
        print(f"     File: {f['file']}")
        print(f"     Fix:  {f['fix']}")

    return len(fatal) == 0 and len(errors) == 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python preflight_lint.py <package_dir_or_all>")
        print("       python preflight_lint.py --all /tmp/obl-packages/")
        sys.exit(1)

    if sys.argv[1] == "--all":
        base = sys.argv[2] if len(sys.argv) > 2 else "/tmp/obl-packages/"
        skip = {"__pycache__", ".git", "src", ".pytest_cache"}
        pkgs = [d for d in Path(base).iterdir()
                if d.is_dir() and d.name not in skip]
    else:
        pkgs = [Path(sys.argv[1])]

    all_clean = True
    for pkg in sorted(pkgs):
        pkg_name = pkg.name
        findings = []
        findings.extend(scan_package(str(pkg)))
        findings.extend(scan_required_objects(str(pkg), pkg_name))
        findings.extend(check_checker_quality(str(pkg)))
        findings.extend(check_test_coverage(str(pkg)))
        findings.extend(check_manifest(str(pkg)))
        clean = print_report(pkg_name, findings)
        if not clean:
            all_clean = False

    print(f"\n{'='*60}")
    if all_clean:
        print("  OVERALL: ALL PACKAGES CLEAN")
    else:
        print("  OVERALL: ISSUES FOUND — fix before externalizing")
    print(f"{'='*60}")

    sys.exit(0 if all_clean else 1)


if __name__ == "__main__":
    main()
