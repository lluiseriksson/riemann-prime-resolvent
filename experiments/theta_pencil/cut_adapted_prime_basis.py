"""Prime-2 translation in a Legendre basis adapted to its internal cut."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.support_window import (
    in_first_prime_window,
    in_second_prime_window,
    in_third_prime_partition_window,
)


@dataclass(frozen=True)
class FirstPrimePartition:
    half_width: float
    displacement: float
    left: tuple[float, float]
    center: tuple[float, float]
    right: tuple[float, float]


@dataclass(frozen=True)
class CutAdaptedPrimeMatrix:
    partition: FirstPrimePartition
    edge_degree: int
    center_degree: int
    matrix: np.ndarray
    diagonalizing_transform: np.ndarray
    diagonal: np.ndarray


@dataclass(frozen=True)
class SecondPrimePartition:
    half_width: float
    displacement_two: float
    displacement_three: float
    intervals: tuple[tuple[float, float], ...]
    prime_two_pairs: tuple[tuple[int, int], ...]
    prime_three_pairs: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class SecondWindowPrimeMatrix:
    partition: SecondPrimePartition
    interval_degrees: tuple[int, ...]
    offsets: tuple[int, ...]
    matrix: np.ndarray


@dataclass(frozen=True)
class ThirdPrimePartition:
    half_width: float
    displacement_two: float
    displacement_three: float
    displacement_four: float
    intervals: tuple[tuple[float, float], ...]
    prime_two_pairs: tuple[tuple[int, int], ...]
    prime_three_pairs: tuple[tuple[int, int], ...]
    prime_four_pairs: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class ThirdWindowPrimeMatrix:
    partition: ThirdPrimePartition
    interval_degrees: tuple[int, ...]
    offsets: tuple[int, ...]
    matrix: np.ndarray


def first_prime_partition(half_width: float) -> FirstPrimePartition:
    """Partition the whole prime-2-only window into edges and complement.

    At the upper endpoint the prime-3 translation touches only an endpoint,
    hence is zero as an ``L^2`` operator.  Above it a second internal cut is
    needed and this three-block architecture is no longer complete.
    """
    if not in_first_prime_window(half_width):
        raise ValueError("the cut-adapted partition is for the first prime window")
    displacement = math.log(2.0) / half_width
    cut = 1.0 - displacement
    return FirstPrimePartition(
        half_width=half_width,
        displacement=displacement,
        left=(-1.0, cut),
        center=(cut, -cut),
        right=(-cut, 1.0),
    )


def second_prime_partition(half_width: float) -> SecondPrimePartition:
    """Seven-interval closure for the active prime powers two and three.

    Merely inserting the two pairs of translation cuts gives five intervals
    but is not closed under the prime-two translation. The images of the
    prime-three cuts add the pair ``+/- (1-h_3+h_2)``, yielding seven blocks.
    """

    if not in_second_prime_window(half_width):
        raise ValueError("the seven-block partition is for the second prime window")
    h_two = math.log(2.0) / half_width
    h_three = math.log(3.0) / half_width
    breakpoints = (
        -1.0,
        1.0 - h_three,
        h_three - h_two - 1.0,
        1.0 - h_two,
        h_two - 1.0,
        1.0 - h_three + h_two,
        h_three - 1.0,
        1.0,
    )
    if not all(
        breakpoints[index] < breakpoints[index + 1]
        for index in range(len(breakpoints) - 1)
    ):
        raise ArithmeticError("the second-window cut ordering did not close")
    intervals = tuple(zip(breakpoints[:-1], breakpoints[1:]))
    return SecondPrimePartition(
        half_width=half_width,
        displacement_two=h_two,
        displacement_three=h_three,
        intervals=intervals,
        prime_two_pairs=((0, 4), (1, 5), (2, 6)),
        prime_three_pairs=((0, 6),),
    )


def third_prime_partition(half_width: float) -> ThirdPrimePartition:
    """Thirteen-interval closure after the prime-power-four threshold."""

    if not in_third_prime_partition_window(half_width):
        raise ValueError("the thirteen-block partition is for the third window")
    h_two = math.log(2.0) / half_width
    h_three = math.log(3.0) / half_width
    h_four = 2.0 * h_two
    breakpoints = (
        -1.0,
        1.0 - 2.0 * h_two,
        -1.0 + 2.0 * h_two - h_three,
        1.0 - h_three,
        -1.0 - h_two + h_three,
        1.0 - 3.0 * h_two + h_three,
        -1.0 + h_two,
        1.0 - h_two,
        -1.0 + 3.0 * h_two - h_three,
        1.0 + h_two - h_three,
        -1.0 + h_three,
        1.0 - 2.0 * h_two + h_three,
        -1.0 + 2.0 * h_two,
        1.0,
    )
    if not all(
        breakpoints[index] < breakpoints[index + 1]
        for index in range(len(breakpoints) - 1)
    ):
        raise ArithmeticError("the third-window cut ordering did not close")
    return ThirdPrimePartition(
        half_width=half_width,
        displacement_two=h_two,
        displacement_three=h_three,
        displacement_four=h_four,
        intervals=tuple(zip(breakpoints[:-1], breakpoints[1:])),
        prime_two_pairs=(
            (0, 6),
            (1, 7),
            (2, 8),
            (3, 9),
            (4, 10),
            (5, 11),
            (6, 12),
        ),
        prime_three_pairs=((0, 10), (1, 11), (2, 12)),
        prime_four_pairs=((0, 12),),
    )


def build_third_window_prime_matrix(
    half_width: float,
    edge_degree: int,
    bridge_degree: int,
    center_degree: int,
) -> ThirdWindowPrimeMatrix:
    """Exact prime-power graph in the thirteen-interval local basis."""

    if min(edge_degree, bridge_degree, center_degree) < 1:
        raise ValueError("all local degree counts must be positive")
    partition = third_prime_partition(half_width)
    degrees = (
        edge_degree,
        bridge_degree,
        edge_degree,
        center_degree,
        edge_degree,
        bridge_degree,
        edge_degree,
        bridge_degree,
        edge_degree,
        center_degree,
        edge_degree,
        bridge_degree,
        edge_degree,
    )
    offsets = [0]
    for degree in degrees:
        offsets.append(offsets[-1] + degree)
    matrix = np.zeros((offsets[-1], offsets[-1]))

    def add(pairs, coefficient):
        for left, right in pairs:
            if degrees[left] != degrees[right]:
                raise ArithmeticError("translated interval degrees differ")
            left_slice = slice(offsets[left], offsets[left + 1])
            right_slice = slice(offsets[right], offsets[right + 1])
            block = -coefficient * np.eye(degrees[left])
            matrix[left_slice, right_slice] += block
            matrix[right_slice, left_slice] += block

    add(partition.prime_two_pairs, math.log(2.0) / math.sqrt(2.0))
    add(partition.prime_three_pairs, math.log(3.0) / math.sqrt(3.0))
    add(partition.prime_four_pairs, math.log(2.0) / math.sqrt(4.0))
    return ThirdWindowPrimeMatrix(
        partition=partition,
        interval_degrees=degrees,
        offsets=tuple(offsets),
        matrix=matrix,
    )


def build_second_window_prime_matrix(
    half_width: float,
    edge_degree: int,
    bridge_degree: int,
    center_degree: int,
) -> SecondWindowPrimeMatrix:
    """Exact finite prime graph in the seven-interval local Legendre basis."""

    if edge_degree < 1 or bridge_degree < 1 or center_degree < 0:
        raise ValueError(
            "edge and bridge degrees must be positive; center may be zero"
        )
    partition = second_prime_partition(half_width)
    degrees = (
        edge_degree,
        bridge_degree,
        edge_degree,
        center_degree,
        edge_degree,
        bridge_degree,
        edge_degree,
    )
    offsets = [0]
    for degree in degrees:
        offsets.append(offsets[-1] + degree)
    matrix = np.zeros((offsets[-1], offsets[-1]))

    def add_translation(left: int, right: int, coefficient: float) -> None:
        degree = degrees[left]
        if degrees[right] != degree:
            raise ArithmeticError("translated intervals have unequal local degrees")
        left_slice = slice(offsets[left], offsets[left + 1])
        right_slice = slice(offsets[right], offsets[right + 1])
        block = -coefficient * np.eye(degree)
        matrix[left_slice, right_slice] += block
        matrix[right_slice, left_slice] += block

    coefficient_two = math.log(2.0) / math.sqrt(2.0)
    coefficient_three = math.log(3.0) / math.sqrt(3.0)
    for left, right in partition.prime_two_pairs:
        add_translation(left, right, coefficient_two)
    for left, right in partition.prime_three_pairs:
        add_translation(left, right, coefficient_three)
    return SecondWindowPrimeMatrix(
        partition=partition,
        interval_degrees=degrees,
        offsets=tuple(offsets),
        matrix=matrix,
    )


def build_cut_adapted_prime_matrix(
    half_width: float,
    edge_degree: int,
    center_degree: int,
) -> CutAdaptedPrimeMatrix:
    """Return the exact prime-2 block and its symmetric/antisymmetric basis.

    The original ordering is left-edge, center, right-edge.  Columns of the
    transform are symmetric edges, center, then antisymmetric edges.
    """
    if edge_degree < 1 or center_degree < 0:
        raise ValueError("edge_degree must be positive and center_degree nonnegative")
    partition = first_prime_partition(half_width)
    total = 2 * edge_degree + center_degree
    coefficient = math.log(2.0) / math.sqrt(2.0)

    matrix = np.zeros((total, total))
    left = np.arange(edge_degree)
    right = np.arange(edge_degree) + edge_degree + center_degree
    matrix[left, right] = -coefficient
    matrix[right, left] = -coefficient

    transform = np.zeros_like(matrix)
    inverse_sqrt_two = 1.0 / math.sqrt(2.0)
    for degree in range(edge_degree):
        transform[degree, degree] = inverse_sqrt_two
        transform[edge_degree + center_degree + degree, degree] = inverse_sqrt_two
    for degree in range(center_degree):
        transform[edge_degree + degree, edge_degree + degree] = 1.0
    antisymmetric_offset = edge_degree + center_degree
    for degree in range(edge_degree):
        column = antisymmetric_offset + degree
        transform[degree, column] = inverse_sqrt_two
        transform[edge_degree + center_degree + degree, column] = -inverse_sqrt_two

    diagonal = np.concatenate(
        (
            np.full(edge_degree, -coefficient),
            np.zeros(center_degree),
            np.full(edge_degree, coefficient),
        )
    )
    return CutAdaptedPrimeMatrix(
        partition=partition,
        edge_degree=edge_degree,
        center_degree=center_degree,
        matrix=matrix,
        diagonalizing_transform=transform,
        diagonal=diagonal,
    )
