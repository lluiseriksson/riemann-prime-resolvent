import math

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.special import eval_legendre

from experiments.theta_pencil.legendre_log_matrix import (
    boundary_potential_matrix,
    diagonal_correction,
    dominant_operator_matrix,
    harmonic,
    legendre_log_integral,
)


def numerical_log_integral(left: int, right: int) -> float:
    value, _ = quad(
        lambda x: eval_legendre(left, x)
        * eval_legendre(right, x)
        * math.log1p(-(x * x)),
        -1.0,
        1.0,
        epsabs=2e-13,
        epsrel=2e-13,
        limit=300,
    )
    return value


@pytest.mark.parametrize(
    ("left", "right"),
    [(0, 0), (1, 1), (5, 5), (0, 8), (3, 9), (10, 20), (19, 21), (4, 7)],
)
def test_closed_log_integral_matches_independent_quadrature(left, right):
    assert legendre_log_integral(left, right) == pytest.approx(
        numerical_log_integral(left, right), abs=3e-12
    )


def test_low_degree_exact_values():
    assert legendre_log_integral(0, 2) == pytest.approx(-2.0 / 3.0)
    assert legendre_log_integral(1, 3) == pytest.approx(-2.0 / 5.0)
    assert legendre_log_integral(2, 4) == pytest.approx(-2.0 / 7.0)
    assert diagonal_correction(0) == 1.0
    assert diagonal_correction(1) == pytest.approx(4.0 / 3.0)


def test_boundary_matrix_normalization_against_integrals():
    size = 7
    matrix = boundary_potential_matrix(size)
    for left in range(size):
        for right in range(size):
            normalization = math.sqrt((2 * left + 1) * (2 * right + 1)) / 2.0
            expected = -0.5 * normalization * legendre_log_integral(left, right)
            assert matrix[left, right] == pytest.approx(expected, abs=2e-14)


def test_dominant_operator_is_symmetric_positive_in_finite_sections():
    matrix = dominant_operator_matrix(64)
    assert np.array_equal(matrix, matrix.T)
    assert np.linalg.eigvalsh(matrix)[0] > 0.0
    assert harmonic(0) == 0.0
    assert harmonic(10) == pytest.approx(2.9289682539682538)


@pytest.mark.parametrize("bad", [-2, -1])
def test_negative_indices_rejected(bad):
    with pytest.raises(ValueError):
        harmonic(bad)
    with pytest.raises(ValueError):
        diagonal_correction(bad)
    with pytest.raises(ValueError):
        legendre_log_integral(bad, 0)

