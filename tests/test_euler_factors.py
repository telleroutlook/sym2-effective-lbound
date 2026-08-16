"""
Unit tests for src/euler_factors.py.

Verifies Theorem F-1: local Euler factor factorization and (1+q^{-s}) cancellation.
"""
import pytest
from src.euler_factors import (
    chi_l, l_series_exact, local_euler_factor, adjoint_local_factor,
    zeta_local, verify_cancellation, delta_satake_params, delta_local_sym2_factor,
)


class TestChiL:
    def test_chi_0(self):
        assert chi_l(1.5, 1 / 1.5, 0) == pytest.approx(1.0)

    def test_chi_1(self):
        alpha, beta = 1.5, 1 / 1.5
        assert chi_l(alpha, beta, 1) == pytest.approx(alpha + beta)

    def test_chi_2(self):
        alpha, beta = 1.5, 1 / 1.5
        assert chi_l(alpha, beta, 2) == pytest.approx(alpha**2 + 1 + beta**2, rel=1e-10)

    def test_degenerate(self):
        assert chi_l(1.0, 1.0, 3) == pytest.approx(4.0)

    def test_unitarity(self):
        alpha = complex(0.6, 0.8)
        beta = 1 / alpha
        val = chi_l(alpha, beta, 4)
        assert abs(val.imag) < 1e-10


class TestLSeriesExact:
    def test_closed_form_vs_series(self):
        alpha, beta, x = 1.5, 1 / 1.5, 0.3
        series = sum(chi_l(alpha, beta, l)**2 * x**l for l in range(51))
        assert series == pytest.approx(l_series_exact(alpha, beta, x), rel=1e-6)

    def test_positive_at_x_half(self):
        for av in [0.7, 1.0, 1.3, 1.8]:
            assert l_series_exact(av, 1 / av, 0.5) > 0


class TestEulerFactorCancellation:
    @pytest.mark.parametrize("alpha_val,q,s", [
        (1.5, 2, 1.0), (1.2, 3, 1.0), (0.8, 5, 1.0), (1.0, 7, 1.0 + 0.5j),
    ])
    def test_cancellation(self, alpha_val, q, s):
        alpha = complex(alpha_val)
        beta = 1 / alpha
        r = verify_cancellation(alpha, beta, q, s)
        assert r["cancellation_verified"], f"Cancellation failed: {r}"

    def test_factored_form(self):
        alpha = complex(0.6, 0.8)
        r = verify_cancellation(alpha, 1 / alpha, 5, 1.0)
        assert r["rel_error_factored"] < 1e-10

    def test_positivity_at_s1(self):
        alpha = complex(0.6, 0.8)
        val = local_euler_factor(alpha, 1 / alpha, 3, 1.0)
        assert val.real > 0


class TestDeltaSatakeParams:
    def test_product_one(self):
        for p in [2, 3, 5, 7, 11]:
            alpha, beta = delta_satake_params(p)
            assert abs(alpha * beta - 1.0) < 1e-10, f"alpha*beta != 1 at p={p}"

    def test_local_factor_positive(self):
        for p in [2, 3, 5, 7, 11, 13]:
            fi = delta_local_sym2_factor(p, s=1.0)
            assert fi.real > 0, f"factor_inv={fi} at p={p}"
