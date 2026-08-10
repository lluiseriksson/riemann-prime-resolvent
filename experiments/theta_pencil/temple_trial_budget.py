"""A posteriori Kato--Temple budget for an explicit Legendre trial vector."""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, field

import numpy as np
from numpy.polynomial.legendre import legder, leggauss, legval
from scipy.linalg import eigh, null_space

from experiments.theta_pencil.legendre_feshbach import (
    build_legendre_weil_components,
    normalized_legendre_values,
)
from experiments.theta_pencil.legendre_jump_tail import (
    bernstein_jump_tail_bound,
    potential_tail_bound,
    temple_lower_bound,
    wang_normalized_tail_bound,
)
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_matrix,
    smooth_kernel_series_remainder_bound,
)
from experiments.theta_pencil.screw_weil_operator import von_mangoldt


@dataclass(frozen=True)
class TempleTrialAudit:
    half_width: float
    trial_parity: int
    trial_dimension: int
    residual_end: int
    rayleigh: float
    low_residual: float
    finite_high_residual: float
    jump_tail: float
    prime_remainder_tail: float
    potential_tail: float
    smooth_tail: float
    total_residual_bound: float
    second_floor: float
    temple_lower: float
    endpoint_value: float
    prime_remainder_variation: float
    endpoint_constraints: int
    coefficients: np.ndarray = field(repr=False)


def _legendre_transform_on_interval(
    nodes: np.ndarray,
    weighted_values: np.ndarray,
    maximum_degree: int,
) -> np.ndarray:
    """Legendre coefficients from a polynomial-exact quadrature functional."""
    result = np.empty(maximum_degree, dtype=float)
    previous = np.ones_like(nodes)
    result[0] = math.sqrt(0.5) * float(np.dot(weighted_values, previous))
    if maximum_degree == 1:
        return result
    current = nodes.copy()
    result[1] = math.sqrt(1.5) * float(np.dot(weighted_values, current))
    for degree in range(1, maximum_degree - 1):
        following = (
            (2 * degree + 1) * nodes * current - degree * previous
        ) / (degree + 1)
        result[degree + 1] = math.sqrt((2 * degree + 3) / 2.0) * float(
            np.dot(weighted_values, following)
        )
        previous, current = current, following
    return result


def _prime_coefficients_for_trial(
    half_width: float,
    coefficients: np.ndarray,
    maximum_degree: int,
    prime_power: int = 2,
) -> np.ndarray:
    dimension = len(coefficients)
    weight = von_mangoldt(prime_power) / math.sqrt(prime_power)
    if weight == 0.0:
        raise ValueError("prime_power must be a prime power")
    shift = math.log(prime_power) / half_width
    cut = 1.0 - shift
    order = (maximum_degree + dimension + 2) // 2 + 2
    nodes, weights = leggauss(order)

    def one_interval(left: float, right: float, source_shift: float) -> np.ndarray:
        x = (right - left) * nodes / 2.0 + (right + left) / 2.0
        scaled_weights = weights * (right - left) / 2.0
        trial = coefficients @ normalized_legendre_values(
            x + source_shift, dimension
        )
        return _legendre_transform_on_interval(
            x, scaled_weights * trial, maximum_degree
        )

    return -weight * (
        one_interval(-1.0, cut, shift)
        + one_interval(-cut, 1.0, -shift)
    )


def _potential_coefficients_for_trial(
    coefficients: np.ndarray, maximum_degree: int
) -> np.ndarray:
    dimension = len(coefficients)
    degrees = np.arange(dimension)
    weighted = coefficients * np.sqrt(2.0 * degrees + 1.0)
    eigenvalues = degrees * (degrees + 1.0)
    result = np.zeros(maximum_degree, dtype=float)
    for parity in (0, 1):
        low = np.arange(parity, dimension, 2)
        high = np.arange(dimension + ((dimension - parity) % 2), maximum_degree, 2)
        if len(high) == 0:
            continue
        denominators = high[:, None] * (high[:, None] + 1.0) - eigenvalues[low]
        result[high] = np.sqrt(2.0 * high + 1.0) * (
            (1.0 / denominators) @ weighted[low]
        )
    return result


