"""Rank--trace--inertia diagnostics for finite Weil compressions.

The exact scalar functions in this module package the linear-algebraic core
of the 2026 two-thirds theorem.  The matrix audit is deliberately labelled a
floating-point diagnostic: first and second trace moments can force positive
directions, but they prove positive semidefiniteness only when they force all
directions.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, replace
from fractions import Fraction
from typing import TypeAlias

import numpy as np


Rational: TypeAlias = Fraction | int


def _fraction(value: Rational) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


@dataclass(frozen=True)
class ExactMomentCertificate:
    continuous_lower: Fraction
    forced_integer_lower: int


@dataclass(frozen=True)
class FloatingInertiaAudit:
    dimension: int
    trace: float
    frobenius_squared: float
    moment_lower: float
    moment_forced_positive_count: int
    observed_negative_count: int
    observed_positive_count: int
    observed_unresolved_count: int
    least_eigenvalue: float
    greatest_eigenvalue: float
    context: str = "floating-point diagnostic; not an interval certificate"


@dataclass(frozen=True)
class FloatingSchurInertiaAudit:
    source_dimension: int
    finite_dimension: int
    tail_least_eigenvalue: float
    even: FloatingInertiaAudit
    odd: FloatingInertiaAudit
    combined: FloatingInertiaAudit
    context: str = (
        "finite-section Schur diagnostic; the infinite cross tail is omitted"
    )


def rank_trace_lower_bound(
    trace_positive_part: Rational,
    trace_indefinite_part: Rational,
    positive_index_indefinite_part: int,
    frobenius_squared_total: Rational,
) -> ExactMomentCertificate:
    """Return the exact rank lower bound from the rank--trace lemma.

    If ``G = P + Q``, ``P`` is positive semidefinite of rank ``r`` and
    ``Q`` has positive index at most ``b``, then

        r >= 2 tr(P) + 4 tr(Q) - 4 b - ||G||_F^2.

    The caller is responsible for establishing that decomposition and the
    positive-index bound.  In particular, splitting a prime-side matrix into
    convenient summands does not automatically provide the zero-side
    hypotheses of the lemma.
    """

    if positive_index_indefinite_part < 0:
        raise ValueError("the positive-index bound must be nonnegative")
    frobenius_squared = _fraction(frobenius_squared_total)
    if frobenius_squared < 0:
        raise ValueError("the squared Frobenius norm must be nonnegative")
    lower = (
        2 * _fraction(trace_positive_part)
        + 4 * _fraction(trace_indefinite_part)
        - 4 * positive_index_indefinite_part
        - frobenius_squared
    )
    return ExactMomentCertificate(lower, max(0, _ceil_fraction(lower)))


def positive_inertia_from_moments(
    trace_total: Rational, frobenius_squared_total: Rational
) -> ExactMomentCertificate:
    """Force positive eigenvalues using only ``tr G`` and ``tr G^2``.

    For Hermitian ``G`` with positive trace,

        n_+(G) >= (tr G)^2 / ||G||_F^2.

    Exact rational inputs make the returned integer lower bound exact.  A
    zero matrix is treated separately; its positive index is zero.
    """

    trace = _fraction(trace_total)
    frobenius_squared = _fraction(frobenius_squared_total)
    if frobenius_squared < 0:
        raise ValueError("the squared Frobenius norm must be nonnegative")
    if trace <= 0 or frobenius_squared == 0:
        return ExactMomentCertificate(Fraction(0), 0)
    lower = trace * trace / frobenius_squared
    return ExactMomentCertificate(lower, _ceil_fraction(lower))


def audit_floating_symmetric_matrix(
    matrix: np.ndarray, zero_tolerance: float = 1.0e-10
) -> FloatingInertiaAudit:
    """Report the moment certificate and observed inertia of a point matrix."""

    array = np.asarray(matrix, dtype=float)
    if array.ndim != 2 or array.shape[0] != array.shape[1] or len(array) == 0:
        raise ValueError("matrix must be nonempty and square")
    if zero_tolerance < 0:
        raise ValueError("zero_tolerance must be nonnegative")
    if not np.allclose(array, array.T, atol=1.0e-12, rtol=0.0):
        raise ValueError("matrix must be symmetric")
    symmetric = 0.5 * (array + array.T)
    eigenvalues = np.linalg.eigvalsh(symmetric)
    trace = float(np.trace(symmetric))
    frobenius_squared = float(np.sum(symmetric * symmetric))
    if trace > 0.0 and frobenius_squared > 0.0:
        moment_lower = trace * trace / frobenius_squared
        conservative = math.nextafter(moment_lower, -math.inf)
        forced = max(0, math.ceil(conservative))
    else:
        moment_lower = 0.0
        forced = 0
    negative = int(np.count_nonzero(eigenvalues < -zero_tolerance))
    positive = int(np.count_nonzero(eigenvalues > zero_tolerance))
    unresolved = len(eigenvalues) - negative - positive
    return FloatingInertiaAudit(
        dimension=len(array),
        trace=trace,
        frobenius_squared=frobenius_squared,
        moment_lower=moment_lower,
        moment_forced_positive_count=min(len(array), forced),
        observed_negative_count=negative,
        observed_positive_count=positive,
        observed_unresolved_count=unresolved,
        least_eigenvalue=float(eigenvalues[0]),
        greatest_eigenvalue=float(eigenvalues[-1]),
    )


def combine_block_audits(
    *audits: FloatingInertiaAudit,
) -> FloatingInertiaAudit:
    """Combine moment and observed-inertia data for a block direct sum."""

    if not audits:
        raise ValueError("at least one block audit is required")
    trace = math.fsum(audit.trace for audit in audits)
    frobenius_squared = math.fsum(
        audit.frobenius_squared for audit in audits
    )
    if trace > 0.0 and frobenius_squared > 0.0:
        moment_lower = trace * trace / frobenius_squared
        forced = math.ceil(math.nextafter(moment_lower, -math.inf))
    else:
        moment_lower = 0.0
        forced = 0
    dimension = sum(audit.dimension for audit in audits)
    return FloatingInertiaAudit(
        dimension=dimension,
        trace=trace,
        frobenius_squared=frobenius_squared,
        moment_lower=moment_lower,
        moment_forced_positive_count=min(dimension, max(0, forced)),
        observed_negative_count=sum(
            audit.observed_negative_count for audit in audits
        ),
        observed_positive_count=sum(
            audit.observed_positive_count for audit in audits
        ),
        observed_unresolved_count=sum(
            audit.observed_unresolved_count for audit in audits
        ),
        least_eigenvalue=min(audit.least_eigenvalue for audit in audits),
        greatest_eigenvalue=max(
            audit.greatest_eigenvalue for audit in audits
        ),
        context="floating block-direct-sum diagnostic; not an interval certificate",
    )


def support_one_source_audit(
    dimension: int = 58,
    quadrature_order: int = 128,
    maximum_smooth_power: int = 95,
) -> tuple[FloatingInertiaAudit, FloatingInertiaAudit]:
    """Audit the raw even/odd support-one source blocks.

    This is not the degree-58 Schur complement: the certified infinite-tail
    floor and the cross correction remain separate obligations.
    """

    from experiments.theta_pencil.legendre_feshbach import (
        build_legendre_weil_components,
    )
    from experiments.theta_pencil.smooth_legendre_series import (
        smooth_kernel_series_matrix,
        smooth_kernel_series_remainder_bound,
    )

    components = build_legendre_weil_components(
        1.0, dimension, quadrature_order
    )
    expected = (2, 3, 4, 5, 7)
    if components.active_prime_powers != expected:
        raise ArithmeticError(
            f"unexpected support-one prime powers: {components.active_prime_powers}"
        )
    matrix = (
        components.dominant
        + components.scalar
        + components.prime
        + smooth_kernel_series_matrix(
            1.0, dimension, maximum_smooth_power
        )
    )
    matrix = 0.5 * (matrix + matrix.T)
    smooth_remainder = smooth_kernel_series_remainder_bound(
        1.0, maximum_smooth_power
    )
    context = (
        "floating source diagnostic with smooth-series remainder "
        f"{smooth_remainder:.17g}; not an interval certificate"
    )
    even = np.arange(0, dimension, 2)
    odd = np.arange(1, dimension, 2)
    return (
        replace(
            audit_floating_symmetric_matrix(
                matrix[np.ix_(even, even)], zero_tolerance=1.0e-12
            ),
            context=context,
        ),
        replace(
            audit_floating_symmetric_matrix(
                matrix[np.ix_(odd, odd)], zero_tolerance=1.0e-12
            ),
            context=context,
        ),
    )


def support_one_finite_schur_audit(
    source_dimension: int = 58,
    finite_dimension: int = 256,
    quadrature_order: int = 1024,
) -> FloatingSchurInertiaAudit:
    """Audit a finite Schur approximation to the support-one source gate."""

    if not 0 < source_dimension < finite_dimension:
        raise ValueError("dimensions must satisfy 0 < source < finite")
    from experiments.theta_pencil.legendre_feshbach import (
        build_legendre_weil_components,
    )

    components = build_legendre_weil_components(
        1.0, finite_dimension, quadrature_order
    )
    expected = (2, 3, 4, 5, 7)
    if components.active_prime_powers != expected:
        raise ArithmeticError(
            f"unexpected support-one prime powers: {components.active_prime_powers}"
        )
    matrix = components.total
    low = matrix[:source_dimension, :source_dimension]
    cross = matrix[:source_dimension, source_dimension:]
    tail = matrix[source_dimension:, source_dimension:]
    tail_eigenvalues = np.linalg.eigvalsh(tail)
    tail_least = float(tail_eigenvalues[0])
    if tail_least <= 0.0:
        raise ArithmeticError("the finite tail block is not positive definite")
    schur = low - np.linalg.solve(tail, cross.T).T @ cross.T
    even_indices = np.arange(0, source_dimension, 2)
    odd_indices = np.arange(1, source_dimension, 2)
    even = audit_floating_symmetric_matrix(
        schur[np.ix_(even_indices, even_indices)]
    )
    odd = audit_floating_symmetric_matrix(
        schur[np.ix_(odd_indices, odd_indices)]
    )
    return FloatingSchurInertiaAudit(
        source_dimension=source_dimension,
        finite_dimension=finite_dimension,
        tail_least_eigenvalue=tail_least,
        even=even,
        odd=odd,
        combined=combine_block_audits(even, odd),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, default=58)
    parser.add_argument("--quadrature", type=int, default=1024)
    parser.add_argument("--finite-dimension", type=int, default=256)
    parser.add_argument("--smooth-power", type=int, default=95)
    arguments = parser.parse_args()
    even, odd = support_one_source_audit(
        arguments.dimension, arguments.quadrature, arguments.smooth_power
    )
    print("even", even)
    print("odd", odd)
    print("combined", combine_block_audits(even, odd))
    print(
        "finite_schur",
        support_one_finite_schur_audit(
            arguments.dimension,
            arguments.finite_dimension,
            arguments.quadrature,
        ),
    )


if __name__ == "__main__":
    main()
