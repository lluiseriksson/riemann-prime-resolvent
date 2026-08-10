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


def projective_cross_ratio(values: tuple[complex, complex, complex, complex]) -> complex:
    """Return a cross-ratio, invariant under a constant Möbius map."""

    first, second, third, fourth = values
    denominator = (first - fourth) * (second - third)
    if abs(denominator) == 0.0:
        raise ZeroDivisionError("the cross-ratio is degenerate")
    return (first - third) * (second - fourth) / denominator


def shifted_herglotz_value(value: complex, shift: float) -> complex:
    """Apply the real Möbius shift ``m -> m/(1-shift*m)``."""

    denominator = 1.0 - shift * value
    if abs(denominator) == 0.0:
        raise ZeroDivisionError("the shifted Herglotz value has a pole")
    return value / denominator


def unshift_herglotz_value(value: complex, shift: float) -> complex:
    """Invert :func:`shifted_herglotz_value`."""

    denominator = 1.0 + shift * value
    if abs(denominator) == 0.0:
        raise ZeroDivisionError("the inverse Möbius normalization has a pole")
    return value / denominator


def exact_unshift_error(value: complex, error: complex, shift: float) -> complex:
    """Return the exact error after undoing a shifted noisy value.

    If ``w = value/(1-shift*value)`` and only ``w+error`` is known, this
    equals ``unshift(w+error)-value``.  The formula exposes the quadratic
    amplification in a large shift.
    """

    factor = 1.0 - shift * value
    denominator = 1.0 + shift * error * factor
    if abs(denominator) == 0.0:
        raise ZeroDivisionError("the perturbed inverse normalization has a pole")
    return error * factor * factor / denominator


@dataclass(frozen=True)
class ResolventShiftAudit:
    lower_shift: float
    upper_shift: float
    lower_gap: float
    upper_gap: float
    difference_norm: float
    identity_residual: float
    norm_bound: float


@dataclass(frozen=True)
class TwoChannelShiftAudit:
    """Exact shift law for a quotient of two resolvent matrix elements.

    If ``R_t = (A-tG)^-1``, ``N_t = ell(R_t u)`` and
    ``D_t = ell(R_t v)``, the quotient is ``q_t=N_t/D_t``.  The field
    ``cross_difference`` is the numerator of ``q_mu-q_lambda``.  Its
    predicted value uses only the resolvent identity

    ``R_mu-R_lambda = (mu-lambda) R_mu G R_lambda``.
    """

    lower_shift: float
    upper_shift: float
    lower_ratio: complex
    upper_ratio: complex
    cross_difference: complex
    predicted_cross_difference: complex
    identity_residual: float
    lower_ratio_derivative: complex


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


def audit_two_channel_shift(
    operator: np.ndarray,
    plus_vector: np.ndarray,
    minus_vector: np.ndarray,
    observation: np.ndarray,
    lower_shift: float,
    upper_shift: float,
    metric: np.ndarray | None = None,
) -> TwoChannelShiftAudit:
    """Audit the exact shift dependence of a two-channel resolvent ratio.

    ``operator`` and ``metric`` may be weak Galerkin matrices.  The
    observation is a complex-linear row functional, so this routine uses a
    transpose product rather than a Hermitian inner product.  This matches
    Fourier evaluation ``integral v(x) exp(i z x) dx``.
    """

    matrix = np.asarray(operator, dtype=float)
    plus = np.asarray(plus_vector, dtype=float)
    minus = np.asarray(minus_vector, dtype=float)
    functional = np.asarray(observation, dtype=complex)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("operator must be square")
    dimension = matrix.shape[0]
    if plus.shape != (dimension,) or minus.shape != (dimension,):
        raise ValueError("channel vectors have the wrong shape")
    if functional.shape != (dimension,):
        raise ValueError("observation has the wrong shape")
    if not np.allclose(matrix, matrix.T, atol=1.0e-14, rtol=0.0):
        raise ValueError("operator must be self-adjoint")

    gram = np.eye(dimension) if metric is None else np.asarray(metric, dtype=float)
    if gram.shape != matrix.shape:
        raise ValueError("metric has the wrong shape")
    if not np.allclose(gram, gram.T, atol=1.0e-14, rtol=0.0):
        raise ValueError("metric must be self-adjoint")
    if float(np.linalg.eigvalsh(gram)[0]) <= 0.0:
        raise ValueError("metric must be positive definite")

    def channels(shift: float) -> tuple[np.ndarray, np.ndarray, complex, complex]:
        pencil = matrix - shift * gram
        plus_solution = np.linalg.solve(pencil, plus)
        minus_solution = np.linalg.solve(pencil, minus)
        return (
            plus_solution,
            minus_solution,
            complex(functional @ plus_solution),
            complex(functional @ minus_solution),
        )

    low_plus, low_minus, low_numerator, low_denominator = channels(lower_shift)
    high_plus, high_minus, high_numerator, high_denominator = channels(upper_shift)
    if abs(low_denominator) == 0.0 or abs(high_denominator) == 0.0:
        raise ZeroDivisionError("the denominator channel vanishes")

    cross = high_numerator * low_denominator - low_numerator * high_denominator
    high_pencil = matrix - upper_shift * gram
    mixed_plus = np.linalg.solve(high_pencil, gram @ low_plus)
    mixed_minus = np.linalg.solve(high_pencil, gram @ low_minus)
    mixed_numerator = complex(functional @ mixed_plus)
    mixed_denominator = complex(functional @ mixed_minus)
    predicted = (upper_shift - lower_shift) * (
        mixed_numerator * low_denominator
        - low_numerator * mixed_denominator
    )

    low_pencil = matrix - lower_shift * gram
    derivative_plus = np.linalg.solve(low_pencil, gram @ low_plus)
    derivative_minus = np.linalg.solve(low_pencil, gram @ low_minus)
    numerator_derivative = complex(functional @ derivative_plus)
    denominator_derivative = complex(functional @ derivative_minus)
    ratio_derivative = (
        numerator_derivative * low_denominator
        - low_numerator * denominator_derivative
    ) / (low_denominator * low_denominator)

    return TwoChannelShiftAudit(
        lower_shift=lower_shift,
        upper_shift=upper_shift,
        lower_ratio=low_numerator / low_denominator,
        upper_ratio=high_numerator / high_denominator,
        cross_difference=cross,
        predicted_cross_difference=predicted,
        identity_residual=float(abs(cross - predicted)),
        lower_ratio_derivative=ratio_derivative,
    )
