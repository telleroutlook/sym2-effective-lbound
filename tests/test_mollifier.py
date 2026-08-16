"""Tests for src/mollifier.py (discovery tier -- mathematical correctness only)."""
import math
import pytest
from src.mollifier import (
    mobius,
    sym2_hecke_eigenvalue_at_prime,
    mollifier_coefficients,
)


class TestMobius:
    def test_mu_1(self):
        assert mobius(1) == 1

    def test_mu_prime(self):
        assert mobius(2) == -1
        assert mobius(3) == -1
        assert mobius(5) == -1

    def test_mu_product_two_primes(self):
        assert mobius(6) == 1  # 2*3
        assert mobius(15) == 1  # 3*5

    def test_mu_prime_squared(self):
        assert mobius(4) == 0   # 2^2
        assert mobius(9) == 0   # 3^2
        assert mobius(12) == 0  # 2^2 * 3

    def test_mu_product_three_primes(self):
        assert mobius(30) == -1  # 2*3*5


class TestSym2HeckeAtPrime:
    """a_Pi(p) = tau(p)^2 / p^{k-1} - 1 for sym^2 Delta."""

    def test_p2_k12(self):
        # tau(2) = -24, k=12, p^{k-1} = 2^11 = 2048
        # c = -24/2^{5.5} = -24/45.2548...
        # a_Pi = c^2 - 1 = 576/2048 - 1 = 0.28125 - 1 = -0.71875
        a = sym2_hecke_eigenvalue_at_prime(2, -24, 12)
        expected = (-24)**2 / 2**11 - 1  # 576/2048 - 1
        assert abs(a - expected) < 1e-12

    def test_p3_k12(self):
        # tau(3) = 252, 3^{11} = 177147
        a = sym2_hecke_eigenvalue_at_prime(3, 252, 12)
        expected = 252**2 / 3**11 - 1
        assert abs(a - expected) < 1e-10


class TestMollifierCoefficients:
    TAU = {2: -24, 3: 252, 5: 4830, 7: -16744, 11: 534612}

    def test_n1_coeff_is_one(self):
        coeffs = mollifier_coefficients(20, self.TAU)
        assert 1 in coeffs
        assert coeffs[1]["coeff"] == 1.0

    def test_prime_coeff_sign(self):
        """For prime p, mu(p) = -1, so coeff(p) = -a_Pi(p)."""
        coeffs = mollifier_coefficients(20, self.TAU)
        p = 2
        a = sym2_hecke_eigenvalue_at_prime(p, -24)
        assert abs(coeffs[p]["coeff"] - (-a)) < 1e-12

    def test_squarefree_only(self):
        """No coefficient for n=4 (not squarefree)."""
        coeffs = mollifier_coefficients(20, self.TAU)
        assert 4 not in coeffs

    def test_product_two_primes_sign(self):
        """n=6=2*3: mu(6)=1, coeff = a_Pi(2)*a_Pi(3)."""
        coeffs = mollifier_coefficients(20, self.TAU)
        a2 = sym2_hecke_eigenvalue_at_prime(2, -24)
        a3 = sym2_hecke_eigenvalue_at_prime(3, 252)
        expected = a2 * a3  # mu(6)=+1
        assert abs(coeffs[6]["coeff"] - expected) < 1e-11
