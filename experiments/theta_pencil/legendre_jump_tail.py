"""Explicit Legendre tail budgets for internal jumps and smooth remainders."""

from __future__ import annotations

import math

import numpy as np
from scipy.special import eval_legendre


def normalized_step_coefficient(cut: float, degree: int) -> float:
    """Coefficient of 1_{[-1, cut]} in the normalized Legendre basis."""
    if not -1.0 < cut < 1.0:
        raise ValueError("cut must lie strictly inside (-1, 1)")
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    if degree == 0:
        return (cut + 1.0) / math.sqrt(2.0)
    normalization = math.sqrt((2 * degree + 1) / 2.0)
    return normalization * (
        eval_legendre(degree + 1, cut) - eval_legendre(degree - 1, cut)
    ) / (2 * degree + 1)


def bernstein_jump_tail_bound(
    jump_total: float, minimum_cut_weight: float, first_degree: int
) -> float:
    """L2 tail bound for finitely many jumps.

    ``jump_total`` is the sum of absolute jump sizes and
    ``minimum_cut_weight`` is min (1-c_j^2)^(1/4).  The estimate combines the
    exact antiderivative of P_n with the sharp Bernstein inequality and
    sum_{n>=N} n^-2 <= 1/(N-1).
    """
    if jump_total < 0.0:
        raise ValueError("jump_total must be nonnegative")
    if minimum_cut_weight <= 0.0:
        raise ValueError("minimum_cut_weight must be positive")
    if first_degree < 2:
        raise ValueError("first_degree must be at least two")
    constant = math.sqrt(8.0 / (3.0 * math.pi))
    return (
        constant
        * jump_total
        / (minimum_cut_weight * math.sqrt(first_degree - 1.0))
    )


def wang_normalized_coefficient_bound(variation: float, degree: int) -> float:
    """Wang's m=1 bound converted to normalized Legendre coefficients."""
    if variation < 0.0:
        raise ValueError("variation must be nonnegative")
    if degree < 2:
        raise ValueError("degree must be at least two")
    return (
        math.sqrt(2.0 / (2 * degree + 1))
        * 2.0
        * variation
        / (
            math.sqrt(math.pi * (2 * degree - 3))
            * (degree - 0.5)
        )
    )


def wang_normalized_tail_bound(variation: float, first_degree: int) -> float:
    """Elementary l2 tail consequence of Wang's coefficient estimate."""
    if variation < 0.0:
        raise ValueError("variation must be nonnegative")
    if first_degree < 3:
        raise ValueError("first_degree must be at least three")
    return (
        4.0
        * variation
        / (math.sqrt(3.0 * math.pi) * (first_degree - 1.0) ** 1.5)
    )


def potential_tail_bound(
    coefficients: np.ndarray, first_degree: int, expansion_order: int = 2
) -> float:
    """Bound the Legendre tail of -(1/2)log(1-x^2) times a polynomial.

    The exact off-diagonal denominator is
    n(n+1)-m(m+1).  Expanding its reciprocal isolates signed endpoint moments;
    the final term is bounded absolutely.  ``coefficients`` are coordinates in
    the normalized Legendre basis and all omitted degrees must exceed them.
    """
    vector = np.asarray(coefficients, dtype=float)
    dimension = len(vector)
    if dimension < 1:
        raise ValueError("coefficients must be nonempty")
    if first_degree < max(2, dimension):
        raise ValueError("first_degree must be at least the polynomial dimension")
    if expansion_order < 1:
        raise ValueError("expansion_order must be positive")

    degrees = np.arange(dimension, dtype=float)
    eigenvalues = degrees * (degrees + 1.0)
    weighted = vector * np.sqrt(2.0 * degrees + 1.0)
    bound = 0.0
    for order in range(expansion_order):
        moment = abs(math.fsum((weighted * eigenvalues**order).tolist()))
        bound += (
            math.sqrt(3.0)
            * moment
            / math.sqrt(4.0 * order + 2.0)
            * (first_degree - 1.0) ** (-(2.0 * order + 1.0))
        )

    largest = float(eigenvalues[-1])
    ratio = largest / (first_degree * first_degree)
    absolute_moment = math.fsum(
        (np.abs(weighted) * eigenvalues**expansion_order).tolist()
    )
    order = expansion_order
    bound += (
        math.sqrt(3.0)
        * absolute_moment
        / (1.0 - ratio)
        / math.sqrt(4.0 * order + 2.0)
        * (first_degree - 1.0) ** (-(2.0 * order + 1.0))
    )
    return bound


def temple_lower_bound(rayleigh: float, residual: float, second_floor: float) -> float:
    """Kato--Temple lower bound assuming the next spectral point is >= floor."""
    if residual < 0.0:
        raise ValueError("residual must be nonnegative")
    if second_floor <= rayleigh:
        raise ValueError("second_floor must exceed the Rayleigh quotient")
    return rayleigh - residual * residual / (second_floor - rayleigh)

