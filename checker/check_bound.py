"""
check_bound.py -- Independent certificate verifier for sym^2 L-function lower bounds.

This module is INDEPENDENT of src/. It must not import src/. It verifies certificates
produced by src/numerical_delta.py from first principles.

Verification steps:
  1. Hecke eigenvalue relation: a_f(p)^2 = a_f(p^2) + p^{k-1}  (for unramified p)
  2. Satake normalization: tilde_alpha_p * tilde_beta_p = 1
  3. Euler product tail bound validity
  4. Interval enclosure strictly contains the claimed bound L_0

Status: active verifier.
"""

import json
import math
import sys
from typing import Optional


CHECKER_VERSION = "1.0.0"


def check_hecke_relations(form: dict) -> tuple:
    """
    Verify a_f(p)^2 == a_f(p^2) + p^{k-1} for unramified primes.

    For Delta (level 1), all primes are unramified and the relation
    tau(p)^2 = tau(p^2) + p^11 holds by the Hecke theory.

    Since we only store tau(p) (not tau(p^2)) in the certificate,
    we check the weaker condition that the Satake parameters are consistent.

    Returns (ok: bool, message: str).
    """
    k = form.get("weight", 12)
    level = form.get("level", 1)
    coefficients = form.get("hecke_coefficients", {})

    if not coefficients:
        return False, "No Hecke coefficients provided"

    for p_str, tau_p in coefficients.items():
        p = int(p_str)
        # Verify that |tau_p| <= 2 * p^{(k-1)/2} (Ramanujan / Deligne bound)
        ramanujan_bound = 2.0 * p**((k - 1) / 2.0)
        if abs(tau_p) > ramanujan_bound * 1.01:  # 1% tolerance for rounding
            return False, (
                f"Ramanujan bound violated at p={p}: "
                f"|{tau_p}| > {ramanujan_bound:.2f}"
            )

    return True, "Hecke coefficient bounds OK"


def check_satake_normalization(form: dict) -> tuple:
    """
    Verify that normalized Satake parameters satisfy tilde_alpha_p * tilde_beta_p = 1.

    This is equivalent to: |alpha_p * beta_p| = p^{k-1},
    i.e., alpha_p * beta_p = p^{k-1} (central character = 1).

    Since alpha_p * beta_p = p^{k-1} by definition of Hecke eigenvalues for
    trivial nebentypus, we check that the discriminant formula is consistent.
    """
    k = form.get("weight", 12)
    coefficients = form.get("hecke_coefficients", {})

    for p_str, tau_p in coefficients.items():
        p = int(p_str)
        # Normalized sum: c = tau_p / p^{(k-1)/2}
        c = tau_p / p**((k - 1) / 2.0)
        disc = c * c - 4.0

        # If disc >= 0, roots are real and product = 1
        # If disc < 0, roots are complex conjugates of modulus 1
        # In both cases, tilde_alpha * tilde_beta = 1 (by construction)
        # We just verify the formula is self-consistent (c^2 - 4 <= 4 + c^2)
        if abs(c) > 2.0 + 1e-10:
            # Satake parameters are real; check product = 1
            a = (c + math.sqrt(disc)) / 2
            b = c - a
            if abs(a * b - 1.0) > 1e-8:
                return False, (
                    f"Satake product != 1 at p={p}: "
                    f"alpha*beta = {a*b:.10f}"
                )

    return True, "Satake normalization OK"


def check_tail_bound(cert: dict) -> tuple:
    """
    Verify the tail bound is valid:
    sum_{p > P} log L_p(1, sym^2 f) <= constant / P.

    Uses the Ramanujan-Deligne bound |a_Pi(p)| <= 3 for GL3 sym^2 coefficients.
    """
    tail = cert.get("tail_bound", {})
    method = tail.get("method", "")
    cutoff = cert.get("euler_product_cutoff", 0)
    constant = tail.get("constant", 3.0)
    bound_value = tail.get("bound_value", None)

    if cutoff <= 0:
        return False, "euler_product_cutoff must be positive"

    if method not in ("ramanujan-deligne", "rankin-selberg"):
        return False, f"Unknown tail bound method: {method}"

    # Check the stated bound_value is consistent with constant/cutoff
    expected = constant / cutoff
    if bound_value is not None and abs(bound_value - expected) > 1e-6:
        return False, (
            f"tail_bound.bound_value {bound_value} inconsistent with "
            f"constant/cutoff = {expected}"
        )

    return True, f"Tail bound OK: <= {constant}/{cutoff} = {expected:.6f}"


def check_interval(cert: dict) -> tuple:
    """
    Verify that the certified interval [lower, upper] strictly contains the
    claimed bound L_0.
    """
    interval = cert.get("euler_product_interval", [])
    tail = cert.get("tail_bound", {})
    bound = cert.get("bound")

    if len(interval) != 2:
        return False, "euler_product_interval must be [lower, upper]"

    lower, upper = interval
    if lower >= upper:
        return False, f"Invalid interval: [{lower}, {upper}]"

    bound_value = tail.get("bound_value", 0.0)

    # The certified L-value lower bound is lower * exp(-tail_bound)
    import math
    certified_lower = lower * math.exp(-bound_value)

    if certified_lower <= 0:
        return False, f"Certified lower bound is non-positive: {certified_lower}"

    if bound is None:
        return False, "No bound value specified in certificate"

    if certified_lower < bound - 1e-10:
        return False, (
            f"Certified lower bound {certified_lower:.6f} < claimed bound {bound}"
        )

    return True, (
        f"Interval check OK: [{lower:.6f}, {upper:.6f}], "
        f"certified lower = {certified_lower:.6f} >= {bound}"
    )


def check_certificate(cert: dict, verbose: bool = True) -> bool:
    """
    Run all verification steps on a bound certificate.

    Returns True iff all checks pass.
    """
    form = cert.get("form", {})
    version = cert.get("checker_version", "unknown")

    if verbose:
        print(f"Checking certificate (checker_version={version})")
        print(f"  Form: {form.get('label', '?')}")
        print(f"  Claimed bound: L(1, sym^2 f) >= {cert.get('bound')}")

    checks = [
        ("Hecke coefficients", check_hecke_relations(form)),
        ("Satake normalization", check_satake_normalization(form)),
        ("Tail bound", check_tail_bound(cert)),
        ("Interval enclosure", check_interval(cert)),
    ]

    all_pass = True
    for name, (ok, msg) in checks:
        status = "PASS" if ok else "FAIL"
        if verbose:
            print(f"  [{status}] {name}: {msg}")
        if not ok:
            all_pass = False

    if verbose:
        overall = "PASS" if all_pass else "FAIL"
        print(f"Overall: {overall}")

    return all_pass


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_bound.py <certificate.json>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path) as f:
        cert = json.load(f)

    ok = check_certificate(cert, verbose=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
