"""Signed adjacent-singular Gram on the thirteen-block third window."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_adjacent_singular_gram import (
    _build_adjacent_singular_map,
)
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_second_window_singular_gram import (
    _weighted_remainder,
)
from experiments.theta_pencil.arb_third_window_source import (
    _arb_breakpoints_lengths,
    _degree_pattern,
    _offsets,
    _parity_transforms,
)
from experiments.theta_pencil.cut_adapted_prime_basis import third_prime_partition


@dataclass(frozen=True)
class ArbThirdWindowSingularGram:
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


def _export(matrix):
    midpoint = np.empty((matrix.nrows(), matrix.ncols()), dtype=float)
    radius = np.empty_like(midpoint)
    for row in range(matrix.nrows()):
        for column in range(matrix.ncols()):
            midpoint[row, column] = float(matrix[row, column].mid())
            radius[row, column] = _arb_radius_as_float(matrix[row, column])
    return midpoint, radius


def build_arb_third_window_singular_gram(
    half_width: float = 0.7,
    edge_degree: int = 16,
    bridge_degree: int = 16,
    center_degree: int = 16,
    first_degree: int = 640,
    last_degree: int = 4096,
    moment_order: int = 8,
    precision: int = 512,
) -> ArbThirdWindowSingularGram:
    """Retain cross terms between both neighbours of every target block."""

    third_prime_partition(half_width)
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
        _, _, lengths = _arb_breakpoints_lengths(arb, half_width)
        offsets = _offsets(degrees)
        total = offsets[-1]
        full = arb_mat(total, total)
        remainder_square = arb(0)
        maps = {}
        for target in range(13):
            for source in (target - 1, target + 1):
                if 0 <= source < 13:
                    maps[target, source] = _build_adjacent_singular_map(
                        arb,
                        arb_mat,
                        lengths[target],
                        lengths[source],
                        degrees[source],
                    )

        for target in range(13):
            sources = tuple(
                source
                for source in (target - 1, target + 1)
                if 0 <= source < 13
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
                            full[
                                offsets[left_source] + left,
                                offsets[right_source] + right,
                            ] += local[
                                local_offsets[left_index] + left,
                                local_offsets[right_index] + right,
                            ]
                remainder = _weighted_remainder(
                    arb, maps[target, left_source], last_degree, moment_order
                )
                remainder_square += remainder**2

        for index in range(total):
            full[index, index] += remainder_square
        even_transform, odd_transform = _parity_transforms(
            arb, arb_mat, degrees, offsets
        )
        even = even_transform.transpose() * full * even_transform
        odd = odd_transform.transpose() * full * odd_transform
        even_midpoint, even_radius = _export(even)
        odd_midpoint, odd_radius = _export(odd)
    finally:
        ctx.prec = previous_precision

    return ArbThirdWindowSingularGram(
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
