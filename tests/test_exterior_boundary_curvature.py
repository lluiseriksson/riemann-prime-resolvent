import math

import numpy as np
import pytest

from experiments.theta_pencil.exterior_boundary_curvature import (
    active_exterior_prime_powers,
    chebyshev_right_prime_tail_bound,
    exterior_curvature,
    normalized_remainder_pairing,
    pnt_centered_prime_window,
    safe_shift_right_prime_tail_bound,
    smooth_screw_second,
    smooth_screw_second_series,
)


def test_pnt_centering_is_the_exact_growing_smooth_counterterm():
    coordinate = np.linspace(-0.4, 0.4, 4001)
    values = coordinate**2 - np.trapezoid(coordinate**2, coordinate) / 0.8
    exterior = 1.2
    prime, main, remainder = pnt_centered_prime_window(
        coordinate, values, exterior
    )
    assert remainder == pytest.approx(prime - main)
    moment = np.trapezoid(np.exp(-coordinate / 2.0) * values, coordinate)
    assert main == pytest.approx(np.exp(exterior / 2.0) * moment)


def test_normalized_remainder_pairing_annihilates_constants_for_mean_zero_source():
    coordinate = np.linspace(-0.7, 0.7, 4001)
    values = coordinate
    derivatives = np.ones_like(coordinate)
    remainder = np.sin(1.3 * coordinate) + 0.2 * coordinate**2
    original = normalized_remainder_pairing(
        coordinate, values, derivatives, remainder
    )
    translated = normalized_remainder_pairing(
        coordinate, values, derivatives, remainder + 17.0
    )
    assert translated == pytest.approx(original, abs=2.0e-14)


def test_one_sided_safe_shift_tail_has_the_eta_two_threshold():
    eta = 2.4
    first = safe_shift_right_prime_tail_bound(8.0, eta)
    second = safe_shift_right_prime_tail_bound(12.0, eta)
    assert second < first
    expected_asymptotic_ratio = np.exp(-(eta - 2.0) * 4.0)
    assert second / first == pytest.approx(expected_asymptotic_ratio, rel=2.0e-4)

    direct = chebyshev_right_prime_tail_bound(1.0, 1.5, 3.0)
    expected = 4.0 * np.log(2.0) * 2.0 * np.exp(-1.0) * 3.0
    assert direct == pytest.approx(expected)
    with pytest.raises(ValueError):
        chebyshev_right_prime_tail_bound(1.0, 0.5, 3.0)


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
