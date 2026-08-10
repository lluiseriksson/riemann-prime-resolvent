"""Rigorous comparison floors in the upper part of the first-prime window."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_remainder_bound,
    smooth_remainder_series_coefficients,
)
from experiments.theta_pencil.support_window import (
    at_most_prime_three_boundary,
    in_prime_two_comparison_window,
    in_second_prime_window,
)


@dataclass(frozen=True)
class Support05Comparison:
    half_width: float
    paired_boundary_prime_lower: float
    smooth_lower_loss: float
    even_third_floor: float
    odd_third_floor: float
    minimum_second_derivative: float
    tail_determinant_lower: float
    precision: int


@dataclass(frozen=True)
class SecondWindowComplementFloor:
    half_width: float
    local_degree: int
    harmonic_floor: float
    prime_two_perturbation_lower: float
    prime_three_norm_upper: float
    complement_floor: float
    precision: int


def _smooth_lower_loss(
    half_width: float = 0.5, maximum_power: int = 23
) -> float:
    """Upper bound C such that the smooth operator is at least -C I.

    The constant kernel (power zero) is positive semidefinite.  At power two,
    the kernel |x-y|^2 has least eigenvalue -4/3.  Power one and powers at
    least three use the Schur test
    sup_x integral |x-y|^p dy = 2^(p+1)/(p+1).
    """

    if maximum_power < 3:
        raise ValueError("maximum_power must be at least three")
    if not 0.0 < half_width < 1.5:
        raise ValueError("require 0 < a < 3/2")
    coefficients = smooth_remainder_series_coefficients(maximum_power)
    a = Fraction(str(half_width))
    # Power one has coefficient a^2/48 and Schur norm at most 2.
    loss = a * a / 24
    # Power two has coefficient 9a^3/32 and least eigenvalue -4/3.
    loss += 3 * a**3 / 8
    for power, coefficient in enumerate(coefficients):
        if power < 3:
            continue
        loss += (
            2
            * a
            * abs(coefficient)
            * (2 * a) ** power
            / (power + 1)
        )
    remainder = smooth_kernel_series_remainder_bound(half_width, maximum_power)
    return math.nextafter(float(loss) + remainder, math.inf)


def certify_prime_two_comparison(
    half_width: float,
    precision: int = 256,
    subdivisions: int = 300,
) -> Support05Comparison:
    """Certify the prime-two comparison for ``1/2 <= a < log(2)``.

    The translated edge points are ``z-t`` and ``z+t`` with
    ``t=log(2)/(2a)``.  The determinant after shifting by
    ``V(t)-log(2)/sqrt(2)`` is even, vanishes at zero, and is convex on the
    central interval.  The remaining short endpoint interval is handled by
    monotonicity exactly as in the original ``a=1/2`` certificate.

    This comparison intentionally omits every prime other than two.  In the
    second prime window it is a lower comparison for the prime-two part, not
    a certificate for the full operator.
    """

    if not in_prime_two_comparison_window(half_width):
        raise ValueError("the prime-two comparison requires 1/2 <= a < log(2)")
    if subdivisions < 1:
        raise ValueError("subdivisions must be positive")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        one = arb(1)
        a = arb(str(half_width))
        t = arb.const_log2() / (2 * a)
        prime = arb.const_log2() / arb(2).sqrt()

        def potential(value):
            return -(one - value * value).log() / 2

        def first(value):
            return value / (one - value * value)

        def second(value):
            return (one + value * value) / (one - value * value) ** 2

        paired_floor = potential(t) - prime
        minimum_second = math.inf
        denominator = 10 * subdivisions
        for index in range(3 * subdivisions):
            lower = arb(index) / denominator
            upper = arb(index + 1) / denominator
            midpoint = (lower + upper) / 2
            z = midpoint + arb(0, (upper - lower) / 2)
            left = z - t
            right = z + t
            left_shifted = potential(left) - paired_floor
            right_shifted = potential(right) - paired_floor
            determinant_second = (
                second(left) * right_shifted
                + 2 * first(left) * first(right)
                + left_shifted * second(right)
            )
            if not determinant_second.lower() > 0:
                raise ArithmeticError("the determinant convexity check was unresolved")
            minimum_second = min(minimum_second, float(determinant_second.lower()))

        z0 = arb(3) / 10
        left_minimum = potential(one - 2 * t) - paired_floor
        right_minimum = potential(t + z0) - paired_floor
        tail_determinant = left_minimum * right_minimum - prime**2
        if not tail_determinant.lower() > 0:
            raise ArithmeticError("the endpoint determinant check was unresolved")

        scalar = -a.log() - (arb(2) * arb.pi()).log() - arb.const_euler()
        smooth_loss = arb(str(_smooth_lower_loss(half_width)))
        harmonic_four = sum((arb(1) / degree for degree in range(1, 5)), arb(0))
        harmonic_five = harmonic_four + arb(1) / 5
        even_floor = harmonic_four + scalar + paired_floor - smooth_loss
        odd_floor = harmonic_five + scalar + paired_floor - smooth_loss
    finally:
        ctx.prec = previous_precision

    return Support05Comparison(
        half_width=half_width,
        paired_boundary_prime_lower=float(paired_floor.lower()),
        smooth_lower_loss=_smooth_lower_loss(half_width),
        even_third_floor=float(even_floor.lower()),
        odd_third_floor=float(odd_floor.lower()),
        minimum_second_derivative=minimum_second,
        tail_determinant_lower=float(tail_determinant.lower()),
        precision=precision,
    )


def certify_first_prime_comparison(
    half_width: float,
    precision: int = 256,
    subdivisions: int = 300,
) -> Support05Comparison:
    """Certify comparison floors in the prime-two-only support window."""

    if not 0.5 <= half_width or not at_most_prime_three_boundary(half_width):
        raise ValueError("the comparison certificate requires 1/2 <= a <= log(3)/2")
    return certify_prime_two_comparison(half_width, precision, subdivisions)


def certify_second_window_complement_floor(
    half_width: float,
    local_degree: int = 16,
    precision: int = 256,
    subdivisions: int = 300,
) -> SecondWindowComplementFloor:
    """Lower-bound the common complement after activating prime three.

    A complement orthogonal to every local polynomial of degree below ``d``
    is orthogonal to the global polynomials of those degrees, so the dominant
    form contributes at least ``H_d``.  The prime-two comparison supplies the
    remaining lower perturbation.  The new prime-three translation has norm
    at most ``log(3)/sqrt(3)`` and is subtracted once.
    """

    if not in_second_prime_window(half_width):
        raise ValueError("the complement floor is for the second prime window")
    if local_degree < 4:
        raise ValueError("local_degree must be at least four")
    comparison = certify_prime_two_comparison(
        half_width, precision, subdivisions
    )
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        harmonic = sum((arb(1) / k for k in range(1, local_degree + 1)), arb(0))
        harmonic_four = sum((arb(1) / k for k in range(1, 5)), arb(0))
        perturbation = arb(str(comparison.even_third_floor)) - harmonic_four
        prime_three = arb(3).log() / arb(3).sqrt()
        floor = harmonic + perturbation - prime_three
        if not floor.lower() > 0:
            raise ArithmeticError("the second-window complement floor is unresolved")
    finally:
        ctx.prec = previous_precision

    return SecondWindowComplementFloor(
        half_width=half_width,
        local_degree=local_degree,
        harmonic_floor=float(harmonic.lower()),
        prime_two_perturbation_lower=float(perturbation.lower()),
        prime_three_norm_upper=math.nextafter(float(prime_three.upper()), math.inf),
        complement_floor=float(floor.lower()),
        precision=precision,
    )


def certify_support_05_comparison(
    precision: int = 256,
    subdivisions: int = 300,
) -> Support05Comparison:
    """Certify the pointwise prime--boundary floor and parity tail floors.

    On a translated edge pair write x=z-log(2), y=z+log(2).  The smallest
    eigenvalue of the two-by-two multiplication matrix is bounded below by
    m=V(log(2))-log(2)/sqrt(2).  Equivalently, its shifted determinant is
    nonnegative.  The determinant is even, vanishes at zero, and has positive
    second derivative on 0 <= z <= 3/10; Arb checks the latter interval by
    interval subdivision.  Monotonicity of V on either side gives a direct
    positive product bound on the remaining endpoint interval.
    """

    result = certify_first_prime_comparison(0.5, precision, subdivisions)
    if result.even_third_floor <= 0.01 or result.odd_third_floor <= 0.3:
        raise ArithmeticError("the endpoint third-eigenvalue floors did not close")
    return result
