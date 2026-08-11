import math
from fractions import Fraction

from experiments.theta_pencil.support_one_allocated_floor import (
    THETA_FIVE,
    THETA_SEVEN,
    joint_dyadic_floor,
    registered_support_one_floor,
)


def test_registered_allocation_is_exact_and_removes_prime_seven_loss():
    assert THETA_FIVE + THETA_SEVEN == Fraction(1)
    result = registered_support_one_floor(95)
    assert result.prime_seven_raw_floor > 7.1e-4
    assert result.prime_seven_floor == 0.0


def test_joint_dyadic_floor_moves_tail_start_from_256_to_85():
    result = registered_support_one_floor(95)
    assert result.tail_start == 85
    assert 0.0076 < result.complement_margin < 0.0077


def test_joint_dyadic_floor_beats_separate_path_floors():
    result = registered_support_one_floor(95)
    expected = -math.log(2.0) * (1.0 + math.sqrt(17.0)) / 4.0
    assert joint_dyadic_floor() == expected
    assert result.joint_two_four_floor == expected
    assert 0.1519 < result.joint_two_four_gain < 0.1520
