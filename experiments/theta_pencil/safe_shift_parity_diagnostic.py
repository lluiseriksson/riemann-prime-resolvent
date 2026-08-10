"""Falsification diagnostic for the explicit safe shift on the parity target."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

from experiments.theta_pencil.arb_riemann_weyl_basepoint import (
    certify_riemann_fourier_parity_target,
    certify_riemann_weyl_basepoint,
)
from experiments.theta_pencil.finite_weyl_ratio import (
    renormalized_fourier_parity_ratio,
)
from experiments.theta_pencil.safe_weil_shift import explicit_safe_shift
from experiments.theta_pencil.screw_weyl_shift_diagnostic import (
    run_screw_weyl_shift_diagnostic,
)


@dataclass(frozen=True)
class SafeShiftParityRow:
    half_width: float
    shift: float
    galerkin_ground_state: float
    raw_parity_ratio_real: float
    raw_parity_ratio_imag: float
    renormalized_parity_ratio_real: float
    renormalized_parity_ratio_imag: float
    target_error: float


@dataclass(frozen=True)
class SafeShiftParityDiagnostic:
    imaginary_height: float
    target_parity_ratio: float
    base_imaginary_value: float
    grid_points: int
    basis_size: int
    rows: tuple[SafeShiftParityRow, ...]


def run_safe_shift_parity_diagnostic(
    half_widths: tuple[float, ...] = (0.4, 0.72, 1.5, 3.0),
    imaginary_height: float = 3.0,
    grid_points: int = 4097,
    basis_size: int = 32,
    precision_bits: int = 160,
) -> SafeShiftParityDiagnostic:
    """Compare the safe-shift finite ratios with the certified Riemann target.

    This is a floating Galerkin falsifier.  Only the target value is certified;
    the finite rows make no claim about the infinite-dimensional limit.
    """

    if not half_widths:
        raise ValueError("at least one half-width is required")
    base = certify_riemann_weyl_basepoint(precision_bits)
    target = certify_riemann_fourier_parity_target(
        imaginary_height, precision_bits
    )
    c_value = float((base.xi_value / base.xi_first_derivative).mid())
    target_value = float(target.target_fourier_parity_ratio.mid())
    point = 1j * float(imaginary_height)
    rows: list[SafeShiftParityRow] = []
    for width in half_widths:
        shift = explicit_safe_shift(width)
        diagnostic = run_screw_weyl_shift_diagnostic(
            half_width=width,
            grid_points=grid_points,
            basis_size=basis_size,
            spectral_parameter=point,
            shifts=(shift, shift - 1.0),
        )
        sample = diagnostic.samples[0]
        raw = complex(
            sample.odd_even_ratio_real, sample.odd_even_ratio_imag
        )
        renormalized = renormalized_fourier_parity_ratio(
            raw, point, shift, c_value
        )
        rows.append(
            SafeShiftParityRow(
                half_width=float(width),
                shift=float(shift),
                galerkin_ground_state=diagnostic.galerkin_ground_state,
                raw_parity_ratio_real=float(raw.real),
                raw_parity_ratio_imag=float(raw.imag),
                renormalized_parity_ratio_real=float(renormalized.real),
                renormalized_parity_ratio_imag=float(renormalized.imag),
                target_error=float(abs(renormalized - target_value)),
            )
        )
    return SafeShiftParityDiagnostic(
        imaginary_height=float(imaginary_height),
        target_parity_ratio=target_value,
        base_imaginary_value=c_value,
        grid_points=grid_points,
        basis_size=basis_size,
        rows=tuple(rows),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--half-widths",
        type=float,
        nargs="+",
        default=(0.4, 0.72, 1.5, 3.0),
    )
    parser.add_argument("--eta", type=float, default=3.0)
    parser.add_argument("--grid", type=int, default=4097)
    parser.add_argument("--basis", type=int, default=32)
    parser.add_argument("--precision", type=int, default=160)
    args = parser.parse_args()
    result = run_safe_shift_parity_diagnostic(
        half_widths=tuple(args.half_widths),
        imaginary_height=args.eta,
        grid_points=args.grid,
        basis_size=args.basis,
        precision_bits=args.precision,
    )
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
