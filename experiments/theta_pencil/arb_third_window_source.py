"""Arb finite source on the thirteen-block prime-power-four partition."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_cut_dominant import _cross_block_rectangular
from experiments.theta_pencil.arb_cut_smooth import _power_block_rectangular
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_source_schur import _roundtrip_ball
from experiments.theta_pencil.cut_adapted_prime_basis import third_prime_partition
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_remainder_bound,
    smooth_remainder_series_coefficients,
)


@dataclass(frozen=True)
class ArbThirdWindowComponent:
    midpoint: np.ndarray
    radius: np.ndarray
    interval_degrees: tuple[int, ...]
    offsets: tuple[int, ...]
    precision: int


@dataclass(frozen=True)
class ArbThirdWindowFiniteSource:
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


def _degree_pattern(edge: int, bridge: int, center: int) -> tuple[int, ...]:
    if min(edge, bridge, center) < 1:
        raise ValueError("all local degree counts must be positive")
    return (
        edge,
        bridge,
        edge,
        center,
        edge,
        bridge,
        edge,
        bridge,
        edge,
        center,
        edge,
        bridge,
        edge,
    )


def _offsets(degrees: tuple[int, ...]) -> tuple[int, ...]:
    result = [0]
    for degree in degrees:
        result.append(result[-1] + degree)
    return tuple(result)


def _arb_breakpoints_lengths(arb, half_width: float):
    a = arb(str(half_width))
    one = arb(1)
    h_two = arb.const_log2() / a
    h_three = arb(3).log() / a
    breakpoints = (
        -one,
        one - 2 * h_two,
        -one + 2 * h_two - h_three,
        one - h_three,
        -one - h_two + h_three,
        one - 3 * h_two + h_three,
        -one + h_two,
        one - h_two,
        -one + 3 * h_two - h_three,
        one + h_two - h_three,
        -one + h_three,
        one - 2 * h_two + h_three,
        -one + 2 * h_two,
        one,
    )
    lengths = tuple(
        breakpoints[index + 1] - breakpoints[index] for index in range(13)
    )
    if not all(length.lower() > 0 for length in lengths):
        raise ArithmeticError("the thirteen interval lengths were not positive")
    return a, breakpoints, lengths


def _export(matrix, size: int) -> tuple[np.ndarray, np.ndarray]:
    midpoint = np.empty((size, size), dtype=float)
    radius = np.empty_like(midpoint)
    for row in range(size):
        for column in range(size):
            midpoint[row, column] = float(matrix[row, column].mid())
            radius[row, column] = _arb_radius_as_float(matrix[row, column])
    return midpoint, radius


def build_arb_third_window_dominant(
    half_width: float,
    edge_degree: int,
    bridge_degree: int,
    center_degree: int,
    precision: int = 256,
) -> ArbThirdWindowComponent:
    """Build the exact scale-free logarithmic form on thirteen intervals."""

    third_prime_partition(half_width)
    degrees = _degree_pattern(edge_degree, bridge_degree, center_degree)
    offsets = _offsets(degrees)
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        _, _, lengths = _arb_breakpoints_lengths(arb, half_width)
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

        for left_block in range(13):
            for right_block in range(left_block + 1, 13):
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
                        row = offsets[left_block] + left
                        column = offsets[right_block] + right
                        matrix[row, column] = value
                        matrix[column, row] = value
        midpoint, radius = _export(matrix, total)
    finally:
        ctx.prec = previous_precision
    return ArbThirdWindowComponent(midpoint, radius, degrees, offsets, precision)


def build_arb_third_window_smooth(
    half_width: float,
    edge_degree: int,
    bridge_degree: int,
    center_degree: int,
    maximum_power: int = 47,
    precision: int = 256,
) -> ArbThirdWindowComponent:
    """Build the truncated smooth kernel on thirteen intervals."""

    if maximum_power < 1:
        raise ValueError("maximum_power must be positive")
    third_prime_partition(half_width)
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
        a, _, lengths = _arb_breakpoints_lengths(arb, half_width)
        total = offsets[-1]
        matrix = arb_mat(total, total)
        for left_block in range(13):
            for right_block in range(left_block, 13):
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
                        row = offsets[left_block] + left
                        column = offsets[right_block] + right
                        matrix[row, column] = value
                        matrix[column, row] = value
        midpoint, radius = _export(matrix, total)
    finally:
        ctx.prec = previous_precision
    return ArbThirdWindowComponent(midpoint, radius, degrees, offsets, precision)


def _parity_transforms(arb, arb_mat, degrees, offsets):
    total = offsets[-1]
    pairs = ((0, 12), (1, 11), (2, 10), (3, 9), (4, 8), (5, 7))
    paired_size = sum(degrees[left] for left, _ in pairs)
    center_even = tuple(range(0, degrees[6], 2))
    center_odd = tuple(range(1, degrees[6], 2))
    even = arb_mat(total, paired_size + len(center_even))
    odd = arb_mat(total, paired_size + len(center_odd))
    inverse_sqrt_two = 1 / arb(2).sqrt()
    column_offset = 0
    for left_block, right_block in pairs:
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
        even[offsets[6] + degree, column] = 1
    for column, degree in enumerate(center_odd, start=paired_size):
        odd[offsets[6] + degree, column] = 1
    return even, odd


def build_arb_third_window_source(
    half_width: float = 0.7,
    edge_degree: int = 8,
    bridge_degree: int = 8,
    center_degree: int = 8,
    maximum_power: int = 47,
    precision: int = 384,
) -> ArbThirdWindowFiniteSource:
    """Assemble dominant, scalar, smooth and exact prime-power graph terms."""

    partition = third_prime_partition(half_width)
    dominant = build_arb_third_window_dominant(
        half_width, edge_degree, bridge_degree, center_degree, precision
    )
    smooth = build_arb_third_window_smooth(
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

        def add_prime(pairs, coefficient):
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
        add_prime(partition.prime_four_pairs, arb.const_log2() / arb(4).sqrt())

        even_transform, odd_transform = _parity_transforms(
            arb, arb_mat, degrees, offsets
        )
        even = even_transform.transpose() * source * even_transform
        odd = odd_transform.transpose() * source * odd_transform
        midpoint, radius = _export(source, total)
        even_midpoint, even_radius = _export(even, even.nrows())
        odd_midpoint, odd_radius = _export(odd, odd.nrows())
    finally:
        ctx.prec = previous_precision

    return ArbThirdWindowFiniteSource(
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
