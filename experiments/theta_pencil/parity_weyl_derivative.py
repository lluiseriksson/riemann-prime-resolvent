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
