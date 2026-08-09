"""Quantitative high-mode cutoff for the localized Weil--Suzuki operator."""

from __future__ import annotations

import math

from experiments.theta_pencil.semilocal_weil_matrix import EULER_GAMMA
from experiments.theta_pencil.screw_weil_operator import von_mangoldt


def harmonic(index: int) -> float:
    if index < 0:
        raise ValueError("index must be nonnegative")
    return math.fsum(1.0 / k for k in range(1, index + 1))


def active_prime_weight(half_width: float) -> float:
    """Sum Lambda(n)/sqrt(n) over log(n) < 2a."""
    upper = int(math.floor(math.exp(2.0 * half_width) + 1e-13))
    return math.fsum(
        von_mangoldt(n) / math.sqrt(n)
        for n in range(2, upper + 1)
        if math.log(n) < 2.0 * half_width
    )


def bounded_perturbation_norm(half_width: float) -> float:
    """Elementary norm bound valid for 0 < a <= 1/2.

    It uses |r''(t)| <= 3 on |t| <= 1, the norm-two bound for a
    translation plus its adjoint, and the exact scalar shift.
    """
    if not 0.0 < half_width <= 0.5:
        raise ValueError("the registered tail bound applies only on 0 < a <= 1/2")
    scalar = -math.log(half_width) - math.log(2.0 * math.pi) - EULER_GAMMA
    return (
        abs(scalar)
        + 2.0 * active_prime_weight(half_width)
        + 6.0 * half_width
    )


def required_legendre_tail(half_width: float) -> tuple[int, float]:
    """First N for which H_N exceeds the perturbation norm bound."""
    loss = bounded_perturbation_norm(half_width)
    index = 0
    value = 0.0
    while value <= loss:
        index += 1
        value += 1.0 / index
    return index, value - loss


def main() -> None:
    for half_width in (0.3, 0.3465, 0.4, 0.45, 0.5):
        index, margin = required_legendre_tail(half_width)
        print(
            f"a={half_width:.4f} prime_weight={active_prime_weight(half_width):.12g} "
            f"loss={bounded_perturbation_norm(half_width):.12g} "
            f"N={index} tail_margin={margin:.12g}"
        )


if __name__ == "__main__":
    main()
