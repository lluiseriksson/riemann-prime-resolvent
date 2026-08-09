"""Prime-2 translation in a Legendre basis adapted to its internal cut."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


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


def first_prime_partition(half_width: float) -> FirstPrimePartition:
    """Partition [-1,1] into the two translated edges and their complement."""
    if not math.log(2.0) / 2.0 < half_width <= 0.5:
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
