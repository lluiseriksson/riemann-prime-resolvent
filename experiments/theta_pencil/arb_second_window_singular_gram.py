"""Signed seven-block Gram for the adjacent singular Schur tail."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_adjacent_singular_gram import (
    _build_adjacent_singular_map,
)
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.cut_adapted_prime_basis import second_prime_partition


@dataclass(frozen=True)
class ArbSecondWindowSingularGram:
    midpoint: np.ndarray
    radius: np.ndarray
    even_midpoint: np.ndarray
    even_radius: np.ndarray
    odd_midpoint: np.ndarray
    odd_radius: np.ndarray
    remainder_norm_upper: float
    interval_degrees: tuple[int, ...]
    first_degree: int
    last_degree: int
    moment_order: int
    precision: int


def _degree_pattern(edge: int, bridge: int, center: int) -> tuple[int, ...]:
    if min(edge, bridge, center) < 1:
        raise ValueError("all local degree counts must be positive")
    return (edge, bridge, edge, center, edge, bridge, edge)


def _offsets(counts: tuple[int, ...]) -> tuple[int, ...]:
    result = [0]
    for count in counts:
        result.append(result[-1] + count)
    return tuple(result)


def _weighted_remainder(arb, singular_map, last_degree: int, moment_order: int):
    degree_count = singular_map.nrows()
    remainder = arb(0)
    for order in range(moment_order):
        moment_square = arb(0)
        for source in range(degree_count):
            moment = sum(
                (
                    arb(2 * low + 1).sqrt()
                    * (low * (low + 1)) ** order
                    * singular_map[low, source]
                    for low in range(degree_count)
                ),
                arb(0),
            )
            moment_square += moment.abs_upper() ** 2
        exponent = 4 * order + 7
        scalar_tail = (
            arb(1) / last_degree**exponent
            + arb(1) / ((exponent - 1) * last_degree ** (exponent - 1))
        )
        remainder += (3 * scalar_tail * moment_square).sqrt()

    maximum_eigenvalue = (degree_count - 1) * degree_count
    absolute_moment_square = arb(0)
    for source in range(degree_count):
        absolute_moment = sum(
            (
                arb(2 * low + 1).sqrt()
                * (low * (low + 1)) ** moment_order
                * singular_map[low, source].abs_upper()
                for low in range(degree_count)
            ),
            arb(0),
        )
        absolute_moment_square += absolute_moment**2
    exponent = 4 * moment_order + 7
    scalar_tail = (
        arb(1) / last_degree**exponent
        + arb(1) / ((exponent - 1) * last_degree ** (exponent - 1))
    )
    ratio = arb(maximum_eigenvalue) / (last_degree * (last_degree + 1))
    remainder += (3 * scalar_tail * absolute_moment_square).sqrt() / (1 - ratio)
    return remainder


def _export(matrix):
    rows = matrix.nrows()
    columns = matrix.ncols()
    midpoint = np.empty((rows, columns), dtype=float)
    radius = np.empty_like(midpoint)
    for row in range(rows):
        for column in range(columns):
            midpoint[row, column] = float(matrix[row, column].mid())
            radius[row, column] = _arb_radius_as_float(matrix[row, column])
    return midpoint, radius


def build_arb_second_window_singular_gram(
    half_width: float,
    edge_degree: int = 16,
    bridge_degree: int = 16,
    center_degree: int = 16,
    first_degree: int = 128,
    last_degree: int = 4096,
    moment_order: int = 8,
    precision: int = 512,
) -> ArbSecondWindowSingularGram:
    """Retain all cross terms in the adjacent singular tail Gram.

    For a target block, its left and right adjacent sources contribute to one
    signed row before the outer product.  Reflection of a right-hand target
    contributes ``(-1)^(n+k)`` to source degree ``k``.  Tails above
    ``last_degree`` are bounded in operator norm and added as a scalar PSD
    remainder only after all explicit cross terms have been retained.
    """

    second_prime_partition(half_width)
    degrees = _degree_pattern(edge_degree, bridge_degree, center_degree)
    if first_degree <= max(degrees) or last_degree <= first_degree:
        raise ValueError("the explicit band must start above all source degrees")
    if moment_order < 1:
        raise ValueError("moment_order must be positive")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = arb(str(half_width))
        h_two = arb.const_log2() / a
        h_three = arb(3).log() / a
        edge = 2 - h_three
        bridge = 2 * h_three - h_two - 2
        center = 2 * h_two - 2
        lengths = (edge, bridge, edge, center, edge, bridge, edge)
        offsets = _offsets(degrees)
        total = offsets[-1]
        full = arb_mat(total, total)
        remainder_square = arb(0)

        maps = {}
        for target in range(7):
            for source in (target - 1, target + 1):
                if 0 <= source < 7:
                    maps[target, source] = _build_adjacent_singular_map(
                        arb,
                        arb_mat,
                        lengths[target],
                        lengths[source],
                        degrees[source],
                    )

        for target in range(7):
            sources = tuple(
                source
                for source in (target - 1, target + 1)
                if 0 <= source < 7
            )
            local_offsets = _offsets(tuple(degrees[source] for source in sources))
            local = arb_mat(local_offsets[-1], local_offsets[-1])
            for degree in range(first_degree, last_degree):
                eigenvalue = degree * (degree + 1)
                row = arb_mat(1, local_offsets[-1])
                for source_index, source in enumerate(sources):
                    singular_map = maps[target, source]
                    for source_degree in range(degrees[source]):
                        value = sum(
                            (
                                -arb((2 * degree + 1) * (2 * low + 1)).sqrt()
                                / (eigenvalue - low * (low + 1))
                                * singular_map[low, source_degree]
                                / eigenvalue
                                for low in range(degrees[source])
                            ),
                            arb(0),
                        )
                        if source < target and (degree + source_degree) % 2:
                            value = -value
                        row[0, local_offsets[source_index] + source_degree] = value
                local += row.transpose() * row

            for left_index, left_source in enumerate(sources):
                for right_index, right_source in enumerate(sources):
                    for left in range(degrees[left_source]):
                        for right in range(degrees[right_source]):
                            full[offsets[left_source] + left, offsets[right_source] + right] += local[
                                local_offsets[left_index] + left,
                                local_offsets[right_index] + right,
                            ]
                remainder = _weighted_remainder(
                    arb, maps[target, left_source], last_degree, moment_order
                )
                remainder_square += remainder**2

        # The direct sum of all uncomputed target tails has norm at most the
        # square root of the summed Frobenius remainders.
        for index in range(total):
            full[index, index] += remainder_square

        inverse_sqrt_two = 1 / arb(2).sqrt()
        pair_blocks = ((0, 6), (1, 5), (2, 4))
        paired_size = edge_degree + bridge_degree + edge_degree
        center_even = tuple(range(0, center_degree, 2))
        center_odd = tuple(range(1, center_degree, 2))
        even_transform = arb_mat(total, paired_size + len(center_even))
        odd_transform = arb_mat(total, paired_size + len(center_odd))
        column_offset = 0
        for left_block, right_block in pair_blocks:
            for degree in range(degrees[left_block]):
                reflection = -1 if degree % 2 else 1
                column = column_offset + degree
                even_transform[offsets[left_block] + degree, column] = inverse_sqrt_two
                even_transform[offsets[right_block] + degree, column] = reflection * inverse_sqrt_two
                odd_transform[offsets[left_block] + degree, column] = inverse_sqrt_two
                odd_transform[offsets[right_block] + degree, column] = -reflection * inverse_sqrt_two
            column_offset += degrees[left_block]
        for column, degree in enumerate(center_even, start=paired_size):
            even_transform[offsets[3] + degree, column] = 1
        for column, degree in enumerate(center_odd, start=paired_size):
            odd_transform[offsets[3] + degree, column] = 1

        even = even_transform.transpose() * full * even_transform
        odd = odd_transform.transpose() * full * odd_transform
        midpoint, radius = _export(full)
        even_midpoint, even_radius = _export(even)
        odd_midpoint, odd_radius = _export(odd)
    finally:
        ctx.prec = previous_precision

    return ArbSecondWindowSingularGram(
        midpoint=midpoint,
        radius=radius,
        even_midpoint=even_midpoint,
        even_radius=even_radius,
        odd_midpoint=odd_midpoint,
        odd_radius=odd_radius,
        remainder_norm_upper=math.nextafter(
            float(remainder_square.sqrt().upper()), math.inf
        ),
        interval_degrees=degrees,
        first_degree=first_degree,
        last_degree=last_degree,
        moment_order=moment_order,
        precision=precision,
    )
