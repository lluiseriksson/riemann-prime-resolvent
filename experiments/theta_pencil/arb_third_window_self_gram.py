"""Directional self-regularized tail Gram on thirteen local intervals."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_second_green_tail import (
    certify_second_green_self_tail,
)
from experiments.theta_pencil.arb_third_window_source import (
    _degree_pattern,
    _offsets,
    _parity_transforms,
)


@dataclass(frozen=True)
class ArbThirdWindowSelfGram:
    even_midpoint: np.ndarray
    even_radius: np.ndarray
    odd_midpoint: np.ndarray
    odd_radius: np.ndarray
    first_degree: int
    explicit_end: int
    remainder_norm_upper: float
    precision: int


def _export(matrix):
    midpoint = np.empty((matrix.nrows(), matrix.ncols()), dtype=float)
    radius = np.empty_like(midpoint)
    for row in range(matrix.nrows()):
        for column in range(matrix.ncols()):
            midpoint[row, column] = float(matrix[row, column].mid())
            radius[row, column] = _arb_radius_as_float(matrix[row, column])
    return midpoint, radius


def build_arb_third_window_self_gram(
    edge_degree: int = 16,
    bridge_degree: int = 16,
    center_degree: int = 16,
    first_degree: int = 640,
    explicit_end: int = 4096,
    remainder_end: int = 16384,
    precision: int = 512,
) -> ArbThirdWindowSelfGram:
    """Retain one exact self-tail Gram per interval and then reduce parity."""

    degrees = _degree_pattern(edge_degree, bridge_degree, center_degree)
    if first_degree <= max(degrees):
        raise ValueError("first_degree must exceed every local degree count")
    if explicit_end <= first_degree or remainder_end <= explicit_end:
        raise ValueError("invalid explicit or remainder end")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    local_cache = {}
    remainder_norm = 0.0
    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        offsets = _offsets(degrees)
        total = offsets[-1]
        full = arb_mat(total, total)
        for block, degree_count in enumerate(degrees):
            if degree_count not in local_cache:
                tail = certify_second_green_self_tail(
                    degree_count, explicit_end, remainder_end, precision
                )
                denominator = explicit_end * (explicit_end + 1)
                local_remainder = math.nextafter(
                    tail.total_upper / denominator, math.inf
                )
                local = arb_mat(degree_count, degree_count)
                for target in range(first_degree, explicit_end):
                    target_eigenvalue = target * (target + 1)
                    row = [arb(0) for _ in range(degree_count)]
                    for source in range(degree_count):
                        if (target - source) % 2:
                            continue
                        source_eigenvalue = source * (source + 1)
                        row[source] = (
                            arb((2 * target + 1) * (2 * source + 1)).sqrt()
                            * source_eigenvalue
                            / (target_eigenvalue - source_eigenvalue)
                            / target_eigenvalue
                        )
                    for left in range(degree_count):
                        for right in range(left, degree_count):
                            value = row[left] * row[right]
                            local[left, right] += value
                            if left != right:
                                local[right, left] += value
                remainder_square = arb(str(local_remainder)) ** 2
                for degree in range(degree_count):
                    local[degree, degree] += remainder_square
                local_cache[degree_count] = local, local_remainder
            local, local_remainder = local_cache[degree_count]
            remainder_norm = max(remainder_norm, local_remainder)
            for left in range(degree_count):
                for right in range(degree_count):
                    full[offsets[block] + left, offsets[block] + right] = local[
                        left, right
                    ]

        even_transform, odd_transform = _parity_transforms(
            arb, arb_mat, degrees, offsets
        )
        even = even_transform.transpose() * full * even_transform
        odd = odd_transform.transpose() * full * odd_transform
        even_midpoint, even_radius = _export(even)
        odd_midpoint, odd_radius = _export(odd)
    finally:
        ctx.prec = previous_precision

    return ArbThirdWindowSelfGram(
        even_midpoint=even_midpoint,
        even_radius=even_radius,
        odd_midpoint=odd_midpoint,
        odd_radius=odd_radius,
        first_degree=first_degree,
        explicit_end=explicit_end,
        remainder_norm_upper=remainder_norm,
        precision=precision,
    )
