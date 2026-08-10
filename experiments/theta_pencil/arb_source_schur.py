"""Source-level Arb enclosure for the parity Schur comparison matrices."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_jet_correction import (
    build_arb_active_prime_jet_correction,
)
from experiments.theta_pencil.arb_prime_translation import (
    _arb_radius_as_float,
    build_arb_prime_matrix,
)
from experiments.theta_pencil.arb_smooth_kernel import build_arb_smooth_matrix


@dataclass(frozen=True)
class ArbSourceSchur:
    midpoint: np.ndarray
    radius: np.ndarray
    maximum_target_distance: float
    contained_in_target_box: bool
    target_radius: float
    precision: int
    active_primes: tuple[int, ...]


def _roundtrip_ball(arb, midpoint: float, radius: float):
    pad = math.ulp(midpoint) if midpoint != 0.0 else math.ulp(0.0)
    return arb(midpoint, radius + pad)


def certify_source_schur_box(
    parity: int,
    target_matrix: np.ndarray,
    half_width: float = 0.4,
    low_dimension: int = 88,
    finite_dimension: int = 4096,
    smooth_dimension: int = 512,
    spectral_shift: float = 0.005,
    jet_count: int = 6,
    jet_end: int = 1_000_000,
    target_radius: float = 1.0e-6,
    precision: int = 192,
    prime_precision: int = 8192,
    active_primes: tuple[int, ...] = (2,),
    perturbation_loss: float | None = None,
) -> ArbSourceSchur:
    """Prove that the exact finite Schur source lies near ``target_matrix``.

    Infinite tails are deliberately excluded: this closes the finite source
    obligation to which the separate Wang, jump, and potential tail bounds
    are later applied.
    """
    if parity not in (0, 1):
        raise ValueError("parity must be zero or one")
    if not active_primes:
        raise ValueError("at least one active prime is required")
    low_degrees = np.arange(parity, low_dimension, 2)
    target = np.asarray(target_matrix, dtype=float)
    if target.shape != (len(low_degrees), len(low_degrees)):
        raise ValueError("target matrix has the wrong parity-block shape")
    if not 0 < low_dimension < smooth_dimension <= finite_dimension < jet_end:
        raise ValueError("dimensions must satisfy low < smooth <= finite < jet_end")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    primes = [
        build_arb_prime_matrix(
            half_width,
            prime,
            low_dimension,
            finite_dimension,
            prime_precision,
        )
        for prime in active_primes
    ]
    smooth = build_arb_smooth_matrix(
        half_width, low_dimension, smooth_dimension, 23, precision
    )
    jets = build_arb_active_prime_jet_correction(
        half_width,
        active_primes,
        low_degrees,
        finite_dimension,
        jet_end,
        jet_count,
        spectral_shift,
        precision,
        perturbation_loss=perturbation_loss,
    )

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = arb(str(half_width))
        shift = arb(str(spectral_shift))
        scalar = -a.log() - (arb(2) * arb.pi()).log() - arb.const_euler()
        if not scalar.upper() < 0:
            raise ArithmeticError("could not certify the scalar sign")
        prime_balls = [arb(prime) for prime in active_primes]
        loss = (
            arb(str(perturbation_loss))
            if perturbation_loss is not None
            else -scalar
            + sum(
                (arb(2) * prime.log() / prime.sqrt() for prime in prime_balls),
                arb(0),
            )
            + arb(6) * a
        )

        harmonic = [arb(0)]
        for degree in range(1, finite_dimension + 1):
            harmonic.append(harmonic[-1] + arb(1) / degree)
        diagonal_correction = [arb(1)]
        for degree in range(1, low_dimension):
            diagonal_correction.append(
                diagonal_correction[-1]
                + arb(1) / (degree * (2 * degree - 1) * (2 * degree + 1))
            )

        smooth_tail = arb(str(smooth.analytic_remainder))

        def boundary(left: int, right: int):
            if (left + right) % 2:
                return arb(0)
            if left == right:
                return diagonal_correction[left] - arb.const_log2()
            return arb((2 * left + 1) * (2 * right + 1)).sqrt() / (
                abs(left - right) * (left + right + 1)
            )

        def prime_entry(left: int, right: int):
            return sum(
                (
                    _roundtrip_ball(
                        arb,
                        prime.midpoint[left, right],
                        prime.radius[left, right],
                    )
                    for prime in primes
                ),
                arb(0),
            )

        def smooth_entry(left: int, right: int):
            if right >= smooth_dimension:
                return arb(0)
            return _roundtrip_ball(
                arb, smooth.midpoint[left, right], smooth.radius[left, right]
            ) + arb(0, float(smooth_tail.upper()))

        low_matrix = [[arb(0) for _ in low_degrees] for _ in low_degrees]
        for row, left_value in enumerate(low_degrees):
            left = int(left_value)
            for column, right_value in enumerate(low_degrees):
                right = int(right_value)
                value = boundary(left, right) + prime_entry(left, right) + smooth_entry(left, right)
                if left == right:
                    value += harmonic[left] + scalar - shift
                low_matrix[row][column] = value

        high_degrees = np.arange(
            low_dimension + ((low_dimension - parity) % 2),
            finite_dimension,
            2,
        )
        cross = [[arb(0) for _ in high_degrees] for _ in low_degrees]
        for row, left_value in enumerate(low_degrees):
            left = int(left_value)
            for column, right_value in enumerate(high_degrees):
                right = int(right_value)
                cross[row][column] = (
                    boundary(left, right)
                    + prime_entry(left, right)
                    + smooth_entry(left, right)
                )

        source = [[arb(low_matrix[row][column]) for column in range(len(low_degrees))]
                  for row in range(len(low_degrees))]
        for column, degree_value in enumerate(high_degrees):
            degree = int(degree_value)
            denominator = harmonic[degree] - loss - shift
            if not denominator.lower() > 0:
                raise ArithmeticError("Schur denominator was not certified positive")
            for row in range(len(low_degrees)):
                for other in range(row, len(low_degrees)):
                    value = cross[row][column] * cross[other][column] / denominator
                    source[row][other] -= value
                    if other != row:
                        source[other][row] -= value

        for row in range(len(low_degrees)):
            for column in range(len(low_degrees)):
                source[row][column] -= _roundtrip_ball(
                    arb, jets.midpoint[row, column], jets.radius[row, column]
                )

        midpoint = np.empty_like(target)
        radius = np.empty_like(target)
        distances = np.empty_like(target)
        for row in range(len(low_degrees)):
            for column in range(len(low_degrees)):
                value = source[row][column]
                midpoint[row, column] = float(value.mid())
                radius[row, column] = _arb_radius_as_float(value)
                distances[row, column] = (
                    abs(midpoint[row, column] - target[row, column])
                    + radius[row, column]
                    + math.ulp(midpoint[row, column])
                )
    finally:
        ctx.prec = previous_precision

    maximum_distance = float(np.max(distances))
    return ArbSourceSchur(
        midpoint=midpoint,
        radius=radius,
        maximum_target_distance=maximum_distance,
        contained_in_target_box=maximum_distance < target_radius,
        target_radius=target_radius,
        precision=precision,
        active_primes=active_primes,
    )
