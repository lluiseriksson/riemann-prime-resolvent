import numpy as np

from experiments.theta_pencil.cut_endpoint_flux import (
    endpoint_flux_maps,
    endpoint_flux_tail_psd_upper,
)


def test_endpoint_flux_tail_matrix_bounds_direct_partial_sums():
    degree_count = 5
    first_degree = 17
    flux = endpoint_flux_maps(0.5, degree_count)
    upper = endpoint_flux_tail_psd_upper(0.5, degree_count, first_degree)
    rng = np.random.default_rng(20260809)
    for _ in range(10):
        vector = rng.normal(size=3 * degree_count)
        direct = 0.0
        for degree in range(first_degree, 100_000):
            weight_square = (2 * degree + 1) / (
                2.0 * degree**2 * (degree + 1) ** 2
            )
            for plus, minus in flux:
                value = (plus - (-1.0) ** degree * minus) @ vector
                direct += weight_square * value * value
        assert direct <= vector @ upper @ vector + 2e-14


def test_endpoint_flux_maps_have_rank_at_most_six():
    flux = endpoint_flux_maps(0.5, 16)
    assert np.linalg.matrix_rank(flux.reshape(6, -1), tol=1e-12) <= 6
