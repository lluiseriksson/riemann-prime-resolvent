"""Certified non-directional remainder after the third-window tail Grams."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_adjacent_full_map import (
    certify_adjacent_analytic_tail,
)
from experiments.theta_pencil.arb_second_green_tail import (
    certify_second_green_self_tail,
    certify_second_green_separated_geometric_tail,
)
from experiments.theta_pencil.arb_third_window_source import (
    _arb_breakpoints_lengths,
    _degree_pattern,
)
from experiments.theta_pencil.cut_adapted_prime_basis import third_prime_partition


@dataclass(frozen=True)
class ThirdWindowOtherTail:
    half_width: float
    interval_degrees: tuple[int, ...]
    first_degree: int
    comparison_matrix: np.ndarray
    spectral_norm_upper: float
    row_column_upper: float
    includes_self_blocks: bool
    precision: int


def certify_third_window_other_tail(
    half_width: float = 0.7,
    edge_degree: int = 16,
    bridge_degree: int = 16,
    center_degree: int = 16,
    first_degree: int = 640,
    explicit_end: int = 4096,
    precision: int = 512,
    include_self_blocks: bool = False,
) -> ThirdWindowOtherTail:
    """Bound what remains after flux, singular and optional self extraction."""

    third_prime_partition(half_width)
    degrees = _degree_pattern(edge_degree, bridge_degree, center_degree)
    if first_degree <= max(degrees) or explicit_end <= first_degree:
        raise ValueError("invalid tail degree range")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    labels = (
        "edge",
        "bridge",
        "edge",
        "center",
        "edge",
        "bridge",
        "edge",
        "bridge",
        "edge",
        "center",
        "edge",
        "bridge",
        "edge",
    )
    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        _, _, lengths = _arb_breakpoints_lengths(arb, half_width)
        comparison = np.zeros((13, 13), dtype=float)
        cache = {}
        for target in range(13):
            for source in range(13):
                source_degree = degrees[source]
                if target == source:
                    if include_self_blocks:
                        key = ("self", source_degree)
                        if key not in cache:
                            cache[key] = (
                                certify_second_green_self_tail(
                                    source_degree,
                                    first_degree,
                                    explicit_end,
                                    precision,
                                ).total_upper
                                / (first_degree * (first_degree + 1))
                            )
                    else:
                        key = ("self-removed", source_degree)
                        cache[key] = 0.0
                elif abs(target - source) == 1:
                    key = (
                        "adjacent-analytic",
                        labels[target],
                        labels[source],
                        source_degree,
                    )
                    if key not in cache:
                        cache[key] = certify_adjacent_analytic_tail(
                            lengths[target],
                            lengths[source],
                            source_degree,
                            first_degree,
                            precision,
                        ).frobenius_upper
                else:
                    lower = min(target, source)
                    upper = max(target, source)
                    between = labels[lower + 1 : upper]
                    gap_signature = tuple(
                        between.count(label)
                        for label in ("edge", "bridge", "center")
                    )
                    key = (
                        "separated",
                        labels[target],
                        labels[source],
                        gap_signature,
                        source_degree,
                    )
                    if key not in cache:
                        gap = sum(lengths[lower + 1 : upper], arb(0))
                        cache[key] = (
                            certify_second_green_separated_geometric_tail(
                                lengths[target],
                                lengths[source],
                                gap,
                                first_degree,
                                precision,
                            ).total_upper
                            / (first_degree * (first_degree + 1))
                        )
                comparison[target, source] = cache[key]

        comparison_arb = arb_mat(13, 13)
        for row in range(13):
            for column in range(13):
                comparison_arb[row, column] = arb(
                    str(comparison[row, column])
                )
        row_column = (
            arb(str(np.max(np.sum(comparison, axis=1))))
            * arb(str(np.max(np.sum(comparison, axis=0))))
        ).sqrt()
        gram = comparison_arb.transpose() * comparison_arb
        try:
            eigenvalues = gram.eig(multiple=True, algorithm="rump")
            spectral = min(
                max(value.real.upper() for value in eigenvalues).sqrt(),
                row_column,
            )
        except ValueError:
            spectral = row_column
    finally:
        ctx.prec = previous_precision

    return ThirdWindowOtherTail(
        half_width=half_width,
        interval_degrees=degrees,
        first_degree=first_degree,
        comparison_matrix=comparison,
        spectral_norm_upper=math.nextafter(float(spectral.upper()), math.inf),
        row_column_upper=math.nextafter(float(row_column.upper()), math.inf),
        includes_self_blocks=include_self_blocks,
        precision=precision,
    )
