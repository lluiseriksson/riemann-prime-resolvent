"""Galerkin diagnostic for the shift dependence of Suzuki's Weyl ratio.

This is a falsification instrument, not a certificate for the infinite
operator.  It uses the source-normalized localized Weil matrix and the exact
forcing equations ``(A_a-lambda) v_+ = exp(x)`` and
``(A_a-lambda) v_- = exp(-x)`` from Suzuki's deficiency construction.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

import numpy as np
from scipy.linalg import eigh

from experiments.theta_pencil.finite_weyl_ratio import (
    audit_two_channel_shift,
    projective_cross_ratio,
)
from experiments.theta_pencil.semilocal_weil_matrix import _simpson_weights
from experiments.theta_pencil.screw_weil_operator import (
    build_screw_weil_matrix,
    dirichlet_basis,
)


@dataclass(frozen=True)
class ScrewWeylShiftSample:
    shift: float
    resolvent_ratio_real: float
    resolvent_ratio_imag: float
    characteristic_ratio_real: float
    characteristic_ratio_imag: float
    odd_even_ratio_real: float
    odd_even_ratio_imag: float


@dataclass(frozen=True)
class ScrewWeylShiftDiagnostic:
    half_width: float
    grid_points: int
    basis_size: int
    spectral_parameter_real: float
    spectral_parameter_imag: float
    galerkin_ground_state: float
    samples: tuple[ScrewWeylShiftSample, ...]
    relative_characteristic_spread: float
    maximum_resolvent_identity_residual: float
    maximum_parity_identity_residual: float
    mobius_probe_cross_ratios_real: tuple[float, ...]
    mobius_probe_cross_ratios_imag: tuple[float, ...]
    maximum_mobius_cross_ratio_defect: float


def run_screw_weyl_shift_diagnostic(
    half_width: float = 0.72,
    grid_points: int = 4097,
    basis_size: int = 24,
    spectral_parameter: complex = 0.7 + 0.8j,
    shifts: tuple[float, ...] = (-0.1, -1.0, -10.0),
    mobius_probe_parameters: tuple[complex, complex, complex, complex] = (
        0.2 + 0.4j,
        0.7 + 0.8j,
        -1.1 + 0.5j,
        3.0 + 0.3j,
    ),
) -> ScrewWeylShiftDiagnostic:
    """Measure, without presuming it, whether the Weyl ratio is shift-free."""

    if len(shifts) < 2:
        raise ValueError("at least two shifts are required")
    if spectral_parameter.imag <= 0.0:
        raise ValueError("spectral_parameter must lie in the upper half-plane")

    gram, weil, _, _ = build_screw_weil_matrix(
        half_width, grid_points, basis_size, "dirichlet"
    )
    ground = float(eigh(weil, gram, eigvals_only=True)[0])
    if any(shift >= ground for shift in shifts):
        raise ValueError("every shift must lie below the Galerkin spectrum")

    coordinate = np.linspace(-half_width, half_width, grid_points)
    spacing = float(coordinate[1] - coordinate[0])
    weights = _simpson_weights(grid_points - 1) * (spacing / 3.0)
    basis = dirichlet_basis(coordinate, half_width, basis_size)
    plus = basis @ (weights * np.exp(coordinate))
    minus = basis @ (weights * np.exp(-coordinate))
    observation = basis @ (
        weights * np.exp(1j * spectral_parameter * coordinate)
    )

    sample_rows: list[ScrewWeylShiftSample] = []
    raw_channels: list[tuple[complex, complex, complex, complex]] = []
    prefactor = -(
        (spectral_parameter - 1j) / (spectral_parameter + 1j)
    )
    for shift in shifts:
        pencil = weil - shift * gram
        plus_solution = np.linalg.solve(pencil, plus)
        minus_solution = np.linalg.solve(pencil, minus)
        numerator = complex(observation @ plus_solution)
        denominator = complex(observation @ minus_solution)
        even_channel = (numerator + denominator) / 2.0
        odd_channel = (numerator - denominator) / 2.0
        if abs(denominator) == 0.0 or abs(even_channel) == 0.0:
            raise ZeroDivisionError("a diagnostic channel vanishes")
        ratio = numerator / denominator
        characteristic = prefactor * ratio
        odd_even = odd_channel / even_channel
        raw_channels.append((numerator, denominator, even_channel, odd_channel))
        sample_rows.append(
            ScrewWeylShiftSample(
                shift=shift,
                resolvent_ratio_real=float(ratio.real),
                resolvent_ratio_imag=float(ratio.imag),
                characteristic_ratio_real=float(characteristic.real),
                characteristic_ratio_imag=float(characteristic.imag),
                odd_even_ratio_real=float(odd_even.real),
                odd_even_ratio_imag=float(odd_even.imag),
            )
        )

    identity_residuals = []
    parity_residuals = []
    for index in range(1, len(shifts)):
        audit = audit_two_channel_shift(
            weil,
            plus,
            minus,
            observation,
            shifts[0],
            shifts[index],
            metric=gram,
        )
        identity_residuals.append(audit.identity_residual)
        n0, d0, c0, s0 = raw_channels[0]
        ni, di, ci, si = raw_channels[index]
        cross = ni * d0 - n0 * di
        parity_cross = 2.0 * (si * c0 - ci * s0)
        parity_residuals.append(abs(cross - parity_cross))

    characteristics = np.asarray(
        [
            complex(row.characteristic_ratio_real, row.characteristic_ratio_imag)
            for row in sample_rows
        ]
    )
    spread = max(
        abs(value - characteristics[0]) for value in characteristics[1:]
    ) / max(abs(value) for value in characteristics)

    cross_ratios: list[complex] = []
    for shift in shifts:
        pencil = weil - shift * gram
        plus_solution = np.linalg.solve(pencil, plus)
        minus_solution = np.linalg.solve(pencil, minus)
        probe_values: list[complex] = []
        for probe in mobius_probe_parameters:
            if probe.imag <= 0.0:
                raise ValueError("every Möbius probe must lie in the upper half-plane")
            probe_observation = basis @ (weights * np.exp(1j * probe * coordinate))
            probe_values.append(
                complex(probe_observation @ plus_solution)
                / complex(probe_observation @ minus_solution)
            )
        cross_ratios.append(projective_cross_ratio(tuple(probe_values)))
    mobius_defect = max(
        abs(value - cross_ratios[0]) for value in cross_ratios[1:]
    )

    return ScrewWeylShiftDiagnostic(
        half_width=half_width,
        grid_points=grid_points,
        basis_size=basis_size,
        spectral_parameter_real=float(spectral_parameter.real),
        spectral_parameter_imag=float(spectral_parameter.imag),
        galerkin_ground_state=ground,
        samples=tuple(sample_rows),
        relative_characteristic_spread=float(spread),
        maximum_resolvent_identity_residual=float(max(identity_residuals)),
        maximum_parity_identity_residual=float(max(parity_residuals)),
        mobius_probe_cross_ratios_real=tuple(float(value.real) for value in cross_ratios),
        mobius_probe_cross_ratios_imag=tuple(float(value.imag) for value in cross_ratios),
        maximum_mobius_cross_ratio_defect=float(mobius_defect),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--half-width", type=float, default=0.72)
    parser.add_argument("--grid", type=int, default=4097)
    parser.add_argument("--basis", type=int, default=24)
    parser.add_argument("--z-real", type=float, default=0.7)
    parser.add_argument("--z-imag", type=float, default=0.8)
    parser.add_argument("--shifts", type=float, nargs="+", default=(-0.1, -1.0, -10.0))
    args = parser.parse_args()
    result = run_screw_weyl_shift_diagnostic(
        half_width=args.half_width,
        grid_points=args.grid,
        basis_size=args.basis,
        spectral_parameter=complex(args.z_real, args.z_imag),
        shifts=tuple(args.shifts),
    )
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
