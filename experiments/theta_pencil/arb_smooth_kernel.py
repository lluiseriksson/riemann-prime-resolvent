"""Arb enclosure of the finite smooth-kernel Legendre matrix."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_remainder_series_coefficients,
)


@dataclass(frozen=True)
class ArbSmoothMatrix:
    midpoint: np.ndarray
    radius: np.ndarray
    analytic_remainder: float
    precision: int


def build_arb_smooth_matrix(
    half_width: float,
    row_dimension: int,
    column_dimension: int,
    maximum_power: int = 23,
    precision: int = 256,
) -> ArbSmoothMatrix:
    if not 0.0 < half_width <= 0.5:
        raise ValueError("the exact Arb implementation applies for 0 < a <= 1/2")
    if not 1 <= row_dimension <= column_dimension:
        raise ValueError("require 1 <= row_dimension <= column_dimension")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        rows = row_dimension
        columns = column_dimension
        work = columns + maximum_power + 2
        normalizations = [(arb(2 * degree + 1) / 2).sqrt() for degree in range(work)]

        monomials: list[list] = []
        constant = [arb(0) for _ in range(work)]
        constant[0] = arb(2).sqrt()
        monomials.append(constant)
        for _ in range(maximum_power):
            previous = monomials[-1]
            following = [arb(0) for _ in range(work)]
            for degree in range(work - 1):
                link = arb(degree + 1) / arb(
                    (2 * degree + 1) * (2 * degree + 3)
                ).sqrt()
                following[degree] += link * previous[degree + 1]
                following[degree + 1] += link * previous[degree]
            monomials.append(following)

        total = [[arb(0) for _ in range(columns)] for _ in range(rows)]
        series = smooth_remainder_series_coefficients(maximum_power)
        a = arb(str(half_width))
        for power, rational_coefficient in enumerate(series):
            polynomial = [[arb(0) for _ in range(columns)] for _ in range(rows)]
            for left_power in range(power + 1):
                right_power = power - left_power
                coefficient = math.comb(power, left_power) * (-1) ** right_power
                left_vector = monomials[left_power]
                right_vector = monomials[right_power]
                for left in range(rows):
                    factor = coefficient * left_vector[left]
                    if factor == 0:
                        continue
                    for right in range(columns):
                        polynomial[left][right] += factor * right_vector[right]

            if power % 2 == 0:
                kernel_matrix = polynomial
            else:
                kernel_matrix = [[-value for value in row] for row in polynomial]
                multiplier = 2 * math.factorial(power)
                for input_degree in range(columns):
                    standard = [arb(0) for _ in range(input_degree + 1)]
                    standard[input_degree] = normalizations[input_degree]
                    for _ in range(power + 1):
                        integrated = [arb(0) for _ in range(len(standard) + 1)]
                        integrated[0] += standard[0]
                        integrated[1] += standard[0]
                        for degree in range(1, len(standard)):
                            integrated[degree + 1] += standard[degree] / (
                                2 * degree + 1
                            )
                            integrated[degree - 1] -= standard[degree] / (
                                2 * degree + 1
                            )
                        standard = integrated
                    for output_degree in range(min(rows, len(standard))):
                        kernel_matrix[output_degree][input_degree] += (
                            multiplier
                            * standard[output_degree]
                            / normalizations[output_degree]
                        )

            rational = arb(rational_coefficient.numerator) / rational_coefficient.denominator
            scale = -a * rational * a**power
            for left in range(rows):
                for right in range(columns):
                    total[left][right] += scale * kernel_matrix[left][right]

        midpoint = np.empty((rows, columns), dtype=float)
        radius = np.empty_like(midpoint)
        for left in range(rows):
            for right in range(columns):
                midpoint[left, right] = float(total[left][right].mid())
                radius[left, right] = _arb_radius_as_float(total[left][right])
    finally:
        ctx.prec = previous_precision

    # Imported lazily to keep the exact matrix construction independent.
    from experiments.theta_pencil.smooth_legendre_series import (
        smooth_kernel_series_remainder_bound,
    )

    return ArbSmoothMatrix(
        midpoint=midpoint,
        radius=radius,
        analytic_remainder=smooth_kernel_series_remainder_bound(
            half_width, maximum_power
        ),
        precision=precision,
    )
