"""Rigorous comparison floors for the endpoint support a = 1/2."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_remainder_bound,
    smooth_remainder_series_coefficients,
)


@dataclass(frozen=True)
class Support05Comparison:
    paired_boundary_prime_lower: float
    smooth_lower_loss: float
    even_third_floor: float
    odd_third_floor: float
    minimum_second_derivative: float
    tail_determinant_lower: float
    precision: int


def _smooth_lower_loss(maximum_power: int = 23) -> float:
    """Upper bound C such that the smooth operator is at least -C I.

    The constant kernel (power zero) is positive semidefinite.  At power two,
    the kernel |x-y|^2 has least eigenvalue -4/3, giving the exact loss 3/64
    at a=1/2.  Power one and powers at least three use the Schur test
    sup_x integral |x-y|^p dy = 2^(p+1)/(p+1).
    """

    if maximum_power < 3:
        raise ValueError("maximum_power must be at least three")
    coefficients = smooth_remainder_series_coefficients(maximum_power)
    # Power one: coefficient 1/192 and Schur norm at most 2.
    loss = Fraction(1, 96)
    # Power two: coefficient 9/256 and lambda_min(|x-y|^2) = -4/3.
    loss += Fraction(3, 64)
    a = Fraction(1, 2)
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
    remainder = smooth_kernel_series_remainder_bound(0.5, maximum_power)
    return math.nextafter(float(loss) + remainder, math.inf)


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
        t = arb.const_log2()
        prime = t / arb(2).sqrt()

        def potential(value):
            return -(one - value * value).log() / 2

        def first(value):
            return value / (one - value * value)

        def second(value):
            return (one + value * value) / (one - value * value) ** 2

        paired_floor = potential(t) - prime
        minimum_second = math.inf
        denominator = 10 * subdivisions
        # The certified central interval is [0, 3/10].
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
                raise ArithmeticError(
                    "the determinant convexity check was unresolved"
                )
            minimum_second = min(
                minimum_second, float(determinant_second.lower())
            )

        z0 = arb(3) / 10
        # For z >= z0, V(z-log2) decreases to V(1-2log2), while
        # V(z+log2) increases.  Their shifted product therefore has this
        # elementary positive lower bound.
        left_minimum = potential(one - 2 * t) - paired_floor
        right_minimum = potential(t + z0) - paired_floor
        tail_determinant = left_minimum * right_minimum - prime**2
        if not tail_determinant.lower() > 0:
            raise ArithmeticError("the endpoint determinant check was unresolved")

        a = arb(1) / 2
        scalar = -a.log() - (arb(2) * arb.pi()).log() - arb.const_euler()
        smooth_loss = arb(str(_smooth_lower_loss()))
        harmonic_four = sum((arb(1) / degree for degree in range(1, 5)), arb(0))
        harmonic_five = harmonic_four + arb(1) / 5
        even_floor = harmonic_four + scalar + paired_floor - smooth_loss
        odd_floor = harmonic_five + scalar + paired_floor - smooth_loss
        if not even_floor.lower() > arb("0.01"):
            raise ArithmeticError("the even third-eigenvalue floor did not close")
        if not odd_floor.lower() > arb("0.3"):
            raise ArithmeticError("the odd third-eigenvalue floor did not close")
    finally:
        ctx.prec = previous_precision

    return Support05Comparison(
        paired_boundary_prime_lower=float(paired_floor.lower()),
        smooth_lower_loss=_smooth_lower_loss(),
        even_third_floor=float(even_floor.lower()),
        odd_third_floor=float(odd_floor.lower()),
        minimum_second_derivative=minimum_second,
        tail_determinant_lower=float(tail_determinant.lower()),
        precision=precision,
    )
