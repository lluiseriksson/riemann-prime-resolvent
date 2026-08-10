"""Exact finite algebra for the Euler-axis Nevanlinna--Pick criterion."""

from __future__ import annotations

import numpy as np


def off_line_orbit_defect_ceiling(verified_height: float) -> float:
    """Return the uniform defect ceiling above a verified RH height.

    If every zero with ``abs(gamma) <= T`` is on the critical line, then every
    hypothetical off-line zero orbit satisfies

    ``delta <= T^2 / (T^2 - 1/4)^2``.
    """

    height = float(verified_height)
    if height <= 0.5:
        raise ValueError("verified_height must exceed 1/2")
    square = height * height
    return square / ((square - 0.25) * (square - 0.25))


def centered_zero_orbit_profile(
    centered_real_part: float,
    zero_height: float,
    imaginary_height: float,
) -> tuple[float, float, float, float]:
    """Return mass, slope, curvature, and lower slack of one zero orbit.

    The orbit is grouped with its conjugate when ``alpha != 0``.  With
    ``t=log(eta)/2``, the returned quantities are

    ``T, p=d(log T)/d(log eta), q=dp/dt, q+2*(1-p^2)``.

    The last entry is zero on the critical line and strictly negative away
    from it.
    """

    alpha = float(centered_real_part)
    gamma = abs(float(zero_height))
    eta = float(imaginary_height)
    if abs(alpha) >= 0.5:
        raise ValueError("centered_real_part must lie in (-1/2,1/2)")
    if gamma <= 0.0 or eta <= 0.0:
        raise ValueError("zero_height and imaginary_height must be positive")
    radius = eta * eta
    offset = gamma * gamma - alpha * alpha
    real_part = radius + offset
    imaginary_square = 4.0 * alpha * alpha * gamma * gamma
    denominator = real_part * real_part + imaginary_square
    orbit_factor = 2.0 if alpha == 0.0 else 4.0
    mass = orbit_factor * eta * real_part / denominator
    slope = (
        1.0
        + 2.0 * radius / real_part
        - 4.0 * radius * real_part / denominator
    )
    slope_radius_derivative = (
        2.0 * offset / (real_part * real_part)
        - 4.0
        * (
            (real_part + radius) / denominator
            - 2.0
            * radius
            * real_part
            * real_part
            / (denominator * denominator)
        )
    )
    curvature = 4.0 * radius * slope_radius_derivative
    lower_slack = (
        -16.0
        * radius
        * radius
        * imaginary_square
        / (real_part * real_part * denominator)
    )
    return mass, slope, curvature, lower_slack


def zero_orbit_mixture_lower_slack(
    orbit_masses: tuple[float, ...],
    orbit_slopes: tuple[float, ...],
    orbit_curvatures: tuple[float, ...],
) -> tuple[float, float]:
    """Return direct and variance-decomposed lower curvature slack.

    For a positive sum of orbit profiles, the exact identity is

    ``q+2*(1-p^2) = E[q_j+2*(1-p_j^2)] + 4*Var(p_j)``.
    """

    masses = np.asarray(orbit_masses, dtype=float)
    slopes = np.asarray(orbit_slopes, dtype=float)
    curvatures = np.asarray(orbit_curvatures, dtype=float)
    if masses.shape != slopes.shape or masses.shape != curvatures.shape:
        raise ValueError("orbit vectors must have equal shape")
    if masses.ndim != 1 or len(masses) == 0 or np.any(masses <= 0.0):
        raise ValueError("orbit masses must form a nonempty positive vector")
    weights = masses / np.sum(masses)
    slope = float(weights @ slopes)
    variance = float(weights @ (slopes * slopes) - slope * slope)
    curvature = float(2.0 * variance + weights @ curvatures)
    direct = curvature + 2.0 * (1.0 - slope * slope)
    component_slacks = curvatures + 2.0 * (1.0 - slopes * slopes)
    decomposed = float(weights @ component_slacks + 4.0 * variance)
    return direct, decomposed


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


def euler_axis_log_derivative_kernel(
    imaginary_heights: tuple[float, ...],
    completed_log_derivatives: tuple[float, ...],
) -> np.ndarray:
    """Build ``H_jk=(L_j+L_k)/(eta_j+eta_k)``.

    If ``f_j=1/(c*L_j)``, the corresponding reciprocal-log-derivative Pick
    matrix is ``K=(1/c) D_L^{-1} H D_L^{-1}``.  Hence the two matrices have
    the same inertia whenever every ``L_j`` and ``c`` are positive.
    """

    return euler_axis_pick_matrix(
        imaginary_heights, completed_log_derivatives
    )


