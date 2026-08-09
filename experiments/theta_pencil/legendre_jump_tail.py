"""Explicit Legendre tail budgets for internal jumps and smooth remainders."""

from __future__ import annotations

import math

import numpy as np
from scipy.special import eval_legendre

CERTIFIED_R4_BOUND = 1.0
MAX_CERTIFIED_R4_HALF_WIDTH = 0.4


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


def wang_normalized_coefficient_bound(
    variation: float, degree: int, derivative_order: int = 1
) -> float:
    """Wang's order-m bound converted to normalized Legendre coefficients."""
    if variation < 0.0:
        raise ValueError("variation must be nonnegative")
    if derivative_order < 0:
        raise ValueError("derivative_order must be nonnegative")
    if degree < derivative_order + 1:
        raise ValueError("degree must exceed derivative_order")
    product = math.prod(
        1.0 / (degree - offset + 0.5)
        for offset in range(1, derivative_order + 1)
    )
    return (
        math.sqrt(2.0 / (2 * degree + 1))
        * 2.0
        * variation
        / math.sqrt(math.pi * (2 * degree - 2 * derivative_order - 1))
        * product
    )


def wang_normalized_tail_bound(
    variation: float, first_degree: int, derivative_order: int = 1
) -> float:
    """Elementary l2 tail consequence of Wang's coefficient estimate."""
    if variation < 0.0:
        raise ValueError("variation must be nonnegative")
    if derivative_order < 0:
        raise ValueError("derivative_order must be nonnegative")
    if first_degree < max(3, 2 * derivative_order + 1):
        raise ValueError("first_degree is too small for the simplified tail bound")
    return (
        2.0 ** (derivative_order + 1)
        * variation
        / (
            math.sqrt(math.pi * (2 * derivative_order + 1))
            * (first_degree - 1.0) ** (derivative_order + 0.5)
        )
    )


def smooth_kernel_variation_bound(
    half_width: float, fourth_derivative_bound: float = CERTIFIED_R4_BOUND
) -> float:
    """Bound V_1 of the smooth-kernel image of a unit L2 vector.

    This uses the distributional cusp of r'' at zero and assumes
    |r''''(t)| <= ``fourth_derivative_bound`` for |t| <= 2a.
    """
    if half_width <= 0.0:
        raise ValueError("half_width must be positive")
    if (
        fourth_derivative_bound == CERTIFIED_R4_BOUND
        and half_width > MAX_CERTIFIED_R4_HALF_WIDTH
    ):
        raise ValueError("the certified unit r'''' bound applies only for a <= 0.4")
    if fourth_derivative_bound < 0.0:
        raise ValueError("fourth_derivative_bound must be nonnegative")
    weighted_l1 = (
        math.sqrt(math.pi)
        * math.gamma(0.75)
        / math.gamma(1.25)
    )
    return (
        half_width**2 * math.sqrt(math.pi) / 24.0
        + half_width**3
        * fourth_derivative_bound
        * math.sqrt(2.0)
        * weighted_l1
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


def potential_operator_tail_bound(
    degrees: np.ndarray, first_degree: int, expansion_order: int = 2
) -> float:
    """Uniform version of ``potential_tail_bound`` on a coordinate block."""
    selected = np.asarray(degrees, dtype=float)
    if len(selected) < 1:
        raise ValueError("degrees must be nonempty")
    if first_degree <= int(selected[-1]):
        raise ValueError("first_degree must exceed every selected degree")
    if expansion_order < 1:
        raise ValueError("expansion_order must be positive")
    eigenvalues = selected * (selected + 1.0)
    weights = np.sqrt(2.0 * selected + 1.0)
    bound = 0.0
    for order in range(expansion_order):
        moment_norm = float(np.linalg.norm(weights * eigenvalues**order))
        bound += (
            math.sqrt(3.0)
            * moment_norm
            / math.sqrt(4.0 * order + 2.0)
            * (first_degree - 1.0) ** (-(2.0 * order + 1.0))
        )
    largest = float(eigenvalues[-1])
    ratio = largest / (first_degree * first_degree)
    remainder_norm = float(
        np.linalg.norm(weights * eigenvalues**expansion_order)
    )
    order = expansion_order
    bound += (
        math.sqrt(3.0)
        * remainder_norm
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
