"""Tests for the zero-free scan module (src/zero_free_arb.py)."""

import json
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from src.zero_free_arb import (
    find_partial_sum_bound,
    L_dirichlet,
    precompute,
    tail_from_partial_sums,
)


def test_a1_equals_one():
    """A(1) must be 1."""
    a, _ = precompute(100)
    assert abs(a[0] - 1.0) < 1e-10


def test_a2_formula():
    """A(2) = c_2^2 - 1 where c_2 = tau(2)/2^5.5."""
    from src.tau_sieve import compute_tau
    tau = compute_tau(100)
    c2 = tau[1] / 2 ** 5.5
    expected = c2 ** 2 - 1
    a, _ = precompute(100)
    assert abs(a[1] - expected) < 1e-6


def test_partial_sum_bound():
    """C, alpha satisfy |S(X)| <= C * X^alpha for all X in [100, N]."""
    N = 1000
    _, S = precompute(N)
    C, alpha = find_partial_sum_bound(S, N)
    for X in range(100, N + 1):
        assert abs(S[X]) <= C * X ** alpha + 1e-10, (
            f"|S({X})| = {abs(S[X]):.6f} > C*X^alpha = {C * X ** alpha:.6f}")


def test_L_dirichlet_at_sigma2():
    """L(2) should be ~ 0.806 (known value)."""
    N = 5000
    a, _ = precompute(N)
    L2 = L_dirichlet(a, N, 2.0, 0.0)
    assert abs(L2.real - 0.806) < 0.01, f"L(2) = {L2.real:.6f}"


def test_L_dirichlet_increasing():
    """L(sigma) should be increasing for real sigma > 1 (→ 1 as sigma → ∞)."""
    N = 5000
    a, _ = precompute(N)
    vals = [L_dirichlet(a, N, s, 0.0).real for s in [1.5, 2.0, 3.0]]
    assert vals[0] < vals[1] < vals[2], f"Not increasing: {vals}"


def test_tail_bound_positive():
    """Tail bound should be positive and decreasing in sigma."""
    N = 5000
    _, S = precompute(N)
    C, alpha = find_partial_sum_bound(S, N)
    tails = [tail_from_partial_sums(S[N], s, 0, C, alpha, N)
             for s in [1.1, 1.5, 2.0, 3.0]]
    assert all(t > 0 for t in tails), f"Non-positive tail: {tails}"
    assert tails == sorted(tails, reverse=True), "Tail not decreasing"


def test_certified_min_positive():
    """At sigma=2, certified min |L| should be positive."""
    N = 2000
    a, S = precompute(N)
    C, alpha = find_partial_sum_bound(S, N)
    L2 = L_dirichlet(a, N, 2.0, 0.0)
    mod = abs(L2)
    tail = tail_from_partial_sums(S[N], 2.0, 0, C, alpha, N)
    cert_min = max(0.0, mod - tail)
    assert cert_min > 0, f"certified_min_L = {cert_min} at sigma=2"


def test_certificate_valid():
    """Certificate JSON has required fields and certifies_zero_free=True."""
    cert_path = os.path.join(_REPO, "baseline", "zero_free_scan.json")
    if not os.path.exists(cert_path):
        return  # skip if not yet generated
    with open(cert_path) as f:
        cert = json.load(f)
    assert cert["module"] == "M-3"
    assert cert["certifies_zero_free"] is True
    assert cert["certified_min_L"] > 0
    assert "N_terms" in cert
    assert "partial_sum_bound" in cert
    assert "sigma_range" in cert


def test_checker_passes():
    """The independent checker should pass on the certificate."""
    cert_path = os.path.join(_REPO, "baseline", "zero_free_scan.json")
    if not os.path.exists(cert_path):
        return
    sys.path.insert(0, os.path.join(_REPO, "checker"))
    from check_zero_free import verify
    errors, warnings = verify(cert_path)
    assert not errors, f"Checker errors: {errors}"