def _prime_remainder_variation(
    half_width: float,
    coefficients: np.ndarray,
    quadrature_order: int = 3000,
    prime_power: int = 2,
    derivative_order: int = 1,
) -> float:
    """Weighted variation after retaining ``derivative_order`` endpoint jets."""
    if derivative_order < 1:
        raise ValueError("derivative_order must be positive")
    polynomial = coefficients * np.sqrt(
        (2.0 * np.arange(len(coefficients)) + 1.0) / 2.0
    )
    retained_derivative = polynomial
    for _ in range(derivative_order):
        retained_derivative = legder(retained_derivative)
    remainder_derivative = legder(retained_derivative)
    weight = von_mangoldt(prime_power) / math.sqrt(prime_power)
    if weight == 0.0:
        raise ValueError("prime_power must be a prime power")
    shift = math.log(prime_power) / half_width
    cut = 1.0 - shift
    nodes, weights = leggauss(quadrature_order)
    x = (cut + 1.0) * nodes / 2.0 + (cut - 1.0) / 2.0
    scaled_weights = weights * (cut + 1.0) / 2.0
    integral = float(
        np.dot(
            scaled_weights,
            np.abs(legval(x + shift, remainder_derivative))
            / (1.0 - x * x) ** 0.25,
        )
    )
    return 2.0 * weight * (
        integral
        + abs(float(legval(1.0, retained_derivative)))
        / (1.0 - cut * cut) ** 0.25
    )


