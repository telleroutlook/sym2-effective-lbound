"""
check_zero_free.py -- Independent checker for zero-free scan certificate.

Reads baseline/zero_free_scan.json and independently verifies:
  1. Certificate structure and required fields
  2. Recomputes L(s) at the claimed minimum point via truncated Dirichlet series
  3. Recomputes the partial-sum tail bound
  4. Verifies certified_min_L = min|L| - tail > 0

Does NOT import src/zero_free_arb.py (independent verification).
"""

import json
import math
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CERT_PATH = os.path.join(_REPO, "baseline", "zero_free_scan.json")
VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv


def log(msg):
    if VERBOSE:
        print(f"  [check] {msg}")


# ---------------------------------------------------------------------------
# Tau function (inlined from src/tau_sieve.py for independence)
# ---------------------------------------------------------------------------

def _compute_tau(N):
    """tau(n) via q-product: Delta(q) = q * prod(1-q^k)^24."""
    p = [0] * (N + 1)
    p[0] = 1
    for k in range(1, N + 1):
        for _ in range(24):
            for n in range(N, k - 1, -1):
                p[n] -= p[n - k]
    return [p[n - 1] for n in range(1, N + 1)]


# ---------------------------------------------------------------------------
# Recompute sym^2 coefficients (independent implementation)
# ---------------------------------------------------------------------------

def _compute_sym2_coeffs(tau_values):
    """Recompute A(n) from tau(n) — independent of zero_free_arb."""
    N = len(tau_values)
    coeffs = [0.0] * (N + 1)
    coeffs[1] = 1.0
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    smallest_prime = [0] * (N + 1)
    for p in range(2, N + 1):
        if is_prime[p]:
            smallest_prime[p] = p
            c = tau_values[p - 1] / p ** 5.5
            c2 = c * c
            max_k = max(1, int(math.log(N, p)) + 1)
            ap = [0.0] * (max_k + 1)
            ap[0] = 1.0
            ap[1] = c2 - 1.0
            if max_k >= 2:
                ap[2] = (c2 - 1) * ap[1] - (c2 - 1) * ap[0]
            for k in range(3, max_k + 1):
                ap[k] = (c2 - 1) * ap[k - 1] - (c2 - 1) * ap[k - 2] + ap[k - 3]
            pk = p
            k = 1
            while pk <= N:
                coeffs[pk] = ap[k]
                pk *= p
                k += 1
            j = p * p
            while j <= N:
                is_prime[j] = False
                if smallest_prime[j] == 0:
                    smallest_prime[j] = p
                j += p
    for n in range(4, N + 1):
        if is_prime[n]:
            continue
        p = smallest_prime[n]
        m = n // p
        pk = p
        k = 1
        while m % p == 0:
            m //= p
            pk *= p
            k += 1
        if m != 1:
            coeffs[n] = coeffs[pk] * coeffs[m]
    return [coeffs[i] for i in range(1, N + 1)]


def _L_dirichlet(a_sym2, N, sigma, t):
    """Truncated Dirichlet series (independent)."""
    re_s = 0.0
    im_s = 0.0
    for n in range(1, N + 1):
        an = a_sym2[n - 1]
        nsigma = n ** sigma
        if t == 0:
            re_s += an / nsigma
        else:
            logn = math.log(n)
            re_s += an * math.cos(-t * logn) / nsigma
            im_s += an * math.sin(-t * logn) / nsigma
    return complex(re_s, im_s)


