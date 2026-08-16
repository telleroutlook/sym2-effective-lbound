"""
Tests for src/numerical_delta.py: partial Euler product computations.

NOTE: Theorem F-3 (L(1,sym^2 Delta) in [2.405,2.407]) has been retracted.
The Euler product does not converge to L(1) for GL3 L-functions at s=1.
The correct RS estimate gives L(1, sym^2 Delta) ~ 0.384 (see discovery/rs_estimate.py).
Certification requires the approximate functional equation [OBL E-2].
"""
import pytest
from src.numerical_delta import (
    sieve_primes, local_sym2_factor_mpmath, compute_l1_sym2_delta_mpmath,
    produce_certificate, TAU_PRIMES,
)


class TestSievePrimes:
    def test_small_primes(self):
        assert sieve_primes(10) == [2, 3, 5, 7]
        assert sieve_primes(20) == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_empty(self):
        assert sieve_primes(1) == []


class TestLocalFactors:
    @pytest.mark.parametrize("p", [2, 3, 5, 7, 11, 13])
    def test_local_factor_in_range(self, p):
        tau_p = TAU_PRIMES[p]
        val = local_sym2_factor_mpmath(p, tau_p, s=1.0)
        assert val > 0, f"Local factor at p={p}: {val}"

    def test_p2_factor(self):
        val = local_sym2_factor_mpmath(2, -24, s=1.0)
        assert 0.9 < val < 1.2, f"L_2(1)^{{-1}} = {val}"


@pytest.mark.slow
class TestEulerProduct:
    def test_mpmath_lower_bound(self):
        # The Euler product at s=1 for GL3 converges extremely slowly (requires
        # ~10^6 primes to approach L(1)).  Over 25 primes the partial product is
        # ~0.53.  Correct computation requires the approximate functional equation
        # [OBL E-2].  This test just confirms the partial product is positive.
        partial = compute_l1_sym2_delta_mpmath(cutoff=200)
        assert partial["lower_bound"] > 0
        assert partial["product"] < 1.5  # partial Euler product << L(1)

    def test_mpmath_upper_bound(self):
        ub = compute_l1_sym2_delta_mpmath(cutoff=200)["upper_bound"]
        assert ub < 1.5  # partial Euler product over 25 primes is ~0.57


class TestCertificate:
    def test_certificate_structure(self):
        cert = produce_certificate(cutoff=50)
        for key in ["form", "bound", "euler_product_cutoff", "tail_bound",
                    "euler_product_interval", "arb_precision_bits", "checker_version"]:
            assert key in cert

    def test_certificate_bound(self):
        assert produce_certificate(cutoff=50)["bound"] is None

    def test_interval_valid(self):
        lower, upper = produce_certificate(cutoff=50)["euler_product_interval"]
        assert 0 < lower < upper