def run_temple_trial_audit(
    half_width: float = 0.4,
    trial_dimension: int = 512,
    residual_end: int = 8192,
    second_floor: float = 0.005,
    trial_parity: int = 0,
    endpoint_constraints: int = 0,
    prime_jet_count: int = 1,
) -> TempleTrialAudit:
    if trial_parity not in (0, 1):
        raise ValueError("trial_parity must be zero or one")
    selected = np.arange(trial_parity, trial_dimension, 2)
    if endpoint_constraints < 0 or endpoint_constraints >= len(selected):
        raise ValueError("endpoint_constraints must fit the parity subspace")
    if prime_jet_count < 1 or prime_jet_count >= trial_dimension:
        raise ValueError("prime_jet_count must lie below trial_dimension")
    components = build_legendre_weil_components(
        half_width, trial_dimension, max(1400, 2 * trial_dimension)
    )
    matrix = (
        components.dominant
        + components.scalar
        + components.prime
        + smooth_kernel_series_matrix(half_width, trial_dimension, 23)
    )
    parity_matrix = matrix[np.ix_(selected, selected)]
    if endpoint_constraints:
        constraint_rows = []
        for derivative_order in range(endpoint_constraints):
            row = np.sqrt((2.0 * selected + 1.0) / 2.0)
            for factor in range(derivative_order):
                row *= (
                    (selected - factor) * (selected + factor + 1)
                    / (2 * (factor + 1))
                )
            row /= np.linalg.norm(row)
            constraint_rows.append(row)
        constraint_kernel = null_space(np.asarray(constraint_rows))
        _, reduced_vector = eigh(
            constraint_kernel.T @ parity_matrix @ constraint_kernel,
            subset_by_index=[0, 0],
        )
        eigenvector = constraint_kernel @ reduced_vector
    else:
        _, eigenvector = eigh(parity_matrix, subset_by_index=[0, 0])
    coefficients = np.zeros(trial_dimension)
    coefficients[selected] = eigenvector[:, 0]
    center = coefficients @ normalized_legendre_values(
        np.array([0.0]), trial_dimension
    )[:, 0]
    if center < 0.0:
        coefficients = -coefficients
    rayleigh = float(coefficients @ matrix @ coefficients)
    low_residual = float(np.linalg.norm(matrix @ coefficients - rayleigh * coefficients))

    prime = sum(
        (
            _prime_coefficients_for_trial(
                half_width, coefficients, residual_end, prime_power
            )
            for prime_power in components.active_prime_powers
        ),
        np.zeros(residual_end),
    )
    potential = _potential_coefficients_for_trial(coefficients, residual_end)
    smooth_power = 23
    smooth_extent = min(residual_end, trial_dimension + smooth_power + 2)
    padded = np.zeros(smooth_extent)
    padded[:trial_dimension] = coefficients
    smooth_action = (
        smooth_kernel_series_matrix(half_width, smooth_extent, smooth_power)
        @ padded
    )
    finite_vector = prime + potential
    finite_vector[trial_dimension:smooth_extent] += smooth_action[
        trial_dimension:smooth_extent
    ]
    finite_high = float(
        np.linalg.norm(finite_vector[trial_dimension:residual_end])
    )

    polynomial = coefficients * np.sqrt(
        (2.0 * np.arange(trial_dimension) + 1.0) / 2.0
    )
    endpoint = float(legval(1.0, polynomial))
    endpoint_jets = []
    derivative = polynomial
    for jet in range(prime_jet_count):
        endpoint_jets.append(
            float(legval(1.0, derivative)) / math.factorial(jet)
        )
        derivative = legder(derivative)
    jump_terms = []
    for prime_power in components.active_prime_powers:
        weight = von_mangoldt(prime_power) / math.sqrt(prime_power)
        cut = 1.0 - math.log(prime_power) / half_width
        cut_weight = (1.0 - cut * cut) ** 0.25
        jump_terms.append(
            2.0
            * weight
            * abs(endpoint_jets[0])
            * bernstein_jump_tail_bound(1.0, cut_weight, residual_end)
        )
        for jet in range(1, prime_jet_count):
            scalar_tail = wang_normalized_tail_bound(
                math.factorial(jet) / cut_weight,
                residual_end,
                jet,
            )
            jump_terms.append(
                2.0 * weight * abs(endpoint_jets[jet]) * scalar_tail
            )
    jump_tail = math.fsum(jump_terms)
    variation = math.fsum(
        _prime_remainder_variation(
            half_width,
            coefficients,
            prime_power=prime_power,
            derivative_order=prime_jet_count,
        )
        for prime_power in components.active_prime_powers
    )
    prime_remainder_tail = wang_normalized_tail_bound(
        variation, residual_end, prime_jet_count
    )
    potential_tail = potential_tail_bound(coefficients, residual_end, 2)
    smooth_tail = 2.0 * smooth_kernel_series_remainder_bound(
        half_width, smooth_power
    )
    prime_potential_tail = jump_tail + prime_remainder_tail + potential_tail
    prime_potential_high = math.hypot(finite_high, prime_potential_tail)
    total = math.hypot(
        low_residual,
        prime_potential_high + smooth_tail,
    )
    lower = temple_lower_bound(rayleigh, total, second_floor)
    return TempleTrialAudit(
        half_width=half_width,
        trial_parity=trial_parity,
        trial_dimension=trial_dimension,
        residual_end=residual_end,
        rayleigh=rayleigh,
        low_residual=low_residual,
        finite_high_residual=finite_high,
        jump_tail=jump_tail,
        prime_remainder_tail=prime_remainder_tail,
        potential_tail=potential_tail,
        smooth_tail=smooth_tail,
        total_residual_bound=total,
        second_floor=second_floor,
        temple_lower=lower,
        endpoint_value=endpoint,
        prime_remainder_variation=variation,
        endpoint_constraints=endpoint_constraints,
        coefficients=coefficients,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, default=512)
    parser.add_argument("--residual-end", type=int, default=8192)
    args = parser.parse_args()
    result = run_temple_trial_audit(
        trial_dimension=args.dimension, residual_end=args.residual_end
    )
    print(result)


if __name__ == "__main__":
    main()
