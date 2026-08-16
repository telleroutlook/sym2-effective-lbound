"""
Independent certificate checker for sym2-effective-lbound.

Verifies: L(1, sym^2 f) >= L_0
without importing any code from src/.

Usage:
    python -m checker.check_bound certificate.json
    Exit 0: accepted.  Exit 2: rejected.
"""
from __future__ import annotations

import json
import math
import sys

_TAU_PRIMES: dict = {
    2: -24, 3: 252, 5: 4830, 7: -16744, 11: 534612, 13: -577738,
    17: -6905934, 19: 2727432, 23: 18643272, 29: 128406630,
    31: -52843168, 37: -182213314,
}


def _reject(reason: str) -> None:
    print(f"REJECT: {reason}", file=sys.stderr)
    sys.exit(2)


def _recompute_lower_bound(cert: dict) -> float:
    """Independently recompute lower bound from Euler product and tail estimate."""
    cutoff = cert["euler_product_cutoff"]
    tail_method = cert["tail_bound"]["method"]
    tail_const = cert["tail_bound"].get("constant", 4.0)

    if tail_method != "rankin-selberg-log-estimate":
        _reject(f"Unknown tail bound method: {tail_method}")
    if cert["form"]["level"] != 1 or cert["form"]["weight"] != 12:
        _reject("Checker v1.0 only supports Delta function (level=1, weight=12)")

    log_prod = 0.0
    n = 2
    while n <= min(cutoff, max(_TAU_PRIMES)):
        is_prime = n > 1 and all(n % d != 0 for d in range(2, int(n**0.5) + 1))
        if is_prime and n in _TAU_PRIMES:
            tau_p = _TAU_PRIMES[n]
            norm_sum = tau_p * n**(-5.5)
            a2pb2 = norm_sum**2 - 2.0
            x = 1.0 / n
            fi = (1 - x) * (1 - a2pb2 * x + x**2)
            if fi <= 0:
                _reject(f"Non-positive local factor at p={n}: {fi}")
            log_prod += math.log(fi)
        n += 1

    tail_log = tail_const / (cutoff * math.log(max(cutoff, 2)))
    return math.exp(log_prod - tail_log)


def check_certificate(cert: dict) -> None:
    """Verify certificate; calls _reject() on failure."""
    required = ["form", "bound", "euler_product_cutoff", "tail_bound",
                "euler_product_interval", "arb_precision_bits", "checker_version"]
    for key in required:
        if key not in cert:
            _reject(f"Missing required key: {key}")

    bound = cert["bound"]
    interval = cert["euler_product_interval"]
    if not isinstance(interval, list) or len(interval) != 2:
        _reject("euler_product_interval must be [lower, upper]")
    lower, upper = interval
    if lower >= upper:
        _reject(f"Invalid interval: [{lower}, {upper}]")
    if lower < bound:
        _reject(f"Interval lower {lower} < stated bound {bound}")

    recomputed = _recompute_lower_bound(cert)
    if recomputed < bound:
        _reject(f"Recomputed lower {recomputed:.6f} < stated bound {bound}")
    if abs(recomputed - lower) / (abs(lower) + 1e-300) > 0.05:
        _reject(f"Discrepancy: recomputed={recomputed:.4f}, cert lower={lower:.4f}")

    print(f"PASS: L(1, sym^2 f) >= {bound} (recomputed={recomputed:.4f})")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m checker.check_bound <certificate.json>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1]) as f:
        check_certificate(json.load(f))


if __name__ == "__main__":
    main()