def _tail_bound(S_N, sigma, t, C, alpha, N):
    """Recompute tail bound from partial sums."""
    if sigma <= alpha:
        return float('inf')
    ms = math.sqrt(sigma ** 2 + t ** 2)
    return abs(S_N) / N ** sigma + ms * C * N ** (alpha - sigma) / (sigma - alpha)


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify(cert_path=CERT_PATH):
    errors = []
    warnings = []

    # --- 1. Load and validate certificate structure ---
    log(f"Loading certificate from {cert_path}")
    if not os.path.exists(cert_path):
        errors.append(f"Certificate not found: {cert_path}")
        return errors, warnings

    with open(cert_path) as f:
        cert = json.load(f)

    required_fields = [
        "module", "status", "certifies_zero_free", "N_terms",
        "partial_sum_bound", "sigma_range", "t_max",
        "min_L_grid", "min_L_sigma", "min_L_t",
        "tail_at_min", "certified_min_L"
    ]
    for field in required_fields:
        if field not in cert:
            errors.append(f"Missing required field: {field}")

    if errors:
        return errors, warnings

    if cert["module"] != "M-3":
        errors.append(f"Expected module M-3, got {cert['module']}")

    N = cert["N_terms"]
    sigma_min, sigma_max = cert["sigma_range"]
    t_max = cert["t_max"]
    C = cert["partial_sum_bound"]["C"]
    alpha = cert["partial_sum_bound"]["alpha"]
    s0 = cert["min_L_sigma"]
    t0 = cert["min_L_t"]

    log(f"  N={N}, sigma=[{sigma_min},{sigma_max}], |t|<={t_max}")
    log(f"  Partial-sum bound: C={C}, alpha={alpha}")
    log(f"  Claimed minimum at ({s0}, {t0})")

    # --- 2. Recompute coefficients ---
    log("Recomputing tau and A(n)...")
    tau_vals = _compute_tau(N)
    a_sym2 = _compute_sym2_coeffs(tau_vals)

    # Verify A(1) = 1
    if abs(a_sym2[0] - 1.0) > 1e-10:
        errors.append(f"A(1) = {a_sym2[0]}, expected 1.0")

    # Verify A(2) = c_2^2 - 1 where c_2 = tau(2)/2^5.5
    c2 = tau_vals[1] / 2 ** 5.5
    expected_a2 = c2 ** 2 - 1
    if abs(a_sym2[1] - expected_a2) > 1e-6:
        errors.append(f"A(2) = {a_sym2[1]}, expected {expected_a2}")

    log(f"  A(1)={a_sym2[0]:.6f}, A(2)={a_sym2[1]:.6f}, A(3)={a_sym2[2]:.6f}")

    # --- 3. Recompute partial sums and bound ---
    S = [0.0] * (N + 1)
    for n in range(1, N + 1):
        S[n] = S[n - 1] + a_sym2[n - 1]

    # Verify C, alpha
    C_check = max(abs(S[X]) / X ** alpha
                  for X in range(100, N + 1))
    if C_check > C * 1.01:
        errors.append(
            f"Partial-sum bound violated: actual max |S(X)|/X^alpha = "
            f"{C_check:.6f} > claimed C = {C}")
    else:
        log(f"  Partial-sum bound verified: C_actual={C_check:.6f} <= C={C}")

    # --- 4. Recompute L(s) at minimum point ---
    log(f"Recomputing L({s0} + {t0}i)...")
    L_val = _L_dirichlet(a_sym2, N, s0, t0)
    L_mod = abs(L_val)
    log(f"  |L| = {L_mod:.8f} (claimed: {cert['min_L_grid']:.8f})")
    if abs(L_mod - cert["min_L_grid"]) > 0.01:
        errors.append(
            f"|L| mismatch: recomputed {L_mod:.8f} vs "
            f"claimed {cert['min_L_grid']:.8f}")

    # --- 5. Recompute tail bound ---
    tail_check = _tail_bound(S[N], s0, t0, C, alpha, N)
    log(f"  tail = {tail_check:.8f} (claimed: {cert['tail_at_min']:.8f})")
    if abs(tail_check - cert["tail_at_min"]) > 0.001:
        errors.append(
            f"Tail mismatch: recomputed {tail_check:.8f} vs "
            f"claimed {cert['tail_at_min']:.8f}")

    # --- 6. Verify certified_min_L ---
    cert_min_check = max(0.0, L_mod - tail_check)
    log(f"  certified_min_L = {cert_min_check:.8f} "
        f"(claimed: {cert['certified_min_L']:.8f})")
    if abs(cert_min_check - cert["certified_min_L"]) > 0.001:
        errors.append(
            f"certified_min_L mismatch: recomputed {cert_min_check:.8f} vs "
            f"claimed {cert['certified_min_L']:.8f}")

    if cert_min_check <= 0 and cert["certifies_zero_free"]:
        errors.append("certifies_zero_free=True but certified_min_L <= 0")

    # --- 7. Spot-check at a few other grid points ---
    spot_checks = [
        (1.5, 0.0),
        (1.01, 0.0),
        (2.0, 0.0),
    ]
    for sigma, t in spot_checks:
        if sigma < sigma_min or sigma > sigma_max:
            continue
        L_spot = _L_dirichlet(a_sym2, N, sigma, t)
        mod_spot = abs(L_spot)
        tail_spot = _tail_bound(S[N], sigma, t, C, alpha, N)
        cert_spot = max(0, mod_spot - tail_spot)
        log(f"  Spot check ({sigma},{t}): |L|={mod_spot:.6f}, "
            f"tail={tail_spot:.6f}, cert={cert_spot:.6f}")
        if cert_spot <= 0:
            warnings.append(
                f"Spot check ({sigma},{t}): certified_min_L = {cert_spot} <= 0")

    # --- Summary ---
    if not errors:
        log("\n  RESULT: PASS -- all checks passed")
    else:
        log(f"\n  RESULT: FAIL -- {len(errors)} error(s)")

    return errors, warnings


def main():
    print("=" * 60)
    print("Independent checker: zero-free scan certificate")
    print("=" * 60)
    errors, warnings = verify()
    for w in warnings:
        print(f"  WARNING: {w}")
    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        print(f"\n  VERDICT: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    else:
        print(f"\n  VERDICT: PASS ({len(warnings)} warning(s))")
        return 0


if __name__ == "__main__":
    sys.exit(main())
