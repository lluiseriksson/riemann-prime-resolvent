"""Exact-power smooth kernel in the first-prime cut-adapted basis."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_cut_dominant import (
    _local_legendre_coefficients,
)
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.cut_adapted_prime_basis import first_prime_partition
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_remainder_bound,
    smooth_remainder_series_coefficients,
)


@dataclass(frozen=True)
class ArbCutSmoothMatrix:
    midpoint: np.ndarray
    radius: np.ndarray
    analytic_remainder: float
    precision: int


def _absolute_distance_moment(arb, p: int, q: int, power: int, length):
    """Integral u^p v^q |u-v|^power over [0,length]^2."""

    total_degree = p + q + power + 2
    common = length**total_degree / total_degree
    first_beta = (
        arb(math.factorial(q) * math.factorial(power))
        / math.factorial(q + power + 1)
    )
    second_beta = (
        arb(math.factorial(p) * math.factorial(power))
        / math.factorial(p + power + 1)
    )
    return common * (first_beta + second_beta)


def _separated_distance_moment(
    arb, p: int, q: int, power: int, left_length, right_length, gap
):
    """Integral u^p v^q (gap+u+v)^power on a rectangle."""

    result = arb(0)
    factorial = math.factorial(power)
    for gap_power in range(power + 1):
        for left_power in range(power - gap_power + 1):
            right_power = power - gap_power - left_power
            multinomial = factorial // (
                math.factorial(gap_power)
                * math.factorial(left_power)
                * math.factorial(right_power)
            )
            result += (
                multinomial
                * gap**gap_power
                * left_length ** (p + left_power + 1)
                / (p + left_power + 1)
                * right_length ** (q + right_power + 1)
                / (q + right_power + 1)
            )
    return result


def _power_block(
    arb,
    arb_mat,
    left_length,
    right_length,
    gap,
    degree_count: int,
    power: int,
    same_interval: bool,
):
    return _power_block_rectangular(
        arb,
        arb_mat,
        left_length,
        right_length,
        gap,
        degree_count,
        degree_count,
        power,
        same_interval,
    )


def _power_block_rectangular(
    arb,
    arb_mat,
    left_length,
    right_length,
    gap,
    left_degree_count: int,
    right_degree_count: int,
    power: int,
    same_interval: bool,
):
    """Power-kernel block for possibly different local degree counts."""

    if same_interval and left_degree_count != right_degree_count:
        raise ValueError("a diagonal power block must be square")
    left = _local_legendre_coefficients(
        arb, left_length, left_degree_count, reversed_=not same_interval
    )
    right = _local_legendre_coefficients(
        arb, right_length, right_degree_count, reversed_=False
    )
    moments = []
    for p in range(left_degree_count):
        row = []
        for q in range(right_degree_count):
            if same_interval:
                value = _absolute_distance_moment(
                    arb, p, q, power, left_length
                )
            else:
                value = _separated_distance_moment(
                    arb,
                    p,
                    q,
                    power,
                    left_length,
                    right_length,
                    gap,
                )
            row.append(value)
        moments.append(row)
    right_transpose = [
        [right[row][column] for row in range(right_degree_count)]
        for column in range(right_degree_count)
    ]
    return arb_mat(left) * arb_mat(moments) * arb_mat(right_transpose)


def build_arb_cut_smooth_matrix(
    half_width: float,
    degree_count: int,
    maximum_power: int = 23,
    precision: int = 256,
) -> ArbCutSmoothMatrix:
    """Build the truncated smooth-kernel series in the three-interval basis."""

    if degree_count < 1:
        raise ValueError("degree_count must be positive")
    if maximum_power < 1:
        raise ValueError("maximum_power must be positive")
    first_prime_partition(half_width)
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = arb(str(half_width))
        displacement = arb.const_log2() / a
        edge_length = arb(2) - displacement
        center_length = arb(2) * displacement - arb(2)
        lengths = (edge_length, center_length, edge_length)
        total = 3 * degree_count
        matrix = [[arb(0) for _ in range(total)] for _ in range(total)]
        coefficients = smooth_remainder_series_coefficients(maximum_power)

        for left_block in range(3):
            for right_block in range(left_block, 3):
                same = left_block == right_block
                gap = arb(0)
                if (left_block, right_block) == (0, 2):
                    gap = center_length
                block = arb_mat(degree_count, degree_count)
                for power, coefficient in enumerate(coefficients):
                    power_matrix = _power_block(
                        arb,
                        arb_mat,
                        lengths[left_block],
                        lengths[right_block],
                        gap,
                        degree_count,
                        power,
                        same,
                    )
                    rational = arb(coefficient.numerator) / coefficient.denominator
                    block += (-a * rational * a**power) * power_matrix
                for left in range(degree_count):
                    for right in range(degree_count):
                        value = block[left, right]
                        matrix[left_block * degree_count + left][
                            right_block * degree_count + right
                        ] = value
                        matrix[right_block * degree_count + right][
                            left_block * degree_count + left
                        ] = value

        midpoint = np.empty((total, total), dtype=float)
        radius = np.empty_like(midpoint)
        for left in range(total):
            for right in range(total):
                value = matrix[left][right]
                midpoint[left, right] = float(value.mid())
                radius[left, right] = _arb_radius_as_float(value)
    finally:
        ctx.prec = previous_precision

    return ArbCutSmoothMatrix(
        midpoint=midpoint,
        radius=radius,
        analytic_remainder=smooth_kernel_series_remainder_bound(
            half_width, maximum_power
        ),
        precision=precision,
    )
