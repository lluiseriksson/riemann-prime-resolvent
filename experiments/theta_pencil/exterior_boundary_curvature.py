"""Exterior curvature of the continuous-kernel Suzuki boundary data."""

from __future__ import annotations

import math

import numpy as np

from experiments.theta_pencil.screw_weil_operator import von_mangoldt


def smooth_screw_second(t: float) -> float:
    """Return the smooth part of the second derivative for positive t."""

    if t <= 0.0:
        raise ValueError("t must be positive")
    return (
        -math.exp(t / 2.0)
        - math.exp(-t / 2.0)
        + math.exp(-t / 2.0) / (-math.expm1(-2.0 * t))
    )


def smooth_screw_second_series(t: float, terms: int) -> float:
    """Evaluate the geometric-series decomposition of the smooth kernel."""

    if t <= 0.0 or terms < 1:
        raise ValueError("t and terms must be positive")
    tail = sum(math.exp(-(2 * index + 0.5) * t) for index in range(terms))
    return -math.exp(t / 2.0) - math.exp(-t / 2.0) + tail


def active_exterior_prime_powers(
    half_width: float,
    exterior_point: float,
) -> tuple[int, ...]:
    """Return prime powers whose translated sample lies inside [-a,a]."""

    if half_width <= 0.0 or exterior_point <= half_width:
        raise ValueError("the point must lie to the right of the interval")
    lower = math.exp(exterior_point - half_width)
    upper = math.exp(exterior_point + half_width)
    result = []
    for integer in range(max(2, math.floor(lower) + 1), math.ceil(upper)):
        if von_mangoldt(integer) > 0.0:
            result.append(integer)
    return tuple(result)


def exterior_curvature(
    coordinate: np.ndarray,
    values: np.ndarray,
    exterior_point: float,
) -> tuple[float, float, float]:
    """Numerically evaluate the smooth and prime pieces of h''(x)."""

    points = np.asarray(coordinate, dtype=float)
    source = np.asarray(values, dtype=float)
    if points.ndim != 1 or source.shape != points.shape or len(points) < 3:
        raise ValueError(
            "coordinate and values must be matching one-dimensional grids"
        )
    steps = np.diff(points)
    if not np.allclose(steps, steps[0], atol=1.0e-12, rtol=1.0e-12):
        raise ValueError("coordinate grid must be equally spaced")
    half_width = max(abs(float(points[0])), abs(float(points[-1])))
    if exterior_point <= half_width:
        raise ValueError("exterior_point must exceed the grid half-width")

    kernel = np.asarray(
        [smooth_screw_second(exterior_point - point) for point in points]
    )
    smooth = float(np.trapezoid(kernel * source, points))
    prime = 0.0
    for integer in active_exterior_prime_powers(half_width, exterior_point):
        sample_point = exterior_point - math.log(integer)
        sample = float(np.interp(sample_point, points, source))
        prime += von_mangoldt(integer) * sample / math.sqrt(integer)
    return smooth, prime, smooth + prime


def pnt_centered_prime_window(
    coordinate: np.ndarray,
    values: np.ndarray,
    exterior_point: float,
) -> tuple[float, float, float]:
    """Return the prime window, its PNT main term, and their difference.

    Writing ``psi(X)=X+R(X)``, the Stieltjes integral for the moving prime
    window has main term

    ``exp(x/2) * integral exp(-y/2) v(y) dy``.

    This is exactly the growing smooth term with the opposite sign in the
    exterior-curvature equation. The final component is therefore the
    arithmetic remainder that survives this cancellation.
    """

    points = np.asarray(coordinate, dtype=float)
    source = np.asarray(values, dtype=float)
    if points.ndim != 1 or source.shape != points.shape or len(points) < 3:
        raise ValueError(
            "coordinate and values must be matching one-dimensional grids"
        )
    steps = np.diff(points)
    if not np.allclose(steps, steps[0], atol=1.0e-12, rtol=1.0e-12):
        raise ValueError("coordinate grid must be equally spaced")
    half_width = max(abs(float(points[0])), abs(float(points[-1])))
    if exterior_point <= half_width:
        raise ValueError("exterior_point must exceed the grid half-width")

    prime = 0.0
    for integer in active_exterior_prime_powers(half_width, exterior_point):
        sample_point = exterior_point - math.log(integer)
        sample = float(np.interp(sample_point, points, source))
        prime += von_mangoldt(integer) * sample / math.sqrt(integer)
    main = math.exp(exterior_point / 2.0) * float(
        np.trapezoid(np.exp(-points / 2.0) * source, points)
    )
    return prime, main, prime - main


def normalized_remainder_pairing(
    coordinate: np.ndarray,
    values: np.ndarray,
    derivatives: np.ndarray,
    normalized_remainder: np.ndarray,
) -> float:
    """Evaluate the integration-by-parts remainder functional.

    The last input samples

    ``r_x(y) = exp(-(x-y)/2) * R(exp(x-y))``

    on the same increasing ``y`` grid as the source.  For a mean-zero source,
    the functional is invariant under adding a constant to ``r_x``.  This is
    the exact cancellation behind the local-oscillation bound in the notes.
    """

    points = np.asarray(coordinate, dtype=float)
    source = np.asarray(values, dtype=float)
    slope = np.asarray(derivatives, dtype=float)
    remainder = np.asarray(normalized_remainder, dtype=float)
    if points.ndim != 1 or len(points) < 3:
        raise ValueError("coordinate must be a one-dimensional grid")
    if source.shape != points.shape:
        raise ValueError("values has the wrong shape")
    if slope.shape != points.shape:
        raise ValueError("derivatives has the wrong shape")
    if remainder.shape != points.shape:
        raise ValueError("normalized_remainder has the wrong shape")
    return float(
        source[0] * remainder[0]
        - source[-1] * remainder[-1]
        + np.trapezoid(remainder * (slope + 0.5 * source), points)
    )
