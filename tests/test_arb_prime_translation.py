import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss

from experiments.theta_pencil.arb_prime_translation import (
    _restarted_arb_legendre_values,
    build_arb_active_prime_action,
    build_arb_prime_action,
    build_arb_prime_matrix,
    build_arb_prime_two_action,
    build_arb_prime_two_matrix,
)
from experiments.theta_pencil.legendre_feshbach import normalized_legendre_values


def test_arb_prime_matrix_encloses_independent_gauss_values():
    pytest.importorskip("flint")
    low = 8
    maximum = 32
    result = build_arb_prime_two_matrix(0.4, low, maximum, precision=512)
    shift = np.log(2.0) / 0.4
    cut = 1.0 - shift
    nodes, weights = leggauss(40)
    x = (cut + 1.0) * nodes / 2.0 + (cut - 1.0) / 2.0
    scaled = weights * (cut + 1.0) / 2.0
    at_x = normalized_legendre_values(x, maximum)
    at_shift = normalized_legendre_values(x + shift, maximum)
    direct = -np.log(2.0) / np.sqrt(2.0) * (
        (at_shift[:low] * scaled) @ at_x.T
        + (at_x[:low] * scaled) @ at_shift.T
    )
    error = np.abs(result.midpoint - direct)
    assert np.max(error) < 2e-13
    assert np.max(result.radius) < 1e-40


def test_streamed_arb_action_matches_matrix_product():
    coefficients = np.zeros(12)
    coefficients[::2] = np.linspace(0.1, 0.6, 6)
    action = build_arb_prime_two_action(0.4, coefficients, 80, precision=1024)
    matrix = build_arb_prime_two_matrix(0.4, 12, 80, precision=1024)
    expected = coefficients @ matrix.midpoint
    assert np.max(action.radius) < 1.0e-100
    assert np.max(np.abs(action.midpoint - expected)) < 1.0e-13


def test_streamed_odd_action_matches_matrix_product_at_second_width():
    coefficients = np.zeros(12)
    coefficients[1::2] = np.linspace(0.1, 0.6, 6)
    action = build_arb_prime_two_action(0.42, coefficients, 80, precision=1024)
    matrix = build_arb_prime_two_matrix(0.42, 12, 80, precision=1024)
    expected = coefficients @ matrix.midpoint
    assert np.max(action.radius) < 1.0e-100
    assert np.max(np.abs(action.midpoint - expected)) < 1.0e-13


def test_streamed_prime_three_action_matches_independent_gauss_quadrature():
    coefficients = np.zeros(8)
    coefficients[::2] = np.linspace(0.1, 0.4, 4)
    maximum = 32
    action = build_arb_prime_action(0.62, 3, coefficients, maximum, 1024)
    shift = np.log(3.0) / 0.62
    cut = 1.0 - shift
    nodes, weights = leggauss(40)
    x = (cut + 1.0) * nodes / 2.0 + (cut - 1.0) / 2.0
    scaled = weights * (cut + 1.0) / 2.0
    at_x = normalized_legendre_values(x, maximum)
    at_shift = normalized_legendre_values(x + shift, maximum)
    matrix = -np.log(3.0) / np.sqrt(3.0) * (
        (at_shift[: len(coefficients)] * scaled) @ at_x.T
        + (at_x[: len(coefficients)] * scaled) @ at_shift.T
    )
    expected = coefficients @ matrix
    assert np.max(action.radius) < 1.0e-100
    assert np.max(np.abs(action.midpoint - expected)) < 1.0e-13


def test_prime_three_matrix_encloses_independent_gauss_values():
    low = 8
    maximum = 32
    result = build_arb_prime_matrix(0.62, 3, low, maximum, precision=512)
    shift = np.log(3.0) / 0.62
    cut = 1.0 - shift
    nodes, weights = leggauss(40)
    x = (cut + 1.0) * nodes / 2.0 + (cut - 1.0) / 2.0
    scaled = weights * (cut + 1.0) / 2.0
    at_x = normalized_legendre_values(x, maximum)
    at_shift = normalized_legendre_values(x + shift, maximum)
    direct = -np.log(3.0) / np.sqrt(3.0) * (
        (at_shift[:low] * scaled) @ at_x.T
        + (at_x[:low] * scaled) @ at_shift.T
    )
    assert np.max(np.abs(result.midpoint - direct)) < 2e-13
    assert np.max(result.radius) < 1e-40


def test_active_prime_action_contains_sum_of_individual_actions():
    coefficients = np.zeros(8)
    coefficients[1::2] = np.linspace(0.1, 0.4, 4)
    individual = [
        build_arb_prime_action(0.62, prime, coefficients, 32, 1024)
        for prime in (2, 3)
    ]
    combined = build_arb_active_prime_action(
        0.62, coefficients, 32, (2, 3), 1024
    )
    expected = individual[0].midpoint + individual[1].midpoint
    assert np.all(np.abs(combined.midpoint - expected) <= combined.radius)


@pytest.mark.parametrize("half_width", [0.3, np.log(2.0) / 2.0, 0.56])
def test_prime_two_formula_rejects_widths_outside_first_prime_window(half_width):
    coefficients = np.zeros(4)
    coefficients[::2] = 1.0
    with pytest.raises(ValueError, match="prime-2-only"):
        build_arb_prime_two_matrix(half_width, 4, 8)
    with pytest.raises(ValueError, match="prime-2-only"):
        build_arb_prime_two_action(half_width, coefficients, 8)


def test_restarted_legendre_recurrence_encloses_direct_values():
    from flint import arb

    cut = arb("-0.2836046756755068", "1e-30")
    values = _restarted_arb_legendre_values(cut, 24, arb, stride=5)
    for degree, value in enumerate(values):
        assert (value - cut.legendre_p(degree)).contains(0)
