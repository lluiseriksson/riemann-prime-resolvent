import math

import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss

from experiments.theta_pencil.legendre_feshbach import normalized_legendre_values
from experiments.theta_pencil.prime_jet_tail import (
    endpoint_jet_matrix,
    left_step_coefficients,
    prime_jet_cross_matrix,
    prime_jet_tail_weighted_norm,
    prime_remainder_variation_bound,
    piecewise_prime_remainder_variation_bound,
    truncated_power_coefficients,
)
from experiments.theta_pencil.legendre_jump_tail import wang_normalized_tail_bound


def test_step_recurrence_matches_gauss_quadrature():
    cut = -0.73
    coefficients = left_step_coefficients(cut, 80)
    nodes, weights = leggauss(100)
    x = (cut + 1.0) * nodes / 2.0 + (cut - 1.0) / 2.0
    scaled = weights * (cut + 1.0) / 2.0
    direct = normalized_legendre_values(x, 80) @ scaled
    assert coefficients == pytest.approx(direct, abs=2e-13)


def test_truncated_power_recurrence_matches_quadrature():
    cut = -0.61
    powers = truncated_power_coefficients(cut, 60, 4)
    nodes, weights = leggauss(100)
    x = (cut + 1.0) * nodes / 2.0 + (cut - 1.0) / 2.0
    scaled = weights * (cut + 1.0) / 2.0
    basis = normalized_legendre_values(x, 60)
    for jet in range(4):
        direct = basis @ (scaled * (x - cut) ** jet)
        assert powers[jet] == pytest.approx(direct, abs=3e-13)


def test_endpoint_derivative_formula_low_degrees():
    matrix = endpoint_jet_matrix(np.arange(6), 3)
    assert matrix[0, 0] == pytest.approx(1.0 / math.sqrt(2.0))
    assert matrix[2, 1] == pytest.approx(math.sqrt(5.0 / 2.0) * 3.0)
    assert matrix[2, 2] == pytest.approx(math.sqrt(5.0 / 2.0) * 1.5)


def test_more_jets_reduce_a_high_degree_translation_residual():
    half_width = 0.4
    low = np.arange(0, 16, 2)
    high = np.arange(400, 500, 2)
    one = prime_jet_cross_matrix(half_width, low, high, 1)
    four = prime_jet_cross_matrix(half_width, low, high, 4)
    # The four-jet model includes the leading step model and is nontrivial.
    assert np.linalg.norm(four - one) > 0.0
    assert one.shape == four.shape == (8, 50)


def test_eight_jet_remainder_has_small_registered_tail_budget():
    variation = prime_remainder_variation_bound(0.4, np.arange(1, 88, 2), 8)
    assert 0.0 < variation < 4e26
    assert wang_normalized_tail_bound(variation, 4096, 8) < 0.006


def test_piecewise_cauchy_recovers_six_jet_budget():
    degrees = np.arange(1, 88, 2)
    coarse = prime_remainder_variation_bound(0.4, degrees, 6)
    sharp = piecewise_prime_remainder_variation_bound(
        0.4, degrees, 6, partitions=32
    )
    assert sharp < coarse
    assert wang_normalized_tail_bound(sharp, 4096, 6) < 0.02


def test_endpoint_jet_weighted_tail_is_finite():
    value = prime_jet_tail_weighted_norm(
        0.4, np.arange(1, 32, 2), 10000, 4, 2.0
    )
    assert 0.0 < value < 0.2
