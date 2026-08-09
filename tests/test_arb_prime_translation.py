import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss

from experiments.theta_pencil.arb_prime_translation import (
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


@pytest.mark.parametrize("half_width", [0.3, np.log(2.0) / 2.0, 0.56])
def test_prime_two_formula_rejects_widths_outside_first_prime_window(half_width):
    coefficients = np.zeros(4)
    coefficients[::2] = 1.0
    with pytest.raises(ValueError, match="prime-2-only"):
        build_arb_prime_two_matrix(half_width, 4, 8)
    with pytest.raises(ValueError, match="prime-2-only"):
        build_arb_prime_two_action(half_width, coefficients, 8)
