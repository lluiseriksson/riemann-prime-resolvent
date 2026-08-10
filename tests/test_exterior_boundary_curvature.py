import math

import numpy as np
import pytest

from experiments.theta_pencil.exterior_boundary_curvature import (
    active_exterior_prime_powers,
    exterior_curvature,
    smooth_screw_second,
    smooth_screw_second_series,
)


def test_smooth_kernel_geometric_decomposition():
    for t in (0.3, 0.7, 2.0):
        assert smooth_screw_second_series(t, 100) == pytest.approx(
            smooth_screw_second(t), rel=1.0e-13, abs=1.0e-13
        )


def test_exterior_prime_window_selects_exact_translated_samples():
    half_width = 0.4
    exterior_point = 1.0
    powers = active_exterior_prime_powers(half_width, exterior_point)
    assert powers == (2, 3, 4)
    for integer in powers:
        sample = exterior_point - math.log(integer)
        assert -half_width < sample < half_width


def test_exterior_curvature_splits_smooth_and_prime_terms():
    coordinate = np.linspace(-0.4, 0.4, 4001)
    values = 1.0 - (coordinate / 0.4) ** 2
    smooth, prime, total = exterior_curvature(coordinate, values, 1.0)
    assert total == pytest.approx(smooth + prime)
    assert prime > 0.0
