import pytest

from experiments.theta_pencil.support_05_comparison import (
    _smooth_lower_loss,
    certify_first_prime_comparison,
    certify_prime_two_comparison,
    certify_second_window_complement_floor,
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


def test_first_prime_comparison_extends_to_point_54():
    pytest.importorskip("flint")
    result = certify_first_prime_comparison(0.54, 192, 100)
    assert result.half_width == 0.54
    assert result.minimum_second_derivative > 1.5
    assert result.tail_determinant_lower > 0
    assert -0.014 < result.even_third_floor < -0.011
    assert result.odd_third_floor > 0.18


def test_first_prime_wrapper_still_rejects_the_second_window():
    pytest.importorskip("flint")
    with pytest.raises(ValueError, match=r"log\(3\)/2"):
        certify_first_prime_comparison(0.551, 192, 80)


def test_prime_two_comparison_and_prime_three_loss_leave_a_positive_floor():
    pytest.importorskip("flint")
    prime_two = certify_prime_two_comparison(0.551, 192, 80)
    result = certify_second_window_complement_floor(0.551, 16, 192, 80)
    assert prime_two.minimum_second_derivative > 0
    assert prime_two.tail_determinant_lower > 0
    assert result.prime_three_norm_upper > 0
    assert result.complement_floor > 0.61
