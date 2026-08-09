import pytest

from experiments.theta_pencil.support_05_comparison import (
    _smooth_lower_loss,
    certify_support_05_comparison,
)


def test_smooth_lower_loss_is_sharp_enough_for_endpoint_comparison():
    assert 0.057 < _smooth_lower_loss() < 0.059


def test_support_05_comparison_closes_third_eigenvalue_floors():
    pytest.importorskip("flint")
    result = certify_support_05_comparison(192, 100)
    assert -0.163 < result.paired_boundary_prime_lower < -0.162
    assert result.minimum_second_derivative > 1.7
    assert result.tail_determinant_lower > 0.3
    assert result.even_third_floor > 0.14
    assert result.odd_third_floor > 0.34
