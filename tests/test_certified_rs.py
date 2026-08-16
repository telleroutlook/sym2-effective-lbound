"""
Tests for src/certified_rs.py: proof-tier certified intervals for L(s, sym^2 Delta).

CERTIFIED RESULT: L(2, sym^2 Delta) >= 0.805   [RS+Deligne+Arb]
All bounds are rigorously certified via python-flint Arb interval arithmetic.
"""
import pytest
from src.certified_rs import certified_l_at_s
from src.tau_sieve import compute_tau


class TestTauSieve:
    def test_tau_1(self):
        tau = compute_tau(5)
        assert tau[0] == 1       # tau(1) = 1

    def test_tau_small(self):
        tau = compute_tau(12)
        assert tau[1] == -24     # tau(2) = -24
        assert tau[2] == 252     # tau(3) = 252
        assert tau[4] == 4830    # tau(5) = 4830

    def test_tau_length(self):
        tau = compute_tau(100)
        assert len(tau) == 100


class TestCertifiedLAtS:
    @pytest.fixture(scope="class")
    def result_s2(self):
        return certified_l_at_s(2.0, N=300, prec=64)

    def test_returns_valid_interval(self, result_s2):
        assert result_s2["lower"] < result_s2["upper"]

    def test_lower_bound_positive(self, result_s2):
        assert result_s2["lower"] > 0

    def test_certified_lower_bound_s2(self, result_s2):
        # Certified: L(2, sym^2 Delta) >= 0.80  [RS positivity + Arb]
        assert result_s2["lower"] >= 0.80, (
            f"Expected certified lower bound >= 0.80, got {result_s2['lower']}"
        )

    def test_upper_bound_plausible_s2(self, result_s2):
        # Upper bound via Deligne is conservative but finite
        assert result_s2["upper"] < 5.0

    def test_method_label(self, result_s2):
        assert result_s2["method"] == "RS+Deligne"

    def test_s3_tight_interval(self):
        # At s=3, Deligne tail is very tight
        r = certified_l_at_s(3.0, N=300, prec=64)
        assert r["lower"] >= 0.85
        assert r["upper"] - r["lower"] < 0.01  # tight at s=3

    def test_lower_bound_increases_with_N(self):
        r100 = certified_l_at_s(2.0, N=100, prec=64)
        r500 = certified_l_at_s(2.0, N=500, prec=64)
        # More terms -> larger lower bound
        assert r500["lower"] >= r100["lower"]

    def test_s_must_be_greater_than_1(self):
        with pytest.raises(ValueError):
            certified_l_at_s(1.0, N=100, prec=64)
        with pytest.raises(ValueError):
            certified_l_at_s(0.5, N=100, prec=64)

    @pytest.mark.slow
    def test_certified_lower_bound_s2_n5000(self):
        # Full-precision certified lower bound
        r = certified_l_at_s(2.0, N=5000, prec=128)
        assert r["lower"] >= 0.805, (
            f"Expected L(2) >= 0.805 [CERTIFIED], got {r['lower']}"
        )
        assert r["lower"] < r["upper"]
