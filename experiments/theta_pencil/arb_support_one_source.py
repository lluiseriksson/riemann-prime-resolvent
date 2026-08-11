"""Arb enclosure and positive-subspace certificate at support one.

This module addresses only the raw degree-58 source compression.  The Schur
correction from degrees 58 and above is a separate obligation.  The smooth
series remainder is charged as an operator-norm loss before any positive
subspace is certified.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import (
    _arb_radius_as_float,
    build_arb_prime_matrix,
)
from experiments.theta_pencil.arb_smooth_kernel import build_arb_smooth_matrix
from experiments.theta_pencil.arb_source_schur import _roundtrip_ball
from experiments.theta_pencil.interval_inertia import (
    ArbPositiveDefiniteCongruence,
    certify_arb_positive_definite_by_congruence,
)


ACTIVE_SUPPORT_ONE_PRIME_POWERS = (2, 3, 4, 5, 7)


@dataclass(frozen=True)
class ArbSupportOneSource:
    dimension: int
    midpoint: np.ndarray
    radius: np.ndarray
    even_midpoint: np.ndarray
    even_radius: np.ndarray
    odd_midpoint: np.ndarray
    odd_radius: np.ndarray
    smooth_remainder: float
    precision: int
    prime_precision: int
    active_prime_powers: tuple[int, ...]


@dataclass(frozen=True)
class ArbSupportOnePositiveSubspaces:
    dimension: int
    even_positive_count: int
    odd_positive_count: int
    even_certificate: ArbPositiveDefiniteCongruence
    odd_certificate: ArbPositiveDefiniteCongruence
    smooth_remainder: float
    context: str = (
        "raw source compression only; the infinite Schur correction is omitted"
    )


def _export_ball_matrix(matrix) -> tuple[np.ndarray, np.ndarray]:
    midpoint = np.empty((matrix.nrows(), matrix.ncols()), dtype=float)
    radius = np.empty_like(midpoint)
    for row in range(matrix.nrows()):
        for column in range(matrix.ncols()):
            value = matrix[row, column]
            midpoint[row, column] = float(value.mid())
            radius[row, column] = _arb_radius_as_float(value)
    return midpoint, radius


def _ball_from_export(arb, arb_mat, midpoint, radius):
    return arb_mat(
        [
            [
                _roundtrip_ball(
                    arb,
                    float(midpoint[row, column]),
                    float(radius[row, column]),
                )
                for column in range(midpoint.shape[1])
            ]
            for row in range(midpoint.shape[0])
        ]
    )


def build_arb_support_one_source(
    dimension: int = 58,
    maximum_smooth_power: int = 95,
    precision: int = 512,
    prime_precision: int = 2048,
) -> ArbSupportOneSource:
    """Enclose the raw support-one Legendre source matrix."""

    if dimension < 2:
        raise ValueError("dimension must be at least two")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    primes = [
        build_arb_prime_matrix(
            1.0,
            prime_power,
            dimension,
            dimension,
            prime_precision,
        )
        for prime_power in ACTIVE_SUPPORT_ONE_PRIME_POWERS
    ]
    smooth = build_arb_smooth_matrix(
        1.0,
        dimension,
        dimension,
        maximum_smooth_power,
        precision,
    )

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        scalar = -(arb(2) * arb.pi()).log() - arb.const_euler()
        harmonic = [arb(0)]
        for degree in range(1, dimension):
            harmonic.append(harmonic[-1] + arb(1) / degree)
        diagonal_correction = [arb(1)]
        for degree in range(1, dimension):
            diagonal_correction.append(
                diagonal_correction[-1]
                + arb(1) / (degree * (2 * degree - 1) * (2 * degree + 1))
            )

        source = arb_mat(dimension, dimension)
        for left in range(dimension):
            for right in range(left, dimension):
                if (left + right) % 2:
                    value = arb(0)
                elif left == right:
                    value = diagonal_correction[left] - arb.const_log2()
                else:
                    value = arb((2 * left + 1) * (2 * right + 1)).sqrt() / (
                        abs(left - right) * (left + right + 1)
                    )
                value += sum(
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
                value += _roundtrip_ball(
                    arb,
                    smooth.midpoint[left, right],
                    smooth.radius[left, right],
                )
                if left == right:
                    value += harmonic[left] + scalar
                source[left, right] = value
                source[right, left] = value

        even_indices = tuple(range(0, dimension, 2))
        odd_indices = tuple(range(1, dimension, 2))
        even = arb_mat(
            [
                [source[left, right] for right in even_indices]
                for left in even_indices
            ]
        )
        odd = arb_mat(
            [
                [source[left, right] for right in odd_indices]
                for left in odd_indices
            ]
        )
        midpoint, radius = _export_ball_matrix(source)
        even_midpoint, even_radius = _export_ball_matrix(even)
        odd_midpoint, odd_radius = _export_ball_matrix(odd)
    finally:
        ctx.prec = previous_precision

    return ArbSupportOneSource(
        dimension=dimension,
        midpoint=midpoint,
        radius=radius,
        even_midpoint=even_midpoint,
        even_radius=even_radius,
        odd_midpoint=odd_midpoint,
        odd_radius=odd_radius,
        smooth_remainder=math.nextafter(smooth.analytic_remainder, math.inf),
        precision=precision,
        prime_precision=prime_precision,
        active_prime_powers=ACTIVE_SUPPORT_ONE_PRIME_POWERS,
    )


def certify_arb_support_one_positive_subspaces(
    source: ArbSupportOneSource,
    even_positive_count: int = 26,
    odd_positive_count: int = 26,
    precision: int | None = None,
) -> ArbSupportOnePositiveSubspaces:
    """Certify high-eigenvalue trial subspaces in both parity blocks."""

    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    working_precision = precision or source.precision

    def certify(midpoint, radius, count):
        if not 0 < count <= len(midpoint):
            raise ValueError("the selected count must fit the parity block")
        eigenvalues, eigenvectors = np.linalg.eigh(
            0.5 * (midpoint + midpoint.T)
        )
        selected_midpoint_floor = float(eigenvalues[-count])
        if selected_midpoint_floor <= source.smooth_remainder:
            raise ValueError(
                "the requested trial subspace is not positive even at the "
                "midpoint after charging the smooth remainder: "
                f"floor={selected_midpoint_floor!r}, "
                f"remainder={source.smooth_remainder!r}"
            )
        trial = eigenvectors[:, -count:]
        matrix = _ball_from_export(arb, arb_mat, midpoint, radius)
        for index in range(matrix.nrows()):
            matrix[index, index] -= arb(str(source.smooth_remainder))
        transform = arb_mat(
            [
                [arb(float(trial[row, column])) for column in range(count)]
                for row in range(len(midpoint))
            ]
        )
        reduced = transform.transpose() * matrix * transform
        return certify_arb_positive_definite_by_congruence(
            reduced, working_precision
        )

    previous_precision = ctx.prec
    try:
        ctx.prec = working_precision
        even_certificate = certify(
            source.even_midpoint, source.even_radius, even_positive_count
        )
        odd_certificate = certify(
            source.odd_midpoint, source.odd_radius, odd_positive_count
        )
    finally:
        ctx.prec = previous_precision
    return ArbSupportOnePositiveSubspaces(
        dimension=source.dimension,
        even_positive_count=even_positive_count,
        odd_positive_count=odd_positive_count,
        even_certificate=even_certificate,
        odd_certificate=odd_certificate,
        smooth_remainder=source.smooth_remainder,
    )
