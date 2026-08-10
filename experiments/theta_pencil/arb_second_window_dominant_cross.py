"""Seven-block low--high dominant coupling in the second prime window."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_cut_dominant import (
    _cross_block_rectangular,
)
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.cut_adapted_prime_basis import (
    second_prime_partition,
)


@dataclass(frozen=True)
class ArbSecondWindowDominantCross:
    midpoint: np.ndarray
    radius: np.ndarray
    interval_degrees: tuple[int, ...]
    low_offsets: tuple[int, ...]
    high_offsets: tuple[int, ...]
    high_degree_end: int
    precision: int


def _degree_pattern(
    edge_degree: int, bridge_degree: int, center_degree: int
) -> tuple[int, ...]:
    if edge_degree < 1 or bridge_degree < 1 or center_degree < 1:
        raise ValueError("all local degree counts must be positive")
    return (
        edge_degree,
        bridge_degree,
        edge_degree,
        center_degree,
        edge_degree,
        bridge_degree,
        edge_degree,
    )


def _offsets(counts: tuple[int, ...]) -> tuple[int, ...]:
    result = [0]
    for count in counts:
        result.append(result[-1] + count)
    return tuple(result)


def build_arb_second_window_dominant_cross(
    half_width: float,
    edge_degree: int,
    bridge_degree: int,
    center_degree: int,
    high_degree_end: int = 128,
    precision: int = 512,
) -> ArbSecondWindowDominantCross:
    """Enclose each retained local band against degrees below ``high_degree_end``."""

    second_prime_partition(half_width)
    degrees = _degree_pattern(edge_degree, bridge_degree, center_degree)
    if high_degree_end <= max(degrees):
        raise ValueError("high_degree_end must exceed every local degree count")
    low_offsets = _offsets(degrees)
    high_counts = tuple(high_degree_end - degree for degree in degrees)
    high_offsets = _offsets(high_counts)
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
        result = arb_mat(low_offsets[-1], high_offsets[-1])

        def standard_entry(left: int, right: int):
            if (left + right) % 2:
                return arb(0)
            return arb((2 * left + 1) * (2 * right + 1)).sqrt() / (
                abs(left - right) * (left + right + 1)
            )

        for low_block in range(7):
            for high_block in range(7):
                low_count = degrees[low_block]
                high_start = degrees[high_block]
                high_count = high_degree_end - high_start
                if low_block == high_block:
                    block = None
                elif low_block < high_block:
                    gap = sum(lengths[low_block + 1 : high_block], arb(0))
                    block = _cross_block_rectangular(
                        arb,
                        arb_mat,
                        lengths[low_block],
                        lengths[high_block],
                        gap,
                        0,
                        low_count,
                        high_start,
                        high_degree_end,
                    )
                else:
                    gap = sum(lengths[high_block + 1 : low_block], arb(0))
                    block = _cross_block_rectangular(
                        arb,
                        arb_mat,
                        lengths[high_block],
                        lengths[low_block],
                        gap,
                        high_start,
                        high_degree_end,
                        0,
                        low_count,
                    ).transpose()
                for low in range(low_count):
                    for high in range(high_count):
                        value = (
                            standard_entry(low, high_start + high)
                            if block is None
                            else block[low, high]
                        )
                        result[
                            low_offsets[low_block] + low,
                            high_offsets[high_block] + high,
                        ] = value

        midpoint = np.empty((low_offsets[-1], high_offsets[-1]), dtype=float)
        radius = np.empty_like(midpoint)
        for row in range(low_offsets[-1]):
            for column in range(high_offsets[-1]):
                value = result[row, column]
                midpoint[row, column] = float(value.mid())
                radius[row, column] = _arb_radius_as_float(value)
    finally:
        ctx.prec = previous_precision

    return ArbSecondWindowDominantCross(
        midpoint=midpoint,
        radius=radius,
        interval_degrees=degrees,
        low_offsets=low_offsets,
        high_offsets=high_offsets,
        high_degree_end=high_degree_end,
        precision=precision,
    )
