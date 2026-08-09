"""Rectangular low--high block of the cut-adapted dominant operator."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_cut_dominant import (
    _cross_block_rectangular,
)
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.cut_adapted_prime_basis import first_prime_partition


@dataclass(frozen=True)
class ArbCutDominantCross:
    midpoint: np.ndarray
    radius: np.ndarray
    low_degree_count: int
    high_degree_end: int
    precision: int


def build_arb_cut_dominant_cross(
    half_width: float,
    low_degree_count: int,
    high_degree_end: int,
    precision: int = 1024,
) -> ArbCutDominantCross:
    """Enclose degrees [0,d) against [d,D) in every local interval."""

    if not 1 <= low_degree_count < high_degree_end:
        raise ValueError("require 1 <= low_degree_count < high_degree_end")
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
        gaps = {
            (0, 1): arb(0),
            (0, 2): center_length,
            (1, 2): arb(0),
        }
        d = low_degree_count
        high_count = high_degree_end - d
        result = arb_mat(3 * d, 3 * high_count)

        harmonic = [arb(0)]
        diagonal = [arb(1)]
        for degree in range(1, high_degree_end):
            harmonic.append(harmonic[-1] + arb(1) / degree)
            diagonal.append(
                diagonal[-1]
                + arb(1) / (degree * (2 * degree - 1) * (2 * degree + 1))
            )

        def standard_entry(left: int, right: int):
            if (left + right) % 2:
                return arb(0)
            return arb((2 * left + 1) * (2 * right + 1)).sqrt() / (
                abs(left - right) * (left + right + 1)
            )

        for block in range(3):
            for low_degree in range(d):
                for high_degree in range(d, high_degree_end):
                    result[block * d + low_degree,
                           block * high_count + high_degree - d] = standard_entry(
                               low_degree, high_degree
                           )

        for low_block in range(3):
            for high_block in range(3):
                if low_block == high_block:
                    continue
                if low_block < high_block:
                    block = _cross_block_rectangular(
                        arb,
                        arb_mat,
                        lengths[low_block],
                        lengths[high_block],
                        gaps[(low_block, high_block)],
                        0,
                        d,
                        d,
                        high_degree_end,
                    )
                else:
                    reverse = _cross_block_rectangular(
                        arb,
                        arb_mat,
                        lengths[high_block],
                        lengths[low_block],
                        gaps[(high_block, low_block)],
                        d,
                        high_degree_end,
                        0,
                        d,
                    )
                    block = reverse.transpose()
                for left in range(d):
                    for right in range(high_count):
                        result[low_block * d + left,
                               high_block * high_count + right] = block[left, right]

        midpoint = np.empty((3 * d, 3 * high_count), dtype=float)
        radius = np.empty_like(midpoint)
        for left in range(3 * d):
            for right in range(3 * high_count):
                value = result[left, right]
                midpoint[left, right] = float(value.mid())
                radius[left, right] = _arb_radius_as_float(value)
    finally:
        ctx.prec = previous_precision

    return ArbCutDominantCross(
        midpoint=midpoint,
        radius=radius,
        low_degree_count=d,
        high_degree_end=high_degree_end,
        precision=precision,
    )
