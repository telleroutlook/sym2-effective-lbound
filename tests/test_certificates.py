"""Tests for L(1) and J certificates."""
import json
import os
import pytest
from pathlib import Path

WITNESS = Path(__file__).parent.parent / "outsource" / "04-gl3-afe-rigorous-computation" / "witness"
BASELINE = Path(__file__).parent.parent / "baseline"


class TestL1Certificate:
    """Test the L(1) certificate structure and values."""

    @pytest.fixture(autouse=True)
    def load_cert(self):
        cert_path = WITNESS / "single_point_certificate.json"
        if not cert_path.exists():
            pytest.skip("L(1) certificate not found")
        self.cert = json.load(open(cert_path))

    def test_status(self):
        assert self.cert["status"] == "CERTIFIED"

    def test_positive(self):
        assert self.cert["L_positive"] is True

    def test_interval_valid(self):
        lo, hi = self.cert["L_lo"], self.cert["L_hi"]
        assert lo < hi
        assert lo > 0

    def test_interval_width(self):
        lo, hi = self.cert["L_lo"], self.cert["L_hi"]
        width = hi - lo
        assert width < 1e-4, f"Interval too wide: {width}"

    def test_interval_contains_center(self):
        lo, hi = self.cert["L_lo"], self.cert["L_hi"]
        center = self.cert["L_center_real"]
        assert lo <= center <= hi

    def test_truncation_error(self):
        err = self.cert["truncation_error_bound"]
        assert err < 1e-3, f"Truncation error too large: {err}"

    def test_precision(self):
        assert self.cert["precision_bits"] >= 128

    def test_n_afe(self):
        assert self.cert["N_afe_primary"] >= 1000
        assert self.cert["N_afe_secondary"] >= 2 * self.cert["N_afe_primary"]


class TestJCertificate:
    """Test the J certificate structure and values."""

    @pytest.fixture(autouse=True)
    def load_cert(self):
        cert_path = WITNESS / "j_certificate.json"
        if not cert_path.exists():
            pytest.skip("J certificate not found")
        self.cert = json.load(open(cert_path))

    def test_status(self):
        assert self.cert["status"] == "CERTIFIED"

    def test_j_negative(self):
        assert self.cert["J_is_negative"] is True

    def test_interval_valid(self):
        lo, hi = self.cert["J_interval"]
        assert lo < hi
        assert hi < 0

    def test_interval_width(self):
        lo, hi = self.cert["J_interval"]
        width = hi - lo
        assert width < 1e-4, f"J interval too wide: {width}"

    def test_consistency_with_l1(self):
        lo, hi = self.cert["J_interval"]
        S1_lo, S1_hi = self.cert["S1_interval"]
        L1_lo, L1_hi = self.cert["L1_interval"]
        assert lo == pytest.approx(S1_lo - L1_hi, abs=1e-15)
        assert hi == pytest.approx(S1_hi - L1_lo, abs=1e-15)


class TestZeroFreeRegion:
    """Test the zero-free region certificate."""

    @pytest.fixture(autouse=True)
    def load_cert(self):
        cert_path = WITNESS / "derivative_bounds_all_grid.json"
        if not cert_path.exists():
            pytest.skip("Derivative bounds not found")
        self.bounds = json.load(open(cert_path))

    def test_all_grid_points(self):
        assert len(self.bounds) == 205

    def test_all_r_positive(self):
        for k, v in self.bounds.items():
            assert v["r"] > 0, f"r <= 0 at ({k})"

    def test_all_l_positive(self):
        for k, v in self.bounds.items():
            if "L_mod" in v:
                assert v["L_mod"] > 0, f"|L| <= 0 at ({k})"

    def test_coverage_argument(self):
        import math
        r_vals = {}
        for k, v in self.bounds.items():
            s, t = k.split(",")
            r_vals[(float(s), float(t))] = v["r"]

        sigma_centers = [0.65, 0.75, 0.85, 0.95]
        t_centers = [t + 0.5 for t in range(-20, 20)]

        covered = 0
        for sc in sigma_centers:
            for tc in t_centers:
                for gp, r in r_vals.items():
                    d = math.sqrt((sc - gp[0])**2 + (tc - gp[1])**2)
                    if d < r:
                        covered += 1
                        break

        assert covered == 160, f"Only {covered}/160 cells covered"
