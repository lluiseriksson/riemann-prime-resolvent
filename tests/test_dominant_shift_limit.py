import cmath

import pytest

from experiments.theta_pencil.dominant_shift_limit import (
    dominant_shift_canonical_weyl,
    dominant_shift_characteristic,
)


def _integral_exponential(exponent: complex, half_width: float) -> complex:
    return 2.0 * cmath.sinh(exponent * half_width) / exponent


def test_closed_characteristic_matches_direct_source_integrals():
    half_width = 0.72
    z = 0.7 + 0.8j
    plus = _integral_exponential(1.0 + 1j * z, half_width)
    minus = _integral_exponential(-1.0 + 1j * z, half_width)
    direct = -((z - 1j) / (z + 1j)) * plus / minus
    assert dominant_shift_characteristic(half_width, z) == pytest.approx(direct)


def test_dominant_canonical_weyl_converges_to_i_on_upper_half_plane():
    z = 0.7 + 0.8j
    errors = [
        abs(dominant_shift_canonical_weyl(half_width, z) - 1j)
        for half_width in (2.0, 4.0, 8.0)
    ]
    assert errors[0] > errors[1] > errors[2]
    assert errors[-1] < 1.0e-5


def test_dominant_shift_requires_upper_half_plane():
    with pytest.raises(ValueError, match="upper half-plane"):
        dominant_shift_characteristic(1.0, 0.3 - 0.1j)
