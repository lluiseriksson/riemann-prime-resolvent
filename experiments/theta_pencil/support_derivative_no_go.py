"""High-frequency obstruction to a form-level support derivative bound.

Inside a fixed prime window Suzuki's scaled form contains compressed symmetric
translations ``T_h`` with ``h = log(n) / a``.  Their derivative is first order
in frequency, whereas the closed dominant form controls only a logarithmic
Fourier moment.  This module evaluates an exact polynomial-envelope witness.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

from numpy.polynomial import Polynomial


@dataclass(frozen=True)
class DerivativeNoGoWitness:
    half_width: float
    displacement: float
    frequency: float
    overlap: float
    overlap_derivative: float
    translation_value: float
    displacement_derivative: float
    support_derivative: float
    logarithmic_scale: float
    derivative_to_logarithmic_scale: float


def polynomial_bump_overlap(displacement: float) -> tuple[float, float]:
    """Return ``C(h)`` and ``C'(h)`` for chi(x)=(1-x^2)^2 on (-1,1).

    Here ``C(h)=integral chi(x+h) chi(x) dx`` over ``[-1, 1-h]``.
    Both values are obtained by exact polynomial antiderivatives followed by
    floating evaluation; no quadrature is used.
    """

    if not 0.0 < displacement < 2.0:
        raise ValueError("displacement must lie in (0, 2)")
    x = Polynomial((0.0, 1.0))
    shifted = x + displacement
    bump = (1.0 - x * x) ** 2
    shifted_bump = (1.0 - shifted * shifted) ** 2
    integrand = bump * shifted_bump
    derivative_integrand = bump * (-4.0 * shifted * (1.0 - shifted * shifted))
    left = -1.0
    right = 1.0 - displacement
    overlap = float(integrand.integ()(right) - integrand.integ()(left))
    derivative = float(
        derivative_integrand.integ()(right)
        - derivative_integrand.integ()(left)
    )
    return overlap, derivative


def phase_locked_frequency(displacement: float, phase_index: int) -> float:
    """Choose nu so that ``sin(nu*h)=1`` exactly in real arithmetic."""

    if not 0.0 < displacement < 2.0:
        raise ValueError("displacement must lie in (0, 2)")
    if phase_index < 0:
        raise ValueError("phase_index must be nonnegative")
    return (math.pi / 2.0 + 2.0 * math.pi * phase_index) / displacement


def build_derivative_no_go_witness(
    half_width: float = 0.4,
    phase_index: int = 100,
    prime_power: int = 2,
) -> DerivativeNoGoWitness:
    """Evaluate the modulated-bump witness for one active prime power."""

    if half_width <= 0.0 or prime_power < 2:
        raise ValueError("invalid support or prime power")
    displacement = math.log(prime_power) / half_width
    overlap, overlap_derivative = polynomial_bump_overlap(displacement)
    frequency = phase_locked_frequency(displacement, phase_index)
    phase = frequency * displacement
    translation = 2.0 * overlap * math.cos(phase)
    displacement_derivative = 2.0 * (
        overlap_derivative * math.cos(phase)
        - frequency * overlap * math.sin(phase)
    )
    # q_a contains -c T_h and h'(a)=-h/a.  Omitting the positive coefficient
    # c leaves the signed scale (h/a) d<T_h>/dh relevant to the no-go.
    support_derivative = displacement / half_width * displacement_derivative
    logarithmic_scale = 1.0 + math.log1p(frequency**2)
    return DerivativeNoGoWitness(
        half_width=half_width,
        displacement=displacement,
        frequency=frequency,
        overlap=overlap,
        overlap_derivative=overlap_derivative,
        translation_value=translation,
        displacement_derivative=displacement_derivative,
        support_derivative=support_derivative,
        logarithmic_scale=logarithmic_scale,
        derivative_to_logarithmic_scale=(
            support_derivative / logarithmic_scale
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--half-width", type=float, default=0.4)
    parser.add_argument("--phase-index", type=int, default=100)
    args = parser.parse_args()
    print(build_derivative_no_go_witness(args.half_width, args.phase_index))


if __name__ == "__main__":
    main()
