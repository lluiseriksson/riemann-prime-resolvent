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
