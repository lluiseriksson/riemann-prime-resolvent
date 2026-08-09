"""Finite-rank endpoint-jet model for a truncated prime translation."""

from __future__ import annotations

import math

import numpy as np
from numpy.polynomial.legendre import legder, leggauss, legval
from scipy.special import digamma, gammaln, roots_jacobi

from experiments.theta_pencil.semilocal_weil_matrix import EULER_GAMMA
from experiments.theta_pencil.legendre_jump_tail import (
    bernstein_jump_tail_bound,
    wang_normalized_tail_bound,
)


def left_step_coefficients(cut: float, maximum_degree: int) -> np.ndarray:
    """Normalized Legendre coefficients of 1_{[-1, cut]} by recurrence."""
    if not -1.0 < cut < 1.0:
        raise ValueError("cut must lie inside (-1, 1)")
    if maximum_degree < 1:
        raise ValueError("maximum_degree must be positive")
    values = np.empty(maximum_degree + 2, dtype=float)
    values[0] = 1.0
    values[1] = cut
    for degree in range(1, maximum_degree + 1):
        values[degree + 1] = (
            (2 * degree + 1) * cut * values[degree]
            - degree * values[degree - 1]
        ) / (degree + 1)
    result = np.empty(maximum_degree, dtype=float)
    result[0] = (cut + 1.0) / math.sqrt(2.0)
    degrees = np.arange(1, maximum_degree)
    result[1:] = (
        np.sqrt((2 * degrees + 1) / 2.0)
        * (values[degrees + 1] - values[degrees - 1])
        / (2 * degrees + 1)
    )
    return result


def multiply_legendre_coefficients_by_x(coefficients: np.ndarray) -> np.ndarray:
    """Apply the orthonormal Legendre Jacobi matrix to coefficients."""
    vector = np.asarray(coefficients, dtype=float)
    result = np.zeros_like(vector)
    degrees = np.arange(len(vector) - 1)
    links = (degrees + 1.0) / np.sqrt(
        (2.0 * degrees + 1.0) * (2.0 * degrees + 3.0)
    )
    result[:-1] += links * vector[1:]
    result[1:] += links * vector[:-1]
    return result


def truncated_power_coefficients(
    cut: float, maximum_degree: int, jet_count: int
) -> np.ndarray:
    """Rows are coefficients of (x-cut)^j 1_{[-1,cut]}, 0 <= j < J."""
    if jet_count < 1:
        raise ValueError("jet_count must be positive")
    padded_degree = maximum_degree + jet_count
    rows = [left_step_coefficients(cut, padded_degree)]
    degrees = np.arange(1, padded_degree - 1)
    normalizations = np.sqrt((2.0 * np.arange(padded_degree) + 1.0) / 2.0)
    for jet in range(1, jet_count):
        previous = rows[-1]
        following = np.zeros_like(previous)
        # From (2n+1)P_n=P'_{n+1}-P'_{n-1}, integration by parts gives
        # p_{j,n}=-j*N_n/(2n+1)*(p_{j-1,n+1}/N_{n+1}
        #                         -p_{j-1,n-1}/N_{n-1}).
        # Unlike repeated application of X-cut, this form does not lose the
        # high-mode jets to cancellation.
        following[1:-1] = (
            -jet
            * normalizations[1:-1]
            / (2.0 * degrees + 1.0)
            * (
                previous[2:] / normalizations[2:]
                - previous[:-2] / normalizations[:-2]
            )
        )
        following[0] = -(-1.0 - cut) ** (jet + 1) / (
            (jet + 1) * math.sqrt(2.0)
        )
        rows.append(following)
    return np.asarray(rows)[:, :maximum_degree]


def endpoint_jet_matrix(degrees: np.ndarray, jet_count: int) -> np.ndarray:
    """Columns are e_m^(j)(1)/j! for normalized Legendre e_m."""
    degrees = np.asarray(degrees, dtype=int)
    result = np.zeros((len(degrees), jet_count), dtype=float)
    for jet in range(jet_count):
        active = degrees >= jet
        selected = degrees[active]
        result[active, jet] = np.sqrt((2.0 * selected + 1.0) / 2.0) * np.exp(
            gammaln(selected + jet + 1.0)
            - gammaln(selected - jet + 1.0)
            - jet * math.log(2.0)
            - 2.0 * gammaln(jet + 1.0)
        )
    return result


