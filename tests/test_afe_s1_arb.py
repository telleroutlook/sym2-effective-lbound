"""Tests for finite Arb certificates and their independent replay."""

import copy

from checker.check_s1_finite import check_finite_s1_certificate
from src.afe_s1 import _afe_weight
from src.afe_s1_arb import (
    arb_sym2_coeffs,
    finite_s1_certificate,
    truncated_afe_weight,
)
from src.tau_sieve import compute_tau


def test_sym2_coefficients_are_enclosed_and_exact_at_one():
    tau = compute_tau(20)
    coefficients = arb_sym2_coeffs(20, precision=80, tau_values=tau)
    assert coefficients[0].real.lower() <= 1 <= coefficients[0].real.upper()
    # tau(2)=-24, so A(2)=tau(2)^2/2^11-1=-23/32.
    a2 = coefficients[1]
    assert a2.real.lower() <= -0.71875 <= a2.real.upper()


def test_finite_weight_agrees_with_discovery_quadrature():
    arb_weight = truncated_afe_weight(1.0, T=8, precision=96)
    discovery_weight = _afe_weight(1.0, dps=40, T_max=20, n_quad=800)
    assert arb_weight.real.lower() - 1e-12 <= discovery_weight
    assert discovery_weight <= arb_weight.real.upper() + 1e-12


def test_finite_certificate_honesty_and_independent_replay():
    certificate = finite_s1_certificate(N=10, T=6, precision=80)

    assert certificate["method"] == "afe-s1-finite-v1"
    assert certificate["N"] == 10
    assert certificate["certifies_infinite_s1"] is False
    assert certificate["certifies_l1"] is False
    assert certificate["tail_bound"] is None

    lower, upper = certificate["finite_interval"]
    assert lower < upper
    ok, message = check_finite_s1_certificate(certificate)
    assert ok, message
    assert "no tail or L(1) claim" in message


def test_checker_rejects_promotion_or_a_tight_fabricated_interval():
    certificate = finite_s1_certificate(N=8, T=5, precision=64)

    promoted = copy.deepcopy(certificate)
    promoted["certifies_infinite_s1"] = True
    assert not check_finite_s1_certificate(promoted)[0]

    narrowed = copy.deepcopy(certificate)
    midpoint = sum(narrowed["finite_interval"]) / 2
    narrowed["finite_interval"] = [midpoint, midpoint]
    ok, message = check_finite_s1_certificate(narrowed)
    assert not ok
    assert "increasing endpoints" in message


def test_checker_rejects_a_wrong_tau_checksum():
    certificate = finite_s1_certificate(N=8, T=5, precision=64)
    certificate["tau_sha256"] = "0" * 64
    ok, message = check_finite_s1_certificate(certificate)
    assert not ok
    assert "checksum mismatch" in message
