"""Signed endpoint-flux Gram on the thirteen-block third window."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_second_window_flux_gram import _endpoint_rows
from experiments.theta_pencil.arb_third_window_source import (
    _arb_breakpoints_lengths,
    _degree_pattern,
    _offsets,
    _parity_transforms,
)
from experiments.theta_pencil.cut_adapted_prime_basis import third_prime_partition


@dataclass(frozen=True)
class ArbThirdWindowFluxGram:
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
    midpoint = np.empty((matrix.nrows(), matrix.ncols()), dtype=float)
    radius = np.empty_like(midpoint)
    for row in range(matrix.nrows()):
        for column in range(matrix.ncols()):
            midpoint[row, column] = float(matrix[row, column].mid())
            radius[row, column] = _arb_radius_as_float(matrix[row, column])
    return midpoint, radius


def build_arb_third_window_flux_gram(
    half_width: float = 0.7,
    edge_degree: int = 16,
    bridge_degree: int = 16,
    center_degree: int = 16,
    first_degree: int = 640,
    explicit_end: int = 4096,
    precision: int = 512,
) -> ArbThirdWindowFluxGram:
    """Retain the signed endpoint-flux directions before tail bounding."""

    third_prime_partition(half_width)
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
        _, _, lengths = _arb_breakpoints_lengths(arb, half_width)
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
        remainder_trace = arb(0)
        for positive, negative in rows:
            for sign, weight in ((1, even_weight), (-1, odd_weight)):
                row = positive - sign * negative
                full += weight * row.transpose() * row
            remainder = (
                positive.transpose() * positive
                + negative.transpose() * negative
            ) / explicit_end**2
            full += remainder
            remainder_trace += sum(
                (
                    positive[0, index] ** 2 + negative[0, index] ** 2
                    for index in range(total)
                ),
                arb(0),
            ) / explicit_end**2

        even_transform, odd_transform = _parity_transforms(
            arb, arb_mat, degrees, offsets
        )
        even = even_transform.transpose() * full * even_transform
        odd = odd_transform.transpose() * full * odd_transform
        even_midpoint, even_radius = _export(even)
        odd_midpoint, odd_radius = _export(odd)
    finally:
        ctx.prec = previous_precision

    return ArbThirdWindowFluxGram(
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
