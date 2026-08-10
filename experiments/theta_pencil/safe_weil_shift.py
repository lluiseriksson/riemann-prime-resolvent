"""Explicit unconditional safety shifts for the localized Weil operator."""

from __future__ import annotations

import math

from experiments.theta_pencil.semilocal_weil_matrix import EULER_GAMMA


def archimedean_multiplier_floor() -> float:
    """Return psi(1/4)-log(pi) in elementary constants."""

    return (
        -EULER_GAMMA
        - math.pi / 2.0
        - 3.0 * math.log(2.0)
        - math.log(math.pi)
    )


def prime_weight_upper_bound(half_width: float) -> float:
    """Bound the weighted prime-power sum elementarily.

    Two independent bounds are used.  The first uses Lambda(n) <= 2a.
    The second uses the elementary Chebyshev estimate
    psi(x) <= 4 log(2) x and partial summation.
    """

    if half_width <= 0.0:
        raise ValueError("half_width must be positive")
    direct = 4.0 * half_width * math.expm1(half_width)
    chebyshev = 8.0 * math.log(2.0) * math.exp(half_width)
    return min(direct, chebyshev)


def exact_polar_lower_cost(half_width: float) -> float:
    """Return the exact magnitude of the negative polar eigenvalue.

    The polar operator is ``u tensor v + v tensor u`` for
    ``u=exp(x/2)`` and ``v=exp(-x/2)`` on ``(-a,a)``.  Their squared norms
    are ``2*sinh(a)`` and their inner product is ``2*a``.  Hence the two
    nonzero eigenvalues are ``2*a +/- 2*sinh(a)``.
    """

    if half_width <= 0.0:
        raise ValueError("half_width must be positive")
    return 2.0 * (math.sinh(half_width) - half_width)


def localized_weil_lower_bound(half_width: float) -> float:
    """Return a rigorous scalar lower bound for the localized Weil form."""

    return (
        archimedean_multiplier_floor()
        - exact_polar_lower_cost(half_width)
        - 2.0 * prime_weight_upper_bound(half_width)
    )


def explicit_safe_shift(half_width: float, margin: float = 1.0) -> float:
    """Return a shift strictly below the localized spectral lower bound."""

    if margin <= 0.0:
        raise ValueError("margin must be positive")
    return localized_weil_lower_bound(half_width) - margin


def inverse_mobius_error_scale(half_width: float, margin: float = 1.0) -> float:
    """Return the natural raw-error scale (1+abs(lambda_safe))^-2."""

    shift = explicit_safe_shift(half_width, margin)
    return 1.0 / (1.0 + abs(shift)) ** 2