def reciprocal_log_derivative_congruence_residual(
    imaginary_heights: tuple[float, ...],
    completed_log_derivatives: tuple[float, ...],
    positive_normalization: float,
) -> float:
    """Audit the exact diagonal congruence between the two Pick kernels."""

    scale = float(positive_normalization)
    if scale <= 0.0:
        raise ValueError("positive_normalization must be positive")
    log_derivatives = np.asarray(completed_log_derivatives, dtype=float)
    if np.any(log_derivatives == 0.0):
        raise ZeroDivisionError("completed log derivatives must be nonzero")
    reciprocal_values = tuple(1.0 / (scale * log_derivatives))
    reciprocal_pick = euler_axis_pick_matrix(
        imaginary_heights, reciprocal_values
    )
    log_kernel = euler_axis_log_derivative_kernel(
        imaginary_heights, completed_log_derivatives
    )
    inverse_diagonal = np.diag(1.0 / log_derivatives)
    reconstructed = (
        inverse_diagonal @ log_kernel @ inverse_diagonal / scale
    )
    return float(np.max(np.abs(reciprocal_pick - reconstructed)))


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


def centered_zero_orbit_gate_margin(
    centered_real_part: float,
    zero_height: float,
    imaginary_height: float,
) -> float:
    """Return the numerator proving positivity of a conjugate zero orbit.

    For ``a=alpha+i*gamma`` and ``D=eta^2-a^2``, one has

    ``Re(1/D^2) = margin / |D|^4``

    with

    ``margin=(eta^2-alpha^2+gamma^2)^2-(2*alpha*gamma)^2``.

    In the zeta critical strip, ``|alpha|<1/2``. If ``eta>1/2`` and
    ``|gamma|>1``, both factors of the difference of squares are positive.
    """

    alpha = float(centered_real_part)
    gamma = float(zero_height)
    eta = float(imaginary_height)
    if abs(alpha) >= 0.5:
        raise ValueError("centered_real_part must lie in (-1/2,1/2)")
    if abs(gamma) <= 1.0:
        raise ValueError("zero_height must have absolute value greater than one")
    if eta <= 0.5:
        raise ValueError("imaginary_height must exceed one half")
    real_part = eta * eta - alpha * alpha + gamma * gamma
    imaginary_part = 2.0 * alpha * gamma
    return real_part * real_part - imaginary_part * imaginary_part


def normalized_log_derivative_correlation(
    imaginary_heights: tuple[float, ...],
    completed_log_derivatives: tuple[float, ...],
) -> np.ndarray:
    """Normalize the log-derivative Pick kernel to unit diagonal.

    With ``t_j=log(eta_j)/2`` and ``v_j=log(L_j)/2``, the result is exactly

    ``R_jk=cosh(v_j-v_k)/cosh(t_j-t_k)``.
    """

    heights = np.asarray(imaginary_heights, dtype=float)
    values = np.asarray(completed_log_derivatives, dtype=float)
    if heights.shape != values.shape or heights.ndim != 1 or len(heights) == 0:
        raise ValueError("heights and log derivatives must be nonempty vectors")
    if np.any(heights <= 0.0) or np.any(values <= 0.0):
        raise ValueError("heights and log derivatives must be positive")
    log_heights = 0.5 * np.log(heights)
    log_values = 0.5 * np.log(values)
    return np.cosh(log_values[:, None] - log_values[None, :]) / np.cosh(
        log_heights[:, None] - log_heights[None, :]
    )


def local_three_point_curvature_gate(
    logarithmic_slope: float,
    logarithmic_curvature: float,
) -> float:
    """Return the leading confluent three-point Pick determinant coefficient.

    If ``v=v(t)``, ``p=v'(t)``, and ``q=v''(t)``, then for the normalized
    correlation matrix at ``t-h,t,t+h`` one has

    ``det R = (4*(1-p^2)^2-q^2)*h^6 + O(h^8)``.
    """

    slope = float(logarithmic_slope)
    curvature = float(logarithmic_curvature)
    return 4.0 * (1.0 - slope * slope) ** 2 - curvature * curvature
