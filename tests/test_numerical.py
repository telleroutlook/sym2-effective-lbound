"""Tests for L(1, sym^2 Delta) numerical computation.

All mpmath tests are DISCOVERY TIER (may not certify).
The arb-interval test is PROOF TIER when python-flint is available.
"""
import math
import pytest
from src.numerical_delta import (
    satake_sum,
    local_factor_inv_real,
    compute_L1_sym2_delta_mpmath,
    TAU_PRIMES,
)


# Expected value from Dokchitser/LMFDB: L(1, sym^2 Delta) ~ 2.405...
EXPECTED_L1 = 2.405
EXPECTED_L1_LOWER = 2.40
EXPECTED_L1_UPPER = 2.41


class TestSatakeSum:
    def test_p2(self):
        # tau(2) = -24; c = -24 / 2^{5.5}
        c = satake_sum(2, -24, k=12)
        expected = -24.0 / 2**5.5
        assert abs(c - expected) < 1e-14

    def test_ramanujan_bound(self):
        """All |c| < 2 (Ramanujan-Deligne)."""
        for p, tau_p in TAU_PRIMES.items():
            c = satake_sum(p, tau_p)
            assert abs(c) <= 2.0 + 1e-12, (
                f"|c| = {abs(c):.6f} > 2 at p={p}"
            )


class TestLocalFactorInv:
    def test_p2_positive(self):
        """Local factor L_p(1)^{-1} must be positive."""
        val = local_factor_inv_real(2, -24)
        assert val > 0

    def test_p2_value(self):
        # c = -24/2^{5.5}, re_a2 = c^2 - 2, mod_sq = 1 - re_a2/2 + 1/4
        c = -24.0 / 2**5.5
        re_a2 = c * c - 2.0
        mod_sq = 1.0 - re_a2 / 2.0 + 1.0 / 4.0
        expected = (1.0 - 0.5) * mod_sq
        assert abs(local_factor_inv_real(2, -24) - expected) < 1e-14

    def test_all_primes_positive(self):
        """All local factors L_p(1)^{-1} must be positive."""
        for p, tau_p in TAU_PRIMES.items():
            val = local_factor_inv_real(p, tau_p)
            assert val > 0, f"L_{p}(1)^{{-1}} = {val} <= 0"


@pytest.mark.slow
def test_L1_mpmath_in_expected_range():
    """
    L(1, sym^2 Delta) computed via mpmath should lie in [2.40, 2.41].
    Discovery tier only.
    """
    result = compute_L1_sym2_delta_mpmath(prec=50, n_terms=200)
    L1 = result["L1_value"]
    assert EXPECTED_L1_LOWER <= L1 <= EXPECTED_L1_UPPER, (
        f"L(1, sym^2 Delta) = {L1:.6f} outside expected range "
        f"[{EXPECTED_L1_LOWER}, {EXPECTED_L1_UPPER}]"
    )


@pytest.mark.slow
def test_L1_mpmath_exceeds_bound():
    """
    L(1, sym^2 Delta) >= 2.405 > 1/log(N) for all N >= 1.
    The core assertion for the N=1 case (level-1 form).
    Discovery tier.
    """
    result = compute_L1_sym2_delta_mpmath(prec=50, n_terms=200)
    L1 = result["L1_value"]
    assert L1 >= 2.40, (
        f"L1 = {L1:.6f} failed to exceed the claimed lower bound 2.40"
    )


@pytest.mark.certified
def test_L1_certified_interval():
    """
    [PROOF TIER] L(1, sym^2 Delta) certified to lie in an interval
    strictly containing 2.405.

    Requires python-flint (Arb). If not installed, test is skipped.
    """
    try:
        from src.numerical_delta import compute_L1_sym2_delta_certified
    except ImportError:
        pytest.skip("python-flint not installed -- certified test skipped")

    cert = compute_L1_sym2_delta_certified(primes_up_to=50, prec_bits=128)
    lower = cert["interval"][0]
    upper = cert["interval"][1]

    assert lower > 2.40, (
        f"Certified lower bound {lower} does not exceed 2.40"
    )
    assert upper < 2.42, (
        f"Certified upper bound {upper} implausibly large: {upper}"
    )
    assert cert["bound"] <= lower, (
        "Claimed bound is not covered by the certified lower bound"
    )
