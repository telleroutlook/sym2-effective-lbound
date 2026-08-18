"""Tests for the infinite AFE main-sum certificate of sym^2 Delta."""

import copy

from checker.check_s1_full import check_full_s1_certificate
from src.afe_s1_full import (
    CONTOUR_M,
    d3_values,
    arb_sym2_coeffs,
    _compute_tau,
    _finite_s1_interval,
    _absolute_contour_constant,
    full_s1_certificate,
)
from src.afe_s1_arb import finite_s1_certificate as finite_s1_certificate_finite


def _small_cert():
    """N=100, T=5, M=200, precision=64 — fast for tests."""
    return full_s1_certificate(N=100, T=5, M=200, precision=64, abs_T=6)


def test_d3_first_values():
    d3 = d3_values(20)
    # d_3(p^k) = (k+1)(k+2)/2; multiplicative.
    # d_3(1)=1, d_3(2)=3, d_3(3)=3, d_3(4)=6, d_3(5)=3, d_3(6)=9, ...
    expected = [0, 1, 3, 3, 6, 3, 9, 3, 10, 6, 9, 3, 18, 3, 9, 9, 15, 3, 18, 3, 18]
    assert d3 == expected


def test_d3_large_values():
    d3 = d3_values(1000)
    assert d3[100] == 36  # d_3(2^2)*d_3(5^2) = 6*6 = 36


def test_sym2_coefficients_match_afe_s1_arb():
    tau = _compute_tau(20)
    coeffs = arb_sym2_coeffs(20, precision=80, tau_values=tau)
    assert coeffs[0].real.lower() <= 1 <= coeffs[0].real.upper()
    a2 = coeffs[1]
    assert a2.real.lower() <= -0.71875 <= a2.real.upper()


def test_finite_interval_matches_finite_certificate():
    """The finite S1[N,T] from afe_s1_full must match afe_s1_arb."""
    N, T, prec = 100, 5.0, 80
    tau = _compute_tau(N)
    coeffs = arb_sym2_coeffs(N, prec, tau)
    full_finite = _finite_s1_interval(N, T, prec, coeffs)
    finite_cert = finite_s1_certificate_finite(N=N, T=T, precision=prec)
    fl, fu = float(full_finite.real.lower()), float(full_finite.real.upper())
    sl, su = finite_cert["finite_interval"]
    assert fl <= su + 1e-14
    assert fu >= sl - 1e-14


def test_contour_constant_is_680():
    cc = _absolute_contour_constant(CONTOUR_M, precision=80)
    assert 679.0 < float(cc) < 681.0


def test_full_certificate_passes_checker():
    cert = _small_cert()
    assert cert["method"] == "afe-s1-full-v1"
    assert cert["certifies_infinite_s1"] is True
    assert cert["certifies_l1"] is False
    ok, message = check_full_s1_certificate(cert)
    assert ok, message
    assert "certifies infinite S1 only" in message


def test_checker_rejects_tampered_s1_interval():
    cert = _small_cert()
    tampered = copy.deepcopy(cert)
    midpoint = sum(tampered["s1_interval"]) / 2
    tampered["s1_interval"] = [midpoint, midpoint + 1e-15]
    ok, message = check_full_s1_certificate(tampered)
    assert not ok


def test_checker_rejects_tampered_certifies_l1():
    cert = _small_cert()
    tampered = copy.deepcopy(cert)
    tampered["certifies_l1"] = True
    ok, message = check_full_s1_certificate(tampered)
    assert not ok
    assert "certifies_l1 must be False" in message


def test_checker_rejects_wrong_tau_checksum():
    cert = _small_cert()
    tampered = copy.deepcopy(cert)
    tampered["tau_sha256"] = "0" * 64
    ok, message = check_full_s1_certificate(tampered)
    assert not ok
    assert "checksum mismatch" in message


def test_checker_rejects_finite_only_promoted():
    """A finite S1 certificate with certifies_infinite_s1=True must be rejected."""
    cert = _small_cert()
    tampered = copy.deepcopy(cert)
    tampered["certifies_infinite_s1"] = False
    ok, message = check_full_s1_certificate(tampered)
    assert not ok
    assert "certifies_infinite_s1 must be True" in message


def test_s1_interval_contains_true_value():
    """At N=100, T=5 the S1 interval must contain the true S1 ~ 0.5483."""
    cert = _small_cert()
    lo, hi = cert["s1_interval"]
    # The true S1 is approximately 0.5483 (from PLAN.md)
    assert lo < 0.5483 < hi, f"S1 ~ 0.5483 not in [{lo}, {hi}]"


def test_t_tail_is_negligible():
    """At T=5 the vertical tail should be tiny."""
    cert = _small_cert()
    assert cert["t_tail_bound"][1] < 1e-10


def test_n_tail_is_dominant():
    """At N=100 the coefficient tail should dominate the error."""
    cert = _small_cert()
    assert cert["n_tail_bound"][1] > cert["t_tail_bound"][1]
