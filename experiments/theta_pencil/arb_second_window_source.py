"""Arb finite source on the seven-block prime-two/prime-three partition."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_cut_dominant import (
    _cross_block_rectangular,
)
from experiments.theta_pencil.arb_cut_smooth import (
    _power_block_rectangular,
)
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_source_schur import _roundtrip_ball
from experiments.theta_pencil.cut_adapted_prime_basis import (
    second_prime_partition,
)
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_remainder_bound,
    smooth_remainder_series_coefficients,
)


@dataclass(frozen=True)
class ArbSecondWindowComponent:
    midpoint: np.ndarray
    radius: np.ndarray
    interval_degrees: tuple[int, ...]
    offsets: tuple[int, ...]
    precision: int


@dataclass(frozen=True)
class ArbSecondWindowFiniteSource:
    midpoint: np.ndarray
    radius: np.ndarray
    even_midpoint: np.ndarray
    even_radius: np.ndarray
    odd_midpoint: np.ndarray
    odd_radius: np.ndarray
    interval_degrees: tuple[int, ...]
    offsets: tuple[int, ...]
    smooth_remainder: float
    precision: int


def _degree_pattern(
    edge_degree: int, bridge_degree: int, center_degree: int
) -> tuple[int, ...]:
    if edge_degree < 1 or bridge_degree < 1 or center_degree < 1:
        raise ValueError("all three local degree counts must be positive")
    return (
        edge_degree,
        bridge_degree,
        edge_degree,
        center_degree,
        edge_degree,
        bridge_degree,
        edge_degree,
    )


def _offsets(degrees: tuple[int, ...]) -> tuple[int, ...]:
    result = [0]
    for degree in degrees:
        result.append(result[-1] + degree)
    return tuple(result)


def _arb_lengths(arb, half_width: float):
    a = arb(str(half_width))
    h_two = arb.const_log2() / a
    h_three = arb(3).log() / a
    edge = 2 - h_three
    bridge = 2 * h_three - h_two - 2
    center = 2 * h_two - 2
    if not edge.lower() > 0 or not bridge.lower() > 0 or not center.lower() > 0:
        raise ArithmeticError("the seven interval lengths were not positive")
    return a, (edge, bridge, edge, center, edge, bridge, edge)


def _export(matrix, size: int) -> tuple[np.ndarray, np.ndarray]:
    midpoint = np.empty((size, size), dtype=float)
    radius = np.empty_like(midpoint)
    for left in range(size):
        for right in range(size):
            value = matrix[left, right]
            midpoint[left, right] = float(value.mid())
            radius[left, right] = _arb_radius_as_float(value)
    return midpoint, radius


def build_arb_second_window_dominant(
    half_width: float,
    edge_degree: int,
    bridge_degree: int,
    center_degree: int,
    precision: int = 256,
) -> ArbSecondWindowComponent:
    """Build the exact scale-free logarithmic form on seven intervals."""

    second_prime_partition(half_width)
    degrees = _degree_pattern(edge_degree, bridge_degree, center_degree)
    offsets = _offsets(degrees)
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        _, lengths = _arb_lengths(arb, half_width)
        total = offsets[-1]
        matrix = arb_mat(total, total)
        maximum_degree = max(degrees)
        harmonic = [arb(0)]
        diagonal = [arb(1)]
        for degree in range(1, maximum_degree):
            harmonic.append(harmonic[-1] + arb(1) / degree)
            diagonal.append(
                diagonal[-1]
                + arb(1) / (degree * (2 * degree - 1) * (2 * degree + 1))
            )

        def standard_entry(left: int, right: int):
            if (left + right) % 2:
                return arb(0)
            if left == right:
                return harmonic[left] + diagonal[left] - arb.const_log2()
            return arb((2 * left + 1) * (2 * right + 1)).sqrt() / (
                abs(left - right) * (left + right + 1)
            )

        for block, (length, degree_count) in enumerate(zip(lengths, degrees)):
            shift = -(length / 2).log()
            for left in range(degree_count):
                for right in range(degree_count):
                    value = standard_entry(left, right)
                    if left == right:
                        value += shift
                    matrix[offsets[block] + left, offsets[block] + right] = value

        for left_block in range(7):
            for right_block in range(left_block + 1, 7):
                gap = sum(lengths[left_block + 1 : right_block], arb(0))
                cross = _cross_block_rectangular(
                    arb,
                    arb_mat,
                    lengths[left_block],
                    lengths[right_block],
                    gap,
                    0,
                    degrees[left_block],
                    0,
                    degrees[right_block],
                )
                for left in range(degrees[left_block]):
                    for right in range(degrees[right_block]):
                        value = cross[left, right]
                        matrix[offsets[left_block] + left, offsets[right_block] + right] = value
                        matrix[offsets[right_block] + right, offsets[left_block] + left] = value
        midpoint, radius = _export(matrix, total)
    finally:
        ctx.prec = previous_precision
    return ArbSecondWindowComponent(midpoint, radius, degrees, offsets, precision)


def build_arb_second_window_smooth(
    half_width: float,
    edge_degree: int,
    bridge_degree: int,
    center_degree: int,
    maximum_power: int = 23,
    precision: int = 256,
) -> ArbSecondWindowComponent:
    """Build the truncated smooth kernel on the seven intervals."""

    if maximum_power < 1:
        raise ValueError("maximum_power must be positive")
    second_prime_partition(half_width)
    degrees = _degree_pattern(edge_degree, bridge_degree, center_degree)
    offsets = _offsets(degrees)
    coefficients = smooth_remainder_series_coefficients(maximum_power)
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a, lengths = _arb_lengths(arb, half_width)
        total = offsets[-1]
        matrix = arb_mat(total, total)
        for left_block in range(7):
            for right_block in range(left_block, 7):
                same = left_block == right_block
                gap = sum(lengths[left_block + 1 : right_block], arb(0))
                block = arb_mat(degrees[left_block], degrees[right_block])
                for power, coefficient in enumerate(coefficients):
                    power_matrix = _power_block_rectangular(
                        arb,
                        arb_mat,
                        lengths[left_block],
                        lengths[right_block],
                        gap,
                        degrees[left_block],
                        degrees[right_block],
                        power,
                        same,
                    )
                    rational = arb(coefficient.numerator) / coefficient.denominator
                    block += (-a * rational * a**power) * power_matrix
                for left in range(degrees[left_block]):
                    for right in range(degrees[right_block]):
                        value = block[left, right]
                        matrix[offsets[left_block] + left, offsets[right_block] + right] = value
                        matrix[offsets[right_block] + right, offsets[left_block] + left] = value
        midpoint, radius = _export(matrix, total)
    finally:
        ctx.prec = previous_precision
    return ArbSecondWindowComponent(midpoint, radius, degrees, offsets, precision)


def build_arb_second_window_source(
    half_width: float,
    edge_degree: int,
    bridge_degree: int,
    center_degree: int,
    maximum_power: int = 23,
    precision: int = 384,
) -> ArbSecondWindowFiniteSource:
    """Assemble dominant, scalar, exact prime graph and smooth kernel."""

    partition = second_prime_partition(half_width)
    dominant = build_arb_second_window_dominant(
        half_width, edge_degree, bridge_degree, center_degree, precision
    )
    smooth = build_arb_second_window_smooth(
        half_width,
        edge_degree,
        bridge_degree,
        center_degree,
        maximum_power,
        precision,
    )
    degrees = dominant.interval_degrees
    offsets = dominant.offsets
    total = offsets[-1]
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        source = arb_mat(total, total)
        a = arb(str(half_width))
        scalar = -a.log() - (2 * arb.pi()).log() - arb.const_euler()
        for left in range(total):
            for right in range(total):
                source[left, right] = _roundtrip_ball(
                    arb, dominant.midpoint[left, right], dominant.radius[left, right]
                ) + _roundtrip_ball(
                    arb, smooth.midpoint[left, right], smooth.radius[left, right]
                )
                if left == right:
                    source[left, right] += scalar

        def add_prime(pairs, coefficient) -> None:
            for left_block, right_block in pairs:
                if degrees[left_block] != degrees[right_block]:
                    raise ArithmeticError("prime-linked degree counts differ")
                for degree in range(degrees[left_block]):
                    left = offsets[left_block] + degree
                    right = offsets[right_block] + degree
                    source[left, right] -= coefficient
                    source[right, left] -= coefficient

        add_prime(partition.prime_two_pairs, arb.const_log2() / arb(2).sqrt())
        add_prime(partition.prime_three_pairs, arb(3).log() / arb(3).sqrt())

        inverse_sqrt_two = 1 / arb(2).sqrt()
        pair_blocks = ((0, 6), (1, 5), (2, 4))
        center_even = tuple(range(0, center_degree, 2))
        center_odd = tuple(range(1, center_degree, 2))
        paired_size = edge_degree + bridge_degree + edge_degree
        even_size = paired_size + len(center_even)
        odd_size = paired_size + len(center_odd)
        even_transform = arb_mat(total, even_size)
        odd_transform = arb_mat(total, odd_size)
        column_offset = 0
        for left_block, right_block in pair_blocks:
            for degree in range(degrees[left_block]):
                reflection_sign = -1 if degree % 2 else 1
                column = column_offset + degree
                even_transform[offsets[left_block] + degree, column] = inverse_sqrt_two
                even_transform[offsets[right_block] + degree, column] = reflection_sign * inverse_sqrt_two
                odd_transform[offsets[left_block] + degree, column] = inverse_sqrt_two
                odd_transform[offsets[right_block] + degree, column] = -reflection_sign * inverse_sqrt_two
            column_offset += degrees[left_block]
        for column, degree in enumerate(center_even, start=paired_size):
            even_transform[offsets[3] + degree, column] = 1
        for column, degree in enumerate(center_odd, start=paired_size):
            odd_transform[offsets[3] + degree, column] = 1

        even = even_transform.transpose() * source * even_transform
        odd = odd_transform.transpose() * source * odd_transform
        midpoint, radius = _export(source, total)
        even_midpoint, even_radius = _export(even, even_size)
        odd_midpoint, odd_radius = _export(odd, odd_size)
    finally:
        ctx.prec = previous_precision

    return ArbSecondWindowFiniteSource(
        midpoint=midpoint,
        radius=radius,
        even_midpoint=even_midpoint,
        even_radius=even_radius,
        odd_midpoint=odd_midpoint,
        odd_radius=odd_radius,
        interval_degrees=degrees,
        offsets=offsets,
        smooth_remainder=smooth_kernel_series_remainder_bound(
            half_width, maximum_power
        ),
        precision=precision,
    )
