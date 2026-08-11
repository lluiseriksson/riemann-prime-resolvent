"""Gauss--Stieltjes polynomial lower bounds for the boundary potential.

This module is deliberately independent of SciPy.  It constructs the
Chebyshev truncation of

    R_m(x) = 1/2 sum_j w_j x^2 / (1 - t_j x^2)

and compresses multiplication by the resulting polynomial to the normalized
Legendre basis.  The compression is formed in an enlarged Jacobi space; using
``p(P_N X P_N)`` directly would give the wrong boundary rows.

Floating-point matrices returned here are design diagnostics.  The analytic
lower relation and the explicit uniform truncation error are recorded in
``docs/theta-reboot/gauss-stieltjes-potential.md``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.polynomial.chebyshev import chebval
from numpy.polynomial.legendre import Legendre, leggauss, legvander


@dataclass(frozen=True)
class StieltjesPolynomial:
    """Chebyshev data for a certified pointwise lower polynomial."""

    quadrature_order: int
    chebyshev_order: int
    coefficients: np.ndarray
    uniform_error: float


def gauss_stieltjes_chebyshev(
    quadrature_order: int = 8, chebyshev_order: int = 64
) -> StieltjesPolynomial:
    """Return coefficients of ``R_{m,J} - epsilon`` in ``T_k``.

    ``coefficients[k]`` multiplies ``T_k``.  Odd coefficients vanish.  The
    final constant subtraction makes the polynomial a pointwise lower bound
    for ``-log(1-x^2)/2`` on the open interval.
    """

    if quadrature_order < 1 or chebyshev_order < 0:
        raise ValueError("orders must be nonnegative, with quadrature positive")
    raw_nodes, raw_weights = leggauss(quadrature_order)
    nodes = (raw_nodes + 1.0) / 2.0
    weights = raw_weights / 2.0
    root = np.sqrt(1.0 - nodes)
    q = (1.0 - root) / (1.0 + root)

    coefficients = np.zeros(2 * chebyshev_order + 1, dtype=float)
    coefficients[0] = 0.5 * np.sum(
        weights / nodes * (1.0 / root - 1.0)
    )
    for index in range(1, chebyshev_order + 1):
        coefficients[2 * index] = np.sum(
            weights * q**index / (nodes * root)
        )
    error = float(
        np.sum(
            weights
            / (nodes * root)
            * q ** (chebyshev_order + 1)
            / (1.0 - q)
        )
    )
    coefficients[0] -= error
    return StieltjesPolynomial(
        quadrature_order=quadrature_order,
        chebyshev_order=chebyshev_order,
        coefficients=coefficients,
        uniform_error=error,
    )


def _jacobi_links(size: int) -> np.ndarray:
    degrees = np.arange(size - 1, dtype=float)
    return (degrees + 1.0) / np.sqrt(
        (2.0 * degrees + 1.0) * (2.0 * degrees + 3.0)
    )


def _left_multiply_x(matrix: np.ndarray, links: np.ndarray) -> np.ndarray:
    """Return the normalized-Legendre Jacobi matrix times ``matrix``."""

    result = np.zeros_like(matrix)
    result[:-1] += links[:, None] * matrix[1:]
    result[1:] += links[:, None] * matrix[:-1]
    return result


def chebyshev_multiplication_compression(
    coefficients: np.ndarray, size: int
) -> np.ndarray:
    """Compress multiplication by a Chebyshev polynomial exactly in degree.

    The arithmetic is floating point, but no spectral or quadrature
    truncation is made.  If the polynomial degree is ``d``, an extent of
    ``size + d`` prevents paths in the three-term recurrence from reflecting
    off the artificial Jacobi boundary before the requested compression is
    taken.
    """

    vector = np.asarray(coefficients, dtype=float)
    if size < 1 or vector.ndim != 1 or len(vector) < 1:
        raise ValueError("require a positive size and a coefficient vector")
    nonzero = np.flatnonzero(vector)
    degree = int(nonzero[-1]) if len(nonzero) else 0
    extent = size + degree + 1
    links = _jacobi_links(extent)
    identity = np.eye(extent)
    result = vector[0] * identity
    if degree == 0:
        return result[:size, :size]

    previous = identity
    current = _left_multiply_x(identity, links)
    if vector[1] != 0.0:
        result += vector[1] * current
    for index in range(1, degree):
        following = 2.0 * _left_multiply_x(current, links) - previous
        if vector[index + 1] != 0.0:
            result += vector[index + 1] * following
        previous, current = current, following
    compressed = result[:size, :size]
    return 0.5 * (compressed + compressed.T)


def chebyshev_multiplication_compression_gauss(
    coefficients: np.ndarray, size: int
) -> np.ndarray:
    """Polynomial-exact Gauss construction of the same compression.

    If ``p`` has degree ``d``, each matrix integrand has degree at most
    ``2(size-1)+d``.  A Gauss--Legendre rule of order
    ``size + ceil(d/2)`` is therefore exact in symbolic arithmetic.  This
    floating implementation is much faster than the enlarged Jacobi
    recurrence at large ``d`` and supplies an independent cross-check.
    """

    vector = np.asarray(coefficients, dtype=float)
    if size < 1 or vector.ndim != 1 or len(vector) < 1:
        raise ValueError("require a positive size and a coefficient vector")
    nonzero = np.flatnonzero(vector)
    degree = int(nonzero[-1]) if len(nonzero) else 0
    quadrature_order = size + (degree + 1) // 2
    nodes, weights = leggauss(quadrature_order)
    values = chebval(nodes, vector)
    basis = legvander(nodes, size - 1).T
    basis *= np.sqrt((2.0 * np.arange(size) + 1.0) / 2.0)[:, None]
    matrix = (basis * (weights * values)) @ basis.T
    return 0.5 * (matrix + matrix.T)


def gauss_stieltjes_lower_matrix(
    size: int,
    quadrature_order: int = 8,
    chebyshev_order: int = 64,
    method: str = "gauss",
) -> tuple[np.ndarray, StieltjesPolynomial]:
    """Return the finite Legendre compression and its lower-bound metadata."""

    polynomial = gauss_stieltjes_chebyshev(
        quadrature_order, chebyshev_order
    )
    if method == "gauss":
        matrix = chebyshev_multiplication_compression_gauss(
            polynomial.coefficients, size
        )
    elif method == "jacobi":
        matrix = chebyshev_multiplication_compression(
            polynomial.coefficients, size
        )
    else:
        raise ValueError("method must be 'gauss' or 'jacobi'")
    return matrix, polynomial


def taylor_lower_matrix(size: int, order: int) -> np.ndarray:
    """Compression of ``sum_{k=1}^order x^(2k)/(2k)``."""

    if order < 1:
        raise ValueError("Taylor order must be positive")
    extent = size + 2 * order + 1
    links = _jacobi_links(extent)
    power = np.eye(extent)
    result = np.zeros_like(power)
    for index in range(1, 2 * order + 1):
        power = _left_multiply_x(power, links)
        if index % 2 == 0:
            result += power / index
    compressed = result[:size, :size]
    return 0.5 * (compressed + compressed.T)


def harmonic(index: int) -> float:
    return math.fsum(1.0 / value for value in range(1, index + 1))


def endpoint_value(polynomial: StieltjesPolynomial) -> float:
    """Value of the lower polynomial at x=1."""

    return float(np.sum(polynomial.coefficients))


def gauss_stieltjes_rational_value(x: np.ndarray | float, order: int) -> np.ndarray:
    """Evaluate the untruncated Gauss--Stieltjes rational minorant."""

    if order < 1:
        raise ValueError("order must be positive")
    values = np.asarray(x, dtype=float)
    raw_nodes, raw_weights = leggauss(order)
    nodes = (raw_nodes + 1.0) / 2.0
    weights = raw_weights / 2.0
    square = values[..., None] ** 2
    return 0.5 * np.sum(weights * square / (1.0 - nodes * square), axis=-1)


def shifted_legendre_jacobi(size: int) -> np.ndarray:
    """Jacobi matrix of multiplication by t for uniform measure on [0,1]."""

    if size < 1:
        raise ValueError("size must be positive")
    matrix = 0.5 * np.eye(size)
    degrees = np.arange(size - 1, dtype=float)
    links = (degrees + 1.0) / (
        2.0 * np.sqrt((2.0 * degrees + 1.0) * (2.0 * degrees + 3.0))
    )
    matrix[np.arange(size - 1), np.arange(1, size)] = links
    matrix[np.arange(1, size), np.arange(size - 1)] = links
    return matrix


def gauss_stieltjes_jacobi_value(x: float, order: int) -> float:
    """Evaluate ``R_m`` through its finite Jacobi resolvent."""

    if not 0.0 < abs(x) < 1.0:
        raise ValueError("require 0 < |x| < 1")
    square = x * x
    matrix = np.eye(order) - square * shifted_legendre_jacobi(order)
    unit = np.zeros(order)
    unit[0] = 1.0
    return 0.5 * square * float(unit @ np.linalg.solve(matrix, unit))


def gauss_stieltjes_increment(x: float, order: int) -> float:
    """Schur-square formula for ``R_{m+1}(x) - R_m(x)``."""

    if order < 1 or not 0.0 < abs(x) < 1.0:
        raise ValueError("require positive order and 0 < |x| < 1")
    square = x * x
    jacobi = shifted_legendre_jacobi(order)
    block = np.eye(order) - square * jacobi
    first = np.zeros(order)
    first[0] = 1.0
    last = np.zeros(order)
    last[-1] = 1.0
    inverse_first = np.linalg.solve(block, first)
    inverse_last = np.linalg.solve(block, last)
    link = order / (2.0 * math.sqrt((2 * order - 1) * (2 * order + 1)))
    schur = (
        1.0
        - 0.5 * square
        - square**2 * link**2 * float(last @ inverse_last)
    )
    if not schur > 0.0:
        raise ArithmeticError("the finite resolvent Schur complement was not positive")
    cross = float(last @ inverse_first)
    return 0.5 * square**3 * link**2 * cross**2 / schur


def markov_remainder_value(
    x: np.ndarray | float, order: int, integration_order: int = 256
) -> np.ndarray:
    """Evaluate the exact Markov representation of ``V - R_m``.

    The shifted Legendre polynomial need not be made monic: its scale cancels
    between numerator and denominator.  This routine is a numerical audit of
    the displayed identity, not an interval proof.
    """

    if order < 1 or integration_order < order + 1:
        raise ValueError("require positive order and a larger integration rule")
    values = np.asarray(x, dtype=float)
    if np.any(np.abs(values) <= 0.0) or np.any(np.abs(values) >= 1.0):
        raise ValueError("the direct Markov evaluation requires 0 < |x| < 1")
    nodes, weights = leggauss(integration_order)
    t = (nodes + 1.0) / 2.0
    weights = weights / 2.0
    shifted = Legendre.basis(order)(2.0 * t - 1.0)
    z = 1.0 / values**2
    denominator = Legendre.basis(order)(2.0 * z - 1.0) ** 2
    integral = np.sum(
        weights * shifted**2 / (z[..., None] - t), axis=-1
    )
    return 0.5 * integral / denominator


def main() -> None:
    for order in (32, 64, 96, 128, 192, 256):
        data = gauss_stieltjes_chebyshev(8, order)
        print(
            f"m=8 J={order} epsilon={data.uniform_error:.17g} "
            f"endpoint={endpoint_value(data):.17g} H8={harmonic(8):.17g}"
        )
    sample = np.array([0.1, 0.4, 0.8, 0.97])
    direct = -0.5 * np.log1p(-sample**2) - gauss_stieltjes_rational_value(
        sample, 8
    )
    markov = markov_remainder_value(sample, 8)
    print("Markov max discrepancy", float(np.max(np.abs(direct - markov))))


if __name__ == "__main__":
    main()
