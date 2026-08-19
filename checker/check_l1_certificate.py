"""Independent checker for L(1, sym^2 Delta) certificate.

This script verifies the certificate structure and internal consistency
without importing src/ (independent verification).
"""
import json
import sys
from pathlib import Path

WITNESS = Path(__file__).parent.parent / "outsource" / "04-gl3-afe-rigorous-computation" / "witness"
BASELINE = Path(__file__).parent.parent / "baseline"


def check_l1_certificate():
    """Verify L(1) certificate structure and values."""
    cert_path = WITNESS / "single_point_certificate.json"
    if not cert_path.exists():
        print("FAIL: L(1) certificate not found")
        return False

    cert = json.load(open(cert_path))
    errors = []

    # Structure checks
    required = ["status", "L_lo", "L_hi", "L_positive", "truncation_error_bound",
                "N_afe_primary", "N_afe_secondary", "precision_bits"]
    for key in required:
        if key not in cert:
            errors.append(f"Missing key: {key}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return False

    # Value checks
    if cert["status"] != "CERTIFIED":
        print(f"FAIL: status = {cert['status']}, expected CERTIFIED")
        return False

    if not cert["L_positive"]:
        print("FAIL: L_positive = False")
        return False

    lo, hi = cert["L_lo"], cert["L_hi"]
    if lo >= hi:
        print(f"FAIL: interval [{lo}, {hi}] is invalid")
        return False

    if lo <= 0:
        print(f"FAIL: L_lo = {lo} <= 0")
        return False

    width = hi - lo
    if width > 1e-4:
        print(f"FAIL: interval width {width} > 1e-4")
        return False

    if cert["precision_bits"] < 128:
        print(f"FAIL: precision {cert['precision_bits']} < 128 bits")
        return False

    if cert["N_afe_primary"] < 1000:
        print(f"FAIL: N_afe = {cert['N_afe_primary']} < 1000")
        return False

    if cert["N_afe_secondary"] < 2 * cert["N_afe_primary"]:
        print(f"FAIL: N_afe_secondary = {cert['N_afe_secondary']} < 2 * N_afe_primary")

    print(f"PASS: L(1) in [{lo:.10f}, {hi:.10f}] (width {width:.2e})")
    return True


def check_j_certificate():
    """Verify J certificate and consistency with L(1) and S1."""
    cert_path = WITNESS / "j_certificate.json"
    if not cert_path.exists():
        print("FAIL: J certificate not found")
        return False

    cert = json.load(open(cert_path))
    errors = []

    # Structure
    for key in ["status", "J_interval", "J_width", "J_is_negative", "S1_interval", "L1_interval"]:
        if key not in cert:
            errors.append(f"Missing key: {key}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return False

    # Consistency: J = S1 - L(1)
    J_lo, J_hi = cert["J_interval"]
    S1_lo, S1_hi = cert["S1_interval"]
    L1_lo, L1_hi = cert["L1_interval"]

    expected_lo = S1_lo - L1_hi
    expected_hi = S1_hi - L1_lo

    if abs(J_lo - expected_lo) > 1e-15:
        print(f"FAIL: J_lo = {J_lo}, expected {expected_lo}")
        return False

    if abs(J_hi - expected_hi) > 1e-15:
        print(f"FAIL: J_hi = {J_hi}, expected {expected_hi}")
        return False

    if not cert["J_is_negative"]:
        print("FAIL: J should be negative")
        return False

    print(f"PASS: J in [{J_lo:.10f}, {J_hi:.10f}] (width {cert['J_width']:.2e})")
    return True


def check_unified_certificate():
    """Verify unified certificate structure."""
    cert_path = WITNESS / "unified_certificate.json"
    if not cert_path.exists():
        print("FAIL: Unified certificate not found")
        return False

    cert = json.load(open(cert_path))

    # Check all sections
    for section in ["L1", "S1", "J", "zero_free_region", "grid_scan", "summary"]:
        if section not in cert:
            print(f"FAIL: Missing section: {section}")
            return False

    if cert["summary"]["status"] != "CERTIFIED":
        print(f"FAIL: summary status = {cert['summary']['status']}")
        return False

    if not cert["zero_free_region"]["proved"]:
        print("FAIL: zero_free_region.proved = False")
        return False

    print(f"PASS: Unified certificate valid, status = {cert['summary']['status']}")
    return True


def main():
    print("=" * 60)
    print("Independent Checker for L(1, sym^2 Delta) Certificate")
    print("=" * 60)
    print()

    results = []
    results.append(("L(1) certificate", check_l1_certificate()))
    results.append(("J certificate", check_j_certificate()))
    results.append(("Unified certificate", check_unified_certificate()))

    print()
    print("=" * 60)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"Results: {passed}/{total} passed")

    if passed == total:
        print("VERDICT: PASS")
        return 0
    else:
        print("VERDICT: FAIL")
        for name, r in results:
            if not r:
                print(f"  FAILED: {name}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
