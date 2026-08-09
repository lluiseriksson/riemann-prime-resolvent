import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss

from experiments.theta_pencil.legendre_feshbach import (
    normalized_legendre_values,
    smooth_remainder_second_array,
)
from experiments.theta_pencil.smooth_legendre_series import (
    absolute_power_matrix,
    smooth_kernel_series_matrix,
    smooth_kernel_series_remainder_bound,
    smooth_remainder_series_coefficients,
)


@pytest.mark.parametrize("power", range(6))
def test_absolute_power_matrix_matches_tensor_gauss(power):
    size = 8
    nodes, weights = leggauss(240)
    basis = normalized_legendre_values(nodes, size)
    kernel = np.abs(nodes[:, None] - nodes[None, :]) ** power
    direct = (basis * weights) @ kernel @ (basis * weights).T
    assert absolute_power_matrix(power, size) == pytest.approx(direct, abs=3e-5)


def test_rpp_series_begins_with_registered_coefficients():
    coefficients = smooth_remainder_series_coefficients(4)
    assert float(coefficients[0]) == pytest.approx(-7 / 4)
    assert float(coefficients[1]) == pytest.approx(-1 / 48)
    assert float(coefficients[2]) == pytest.approx(-9 / 32)


def test_smooth_series_matches_direct_kernel_matrix():
    size = 16
    nodes, weights = leggauss(500)
    basis = normalized_legendre_values(nodes, size)
    kernel = -0.4 * smooth_remainder_second_array(
        0.4 * (nodes[:, None] - nodes[None, :])
    )
    direct = (basis * weights) @ kernel @ (basis * weights).T
    series = smooth_kernel_series_matrix(0.4, size, 23)
    assert series == pytest.approx(direct, abs=3e-7)
    assert smooth_kernel_series_remainder_bound(0.4, 23) < 1e-13