def prime_jet_cross_matrix(
    half_width: float,
    low_degrees: np.ndarray,
    high_degrees: np.ndarray,
    jet_count: int,
) -> np.ndarray:
    """Endpoint-jet part of the prime-2 cross matrix in one parity block."""
    low = np.asarray(low_degrees, dtype=int)
    high = np.asarray(high_degrees, dtype=int)
    if len(high) == 0:
        return np.zeros((len(low), 0))
    if np.any((low[:, None] + high[None, :]) % 2):
        raise ValueError("low and high degrees must belong to the same parity block")
    cut = 1.0 - math.log(2.0) / half_width
    powers = truncated_power_coefficients(cut, int(high[-1]) + 1, jet_count)
    endpoint = endpoint_jet_matrix(low, jet_count)
    coefficient = -2.0 * math.log(2.0) / math.sqrt(2.0)
    return coefficient * endpoint @ powers[:, high]


def prime_jet_weighted_correction(
    half_width: float,
    low_degrees: np.ndarray,
    first_degree: int,
    last_degree: int,
    jet_count: int,
    perturbation_loss: float,
    spectral_shift: float = 0.0,
) -> np.ndarray:
    """Accumulate J D^-1 J* for endpoint jets over a finite degree range."""
    low = np.asarray(low_degrees, dtype=int)
    parity = int(low[0] % 2)
    high = np.arange(first_degree + ((first_degree - parity) % 2), last_degree, 2)
    cross = prime_jet_cross_matrix(half_width, low, high, jet_count)
    denominators = (
        digamma(high + 1.0)
        + EULER_GAMMA
        - perturbation_loss
        - spectral_shift
    )
    return (cross / denominators) @ cross.T


def prime_remainder_variation_bound(
    half_width: float,
    low_degrees: np.ndarray,
    derivative_order: int,
    quadrature_order: int | None = None,
) -> float:
    """Cauchy--Schwarz bound for V_m after retaining m endpoint jets.

    The only numerical integration is a Gauss--Jacobi rule applied to a
    polynomial of known degree, so it is exact in exact arithmetic.  The
    remaining algebraic factor is replaced by its endpoint maximum.
    """
    low = np.asarray(low_degrees, dtype=int)
    if len(low) < 1:
        raise ValueError("low_degrees must be nonempty")
    if derivative_order < 1:
        raise ValueError("derivative_order must be positive")
    shift = math.log(2.0) / half_width
    length = 2.0 - shift
    if not 0.0 < length < 2.0:
        raise ValueError("the prime-2 overlap must be nonempty and proper")
    inner_endpoint = shift - 1.0
    cut = 1.0 - shift
    order = quadrature_order or max(64, int(low[-1]) + 2)
    nodes, weights = roots_jacobi(order, 0.0, -0.25)
    y = (nodes + 1.0) / 2.0
    weighted_rule = weights * 2.0 ** (-0.75)
    evaluation_points = inner_endpoint + length * y

    derivative_values = []
    for degree in low:
        coefficients = np.zeros(degree + 1)
        coefficients[degree] = math.sqrt((2 * degree + 1) / 2.0)
        derivative_values.append(
            legval(
                evaluation_points,
                legder(coefficients, derivative_order + 1),
            )
        )
    squared_norm = np.sum(np.asarray(derivative_values) ** 2, axis=0)
    scale = (
        length**0.75
        * 2.0 ** (-0.25)
        * (1.0 - length / 2.0) ** (-0.25)
    )
    weighted_l1 = math.sqrt(math.pi) * math.gamma(0.75) / math.gamma(1.25)
    integral_bound = math.sqrt(
        weighted_l1 * scale * float(np.dot(weighted_rule, squared_norm))
    )

    endpoint = endpoint_jet_matrix(low, derivative_order + 1)[
        :, derivative_order
    ] * math.factorial(derivative_order)
    cut_weight = (1.0 - cut * cut) ** 0.25
    prime_coefficient = math.log(2.0) / math.sqrt(2.0)
    return 2.0 * prime_coefficient * (
        integral_bound + float(np.linalg.norm(endpoint)) / cut_weight
    )


