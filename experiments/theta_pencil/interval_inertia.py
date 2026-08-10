"""Ball-arithmetic inertia check for a supplied finite Schur matrix.

The ball radius is an input obligation: this module proves robustness of the
matrix inertia *if* every true entry lies in the supplied ball.  Establishing
that enclosure from the analytic formulas is a separate source-level task.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class IntervalInertiaResult:
    dimension: int
    entry_radius: float
    negative_count: int
    positive_count: int
    unresolved_count: int
    real_intervals: tuple[tuple[float, float], ...]
    maximum_imaginary_radius: float
    method: str = "direct-ball"


@dataclass(frozen=True)
class ArbPositiveDefiniteCongruence:
    dimension: int
    transformed_gershgorin_lower: float
    transformation_gram_lower: float
    transformation_norm_squared_upper: float
    original_spectral_lower: float
    method: str = "congruence-gershgorin"


def certify_arb_positive_definite_by_congruence(
    matrix, precision: int = 192
) -> ArbPositiveDefiniteCongruence:
    """Prove an Arb matrix positive using a midpoint eigenbasis.

    The input retains its individual entry radii.  A floating eigenbasis is
    treated only as a point matrix: Arb verifies both its invertibility and
    strict Gershgorin positivity after congruence.
    """

    if matrix.nrows() != matrix.ncols() or matrix.nrows() < 1:
        raise ValueError("matrix must be nonempty and square")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("python-flint is required") from error

    dimension = matrix.nrows()
    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        symmetric = (matrix + matrix.transpose()) / 2
        midpoint = np.array(
            [
                [float(symmetric[row, column].mid()) for column in range(dimension)]
                for row in range(dimension)
            ],
            dtype=float,
        )
        midpoint = 0.5 * (midpoint + midpoint.T)
        _, eigenvectors = np.linalg.eigh(midpoint)
        transform = arb_mat(
            [
                [arb(float(eigenvectors[row, column])) for column in range(dimension)]
                for row in range(dimension)
            ]
        )

        gram = transform.transpose() * transform
        gram_lowers = []
        gram_uppers = []
        for row in range(dimension):
            off_diagonal = sum(
                (
                    abs(gram[row, column]).upper()
                    for column in range(dimension)
                    if column != row
                ),
                arb(0),
            )
            gram_lowers.append(gram[row, row].lower() - off_diagonal)
            gram_uppers.append(gram[row, row].upper() + off_diagonal)
        gram_lower = min(gram_lowers)
        gram_upper = max(gram_uppers)
        if not gram_lower > 0:
            raise ArithmeticError("the congruence transform was not certified invertible")

        transformed = transform.transpose() * symmetric * transform
        transformed_lowers = []
        for row in range(dimension):
            off_diagonal = sum(
                (
                    abs(transformed[row, column]).upper()
                    for column in range(dimension)
                    if column != row
                ),
                arb(0),
            )
            transformed_lowers.append(
                transformed[row, row].lower() - off_diagonal
            )
        transformed_lower = min(transformed_lowers)
        if not transformed_lower > 0:
            raise ArithmeticError(
                "the congruent interval matrix was not strictly positive"
            )
        original_lower = transformed_lower / gram_upper
    finally:
        ctx.prec = previous_precision

    def lower_float(value) -> float:
        return math.nextafter(float(value.lower()), -math.inf)

    return ArbPositiveDefiniteCongruence(
        dimension=dimension,
        transformed_gershgorin_lower=lower_float(transformed_lower),
        transformation_gram_lower=lower_float(gram_lower),
        transformation_norm_squared_upper=math.nextafter(
            float(gram_upper.upper()), math.inf
        ),
        original_spectral_lower=lower_float(original_lower),
    )


def certify_interval_inertia(
    matrix: np.ndarray, entry_radius: float, precision: int = 192
) -> IntervalInertiaResult:
    """Enclose every eigenvalue of a symmetric entrywise ball matrix."""
    if entry_radius < 0.0:
        raise ValueError("entry_radius must be nonnegative")
    array = np.asarray(matrix, dtype=float)
    if array.ndim != 2 or array.shape[0] != array.shape[1]:
        raise ValueError("matrix must be square")
    if not np.allclose(array, array.T, atol=1e-12, rtol=0.0):
        raise ValueError("matrix must be symmetric")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("python-flint is required for interval inertia") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        ball_matrix = arb_mat(
            [
                [arb(float(array[row, column]), entry_radius) for column in range(len(array))]
                for row in range(len(array))
            ]
        )
        try:
            eigenvalues = ball_matrix.eig(multiple=True, algorithm="rump")
            method = "direct-ball"
        except ValueError:
            # For a symmetric midpoint M and any symmetric perturbation E
            # with |E_ij| <= r, Weyl gives
            # |lambda_k(M+E)-lambda_k(M)| <= ||E||_2 <= dimension*r.
            # Isolating the point spectrum and enlarging every interval by
            # that explicit amount is often stronger than asking Rump to
            # diagonalize an independently ball-valued matrix directly.
            # ``np.allclose`` above admits harmless last-bit asymmetry.  Use
            # the exactly symmetric midpoint and charge half of the maximum
            # antisymmetric defect to the entrywise perturbation budget.
            symmetric_midpoint = 0.5 * (array + array.T)
            antisymmetric_budget = 0.5 * float(np.max(np.abs(array - array.T)))
            fallback_radius = math.nextafter(
                entry_radius + antisymmetric_budget, math.inf
            )
            point_matrix = arb_mat(
                [
                    [
                        arb(float(symmetric_midpoint[row, column]))
                        for column in range(len(array))
                    ]
                    for row in range(len(array))
                ]
            )
            eigenvalues = point_matrix.eig(multiple=True, algorithm="rump")
            method = "point-weyl"
    finally:
        ctx.prec = previous_precision

    weyl_loss = (
        len(array) * fallback_radius if method == "point-weyl" else 0.0
    )
    intervals = tuple(
        (
            math.nextafter(float(value.real.lower()) - weyl_loss, -math.inf),
            math.nextafter(float(value.real.upper()) + weyl_loss, math.inf),
        )
        for value in eigenvalues
    )
    negative = sum(upper < 0.0 for _, upper in intervals)
    positive = sum(lower > 0.0 for lower, _ in intervals)
    unresolved = len(intervals) - negative - positive
    imaginary = (
        0.0
        if method == "point-weyl"
        else max(float(value.imag.rad()) for value in eigenvalues)
    )
    return IntervalInertiaResult(
        dimension=len(array),
        entry_radius=entry_radius,
        negative_count=negative,
        positive_count=positive,
        unresolved_count=unresolved,
        real_intervals=intervals,
        maximum_imaginary_radius=imaginary,
        method=method,
    )


def entrywise_weyl_budget(spectral_margin: float, dimension: int) -> float:
    """Sufficient entrywise radius from ||E||_2 <= dimension * radius."""
    if spectral_margin <= 0.0:
        raise ValueError("spectral_margin must be positive")
    if dimension < 1:
        raise ValueError("dimension must be positive")
    return spectral_margin / dimension
