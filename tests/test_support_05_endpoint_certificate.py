import numpy as np
import pytest

from experiments.theta_pencil.support_05_endpoint_certificate import (
    _arb_flux_upper,
)


def test_arb_flux_upper_dominates_long_direct_sum():
    flint = pytest.importorskip("flint")
    from experiments.theta_pencil.cut_endpoint_flux import endpoint_flux_maps

    degree_count = 3
    transform = np.zeros((3 * degree_count, degree_count + 2))
    transform[:degree_count, :degree_count] = np.eye(degree_count) / np.sqrt(2)
    signs = np.where(np.arange(degree_count) % 2, -1.0, 1.0)
    transform[2 * degree_count :, :degree_count] = np.diag(signs) / np.sqrt(2)
    transform[degree_count + 0, degree_count + 0] = 1
    transform[degree_count + 2, degree_count + 1] = 1

    upper = _arb_flux_upper(
        flint.arb, flint.arb_mat, degree_count, 0, 17, 300
    )
    upper_midpoint = np.array(
        [
            [float(upper[row, column].mid()) for column in range(5)]
            for row in range(5)
        ]
    )
    flux = endpoint_flux_maps(0.5, degree_count)
    rng = np.random.default_rng(271828)
    for _ in range(8):
        vector = rng.normal(size=5)
        original = transform @ vector
        direct = 0.0
        for degree in range(17, 100_000):
            weight = (2 * degree + 1) / (
                2.0 * degree**2 * (degree + 1) ** 2
            )
            for positive, negative in flux:
                value = (positive - (-1.0) ** degree * negative) @ original
                direct += weight * value * value
        assert direct <= vector @ upper_midpoint @ vector + 2e-13
