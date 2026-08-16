"""
Tests for src/afe_s1.py: S1 computation for L(1, sym^2 Delta).

S1 = sum_{n=1}^{N} a(n)/n * W_afe(n/12)  is the main sum in L(1) = S1 - J.
J is [OBL]; only S1 is tested here.

These tests use small N to stay fast (<10 s), and check only consistency
of values, not certified bounds.
"""
import pytest
from src.afe_s1 import _compute_sym2_coeffs, _afe_weight, compute_s1
from src.tau_sieve import compute_tau


class TestSym2Coeffs:
    def test_a1_is_one(self):
        tau = compute_tau(10)
        a = _compute_sym2_coeffs(tau)
        assert abs(a[0] - 1.0) < 1e-12

    def test_a_prime_formula(self):
        tau = compute_tau(10)
        a = _compute_sym2_coeffs(tau)
        # a(2) = (tau(2)/2^5.5)^2 - 1 = (-24/2^5.5)^2 - 1
        c2 = (-24.0 / 2**5.5) ** 2
        expected = c2 - 1.0
        assert abs(a[1] - expected) < 1e-10

    def test_multiplicativity(self):
        # a(4) = a(2^2), must satisfy GL3 recurrence
        tau = compute_tau(10)
        a = _compute_sym2_coeffs(tau)
        c2 = (-24.0 / 2**5.5) ** 2
        # a(p^2) = (c^2-1)*a(p) - (c^2-1)*a(1)  [from recurrence, a(-1)=0]
        ap2_expected = (c2 - 1) * a[1] - (c2 - 1) * a[0]
        assert abs(a[3] - ap2_expected) < 1e-9  # a[3] = a(4)


class TestAfeWeight:
    def test_w_afe_at_zero_is_near_one(self):
        # W_afe(y) -> 1 as y -> 0 (residue at u=0 gives G(1)/G(1) = 1)
        w = _afe_weight(0.001, dps=25, T_max=20, n_quad=200)
        assert 0.95 < w < 1.05, f"W_afe(0.001) = {w}"

    def test_w_afe_decays_for_large_y(self):
        w_small = _afe_weight(0.1, dps=25, T_max=20, n_quad=200)
        w_large = _afe_weight(10.0, dps=25, T_max=20, n_quad=200)
        assert w_small > w_large, "W_afe should decrease with y"
        assert w_large < 0.05, f"W_afe(10) = {w_large} should be small"

    def test_w_afe_at_one_is_positive(self):
        w = _afe_weight(1.0, dps=25, T_max=20, n_quad=200)
        assert 0.25 < w < 0.40, f"W_afe(1) = {w}"


class TestS1Partial:
    def test_s1_n100_range(self):
        # S1(N=100) ~ 0.5479 from convergence table
        result = compute_s1(N=50, dps=30, verbose=False)
        s1 = result["s1_val"]
        # S1 oscillates, but by N=50 should be in [0.50, 0.60]
        assert 0.50 < s1 < 0.60, f"S1(N=50) = {s1}"

    def test_s1_returns_dict_keys(self):
        result = compute_s1(N=20, dps=25, verbose=False)
        assert "s1_val" in result
        assert "s1_error" in result
        assert "N" in result
        assert "w_afe_at_N" in result
        assert result["N"] == 20

    def test_s1_error_positive(self):
        result = compute_s1(N=30, dps=25, verbose=False)
        assert result["s1_error"] > 0

    def test_s1_convergence_direction(self):
        # S1 at N=100 and N=200 should both be near 0.548
        r100 = compute_s1(N=100, dps=30, verbose=False)
        r200 = compute_s1(N=200, dps=30, verbose=False)
        # Both should be in [0.530, 0.570]
        assert 0.530 < r100["s1_val"] < 0.570
        assert 0.530 < r200["s1_val"] < 0.570
        # N=200 should be closer to the limit 0.548302
        assert abs(r200["s1_val"] - 0.548302) < abs(r100["s1_val"] - 0.548302) + 0.002
