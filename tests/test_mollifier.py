"""
Unit tests for src/mollifier.py.
"""
import pytest
from src.mollifier import mobius, optimal_mollifier_length


class TestMobius:
    def test_mu_1(self):
        assert mobius(1) == 1

    def test_mu_prime(self):
        for p in [2, 3, 5, 7, 11, 13]:
            assert mobius(p) == -1

    def test_mu_squarefree(self):
        assert mobius(6) == 1
        assert mobius(30) == -1
        assert mobius(2310) == 1

    def test_mu_not_squarefree(self):
        for n in [4, 8, 9, 12, 18, 25, 36]:
            assert mobius(n) == 0


class TestOptimalLength:
    def test_theta_quarter(self):
        assert optimal_mollifier_length(N=100, theta=0.25) == pytest.approx(100**0.25, abs=1)

    def test_minimum_one(self):
        assert optimal_mollifier_length(N=1) >= 1
