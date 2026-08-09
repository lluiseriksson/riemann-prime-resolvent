import math

import pytest

from experiments.theta_pencil.small_support_bound import (
    coercivity_constant,
    smooth_remainder_second,
)


def test_remainder_has_the_registered_removable_value() -> None:
    assert smooth_remainder_second(0.0) == -7.0 / 4.0
    assert smooth_remainder_second(1e-4) == pytest.approx(-7.0 / 4.0, abs=1e-5)


def test_remainder_bound_on_registered_interval() -> None:
    values = [smooth_remainder_second(k / 8000.0) for k in range(1001)]
    assert max(abs(value) for value in values) < 2.0


def test_endpoint_coercivity_is_strictly_positive() -> None:
    expected = math.log(16.0) - math.log(2.0 * math.pi) - 0.5772156649015329 - 0.25
    assert coercivity_constant(1.0 / 16.0) == pytest.approx(expected)
    assert coercivity_constant(1.0 / 16.0) > 0.107


def test_bound_rejects_unproved_supports() -> None:
    with pytest.raises(ValueError):
        coercivity_constant(0.1)
