"""Ball-arithmetic inertia check for a supplied finite Schur matrix.

The ball radius is an input obligation: this module proves robustness of the
matrix inertia *if* every true entry lies in the supplied ball.  Establishing
that enclosure from the analytic formulas is a separate source-level task.
"""

from __future__ import annotations

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
        eigenvalues = ball_matrix.eig(multiple=True, algorithm="rump")
    finally:
        ctx.prec = previous_precision

    intervals = tuple(
        (float(value.real.lower()), float(value.real.upper()))
        for value in eigenvalues
    )
    negative = sum(upper < 0.0 for _, upper in intervals)
    positive = sum(lower > 0.0 for lower, _ in intervals)
    unresolved = len(intervals) - negative - positive
    imaginary = max(float(value.imag.rad()) for value in eigenvalues)
    return IntervalInertiaResult(
        dimension=len(array),
        entry_radius=entry_radius,
        negative_count=negative,
        positive_count=positive,
        unresolved_count=unresolved,
        real_intervals=intervals,
        maximum_imaginary_radius=imaginary,
    )


def entrywise_weyl_budget(spectral_margin: float, dimension: int) -> float:
    """Sufficient entrywise radius from ||E||_2 <= dimension * radius."""
    if spectral_margin <= 0.0:
        raise ValueError("spectral_margin must be positive")
    if dimension < 1:
        raise ValueError("dimension must be positive")
    return spectral_margin / dimension
