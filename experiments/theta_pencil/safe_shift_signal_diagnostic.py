"""Separate universal and arithmetic terms under the explicit safe shift."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

import numpy as np

from experiments.theta_pencil.finite_weyl_ratio import (
    audit_component_channel_response,
    canonical_weyl_from_channels,
    large_negative_shift_channel_expansion,
)
from experiments.theta_pencil.safe_weil_shift import explicit_safe_shift
from experiments.theta_pencil.semilocal_weil_matrix import _simpson_weights
from experiments.theta_pencil.screw_weil_operator import (
    build_screw_weil_components,
    dirichlet_basis,
)


@dataclass(frozen=True)
class SafeShiftSignalRow:
    half_width: float
    shift: float
    exact_canonical_real: float
    exact_canonical_imag: float
    universal_real: float
    universal_imag: float
    first_approximation_error: float
    second_approximation_error: float
    total_first_coefficient_abs: float
    total_first_coefficient_real: float
    total_first_coefficient_imag: float
    polar_first_coefficient_abs: float
    polar_first_coefficient_real: float
    polar_first_coefficient_imag: float
    archimedean_first_coefficient_abs: float
    archimedean_first_coefficient_real: float
    archimedean_first_coefficient_imag: float
    prime_first_coefficient_abs: float
    prime_first_coefficient_real: float
    prime_first_coefficient_imag: float
    coefficient_additivity_residual: float
    component_cancellation_ratio: float
    scaled_total_signal_abs: float
    scaled_prime_signal_abs: float
    total_second_coefficient_abs: float
    scaled_total_second_signal_abs: float
    scaled_prime_sensitive_second_signal_abs: float
    exact_no_prime_canonical_real: float
    exact_no_prime_canonical_imag: float
    exact_arithmetic_weyl_difference_abs: float
    exact_arithmetic_characteristic_difference_abs: float
    exact_projective_numerator_abs: float
    exact_component_identity_residual: float
    exact_completed_weyl_difference_abs: float
    exact_completed_characteristic_difference_abs: float
    exact_completed_projective_numerator_abs: float
    exact_completed_identity_residual: float


def safe_shift_signal_row(
    half_width: float,
    grid_points: int = 4097,
    basis_size: int = 32,
    z: complex = 0.7 + 0.8j,
) -> SafeShiftSignalRow:
    """Compute the first operator-sensitive coefficient at one support."""

    components = build_screw_weil_components(
        half_width, grid_points, basis_size, "dirichlet"
    )
    gram = components.gram
    operator = components.polar - components.archimedean - components.prime
    coordinate = np.linspace(-half_width, half_width, grid_points)
    spacing = float(coordinate[1] - coordinate[0])
    weights = _simpson_weights(grid_points - 1) * (spacing / 3.0)
    basis = dirichlet_basis(coordinate, half_width, basis_size)
    plus = basis @ (weights * np.exp(coordinate))
    minus = basis @ (weights * np.exp(-coordinate))
    observation = basis @ (weights * np.exp(1j * z * coordinate))

    shift = explicit_safe_shift(half_width)
    scale = -shift
    pencil = operator + scale * gram
    plus_value = complex(observation @ np.linalg.solve(pencil, plus))
    minus_value = complex(observation @ np.linalg.solve(pencil, minus))
    exact = canonical_weyl_from_channels(plus_value, minus_value, z)
    component_response = audit_component_channel_response(
        components.polar - components.archimedean,
        -components.prime,
        plus,
        minus,
        observation,
        shift,
        z,
        metric=gram,
    )
    completed_response = audit_component_channel_response(
        np.zeros_like(operator),
        operator,
        plus,
        minus,
        observation,
        shift,
        z,
        metric=gram,
    )
    exact_no_prime = exact - component_response.canonical_weyl_difference

    def expansion(matrix: np.ndarray):
        return large_negative_shift_channel_expansion(
            matrix, plus, minus, observation, z, metric=gram
        )

    total = expansion(operator)
    polar = expansion(components.polar)
    archimedean = expansion(-components.archimedean)
    prime = expansion(-components.prime)
    without_prime = expansion(components.polar - components.archimedean)
    component_sum = (
        polar.canonical_first_coefficient
        + archimedean.canonical_first_coefficient
        + prime.canonical_first_coefficient
    )
    approximation = total.canonical_leading + total.canonical_first_coefficient / scale
    second_approximation = (
        approximation + total.canonical_second_coefficient / scale**2
    )
    return SafeShiftSignalRow(
        half_width=half_width,
        shift=shift,
        exact_canonical_real=float(exact.real),
        exact_canonical_imag=float(exact.imag),
        universal_real=float(total.canonical_leading.real),
        universal_imag=float(total.canonical_leading.imag),
        first_approximation_error=float(abs(exact - approximation)),
        second_approximation_error=float(abs(exact - second_approximation)),
        total_first_coefficient_abs=float(abs(total.canonical_first_coefficient)),
        total_first_coefficient_real=float(total.canonical_first_coefficient.real),
        total_first_coefficient_imag=float(total.canonical_first_coefficient.imag),
        polar_first_coefficient_abs=float(abs(polar.canonical_first_coefficient)),
        polar_first_coefficient_real=float(polar.canonical_first_coefficient.real),
        polar_first_coefficient_imag=float(polar.canonical_first_coefficient.imag),
        archimedean_first_coefficient_abs=float(
            abs(archimedean.canonical_first_coefficient)
        ),
        archimedean_first_coefficient_real=float(
            archimedean.canonical_first_coefficient.real
        ),
        archimedean_first_coefficient_imag=float(
            archimedean.canonical_first_coefficient.imag
        ),
        prime_first_coefficient_abs=float(abs(prime.canonical_first_coefficient)),
        prime_first_coefficient_real=float(prime.canonical_first_coefficient.real),
        prime_first_coefficient_imag=float(prime.canonical_first_coefficient.imag),
        coefficient_additivity_residual=float(
            abs(total.canonical_first_coefficient - component_sum)
        ),
        component_cancellation_ratio=float(
            abs(total.canonical_first_coefficient)
            / (
                abs(polar.canonical_first_coefficient)
                + abs(archimedean.canonical_first_coefficient)
                + abs(prime.canonical_first_coefficient)
            )
        ),
        scaled_total_signal_abs=float(
            abs(total.canonical_first_coefficient) / scale
        ),
        scaled_prime_signal_abs=float(
            abs(prime.canonical_first_coefficient) / scale
        ),
        total_second_coefficient_abs=float(
            abs(total.canonical_second_coefficient)
        ),
        scaled_total_second_signal_abs=float(
            abs(total.canonical_second_coefficient) / scale**2
        ),
        scaled_prime_sensitive_second_signal_abs=float(
            abs(
                total.canonical_second_coefficient
                - without_prime.canonical_second_coefficient
            )
            / scale**2
        ),
        exact_no_prime_canonical_real=float(exact_no_prime.real),
        exact_no_prime_canonical_imag=float(exact_no_prime.imag),
        exact_arithmetic_weyl_difference_abs=float(
            abs(component_response.canonical_weyl_difference)
        ),
        exact_arithmetic_characteristic_difference_abs=float(
            abs(component_response.characteristic_difference)
        ),
        exact_projective_numerator_abs=float(
            abs(component_response.projective_numerator)
        ),
        exact_component_identity_residual=float(
            component_response.resolvent_identity_residual
        ),
        exact_completed_weyl_difference_abs=float(
            abs(completed_response.canonical_weyl_difference)
        ),
        exact_completed_characteristic_difference_abs=float(
            abs(completed_response.characteristic_difference)
        ),
        exact_completed_projective_numerator_abs=float(
            abs(completed_response.projective_numerator)
        ),
        exact_completed_identity_residual=float(
            completed_response.resolvent_identity_residual
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--supports", type=float, nargs="+", default=(0.4, 0.72, 1.5, 3.0))
    parser.add_argument("--grid", type=int, default=4097)
    parser.add_argument("--basis", type=int, default=32)
    parser.add_argument("--z-real", type=float, default=0.7)
    parser.add_argument("--z-imag", type=float, default=0.8)
    args = parser.parse_args()
    rows = [
        safe_shift_signal_row(
            support,
            grid_points=args.grid,
            basis_size=args.basis,
            z=complex(args.z_real, args.z_imag),
        )
        for support in args.supports
    ]
    print(json.dumps([asdict(row) for row in rows], indent=2))


if __name__ == "__main__":
    main()
