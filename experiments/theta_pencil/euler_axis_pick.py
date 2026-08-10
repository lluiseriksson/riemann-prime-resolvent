"""Exact finite algebra for the Euler-axis Nevanlinna--Pick criterion."""

from __future__ import annotations

import numpy as np


def euler_axis_pick_entry(
    eta_left: float,
    value_left: float,
    eta_right: float,
    value_right: float,
) -> float:
    """Return ``(f(x)+f(y))/(x+y)`` for two imaginary-axis data."""

    x = float(eta_left)
    y = float(eta_right)
    if x <= 0.0 or y <= 0.0:
        raise ValueError("imaginary heights must be positive")
    return (float(value_left) + float(value_right)) / (x + y)


def euler_axis_pick_matrix(
    imaginary_heights: tuple[float, ...],
    normalized_reciprocal_log_derivatives: tuple[float, ...],
) -> np.ndarray:
    """Build the real Pick matrix for ``F(i*eta)=i*f(eta)``."""

    if len(imaginary_heights) != len(normalized_reciprocal_log_derivatives):
        raise ValueError("heights and values must have equal length")
    if not imaginary_heights:
        raise ValueError("at least one interpolation node is required")
    heights = np.asarray(imaginary_heights, dtype=float)
    values = np.asarray(normalized_reciprocal_log_derivatives, dtype=float)
    if np.any(heights <= 0.0):
        raise ValueError("imaginary heights must be positive")
    return (values[:, None] + values[None, :]) / (
        heights[:, None] + heights[None, :]
    )


def two_point_pick_determinant(
    eta_left: float,
    value_left: float,
    eta_right: float,
    value_right: float,
) -> float:
    """Return the exact two-node determinant in its factored form.

    If ``x,y`` are the heights and ``a=f(x), b=f(y)``, then

    ``det K = ((x*a-y*b)*(x*b-y*a))/(x*y*(x+y)^2)``.
    """

    x = float(eta_left)
    y = float(eta_right)
    if x <= 0.0 or y <= 0.0:
        raise ValueError("imaginary heights must be positive")
    a = float(value_left)
    b = float(value_right)
    numerator = (x * a - y * b) * (x * b - y * a)
    return numerator / (x * y * (x + y) ** 2)


def two_point_log_derivative_gate(
    imaginary_height: float,
    completed_log_derivative: float,
    completed_log_derivative_derivative: float,
) -> float:
    """Return the differential gate ``L(eta)-eta*L'(eta)``.

    For ``f=1/(c*L)`` this is nonnegative exactly when ``eta*f(eta)``
    is locally nondecreasing.  It is the coalescing-node limit of one factor
    in the two-by-two Pick determinant, not the full Pick criterion.
    """

    eta = float(imaginary_height)
    if eta <= 0.0:
        raise ValueError("imaginary_height must be positive")
    return float(completed_log_derivative) - eta * float(
        completed_log_derivative_derivative
    )
