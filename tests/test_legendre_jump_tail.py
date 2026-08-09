import math

import numpy as np
import pytest
from scipy.integrate import quad

from experiments.theta_pencil.legendre_jump_tail import (
    bernstein_jump_tail_bound,
    normalized_step_coefficient,
    potential_tail_bound,
    potential_operator_tail_bound,
    smooth_kernel_variation_bound,
    temple_lower_bound,
    wang_normalized_coefficient_bound,
    wang_normalized_tail_bound,
)


def test_step_coefficient_matches_direct_integration():
    cut = -0.73
    for degree in (0, 1, 2, 9, 40):
        expected, _ = quad(
            lambda x: np.polynomial.legendre.Legendre.basis(degree)(x)
            * math.sqrt((2 * degree + 1) / 2.0),
            -1.0,
            cut,
            epsabs=1e-13,
        )
        assert normalized_step_coefficient(cut, degree) == pytest.approx(
            expected, abs=3e-13
        )


def test_jump_tail_bound_dominates_sampled_step_tail():
    cut = -0.73
    first = 100
    sampled = math.sqrt(
        math.fsum(
            normalized_step_coefficient(cut, degree) ** 2
            for degree in range(first, 20000)
        )
    )
    bound = bernstein_jump_tail_bound(1.0, (1.0 - cut * cut) ** 0.25, first)
    assert sampled < bound


def test_wang_tail_bound_dominates_sum_of_pointwise_bounds():
    variation = 7.0
    first = 80
    sampled = math.sqrt(
        math.fsum(
            wang_normalized_coefficient_bound(variation, degree) ** 2
            for degree in range(first, 100000)
        )
    )
    assert sampled < wang_normalized_tail_bound(variation, first)


@pytest.mark.parametrize("order", [0, 1, 2, 3])
def test_general_wang_tail_dominates_pointwise_bounds(order):
    variation = 3.0
    first = max(20, 2 * order + 1)
    sampled = math.sqrt(
        math.fsum(
            wang_normalized_coefficient_bound(variation, degree, order) ** 2
            for degree in range(first, 100000)
        )
    )
    assert sampled < wang_normalized_tail_bound(variation, first, order)


def test_smooth_kernel_variation_budget_at_first_prime_window():
    assert smooth_kernel_variation_bound(0.4, 1.0) < 0.23
    with pytest.raises(ValueError):
        smooth_kernel_variation_bound(0.41)


def test_potential_tail_uses_small_signed_endpoint_moment():
    vector = np.zeros(16)
    vector[0] = 1.0
    assert potential_tail_bound(vector, 128, 2) < 1e-2
    assert potential_operator_tail_bound(np.arange(0, 16, 2), 128, 2) > 0.0


def test_temple_bound_and_guards():
    assert temple_lower_bound(2e-4, 2e-4, 5e-3) > 0.0
    with pytest.raises(ValueError):
        temple_lower_bound(2e-4, 1e-4, 1e-4)
