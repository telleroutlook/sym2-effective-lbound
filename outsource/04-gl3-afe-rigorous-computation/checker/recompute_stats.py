#!/usr/bin/env python3
"""Machine-derive min/max statistics from witness/grid_values.json.

Per the 2026-08-19 external review: proof/witness summaries must never be
hand-copied; this script is the single source for them. The JSON stores a
certificate header plus a grid array; both sources are cross-checked.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    path = (
        Path(__file__).resolve().parents[1] / "witness" / "grid_values.json"
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    grid = data["grid"] if isinstance(data, dict) and "grid" in data else None
    if grid is None:
        # discover the list-valued key
        for key, value in data.items():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                grid = value
                break
    assert grid is not None, "no grid array found in witness JSON"
    best = min(
        grid,
        key=lambda item: item["L_mod"],
    )
    sigma = best["sigma"]
    t = best["t"]
    value = best["L_mod"]
    print(f"entries: {len(grid)}")
    print(f"min |L(s)| = {value:.8f} at sigma={sigma}, t={t}")
    header = data.get("certificate", {})
    claimed = header.get("min_L_grid")
    if claimed is not None:
        status = "OK" if abs(claimed - value) < 1e-6 else "MISMATCH"
        print(f"certificate header min_L_grid={claimed}: {status}")
        if status == "MISMATCH":
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
