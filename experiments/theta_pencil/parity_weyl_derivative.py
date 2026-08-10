"""Parity-sector form of the canonical Weyl derivative at the base point."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ParityWeylDerivativeAudit:
    even_resolvent_mass: float
    odd_resolvent_mass: float
    parity_cross_mass: float
    direct_channel_ratio: float
    parity_channel_ratio: float
    canonical_derivative: float
    parity_identity_residual: float


@dataclass(frozen=True)
class ImaginaryAxisParityAudit:
    direct_fourier_ratio: float
    parity_resolvent_ratio: float
    even_cross_mass: float
    odd_cross_mass: float
    parity_identity_residual: float


def parity_ratio_from_target_derivative(target_derivative: float) -> float:
    """Convert ``m'(i)`` into the required odd/even resolvent-mass ratio.

    With ``q=(E-O)/(E+O)`` and ``m'(i)=-q``, one has
    ``O/E=(1+m'(i))/(1-m'(i))``.
    """

    derivative = float(target_derivative)
    if not -1.0 < derivative < 1.0:
        raise ValueError("target_derivative must lie strictly between -1 and 1")
    return (1.0 + derivative) / (1.0 - derivative)


def schwarz_pick_parity_interval(
    target_derivative: float,
    imaginary_height: float,
) -> tuple[float, float]:
    """Return the sharp parity interval forced by one-point calibration.

    For a real-symmetric Herglotz function with ``m(i)=i`` and
    ``m'(i)=d``, Schwarz--Pick implies, at ``eta >= 1``,

    ``-eta*kappa <= r(i*eta) <= -kappa/eta``,

    where ``kappa=(1+d)/(1-d)`` and ``r`` is the Fourier parity ratio.
    """

    eta = float(imaginary_height)
    if eta < 1.0:
        raise ValueError("imaginary_height must be at least one")
    kappa = parity_ratio_from_target_derivative(target_derivative)
    return -eta * kappa, -kappa / eta


def second_schur_parameter_from_parity_ratio(
    target_derivative: float,
    imaginary_height: float,
    parity_ratio: float,
) -> float:
    """Recover the second Schur parameter from ``r(i*eta)``.

    With ``w=(eta-1)/(eta+1)``, ``h=(r+1)/(r-1)``, and
    ``d=m'(i)``, this is

    ``q=(h-d)/(w*(1-d*h))``.

    Calibrated Herglotz functions have ``q in [-1, 1]`` on this real radius.
    The lower Schwarz--Pick extremal for ``r`` corresponds to ``q=1``.
    """

    derivative = float(target_derivative)
    parity_ratio_from_target_derivative(derivative)
    eta = float(imaginary_height)
    if eta <= 1.0:
        raise ValueError("imaginary_height must exceed one")
    ratio = float(parity_ratio)
    if ratio == 1.0:
        raise ZeroDivisionError("the parity ratio gives an infinite h value")
    w = (eta - 1.0) / (eta + 1.0)
    h_value = (ratio + 1.0) / (ratio - 1.0)
    denominator = w * (1.0 - derivative * h_value)
    if denominator == 0.0:
        raise ZeroDivisionError("the second Schur parameter has a pole")
    return (h_value - derivative) / denominator


def schwarz_pick_excess_from_second_schur_parameter(
    target_derivative: float,
    imaginary_height: float,
    second_schur_parameter: float,
) -> float:
    """Evaluate the exact Schwarz--Pick excess from the second parameter.

    The identity is

    ``Delta = kappa*(eta-1)*(1-q)/(1-w*q)``.
    """

    eta = float(imaginary_height)
    if eta <= 1.0:
        raise ValueError("imaginary_height must exceed one")
    q_value = float(second_schur_parameter)
    w = (eta - 1.0) / (eta + 1.0)
    denominator = 1.0 - w * q_value
    if denominator == 0.0:
        raise ZeroDivisionError("the Schwarz--Pick excess has a pole")
    kappa = parity_ratio_from_target_derivative(target_derivative)
    return kappa * (eta - 1.0) * (1.0 - q_value) / denominator


def schwarz_pick_extremal_weyl(
    target_derivative: float,
    spectral_parameter: complex,
) -> complex:
    """Return the unique lower-endpoint extremal after calibration at ``i``.

    Equality in Schwarz--Pick at one further imaginary point forces

    ``m_*(z)=((1+d)z^2+d-1)/(2z)``.

    In terms of ``kappa=(1+d)/(1-d)``, this is the convex Herglotz mixture

    ``m_*(z) = (kappa*z - 1/z)/(1+kappa)``

    of the two universal parity endpoints ``z`` and ``-1/z``.
    """

    derivative = float(target_derivative)
    kappa = parity_ratio_from_target_derivative(derivative)
    z = complex(spectral_parameter)
    if z == 0.0:
        raise ZeroDivisionError("the extremal Weyl function has a pole at zero")
    return (kappa * z - 1.0 / z) / (1.0 + kappa)


def parity_weyl_derivative_audit(
    operator: np.ndarray,
    metric: np.ndarray,
    plus_vector: np.ndarray,
    minus_vector: np.ndarray,
    shift: float,
) -> ParityWeylDerivativeAudit:
    """Audit ``m'(i)=-(E-O)/(E+O)`` for reflection-separated channels.

    At ``z=i`` the observation vector equals the minus channel. Splitting
    ``f+ = c+s`` and ``f- = c-s`` gives the displayed identity when the
    resolvent preserves parity, equivalently when ``<c,R s>=0``. The audit
    reports this cross term rather than assuming it away.
    """

    matrix = np.asarray(operator, dtype=float)
    gram = np.asarray(metric, dtype=float)
    plus = np.asarray(plus_vector, dtype=float)
    minus = np.asarray(minus_vector, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("operator must be square")
    if gram.shape != matrix.shape:
        raise ValueError("metric has the wrong shape")
    dimension = matrix.shape[0]
    if plus.shape != (dimension,) or minus.shape != (dimension,):
        raise ValueError("channel vectors have the wrong shape")
    pencil = matrix - shift * gram
    even = (plus + minus) / 2.0
    odd = (plus - minus) / 2.0
    even_solution = np.linalg.solve(pencil, even)
    odd_solution = np.linalg.solve(pencil, odd)
    even_mass = float(even @ even_solution)
    odd_mass = float(odd @ odd_solution)
    cross_mass = float(even @ odd_solution)
    plus_solution = even_solution + odd_solution
    minus_solution = even_solution - odd_solution
    numerator = float(minus @ plus_solution)
    denominator = float(minus @ minus_solution)
    if abs(denominator) == 0.0 or abs(even_mass + odd_mass) == 0.0:
        raise ZeroDivisionError("a derivative channel denominator vanishes")
    direct_ratio = numerator / denominator
    parity_ratio = (even_mass - odd_mass) / (even_mass + odd_mass)
    return ParityWeylDerivativeAudit(
        even_resolvent_mass=even_mass,
        odd_resolvent_mass=odd_mass,
        parity_cross_mass=cross_mass,
        direct_channel_ratio=direct_ratio,
        parity_channel_ratio=parity_ratio,
        canonical_derivative=-direct_ratio,
        parity_identity_residual=float(abs(direct_ratio - parity_ratio)),
    )


def imaginary_axis_parity_ratio_audit(
    operator: np.ndarray,
    metric: np.ndarray,
    plus_source: np.ndarray,
    minus_source: np.ndarray,
    positive_observation: np.ndarray,
    negative_observation: np.ndarray,
    shift: float,
) -> ImaginaryAxisParityAudit:
    """Audit the real resolvent formula for ``r(i*eta)``.

    The source pair represents ``exp(plus_or_minus x)`` and the observation
    pair represents ``exp(plus_or_minus eta*x)``. Reflection invariance kills
    the two mixed parity masses and gives

    ``r(i*eta) = -<sinh(eta*x),R sinh(x)> / <cosh(eta*x),R cosh(x)>``.
    """

    matrix = np.asarray(operator, dtype=float)
    gram = np.asarray(metric, dtype=float)
    plus = np.asarray(plus_source, dtype=float)
    minus = np.asarray(minus_source, dtype=float)
    positive = np.asarray(positive_observation, dtype=float)
    negative = np.asarray(negative_observation, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("operator must be square")
    if gram.shape != matrix.shape:
        raise ValueError("metric has the wrong shape")
    dimension = matrix.shape[0]
    for vector in (plus, minus, positive, negative):
        if vector.shape != (dimension,):
            raise ValueError("channel vectors have the wrong shape")

    pencil = matrix - float(shift) * gram
    plus_solution = np.linalg.solve(pencil, plus)
    value_at_positive_imaginary = float(negative @ plus_solution)
    value_at_negative_imaginary = float(positive @ plus_solution)
    direct_denominator = (
        value_at_positive_imaginary + value_at_negative_imaginary
    )
    if abs(direct_denominator) == 0.0:
        raise ZeroDivisionError("the even Fourier channel vanishes")
    direct_ratio = (
        value_at_positive_imaginary - value_at_negative_imaginary
    ) / direct_denominator

    even_source = (plus + minus) / 2.0
    odd_source = (plus - minus) / 2.0
    even_observation = (positive + negative) / 2.0
    odd_observation = (positive - negative) / 2.0
    even_solution = np.linalg.solve(pencil, even_source)
    odd_solution = np.linalg.solve(pencil, odd_source)
    even_mass = float(even_observation @ even_solution)
    odd_mass = float(odd_observation @ odd_solution)
    if abs(even_mass) == 0.0:
        raise ZeroDivisionError("the even resolvent channel vanishes")
    parity_ratio = -odd_mass / even_mass
    return ImaginaryAxisParityAudit(
        direct_fourier_ratio=direct_ratio,
        parity_resolvent_ratio=parity_ratio,
        even_cross_mass=float(even_observation @ odd_solution),
        odd_cross_mass=float(odd_observation @ even_solution),
        parity_identity_residual=float(abs(direct_ratio - parity_ratio)),
    )
