"""Regression tests for repository-wide mathematical status honesty."""

import ast
from pathlib import Path

from checker.check_bound import check_certificate, check_tail_bound


ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_specification_keeps_f3_open():
    spec = _read("spec/SPECIFICATION.md")
    assert "### 2.3 Instance Certification [OBL]" in spec
    assert "[THM] (F-3)" not in spec
    assert "No positive lower bound for" in spec


def test_retracted_delta_certificate_is_not_promoted():
    combined = "\n".join(
        _read(path)
        for path in (
            "spec/SPECIFICATION.md",
            "proof/04-effective-bound.tex",
            "proof/paper.tex",
        )
    )
    assert "L(1, sym^2 Delta) >= 2.405" not in combined
    assert "L(1,\\mathrm{sym}^2\\Delta) \\geq 2.405" not in combined
    assert "in [2.405, 2.407]" not in combined
    assert "\\in [2.405,\\, 2.407]" not in combined


def test_checker_rejects_divergent_euler_product_tail():
    ok, message = check_tail_bound(
        {
            "euler_product_cutoff": 97,
            "tail_bound": {
                "method": "ramanujan-deligne",
                "constant": 3.0,
                "bound_value": 3.0 / 97.0,
            },
        }
    )
    assert not ok
    assert "diverges" in message


def test_checker_rejects_a_fabricated_positive_l1_bound():
    certificate = {
        "form": {
            "weight": 12,
            "level": 1,
            "label": "fabricated Delta certificate",
            "hecke_coefficients": {"2": -24},
        },
        "bound": 0.5,
        "euler_product_cutoff": 2,
        "tail_bound": {
            "method": "ramanujan-deligne",
            "constant": 3.0,
            "bound_value": 1.5,
        },
        "euler_product_interval": [1.0, 2.0],
        "arb_precision_bits": 128,
        "checker_version": "1.0.0",
    }
    assert not check_certificate(certificate, verbose=False)


def test_voronoi_sketch_remains_open_and_records_exact_source_theorem():
    source = _read("discovery/_voronoi_proof_sketch.py")
    assert "Miller-Schmid" in source
    assert "Theorem 1.18" in source
    assert "F(n d^2 / (c^3 q))" in source
    assert "certification is effectively done" not in source
    assert "CONDITIONAL CERTIFIED" not in source


def test_checker_does_not_import_src():
    for path in (ROOT / "checker").glob("*.py"):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        imported_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_names.add(node.module)
        assert not any(name == "src" or name.startswith("src.") for name in imported_names), (
            f"forbidden import in {path}: {sorted(imported_names)}"
        )


def test_pointwise_positivity_is_not_promoted_to_exceptional_zero_exclusion():
    combined = "\n".join(
        _read(path)
        for path in (
            "spec/SPECIFICATION.md",
            "proof/02-global-residue.tex",
            "proof/03-mollifier.tex",
            "proof/04-effective-bound.tex",
            "proof/paper.tex",
        )
    )
    assert "excluded by Theorem~F-2" not in combined
    assert "contradicts Theorem~F-2" not in combined
    assert "eliminates the Siegel zero case" not in combined
    assert "pointwise" in combined.lower()


def test_voronoi_obligation_and_baseline_ledger_exist():
    obligation = _read("proof/05-voronoi-constant.tex")
    assert "Status: [OBL]" in obligation
    assert "nd^2}{c^3q" in obligation
    assert "C_{\\mathrm{Vor}}" in obligation

    ledger = _read("baseline/REFERENCE_BASELINE.md")
    assert "| SH-AD.1 |" in ledger
    assert "| not-found |" in ledger
    assert "| MS-V.1 |" in ledger
    assert "| supported |" in ledger
