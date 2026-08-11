from fractions import Fraction

from experiments.theta_pencil.support_one_allocated_floor import (
    THETA_FIVE,
    THETA_SEVEN,
    registered_support_one_floor,
)


def test_registered_allocation_is_exact_and_removes_prime_seven_loss():
    assert THETA_FIVE + THETA_SEVEN == Fraction(1)
    result = registered_support_one_floor(95)
    assert result.prime_seven_raw_floor > 7.1e-4
    assert result.prime_seven_floor == 0.0


def test_allocated_floor_moves_tail_start_from_256_to_99():
    result = registered_support_one_floor(95)
    assert result.tail_start == 99
    assert 0.0073 < result.complement_margin < 0.0074
