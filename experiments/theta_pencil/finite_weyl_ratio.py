"""Finite resolvent model for the two-extension Weyl-function route."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def finite_weyl_function(
    operator: np.ndarray, cyclic_vector: np.ndarray, z: complex
) -> complex:
    """Return ``<e, (J-zI)^-1 e>`` for a finite self-adjoint model."""

    matrix = np.asarray(operator, dtype=float)
    vector = np.asarray(cyclic_vector, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("operator must be square")
    if vector.shape != (matrix.shape[0],):
        raise ValueError("cyclic_vector has the wrong shape")
    if not np.allclose(matrix, matrix.T, atol=1.0e-14, rtol=0.0):
        raise ValueError("operator must be self-adjoint")
    resolvent_vector = np.linalg.solve(
        matrix.astype(complex) - z * np.eye(len(matrix)), vector
    )
    return complex(np.vdot(vector, resolvent_vector))


@dataclass(frozen=True)
class ResolventShiftAudit:
    lower_shift: float
    upper_shift: float
    lower_gap: float
    upper_gap: float
    difference_norm: float
    identity_residual: float
    norm_bound: float


def audit_resolvent_shift(
    operator: np.ndarray,
    vector: np.ndarray,
    lower_shift: float,
    upper_shift: float,
) -> ResolventShiftAudit:
    """Check the resolvent identity and its spectral-gap sensitivity bound."""

    matrix = np.asarray(operator, dtype=float)
    vector = np.asarray(vector, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("operator must be square")
    if vector.shape != (matrix.shape[0],):
        raise ValueError("vector has the wrong shape")
    if not np.allclose(matrix, matrix.T, atol=1.0e-14, rtol=0.0):
        raise ValueError("operator must be self-adjoint")
    ground = float(np.linalg.eigvalsh(matrix)[0])
    if not lower_shift < ground or not upper_shift < ground:
        raise ValueError("both shifts must lie below the spectrum")

    identity = np.eye(len(matrix))
    lower_resolvent = np.linalg.inv(matrix - lower_shift * identity)
    upper_resolvent = np.linalg.inv(matrix - upper_shift * identity)
    difference = upper_resolvent @ vector - lower_resolvent @ vector
    predicted = (
        (upper_shift - lower_shift)
        * upper_resolvent
        @ lower_resolvent
        @ vector
    )
    lower_gap = ground - lower_shift
    upper_gap = ground - upper_shift
    bound = (
        abs(upper_shift - lower_shift)
        * np.linalg.norm(vector)
        / (lower_gap * upper_gap)
    )
    return ResolventShiftAudit(
        lower_shift=lower_shift,
        upper_shift=upper_shift,
        lower_gap=lower_gap,
        upper_gap=upper_gap,
        difference_norm=float(np.linalg.norm(difference)),
        identity_residual=float(np.linalg.norm(difference - predicted)),
        norm_bound=float(bound),
    )
