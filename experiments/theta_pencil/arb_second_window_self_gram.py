"""Directional self-block Gram for the second-window infinite tail."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_second_green_tail import (
    certify_second_green_self_tail,
)


@dataclass(frozen=True)
class ArbSecondWindowSelfGram:
    even_midpoint: np.ndarray
    even_radius: np.ndarray
    odd_midpoint: np.ndarray
    odd_radius: np.ndarray
    first_degree: int
    explicit_end: int
    remainder_norm_upper: float
    precision: int


def _export(matrix) -> tuple[np.ndarray, np.ndarray]:
    midpoint = np.empty((matrix.nrows(), matrix.ncols()), dtype=float)
    radius = np.empty_like(midpoint)
    for row in range(matrix.nrows()):
        for column in range(matrix.ncols()):
            midpoint[row, column] = float(matrix[row, column].mid())
            radius[row, column] = _arb_radius_as_float(matrix[row, column])
    return midpoint, radius


def build_arb_second_window_self_gram(
    degree_count: int = 16,
    first_degree: int = 640,
    explicit_end: int = 4096,
    remainder_end: int = 16384,
    precision: int = 512,
) -> ArbSecondWindowSelfGram:
    """Bound the self-regularized tail while retaining its low directions.

    After both endpoint fluxes are removed, the exact coefficient from local
    source degree ``k`` to target degree ``n`` is

        sqrt((2n+1)(2k+1)) lambda_k
        / ((lambda_n-lambda_k) lambda_n)

    when ``n-k`` is even, and zero otherwise.  The finite part is accumulated
    before squaring.  The tail after ``explicit_end`` is bounded in norm and
    added as a scalar Gram remainder on each local block.
    """

    if degree_count < 1 or first_degree <= degree_count:
        raise ValueError("first_degree must exceed degree_count")
    if explicit_end <= first_degree or remainder_end <= explicit_end:
        raise ValueError("invalid explicit or remainder end")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    tail = certify_second_green_self_tail(
        degree_count,
        explicit_end,
        remainder_end,
        precision,
    )
    # The helper bounds the numerator before the second Green denominator.
    # On n >= explicit_end, lambda_n >= lambda_explicit_end.
    denominator = explicit_end * (explicit_end + 1)
    remainder_norm = math.nextafter(tail.total_upper / denominator, math.inf)

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
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
        remainder_square = arb(str(remainder_norm)) ** 2
        for degree in range(degree_count):
            local[degree, degree] += remainder_square

        center_even = tuple(range(0, degree_count, 2))
        center_odd = tuple(range(1, degree_count, 2))
        even_size = 3 * degree_count + len(center_even)
        odd_size = 3 * degree_count + len(center_odd)
        even = arb_mat(even_size, even_size)
        odd = arb_mat(odd_size, odd_size)
        for block in range(3):
            offset = block * degree_count
            for left in range(degree_count):
                for right in range(degree_count):
                    even[offset + left, offset + right] = local[left, right]
                    odd[offset + left, offset + right] = local[left, right]
        even_offset = 3 * degree_count
        odd_offset = 3 * degree_count
        for left, source_left in enumerate(center_even):
            for right, source_right in enumerate(center_even):
                even[even_offset + left, even_offset + right] = local[
                    source_left, source_right
                ]
        for left, source_left in enumerate(center_odd):
            for right, source_right in enumerate(center_odd):
                odd[odd_offset + left, odd_offset + right] = local[
                    source_left, source_right
                ]
        even_midpoint, even_radius = _export(even)
        odd_midpoint, odd_radius = _export(odd)
    finally:
        ctx.prec = previous_precision

    return ArbSecondWindowSelfGram(
        even_midpoint=even_midpoint,
        even_radius=even_radius,
        odd_midpoint=odd_midpoint,
        odd_radius=odd_radius,
        first_degree=first_degree,
        explicit_end=explicit_end,
        remainder_norm_upper=remainder_norm,
        precision=precision,
    )
