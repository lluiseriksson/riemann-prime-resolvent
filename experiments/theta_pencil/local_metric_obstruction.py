"""Numerical witness for the exact local-metric obstruction.

The proof is analytic and lives in ``docs/theta-reboot/theta-pencil.md``.
This script evaluates the exact logarithmic-coordinate potential

    V(x) = Phi'(x)^2 - Phi''(x) = psi''(x) / psi(x)

for the positive Riemann theta density. A local weighted L2 metric could
symmetrize the pencil only if this function were constant.

The implementation uses only the Python standard library. For x >= 0 it uses
Hedenmalm's exponentially convergent theta series. Evenness supplies x < 0.
"""

from __future__ import annotations

import argparse
import math


def _scaled_monomial_derivatives(
    coefficient: float, power: float, rate: float, t: float
) -> tuple[float, float, float]:
    """Return f, d/dx f, d^2/dx^2 f for f=c*t^p*exp(-rate*t^2), t=e^x."""

    value = coefficient * (t**power) * math.exp(-rate * t * t)
    slope = power - 2.0 * rate * t * t
    first = value * slope
    second = value * (slope * slope - 4.0 * rate * t * t)
    return value, first, second


def theta_density_jet(x: float, terms: int = 32) -> tuple[float, float, float]:
    """Return psi(x), psi'(x), psi''(x) from the positive theta series."""

    if terms < 1:
        raise ValueError("terms must be positive")
    at_origin = x == 0.0
    sign = 1.0
    if x < 0.0:
        x = -x
        sign = -1.0
    t = math.exp(x)
    values = [0.0, 0.0, 0.0]
    for n in range(1, terms + 1):
        n2 = float(n * n)
        rate = math.pi * n2
        # pi*n^2*(2*pi*n^2*t^(9/2) - 3*t^(5/2))*exp(-pi*n^2*t^2)
        pieces = (
            (2.0 * math.pi * math.pi * n2 * n2, 4.5),
            (-3.0 * math.pi * n2, 2.5),
        )
        for coefficient, power in pieces:
            jet = _scaled_monomial_derivatives(coefficient, power, rate, t)
            for order in range(3):
                values[order] += jet[order]
    values[1] = 0.0 if at_origin else values[1] * sign
    return values[0], values[1], values[2]


def local_metric_potential(x: float, terms: int = 32) -> float:
    """Evaluate V = psi'' / psi, the obstruction potential."""

    psi, _, psi_second = theta_density_jet(x, terms=terms)
    if not psi > 0.0:
        raise ArithmeticError(f"theta density lost positivity at x={x}: {psi}")
    return psi_second / psi


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=int, default=32)
    parser.add_argument(
        "--points", type=float, nargs="*", default=[0.0, 0.25, 0.5, 1.0, 1.5, 2.0]
    )
    args = parser.parse_args()

    print("x,psi,psi_second_over_psi")
    potentials = []
    for x in args.points:
        psi, _, _ = theta_density_jet(x, terms=args.terms)
        potential = local_metric_potential(x, terms=args.terms)
        potentials.append(potential)
        print(f"{x:.8g},{psi:.17g},{potential:.17g}")

    spread = max(potentials) - min(potentials)
    print(f"potential_spread,{spread:.17g}")
    if not spread > 1.0:
        raise SystemExit("unexpectedly small potential spread")


if __name__ == "__main__":
    main()
