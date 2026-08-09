"""Arb finite source for the first-prime cut-adapted architecture."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_cut_dominant import (
    build_arb_cut_dominant_matrix,
)
from experiments.theta_pencil.arb_cut_smooth import build_arb_cut_smooth_matrix
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_source_schur import _roundtrip_ball
from experiments.theta_pencil.cut_adapted_prime_basis import first_prime_partition


@dataclass(frozen=True)
class ArbCutFiniteSource:
    midpoint: np.ndarray
    radius: np.ndarray
    even_midpoint: np.ndarray
    even_radius: np.ndarray
    odd_midpoint: np.ndarray
    odd_radius: np.ndarray
    smooth_remainder: float
    precision: int


def _export_matrix(matrix, size: int) -> tuple[np.ndarray, np.ndarray]:
    midpoint = np.empty((size, size), dtype=float)
    radius = np.empty_like(midpoint)
    for left in range(size):
        for right in range(size):
            value = matrix[left, right]
            midpoint[left, right] = float(value.mid())
            radius[left, right] = _arb_radius_as_float(value)
    return midpoint, radius


def build_arb_cut_finite_source(
    half_width: float = 0.5,
    degree_count: int = 16,
    maximum_power: int = 23,
    precision: int = 384,
) -> ArbCutFiniteSource:
    """Enclose the finite cut-basis compression and its parity blocks.

    The returned matrices contain the truncated smooth series.  The operator
    norm of the omitted analytic kernel is reported separately as
    ``smooth_remainder`` and must be subtracted from lower spectral bounds.
    """

    if degree_count < 1:
        raise ValueError("degree_count must be positive")
    first_prime_partition(half_width)
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    dominant = build_arb_cut_dominant_matrix(
        half_width, degree_count, precision
    )
    smooth = build_arb_cut_smooth_matrix(
        half_width, degree_count, maximum_power, precision
    )

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        total = 3 * degree_count
        source = arb_mat(total, total)
        a = arb(str(half_width))
        scalar = -a.log() - (arb(2) * arb.pi()).log() - arb.const_euler()
        prime_coefficient = arb.const_log2() / arb(2).sqrt()
        for left in range(total):
            for right in range(total):
                source[left, right] = _roundtrip_ball(
                    arb,
                    dominant.midpoint[left, right],
                    dominant.radius[left, right],
                ) + _roundtrip_ball(
                    arb,
                    smooth.midpoint[left, right],
                    smooth.radius[left, right],
                )
                if left == right:
                    source[left, right] += scalar
        for degree in range(degree_count):
            left = degree
            right = 2 * degree_count + degree
            source[left, right] -= prime_coefficient
            source[right, left] -= prime_coefficient

        inverse_sqrt_two = arb(1) / arb(2).sqrt()
        even_center = tuple(range(0, degree_count, 2))
        odd_center = tuple(range(1, degree_count, 2))
        even_size = degree_count + len(even_center)
        odd_size = degree_count + len(odd_center)
        even_transform = arb_mat(total, even_size)
        odd_transform = arb_mat(total, odd_size)
        for degree in range(degree_count):
            reflection_sign = -1 if degree % 2 else 1
            even_transform[degree, degree] = inverse_sqrt_two
            even_transform[2 * degree_count + degree, degree] = (
                reflection_sign * inverse_sqrt_two
            )
            odd_transform[degree, degree] = inverse_sqrt_two
            odd_transform[2 * degree_count + degree, degree] = (
                -reflection_sign * inverse_sqrt_two
            )
        for column, degree in enumerate(even_center, start=degree_count):
            even_transform[degree_count + degree, column] = arb(1)
        for column, degree in enumerate(odd_center, start=degree_count):
            odd_transform[degree_count + degree, column] = arb(1)

        even = even_transform.transpose() * source * even_transform
        odd = odd_transform.transpose() * source * odd_transform
        midpoint, radius = _export_matrix(source, total)
        even_midpoint, even_radius = _export_matrix(even, even_size)
        odd_midpoint, odd_radius = _export_matrix(odd, odd_size)
    finally:
        ctx.prec = previous_precision

    return ArbCutFiniteSource(
        midpoint=midpoint,
        radius=radius,
        even_midpoint=even_midpoint,
        even_radius=even_radius,
        odd_midpoint=odd_midpoint,
        odd_radius=odd_radius,
        smooth_remainder=smooth.analytic_remainder,
        precision=precision,
    )
