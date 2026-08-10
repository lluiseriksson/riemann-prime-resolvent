"""Exact seven-block dominant tail Gram on a finite target band."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_adjacent_full_map import (
    _build_adjacent_full_matrix,
    _build_separated_full_matrix,
)
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_source_schur import _roundtrip_ball
from experiments.theta_pencil.arb_second_window_flux_gram import (
    _parity_transforms,
)
from experiments.theta_pencil.arb_second_window_source import (
    _arb_lengths,
    _degree_pattern,
    _offsets,
    build_arb_second_window_smooth,
)
from experiments.theta_pencil.cut_adapted_prime_basis import second_prime_partition


@dataclass(frozen=True)
class ArbSecondWindowNearTailGram:
    midpoint: np.ndarray
    radius: np.ndarray
    even_midpoint: np.ndarray
    even_radius: np.ndarray
    odd_midpoint: np.ndarray
    odd_radius: np.ndarray
    interval_degrees: tuple[int, ...]
    first_degree: int
    last_degree: int
    precision: int
    working_precision: int
    maximum_smooth_power: int | None


def _export(matrix):
    midpoint = np.empty((matrix.nrows(), matrix.ncols()), dtype=float)
    radius = np.empty_like(midpoint)
    for row in range(matrix.nrows()):
        for column in range(matrix.ncols()):
            midpoint[row, column] = float(matrix[row, column].mid())
            radius[row, column] = _arb_radius_as_float(matrix[row, column])
    return midpoint, radius


def build_arb_second_window_near_tail_gram(
    half_width: float,
    edge_degree: int = 16,
    bridge_degree: int = 16,
    center_degree: int = 16,
    first_degree: int = 16,
    last_degree: int = 512,
    precision: int = 512,
    maximum_smooth_power: int | None = None,
) -> ArbSecondWindowNearTailGram:
    """Accumulate every exact dominant row before squaring.

    This is an explicit band, not yet an infinite-tail certificate.  It is
    nevertheless the correct finite Schur numerator: singular, analytic and
    endpoint-flux terms of every touching block have already been recombined.
    Touching blocks use the recombined second-Green identity.  Strictly
    separated blocks use the difference of two Legendre-Q logarithmic
    expansions.  If ``maximum_smooth_power`` is supplied, the truncated
    smooth kernel is added to each row before its outer product.  Thus no
    cross terms between source blocks or kernel components are lost.
    """

    second_prime_partition(half_width)
    degrees = _degree_pattern(edge_degree, bridge_degree, center_degree)
    if first_degree < max(degrees) or last_degree <= first_degree:
        raise ValueError("the explicit band must start above all source modes")
    if maximum_smooth_power is not None and maximum_smooth_power < 1:
        raise ValueError("maximum_smooth_power must be positive")
    try:
        from flint import acb, arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = max(precision, 128)
        _, pilot_lengths = _arb_lengths(arb, half_width)
        eta_candidates = []
        for target in range(7):
            for source in range(7):
                if source == target:
                    continue
                lower = min(target, source)
                upper = max(target, source)
                gap = sum(pilot_lengths[lower + 1 : upper], arb(0))
                eta_candidates.append(
                    (
                        1
                        + 2
                        * (gap + pilot_lengths[source])
                        / pilot_lengths[target]
                    ).acosh()
                )
        maximum_eta = max(float(value.upper()) for value in eta_candidates)
        working_precision = max(
            precision,
            math.ceil(
                (last_degree + max(degrees) + 2)
                * maximum_eta
                / math.log(2)
            )
            + precision
            + 128,
        )
        ctx.prec = working_precision
        _, lengths = _arb_lengths(arb, half_width)
        labels = ("edge", "bridge", "edge", "center", "edge", "bridge", "edge")
        offsets = _offsets(degrees)
        total = offsets[-1]
        full = arb_mat(total, total)
        smooth = None
        smooth_degree = 0
        if maximum_smooth_power is not None:
            smooth_degree = max(max(degrees), maximum_smooth_power + 1)
            smooth = build_arb_second_window_smooth(
                half_width,
                smooth_degree,
                smooth_degree,
                smooth_degree,
                maximum_smooth_power,
                precision,
            )
        cross_maps = {}
        q_cache = {}
        for target in range(7):
            for source in range(7):
                if source == target:
                    continue
                lower = min(target, source)
                upper = max(target, source)
                between = labels[lower + 1 : upper]
                gap_signature = tuple(
                    between.count(label)
                    for label in ("edge", "bridge", "center")
                )
                geometry = (
                    labels[target],
                    labels[source],
                    gap_signature,
                    degrees[source],
                )
                if geometry not in cross_maps:
                    gap = sum(lengths[lower + 1 : upper], arb(0))
                    builder = (
                        _build_adjacent_full_matrix
                        if abs(target - source) == 1
                        else _build_separated_full_matrix
                    )
                    arguments = (
                        arb,
                        arb_mat,
                        acb,
                        lengths[target],
                        lengths[source],
                    )
                    if builder is _build_separated_full_matrix:
                        arguments += (gap,)
                    cross_maps[geometry] = builder(
                        *arguments,
                        degrees[source],
                        first_degree,
                        last_degree,
                        q_cache,
                    )
                cross_maps[target, source] = cross_maps[geometry]

        for target in range(7):
            sources = tuple(range(7))
            local_offsets = _offsets(tuple(degrees[source] for source in sources))
            local = arb_mat(local_offsets[-1], local_offsets[-1])
            for row, degree in enumerate(range(first_degree, last_degree)):
                vector = arb_mat(1, local_offsets[-1])
                for source_index, source in enumerate(sources):
                    for source_degree in range(degrees[source]):
                        if source == target:
                            value = (
                                arb(
                                    (2 * degree + 1)
                                    * (2 * source_degree + 1)
                                ).sqrt()
                                / (
                                    (degree - source_degree)
                                    * (degree + source_degree + 1)
                                )
                                if (degree + source_degree) % 2 == 0
                                else arb(0)
                            )
                        else:
                            value = cross_maps[target, source][
                                row, source_degree
                            ]
                            if source < target and (degree + source_degree) % 2:
                                value = -value
                        if smooth is not None and degree < smooth_degree:
                            value += _roundtrip_ball(
                                arb,
                                smooth.midpoint[
                                    target * smooth_degree + degree,
                                    source * smooth_degree + source_degree,
                                ],
                                smooth.radius[
                                    target * smooth_degree + degree,
                                    source * smooth_degree + source_degree,
                                ],
                            )
                        vector[
                            0,
                            local_offsets[source_index] + source_degree,
                        ] = value
                local += vector.transpose() * vector

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

        even_transform, odd_transform = _parity_transforms(
            arb, arb_mat, degrees, offsets
        )
        even = even_transform.transpose() * full * even_transform
        odd = odd_transform.transpose() * full * odd_transform
        midpoint, radius = _export(full)
        even_midpoint, even_radius = _export(even)
        odd_midpoint, odd_radius = _export(odd)
    finally:
        ctx.prec = previous_precision

    return ArbSecondWindowNearTailGram(
        midpoint=midpoint,
        radius=radius,
        even_midpoint=even_midpoint,
        even_radius=even_radius,
        odd_midpoint=odd_midpoint,
        odd_radius=odd_radius,
        interval_degrees=degrees,
        first_degree=first_degree,
        last_degree=last_degree,
        precision=precision,
        working_precision=working_precision,
        maximum_smooth_power=maximum_smooth_power,
    )
