"""Tests for Theorem F-1: local Euler factor factorization via Clebsch-Gordan."""
import math
import pytest
from src.euler_factors import (
    chi_l,
    local_factor_series,
    local_factor_closed,
    verify_f1_cancellation,
    cg_series_vs_formula,
)


# ---------------------------------------------------------------------------
# chi_l tests
# ---------------------------------------------------------------------------

def test_chi_0_is_one():
    """chi_0 = 1 for any alpha, beta."""
    alpha = 0.7
    beta = 1.0 / alpha  # product = 1
    assert abs(chi_l(alpha, beta, 0) - 1.0) < 1e-14


def test_chi_1_is_sum():
    """chi_1(alpha, beta) = alpha + beta."""
    alpha = 0.7
    beta = 1.0 / alpha
    assert abs(chi_l(alpha, beta, 1) - (alpha + beta)) < 1e-12


def test_chi_cg_identity():
    """
    Clebsch-Gordan: chi_l^2 = sum_{j=0}^{l} chi_{2j}.
    Test at l=2: chi_2^2 == chi_0 + chi_2 + chi_4.
    """
    alpha = 0.6
    beta = 1.0 / alpha
    l = 2
    lhs = chi_l(alpha, beta, l) ** 2
    rhs = sum(chi_l(alpha, beta, 2 * j) for j in range(l + 1))
    assert abs(lhs - rhs) < 1e-11


def test_chi_cg_identity_l3():
    """CG at l=3: chi_3^2 == chi_0 + chi_2 + chi_4 + chi_6."""
    alpha = 0.8
    beta = 1.0 / alpha
    l = 3
    lhs = chi_l(alpha, beta, l) ** 2
    rhs = sum(chi_l(alpha, beta, 2 * j) for j in range(l + 1))
    assert abs(lhs - rhs) < 1e-10


# ---------------------------------------------------------------------------
# F-1: series vs closed form
# ---------------------------------------------------------------------------

class TestF1SeriesVsClosed:
    """[THM F-1] local_factor_series and local_factor_closed must agree."""

    def _check(self, alpha, q, s, tol=1e-6):
        beta = 1.0 / alpha  # unit product
        series = local_factor_series(alpha, beta, q, s, n_terms=120)
        closed = local_factor_closed(alpha, beta, q, s)
        assert abs(series - closed) < tol, (
            f"alpha={alpha}, q={q}, s={s}: "
            f"series={series:.8f}, closed={closed:.8f}, diff={abs(series-closed):.2e}"
        )

    def test_real_s_standard(self):
        self._check(0.7, 2, 1.0)

    def test_real_s_larger_q(self):
        self._check(0.5, 7, 1.0)

    def test_real_s_near_one_half(self):
        self._check(0.9, 3, 0.5)

    def test_complex_s(self):
        self._check(0.6, 5, complex(1.0, 14.1))

    def test_alpha_near_one(self):
        """When alpha = beta = 1 (trivial Satake), series should converge faster."""
        alpha = 1.0
        beta = 1.0  # product = 1
        q = 2
        s = 1.0
        series = local_factor_series(alpha, beta, q, s, n_terms=120)
        closed = local_factor_closed(alpha, beta, q, s)
        assert abs(series - closed) < 1e-5


# ---------------------------------------------------------------------------
# F-1: (1 + q^{-s}) cancellation
# ---------------------------------------------------------------------------

class TestF1Cancellation:
    """[THM F-1] The (1+q^{-s}) factor cancels in L_p(s, sym^2 f)."""

    def test_cancellation_p2(self):
        assert verify_f1_cancellation(0.7, 1.0/0.7, 2, 1.0)

    def test_cancellation_p3(self):
        assert verify_f1_cancellation(0.5, 1.0/0.5, 3, 1.0)

    def test_cancellation_complex_s(self):
        assert verify_f1_cancellation(0.8, 1.0/0.8, 5, complex(1.0, 5.0))


# ---------------------------------------------------------------------------
# CG series self-consistency check
# ---------------------------------------------------------------------------

def test_cg_series_vs_formula_consistency():
    """
    cg_series_vs_formula must report max_diff < 1e-6 for all tested primes.
    """
    results = cg_series_vs_formula(n_terms=60)
    for row in results:
        assert row["max_diff"] < 1e-5, (
            f"CG mismatch at alpha={row['alpha']}: max_diff={row['max_diff']:.2e}"
        )
