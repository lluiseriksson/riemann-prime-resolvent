"""Arb matrix of Suzuki's scale-free form in the cut-adapted basis."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.cut_adapted_prime_basis import first_prime_partition


@dataclass(frozen=True)
class ArbCutDominantMatrix:
    midpoint: np.ndarray
    radius: np.ndarray
    precision: int


def _log_moment(arb, power: int, length, offset):
    """Integral_0^length u^power log(u+offset) du."""
    if offset.is_zero():
        exponent = power + 1
        return length**exponent * (
            length.log() / exponent - arb(1) / exponent**2
        )

    result = arb(0)
    for degree in range(power + 1):
        coefficient = math.comb(power, degree) * (-offset) ** (power - degree)
        exponent = degree + 1

        def primitive(value):
            return value**exponent * (
                value.log() / exponent - arb(1) / exponent**2
            )

        result += coefficient * (
            primitive(offset + length) - primitive(offset)
        )
    return result


def _inverse_distance_moment(arb, p: int, q: int, left_length, right_length, gap):
    """Integral u^p v^q/(gap+u+v) on a rectangle from the touching edges."""
    # The closed form below has a polynomial loop through q.  Swap variables
    # when possible so rectangular low--high blocks scale with the low degree.
    if q > p:
        return _inverse_distance_moment(
            arb, q, p, right_length, left_length, gap
        )
    polynomial = arb(0)
    for k in range(q):
        outer = arb(0)
        for degree in range(k + 1):
            outer += (
                math.comb(k, degree)
                * gap ** (k - degree)
                * left_length ** (p + degree + 1)
                / (p + degree + 1)
            )
        polynomial += (
            (-1) ** k
            * right_length ** (q - k)
            / (q - k)
            * outer
        )

    logarithmic = arb(0)
    for degree in range(q + 1):
        coefficient = math.comb(q, degree) * gap ** (q - degree)
        logarithmic += coefficient * (
            _log_moment(
                arb, p + degree, left_length, gap + right_length
            )
            - _log_moment(arb, p + degree, left_length, gap)
        )
    return polynomial + (-1) ** q * logarithmic


def _local_legendre_coefficients(arb, length, degree_count: int, reversed_: bool):
    """Rows are normalized local Legendre polynomials in powers of edge distance."""
    coordinate = [-arb(1), arb(2) / length]
    rows = [[arb(1)]]
    if degree_count > 1:
        rows.append(coordinate)
    for degree in range(1, degree_count - 1):
        product = [arb(0)] * (len(rows[-1]) + 1)
        for left, value in enumerate(rows[-1]):
            for right, factor in enumerate(coordinate):
                product[left + right] += value * factor
        following = [
            ((2 * degree + 1) * value) / (degree + 1)
            for value in product
        ]
        for index, value in enumerate(rows[-2]):
            following[index] -= degree * value / (degree + 1)
        rows.append(following)

    result = []
    for degree, row in enumerate(rows):
        sign = -1 if reversed_ and degree % 2 else 1
        normalization = (arb(2 * degree + 1) / length).sqrt()
        result.append(
            [sign * normalization * value for value in row]
            + [arb(0)] * (degree_count - len(row))
        )
    return result


def _cross_block(arb, arb_mat, left_length, right_length, gap, degree_count: int):
    left = _local_legendre_coefficients(
        arb, left_length, degree_count, reversed_=True
    )
    right = _local_legendre_coefficients(
        arb, right_length, degree_count, reversed_=False
    )
    moments = [
        [
            _inverse_distance_moment(
                arb, p, q, left_length, right_length, gap
            )
            for q in range(degree_count)
        ]
        for p in range(degree_count)
    ]
    right_transpose = [
        [right[row][column] for row in range(degree_count)]
        for column in range(degree_count)
    ]
    return -arb(1) / 2 * arb_mat(left) * arb_mat(moments) * arb_mat(
        right_transpose
    )


def _cross_block_rectangular(
    arb,
    arb_mat,
    left_length,
    right_length,
    gap,
    left_start: int,
    left_end: int,
    right_start: int,
    right_end: int,
):
    """Cross-interval block for arbitrary contiguous local-degree ranges."""

    left_all = _local_legendre_coefficients(
        arb, left_length, left_end, reversed_=True
    )
    right_all = _local_legendre_coefficients(
        arb, right_length, right_end, reversed_=False
    )
    left = [row[:left_end] for row in left_all[left_start:left_end]]
    right = [row[:right_end] for row in right_all[right_start:right_end]]
    moments = [
        [
            _inverse_distance_moment(
                arb, p, q, left_length, right_length, gap
            )
            for q in range(right_end)
        ]
        for p in range(left_end)
    ]
    right_transpose = [
        [right[row][column] for row in range(len(right))]
        for column in range(right_end)
    ]
    return (
        -arb(1)
        / 2
        * arb_mat(left)
        * arb_mat(moments)
        * arb_mat(right_transpose)
    )


def build_arb_cut_dominant_matrix(
    half_width: float,
    degree_count: int,
    precision: int = 256,
) -> ArbCutDominantMatrix:
    """Build the exact three-interval matrix of the scale-free form L."""
    if degree_count < 1:
        raise ValueError("degree_count must be positive")
    partition = first_prime_partition(half_width)
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        # Reconstruct the partition inside Arb.  The floating-point partition
        # above is used only to validate the support window; feeding its
        # rounded endpoints back into Arb would not enclose log(2) / a.
        a = arb(str(half_width))
        displacement = arb.const_log2() / a
        edge_length = arb(2) - displacement
        center_length = arb(2) * displacement - arb(2)
        lengths = [edge_length, center_length, edge_length]
        gaps = [arb(0), center_length, arb(0)]
        total = 3 * degree_count
        matrix = [[arb(0) for _ in range(total)] for _ in range(total)]

        harmonic = [arb(0)]
        diagonal = [arb(1)]
        for degree in range(1, degree_count):
            harmonic.append(harmonic[-1] + arb(1) / degree)
            diagonal.append(
                diagonal[-1]
                + arb(1) / (degree * (2 * degree - 1) * (2 * degree + 1))
            )

        def standard_entry(left: int, right: int):
            if (left + right) % 2:
                return arb(0)
            if left == right:
                return harmonic[left] + diagonal[left] - arb.const_log2()
            return arb((2 * left + 1) * (2 * right + 1)).sqrt() / (
                abs(left - right) * (left + right + 1)
            )

        for block, length in enumerate(lengths):
            scale_shift = -(length / 2).log()
            for left in range(degree_count):
                for right in range(degree_count):
                    value = standard_entry(left, right)
                    if left == right:
                        value += scale_shift
                    matrix[block * degree_count + left][block * degree_count + right] = value

        pairs = ((0, 1, gaps[0]), (0, 2, gaps[1]), (1, 2, gaps[2]))
        for left_block, right_block, gap in pairs:
            cross = _cross_block(
                arb,
                arb_mat,
                lengths[left_block],
                lengths[right_block],
                gap,
                degree_count,
            )
            for left in range(degree_count):
                for right in range(degree_count):
                    value = cross[left, right]
                    matrix[left_block * degree_count + left][
                        right_block * degree_count + right
                    ] = value
                    matrix[right_block * degree_count + right][
                        left_block * degree_count + left
                    ] = value

        midpoint = np.empty((total, total))
        radius = np.empty_like(midpoint)
        for left in range(total):
            for right in range(total):
                value = matrix[left][right]
                midpoint[left, right] = float(value.mid())
                radius[left, right] = _arb_radius_as_float(value)
    finally:
        ctx.prec = previous_precision
    return ArbCutDominantMatrix(midpoint, radius, precision)
