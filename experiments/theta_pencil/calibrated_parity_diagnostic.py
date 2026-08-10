"""Predictive audit of the parity-calibrated finite Weyl shift."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq

from experiments.theta_pencil.arb_riemann_weyl_basepoint import (
    certify_riemann_fourier_parity_target,
    certify_riemann_weyl_basepoint,
)
from experiments.theta_pencil.safe_weil_shift import explicit_safe_shift
from experiments.theta_pencil.screw_weil_operator import (
    build_screw_weil_matrix,
    dirichlet_basis,
)
from experiments.theta_pencil.semilocal_weil_matrix import _simpson_weights


@dataclass(frozen=True)
class CalibratedParityRow:
    half_width: float
    galerkin_ground_state: float
    first_gap: float
    calibrated_shift: float
    gap_multiple: float
    predicted_parity_ratio: float
    target_error: float
    kinematic_baseline_improvement: float


@dataclass(frozen=True)
class CalibratedParityDiagnostic:
    imaginary_height: float
    target_balance: float
    target_parity_ratio: float
    kinematic_baseline: float
    kinematic_baseline_error: float
    grid_points: int
    basis_size: int
    rows: tuple[CalibratedParityRow, ...]


def run_calibrated_parity_diagnostic(
    half_widths: tuple[float, ...] = (0.4, 0.5, 0.55, 0.6),
    imaginary_height: float = 3.0,
    grid_points: int = 4097,
    basis_size: int = 32,
    precision_bits: int = 160,
) -> CalibratedParityDiagnostic:
    """Calibrate at ``i`` and test the untouched prediction at ``i*eta``.

    The calculation is a floating Galerkin diagnostic, not a certificate for
    the infinite operator.  The Riemann target and base-point balance are Arb
    certified before being converted to floating midpoints.
    """

    if not half_widths:
        raise ValueError("at least one half-width is required")
    base = certify_riemann_weyl_basepoint(precision_bits)
    target = certify_riemann_fourier_parity_target(
        imaginary_height, precision_bits
    )
    balance = float(base.odd_even_balance.mid())
    target_value = float(target.target_fourier_parity_ratio.mid())
    baseline = -float(imaginary_height) * balance
    baseline_error = abs(baseline - target_value)
    rows: list[CalibratedParityRow] = []

    for width in half_widths:
        gram, operator, _, _ = build_screw_weil_matrix(
            width, grid_points, basis_size, "dirichlet"
        )
        eigenvalues = eigh(
            operator, gram, eigvals_only=True, subset_by_index=(0, 1)
        )
        ground = float(eigenvalues[0])
        gap = float(eigenvalues[1] - eigenvalues[0])
        if gap <= 0.0:
            raise ArithmeticError("the Galerkin ground state is not simple")

        coordinate = np.linspace(-width, width, grid_points)
        spacing = float(coordinate[1] - coordinate[0])
        weights = _simpson_weights(grid_points - 1) * (spacing / 3.0)
        basis = dirichlet_basis(coordinate, width, basis_size)
        plus = basis @ (weights * np.exp(coordinate))
        minus = basis @ (weights * np.exp(-coordinate))
        even_source = (plus + minus) / 2.0
        odd_source = (plus - minus) / 2.0

        def balance_defect(shift: float) -> float:
            pencil = operator - shift * gram
            even_solution = np.linalg.solve(pencil, even_source)
            odd_solution = np.linalg.solve(pencil, odd_source)
            even_mass = float(even_source @ even_solution)
            odd_mass = float(odd_source @ odd_solution)
            return odd_mass / even_mass - balance

        lower = explicit_safe_shift(width)
        upper = ground - max(1.0e-13, 1.0e-8 * gap)
        lower_defect = balance_defect(lower)
        upper_defect = balance_defect(upper)
        if lower_defect * upper_defect >= 0.0:
            raise ArithmeticError("the parity calibration root is not bracketed")
        shift = float(
            brentq(
                balance_defect,
                lower,
                upper,
                xtol=1.0e-14,
                rtol=1.0e-14,
                maxiter=200,
            )
        )

        positive_observation = basis @ (
            weights * np.exp(imaginary_height * coordinate)
        )
        negative_observation = basis @ (
            weights * np.exp(-imaginary_height * coordinate)
        )
        plus_solution = np.linalg.solve(operator - shift * gram, plus)
        value_positive = float(negative_observation @ plus_solution)
        value_negative = float(positive_observation @ plus_solution)
        predicted = (value_positive - value_negative) / (
            value_positive + value_negative
        )
        error = abs(predicted - target_value)
        rows.append(
            CalibratedParityRow(
                half_width=float(width),
                galerkin_ground_state=ground,
                first_gap=gap,
                calibrated_shift=shift,
                gap_multiple=float((ground - shift) / gap),
                predicted_parity_ratio=float(predicted),
                target_error=float(error),
                kinematic_baseline_improvement=float(
                    baseline_error - error
                ),
            )
        )

    return CalibratedParityDiagnostic(
        imaginary_height=float(imaginary_height),
        target_balance=balance,
        target_parity_ratio=target_value,
        kinematic_baseline=baseline,
        kinematic_baseline_error=float(baseline_error),
        grid_points=grid_points,
        basis_size=basis_size,
        rows=tuple(rows),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--half-widths", type=float, nargs="+", default=(0.4, 0.5, 0.55, 0.6)
    )
    parser.add_argument("--eta", type=float, default=3.0)
    parser.add_argument("--grid", type=int, default=4097)
    parser.add_argument("--basis", type=int, default=32)
    parser.add_argument("--precision", type=int, default=160)
    args = parser.parse_args()
    result = run_calibrated_parity_diagnostic(
        half_widths=tuple(args.half_widths),
        imaginary_height=args.eta,
        grid_points=args.grid,
        basis_size=args.basis,
        precision_bits=args.precision,
    )
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
