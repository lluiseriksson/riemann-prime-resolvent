"""Regularized logarithmic tail on the seven-block second-prime window."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_second_green_tail import (
    certify_second_green_adjacent_tail,
    certify_second_green_self_tail,
    certify_second_green_separated_tail,
)
from experiments.theta_pencil.cut_adapted_prime_basis import (
    second_prime_partition,
)


@dataclass(frozen=True)
class SecondWindowRegularizedTail:
    half_width: float
    interval_degrees: tuple[int, ...]
    first_degrees: tuple[int, ...]
    comparison_matrix: np.ndarray
    spectral_norm_upper: float
    row_column_upper: float
    precision: int


def _float_upper(value) -> float:
    return math.nextafter(float(value.upper()), math.inf)


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


def certify_second_window_regularized_tail(
    half_width: float,
    edge_degree: int,
    bridge_degree: int,
    center_degree: int,
    first_degree: int = 128,
    derivative_order: int = 12,
    explicit_end: int = 4096,
    subdivisions: int = 192,
    precision: int = 512,
    moment_order: int = 8,
) -> SecondWindowRegularizedTail:
    """Bound the seven-block map ``Q D L P`` by block comparison.

    Each entry bounds one operator block from a retained source interval to
    an omitted target tail.  The spectral norm of this nonnegative comparison
    matrix bounds the norm of the full block operator.
    """

    second_prime_partition(half_width)
    degrees = _degree_pattern(edge_degree, bridge_degree, center_degree)
    first_degrees = (first_degree,) * 7
    if first_degree <= max(degrees):
        raise ValueError("first_degree must exceed every local degree count")
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
        labels = ("e", "b", "e", "c", "e", "b", "e")
        comparison = np.zeros((7, 7), dtype=float)
        cache: dict[tuple[object, ...], float] = {}
        for target in range(7):
            for source in range(7):
                source_degree = degrees[source]
                if target == source:
                    key = ("self", source_degree, first_degrees[target])
                    if key not in cache:
                        cache[key] = certify_second_green_self_tail(
                            source_degree,
                            first_degrees[target],
                            explicit_end,
                            precision,
                        ).total_upper
                elif abs(target - source) == 1:
                    key = (
                        "adjacent",
                        labels[target],
                        labels[source],
                        source_degree,
                        first_degrees[target],
                    )
                    if key not in cache:
                        cache[key] = certify_second_green_adjacent_tail(
                            lengths[target],
                            lengths[source],
                            source_degree,
                            first_degrees[target],
                            derivative_order,
                            explicit_end,
                            subdivisions,
                            precision,
                            moment_order,
                        ).total_upper
                else:
                    lower = min(target, source)
                    upper = max(target, source)
                    gap_labels = tuple(sorted(labels[lower + 1 : upper]))
                    gap = sum(lengths[lower + 1 : upper], arb(0))
                    key = (
                        "separated",
                        labels[target],
                        labels[source],
                        gap_labels,
                        source_degree,
                        first_degrees[target],
                    )
                    if key not in cache:
                        cache[key] = certify_second_green_separated_tail(
                            lengths[target],
                            lengths[source],
                            gap,
                            source_degree,
                            first_degrees[target],
                            derivative_order,
                            subdivisions,
                            precision,
                        ).total_upper
                comparison[target, source] = cache[key]

        comparison_arb = arb_mat(7, 7)
        for row in range(7):
            for column in range(7):
                comparison_arb[row, column] = arb(str(comparison[row, column]))
        gram = comparison_arb.transpose() * comparison_arb
        eigenvalues = gram.eig(multiple=True, algorithm="rump")
        spectral_norm = max(value.real.upper() for value in eigenvalues).sqrt()
        row_column = (
            arb(str(np.max(np.sum(comparison, axis=1))))
            * arb(str(np.max(np.sum(comparison, axis=0))))
        ).sqrt()
    finally:
        ctx.prec = previous_precision

    return SecondWindowRegularizedTail(
        half_width=half_width,
        interval_degrees=degrees,
        first_degrees=first_degrees,
        comparison_matrix=comparison,
        spectral_norm_upper=_float_upper(spectral_norm),
        row_column_upper=_float_upper(row_column),
        precision=precision,
    )
