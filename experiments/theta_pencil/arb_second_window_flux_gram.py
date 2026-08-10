"""Signed seven-block Gram for the leading endpoint-flux Schur tail."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_second_window_source import (
    _arb_lengths,
    _degree_pattern,
    _offsets,
)
from experiments.theta_pencil.cut_adapted_prime_basis import second_prime_partition


@dataclass(frozen=True)
class ArbSecondWindowFluxGram:
    midpoint: np.ndarray
    radius: np.ndarray
    even_midpoint: np.ndarray
    even_radius: np.ndarray
    odd_midpoint: np.ndarray
    odd_radius: np.ndarray
    remainder_norm_upper: float
    interval_degrees: tuple[int, ...]
    first_degree: int
    explicit_end: int
    precision: int


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


def _parity_transforms(arb, arb_mat, degrees, offsets):
    total = offsets[-1]
    edge_degree, bridge_degree, _, center_degree, *_ = degrees
    paired_size = edge_degree + bridge_degree + edge_degree
    center_even = tuple(range(0, center_degree, 2))
    center_odd = tuple(range(1, center_degree, 2))
    even = arb_mat(total, paired_size + len(center_even))
    odd = arb_mat(total, paired_size + len(center_odd))
    inverse_sqrt_two = 1 / arb(2).sqrt()
    column_offset = 0
    for left_block, right_block in ((0, 6), (1, 5), (2, 4)):
        for degree in range(degrees[left_block]):
            reflection = -1 if degree % 2 else 1
            column = column_offset + degree
            even[offsets[left_block] + degree, column] = inverse_sqrt_two
            even[offsets[right_block] + degree, column] = (
                reflection * inverse_sqrt_two
            )
            odd[offsets[left_block] + degree, column] = inverse_sqrt_two
            odd[offsets[right_block] + degree, column] = (
                -reflection * inverse_sqrt_two
            )
        column_offset += degrees[left_block]
    for column, degree in enumerate(center_even, start=paired_size):
        even[offsets[3] + degree, column] = 1
    for column, degree in enumerate(center_odd, start=paired_size):
        odd[offsets[3] + degree, column] = 1
    return even, odd


def _endpoint_rows(arb, arb_mat, lengths, degrees, offsets):
    """Return the positive/negative boundary rows for every target block."""

    total = offsets[-1]
    minus = []
    plus = []
    for block, (length, degree_count) in enumerate(zip(lengths, degrees)):
        left = arb_mat(1, total)
        right = arb_mat(1, total)
        for degree in range(degree_count):
            normalization = (arb(2 * degree + 1) / length).sqrt()
            left[0, offsets[block] + degree] = (
                (-1 if degree % 2 else 1) * normalization
            )
            right[0, offsets[block] + degree] = normalization
        minus.append(left)
        plus.append(right)

    rows = []
    for target, length in enumerate(lengths):
        scale = (length / 2).sqrt()
        if target + 1 < len(lengths):
            positive = scale * (plus[target] - minus[target + 1])
        else:
            positive = scale * plus[target]
        if target > 0:
            negative = scale * (plus[target - 1] - minus[target])
        else:
            negative = -scale * minus[target]
        rows.append((positive, negative))
    return tuple(rows)


def build_arb_second_window_flux_gram(
    half_width: float,
    edge_degree: int = 16,
    bridge_degree: int = 16,
    center_degree: int = 16,
    first_degree: int = 128,
    explicit_end: int = 4096,
    precision: int = 512,
) -> ArbSecondWindowFluxGram:
    """Retain the signed endpoint-flux Gram before bounding its last tail.

    Integration by parts gives the high-mode coefficient weight

      (2n+1)/(2 n^2 (n+1)^2)
        = (1/2)(n^-2-(n+1)^-2).

    For target block ``j`` the source row is
    ``F_plus[j] - (-1)^n F_minus[j]``.  The explicit range therefore keeps
    all cross-block cancellation.  Only ``n >= explicit_end`` is replaced by
    the elementary PSD upper obtained from ``|p +/- m|^2``.
    """

    second_prime_partition(half_width)
    degrees = _degree_pattern(edge_degree, bridge_degree, center_degree)
    if first_degree < 1 or explicit_end <= first_degree:
        raise ValueError("the explicit flux band must be nonempty and positive")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        _, lengths = _arb_lengths(arb, half_width)
        offsets = _offsets(degrees)
        total = offsets[-1]
        rows = _endpoint_rows(arb, arb_mat, lengths, degrees, offsets)
        full = arb_mat(total, total)
        even_weight = arb(0)
        odd_weight = arb(0)
        for degree in range(first_degree, explicit_end):
            weight = arb(2 * degree + 1) / (
                2 * degree**2 * (degree + 1) ** 2
            )
            if degree % 2:
                odd_weight += weight
            else:
                even_weight += weight
        for positive, negative in rows:
            for sign, weight in ((1, even_weight), (-1, odd_weight)):
                row = positive - sign * negative
                full += weight * row.transpose() * row
            full += (
                positive.transpose() * positive
                + negative.transpose() * negative
            ) / explicit_end**2

        even_transform, odd_transform = _parity_transforms(
            arb, arb_mat, degrees, offsets
        )
        even = even_transform.transpose() * full * even_transform
        odd = odd_transform.transpose() * full * odd_transform
        midpoint, radius = _export(full)
        even_midpoint, even_radius = _export(even)
        odd_midpoint, odd_radius = _export(odd)

        # The Loewner remainder is a sum of outer products divided by M^2.
        # Its trace bounds its operator norm and remains an Arb upper bound.
        remainder_trace = arb(0)
        for positive, negative in rows:
            remainder_trace += sum(
                (
                    positive[0, index] ** 2 + negative[0, index] ** 2
                    for index in range(total)
                ),
                arb(0),
            ) / explicit_end**2
    finally:
        ctx.prec = previous_precision

    return ArbSecondWindowFluxGram(
        midpoint=midpoint,
        radius=radius,
        even_midpoint=even_midpoint,
        even_radius=even_radius,
        odd_midpoint=odd_midpoint,
        odd_radius=odd_radius,
        remainder_norm_upper=math.nextafter(
            float(remainder_trace.upper()), math.inf
        ),
        interval_degrees=degrees,
        first_degree=first_degree,
        explicit_end=explicit_end,
        precision=precision,
    )
