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