def prime_jet_tail_weighted_norm(
    half_width: float,
    low_degrees: np.ndarray,
    first_degree: int,
    jet_count: int,
    denominator_floor: float,
) -> float:
    """Weighted operator-norm tail for retained endpoint jets."""
    if denominator_floor <= 0.0:
        raise ValueError("denominator_floor must be positive")
    low = np.asarray(low_degrees, dtype=int)
    shift = math.log(2.0) / half_width
    cut = 1.0 - shift
    cut_weight = (1.0 - cut * cut) ** 0.25
    endpoint = endpoint_jet_matrix(low, jet_count)
    prime_coefficient = math.log(2.0) / math.sqrt(2.0)
    total = 0.0
    for jet in range(jet_count):
        if jet == 0:
            scalar_tail = bernstein_jump_tail_bound(
                1.0, cut_weight, first_degree
            )
        else:
            scalar_tail = wang_normalized_tail_bound(
                math.factorial(jet) / cut_weight,
                first_degree,
                jet,
            )
        total += (
            2.0
            * prime_coefficient
            * float(np.linalg.norm(endpoint[:, jet]))
            * scalar_tail
        )
    return total / math.sqrt(denominator_floor)


def piecewise_prime_remainder_variation_bound(
    half_width: float,
    low_degrees: np.ndarray,
    derivative_order: int,
    partitions: int = 128,
) -> float:
    """Sharper piecewise Cauchy bound for the same weighted variation.

    The substitution y=s^4 removes the endpoint singularity.  On each piece
    the remaining algebraic factor is replaced by its endpoint maximum, while
    Gauss--Legendre integrates the polynomial squared norm exactly in exact
    arithmetic.
    """
    low = np.asarray(low_degrees, dtype=int)
    if len(low) < 1:
        raise ValueError("low_degrees must be nonempty")
    if derivative_order < 1:
        raise ValueError("derivative_order must be positive")
    if partitions < 1:
        raise ValueError("partitions must be positive")
    shift = math.log(2.0) / half_width
    length = 2.0 - shift
    if not 0.0 < length < 2.0:
        raise ValueError("the prime-2 overlap must be nonempty and proper")
    inner_endpoint = shift - 1.0
    cut = 1.0 - shift
    polynomial_degree = max(0, int(low[-1]) - derivative_order - 1)
    gauss_order = max(8, 4 * polynomial_degree + 2)
    nodes, weights = leggauss(gauss_order)
    derivative_coefficients = []
    for degree in low:
        coefficients = np.zeros(degree + 1)
        coefficients[degree] = math.sqrt((2 * degree + 1) / 2.0)
        derivative_coefficients.append(
            legder(coefficients, derivative_order + 1)
        )

    base = length**0.75 * 2.0 ** (-0.25)
    q = length / 2.0
    integral_bound = 0.0
    for part in range(partitions):
        left = part / partitions
        right = (part + 1) / partitions
        s = (right - left) * nodes / 2.0 + (right + left) / 2.0
        scaled_weights = weights * (right - left) / 2.0
        points = inner_endpoint + length * s**4
        squared_norm = np.zeros_like(points)
        for coefficients in derivative_coefficients:
            squared_norm += legval(points, coefficients) ** 2
        algebraic_maximum = (1.0 - q * right**4) ** (-0.25)
        common = 4.0 * base * algebraic_maximum
        mass = common * (right**3 - left**3) / 3.0
        square_mass = common * float(
            np.dot(scaled_weights, s**2 * squared_norm)
        )
        integral_bound += math.sqrt(mass * square_mass)

    endpoint = endpoint_jet_matrix(low, derivative_order + 1)[
        :, derivative_order
    ] * math.factorial(derivative_order)
    cut_weight = (1.0 - cut * cut) ** 0.25
    prime_coefficient = math.log(2.0) / math.sqrt(2.0)
    return 2.0 * prime_coefficient * (
        integral_bound + float(np.linalg.norm(endpoint)) / cut_weight
    )
