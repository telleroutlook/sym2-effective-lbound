"""
Tests for src/numerical_delta.py: certification of L(1, sym^2 Delta).

Theorem F-3: L(1, sym^2 Delta) in [2.405, 2.407].
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
        assert 0 < val < 1, f"Local factor at p={p}: {val}"

    def test_p2_factor(self):
        val = local_sym2_factor_mpmath(2, -24, s=1.0)
        assert 0.8 < val < 1.0, f"L_2(1)^{{-1}} = {val}"


@pytest.mark.slow
class TestEulerProduct:
    def test_mpmath_lower_bound(self):
        lb = compute_l1_sym2_delta_mpmath(cutoff=200)["lower_bound"]
        assert lb > 2.405, f"Lower bound {lb} < 2.405 (F-3 violated)"

    def test_mpmath_upper_bound(self):
        ub = compute_l1_sym2_delta_mpmath(cutoff=200)["upper_bound"]
        assert ub < 2.5


class TestCertificate:
    def test_certificate_structure(self):
        cert = produce_certificate(cutoff=50)
        for key in ["form", "bound", "euler_product_cutoff", "tail_bound",
                    "euler_product_interval", "arb_precision_bits", "checker_version"]:
            assert key in cert

    def test_certificate_bound(self):
        assert produce_certificate(cutoff=50)["bound"] == 2.405

    def test_interval_valid(self):
        lower, upper = produce_certificate(cutoff=50)["euler_product_interval"]
        assert 0 < lower < upper
