"""Universal large-negative-shift limit of Suzuki's two-channel quotient."""

from __future__ import annotations

import cmath


def dominant_shift_characteristic(half_width: float, z: complex) -> complex:
    """Return the characteristic ratio when the resolvent is scalar.

    If ``(A-lambda)^-1`` is replaced by its leading term ``-1/lambda``, the
    two source channels are just ``exp(x)`` and ``exp(-x)``.  The fixed
    characteristic prefactor then simplifies to the ratio below.
    """

    if half_width <= 0.0:
        raise ValueError("half_width must be positive")
    if z.imag <= 0.0:
        raise ValueError("z must lie in the upper half-plane")
    denominator = cmath.sinh(half_width * (-1.0 + 1j * z))
    if abs(denominator) == 0.0:
        raise ZeroDivisionError("the dominant minus channel vanishes")
    return -cmath.sinh(half_width * (1.0 + 1j * z)) / denominator


def dominant_shift_canonical_weyl(half_width: float, z: complex) -> complex:
    """Return the canonical Weyl value associated with the dominant ratio."""

    characteristic = dominant_shift_characteristic(half_width, z)
    denominator = 1.0 - characteristic
    if abs(denominator) == 0.0:
        raise ZeroDivisionError("the reference extension has an eigenvalue")
    return 1j * (1.0 + characteristic) / denominator
