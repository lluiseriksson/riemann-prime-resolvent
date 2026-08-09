"""Closed Legendre matrix for the dominant localized Weil operator.

On ``(-1, 1)`` Suzuki's scale-free operator is

    L = A_2 - (1/2) log(1 - x^2),

where ``A_2 P_n = H_n P_n``.  This module evaluates its matrix in the
orthonormal Legendre basis without endpoint quadrature.
"""

from __future__ import annotations

import math

import numpy as np


def harmonic(index: int) -> float:
    """Return H_index, with H_0 = 0."""
    if index < 0:
        raise ValueError("index must be nonnegative")
    return math.fsum(1.0 / k for k in range(1, index + 1))


def diagonal_correction(index: int) -> float:
    """Return D_n = 1 + sum_{k=1}^n 1/(k(2k-1)(2k+1))."""
    if index < 0:
        raise ValueError("index must be nonnegative")
    return 1.0 + math.fsum(
        1.0 / (k * (2 * k - 1) * (2 * k + 1))
        for k in range(1, index + 1)
    )


def legendre_log_integral(left: int, right: int) -> float:
    """Return integral P_left P_right log(1-x^2) dx over (-1, 1).

    The closed expression is zero across parity blocks.  Away from the
    diagonal it is rational; on the diagonal the only transcendental term is
    log(2).
    """
    if left < 0 or right < 0:
        raise ValueError("degrees must be nonnegative")
    if (left + right) % 2:
        return 0.0
    if left == right:
        return (
            4.0
            / (2 * left + 1)
            * (math.log(2.0) - diagonal_correction(left))
        )
    return -4.0 / (abs(left - right) * (left + right + 1))


def boundary_potential_matrix(size: int) -> np.ndarray:
    """Matrix of -(1/2) log(1-x^2) in normalized Legendre coordinates."""
    if size < 1:
        raise ValueError("size must be positive")
    result = np.zeros((size, size), dtype=float)
    for left in range(size):
        result[left, left] = diagonal_correction(left) - math.log(2.0)
        for right in range(left + 1, size):
            if (left + right) % 2:
                continue
            value = math.sqrt((2 * left + 1) * (2 * right + 1)) / (
                abs(left - right) * (left + right + 1)
            )
            result[left, right] = value
            result[right, left] = value
    return result


def regional_log_laplacian_matrix(size: int) -> np.ndarray:
    """Diagonal matrix of A_2 in normalized Legendre coordinates."""
    if size < 1:
        raise ValueError("size must be positive")
    return np.diag([harmonic(index) for index in range(size)])


def dominant_operator_matrix(size: int) -> np.ndarray:
    """Return the exact finite section of L = A_2 -(1/2)log(1-x^2)."""
    return regional_log_laplacian_matrix(size) + boundary_potential_matrix(size)

