"""Stable exact band for a touching logarithmic block.

The second-Green decomposition is useful only if its singular and analytic
pieces are recombined before taking norms.  This module evaluates that signed
sum with Legendre-Q coefficients, avoiding both high monomial expansions and
the catastrophic separate Wang bounds on a short source interval.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

import numpy as np

from experiments.theta_pencil.arb_adjacent_singular_gram import (
    _build_adjacent_singular_map,
)
from experiments.theta_pencil.arb_cut_dominant import (
    _local_legendre_coefficients,
)
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_second_green_tail import (
    _source_decomposition,
)


@dataclass(frozen=True)
class ArbAdjacentFullMap:
    midpoint: np.ndarray
    radius: np.ndarray
    target_length: float
    source_length: float
    source_degree_count: int
    first_degree: int
    last_degree: int
    precision: int
    working_precision: int


@dataclass(frozen=True)
class AdjacentAnalyticTailBound:
    target_length: float
    source_length: float
    source_degree_count: int
    first_degree: int
    geometric_ratio_upper: float
    frobenius_upper: float
    precision: int


@lru_cache(maxsize=None)
def _wigner_zero_band(left: int, right: int):
    """All nonzero zero-magnetic Wigner squares via a rational recurrence."""

    if min(left, right) < 0:
        return {}
    small = min(left, right)
    large = max(left, right)
    middle = large - small
    value = Fraction(
        math.comb(large, small) ** 2,
        (2 * large + 1) * math.comb(2 * large, 2 * small),
    )
    result = {middle: value}
    while middle < left + right:
        semiperimeter = (left + middle + right) // 2
        a = 2 * semiperimeter - 2 * left
        b = 2 * semiperimeter - 2 * middle
        c = 2 * semiperimeter - 2 * right
        d = 2 * semiperimeter + 1
        ratio = Fraction(
            (a + 1)
            * (a + 2)
            * (c + 1)
            * (c + 2)
            * (semiperimeter + 1) ** 2
            * (semiperimeter - middle) ** 2,
            b
            * (b - 1)
            * (d + 1)
            * (d + 2)
            * (semiperimeter - left + 1) ** 2
            * (semiperimeter - right + 1) ** 2,
        )
        value *= ratio
        middle += 2
        result[middle] = value
    return result


def _wigner_zero_square(left: int, middle: int, right: int) -> Fraction:
    """Return ``wigner_3j(left,middle,right;0,0,0)^2`` exactly."""

    return _wigner_zero_band(left, right).get(middle, Fraction(0))


def _ordinary_reflected_legendre_map(
    arb, target_length, source_length, count, shift=None
):
    """Ordinary target-Legendre coefficients of every ``f_k(-shift-u)``."""

    source_rows = _local_legendre_coefficients(
        arb, source_length, count, reversed_=False
    )
    target_rows = _local_legendre_coefficients(
        arb, target_length, count, reversed_=False
    )
    result = [[arb(0) for _ in range(count)] for _ in range(count)]
    shift = arb(0) if shift is None else shift
    for source_degree, source in enumerate(source_rows):
        _, reflected = _source_decomposition(source, source_length, arb)
        shifted = [arb(0) for _ in range(count)]
        for power, coefficient in enumerate(reflected):
            for degree in range(power + 1):
                shifted[degree] += (
                    coefficient
                    * math.comb(power, degree)
                    * shift ** (power - degree)
                )
        for target_degree, target in enumerate(target_rows):
            normalized_coefficient = sum(
                (
                    left_value
                    * right_value
                    * target_length ** (left + right + 1)
                    / (left + right + 1)
                    for left, left_value in enumerate(shifted)
                    for right, right_value in enumerate(target)
                ),
                arb(0),
            )
            result[target_degree][source_degree] = normalized_coefficient * (
                arb(2 * target_degree + 1) / target_length
            ).sqrt()
    return result


def _legendre_q_sequence(arb, acb, z, first: int, last: int):
    """Classical real ``Q_n(z)`` by independent certified evaluations.

    A downward recurrence is accurate at midpoint level but its interval
    radii acquire the dominant Legendre-P solution in the long--short
    orientations.  Independent type-3 evaluations avoid that enclosure
    instability.
    """

    if first < 0 or last <= first:
        raise ValueError("invalid Legendre-Q range")
    z_complex = acb(z)
    q = {
        degree: z_complex.legendre_q(degree, 0, 3).real
        for degree in range(first, last + 2)
    }
    if not all(value.is_finite() for value in q.values()):
        raise ArithmeticError("a Legendre-Q value was unresolved")
    return q


def _cached_legendre_q_sequence(arb, acb, z, first, last, cache):
    if cache is None:
        return _legendre_q_sequence(arb, acb, z, first, last)
    key = (str(z), first, last)
    if key not in cache:
        cache[key] = _legendre_q_sequence(arb, acb, z, first, last)
    return cache[key]


def _build_adjacent_full_matrix(
    arb,
    arb_mat,
    acb,
    target_length,
    source_length,
    source_degree_count: int,
    first_degree: int,
    last_degree: int,
    q_cache=None,
):
    """Build the map at the caller's precision from already enclosed lengths."""

    a = target_length
    b = source_length
    singular_map = _build_adjacent_singular_map(
        arb, arb_mat, a, b, source_degree_count
    )
    ordinary = _ordinary_reflected_legendre_map(
        arb, a, b, source_degree_count
    )
    first_q = first_degree - source_degree_count
    last_q = last_degree + source_degree_count
    q = _cached_legendre_q_sequence(
        arb, acb, 1 + 2 * b / a, first_q, last_q, q_cache
    )
    matrix = arb_mat(last_degree - first_degree, source_degree_count)
    for row, degree in enumerate(range(first_degree, last_degree)):
        eigenvalue = degree * (degree + 1)
        for source_degree in range(source_degree_count):
            flux = -(
                (-1 if source_degree % 2 else 1)
                * arb((2 * degree + 1) * (2 * source_degree + 1)).sqrt()
                * (a / b).sqrt()
                / (2 * eigenvalue)
            )
            singular = sum(
                (
                    -arb((2 * degree + 1) * (2 * low + 1)).sqrt()
                    / (eigenvalue - low * (low + 1))
                    * singular_map[low, source_degree]
                    / eigenvalue
                    for low in range(source_degree_count)
                ),
                arb(0),
            )
            analytic = arb(0)
            for polynomial_degree in range(source_degree_count):
                for log_degree in range(
                    abs(degree - polynomial_degree),
                    degree + polynomial_degree + 1,
                    2,
                ):
                    coefficient = _wigner_zero_square(
                        polynomial_degree, log_degree, degree
                    )
                    if not coefficient:
                        continue
                    legendre_log = (
                        (-1 if log_degree % 2 else 1)
                        * (q[log_degree + 1] - q[log_degree - 1])
                    )
                    analytic += (
                        ordinary[polynomial_degree][source_degree]
                        * legendre_log
                        * arb(coefficient.numerator)
                        / coefficient.denominator
                    )
            analytic *= -(
                (-1 if degree % 2 else 1)
                * (a * (2 * degree + 1)).sqrt()
                / 2
            )
            matrix[row, source_degree] = flux + singular + analytic
    return matrix


def _build_separated_full_matrix(
    arb,
    arb_mat,
    acb,
    target_length,
    source_length,
    gap,
    source_degree_count: int,
    first_degree: int,
    last_degree: int,
    q_cache=None,
):
    """Build one strictly separated block in the left-target orientation."""

    a = target_length
    b = source_length
    ordinary = _ordinary_reflected_legendre_map(
        arb, a, b, source_degree_count, gap
    )
    first_q = first_degree - source_degree_count
    last_q = last_degree + source_degree_count
    q_plus = _cached_legendre_q_sequence(
        arb,
        acb,
        1 + 2 * (gap + b) / a,
        first_q,
        last_q,
        q_cache,
    )
    q_minus = _cached_legendre_q_sequence(
        arb,
        acb,
        1 + 2 * gap / a,
        first_q,
        last_q,
        q_cache,
    )
    matrix = arb_mat(last_degree - first_degree, source_degree_count)
    for row, degree in enumerate(range(first_degree, last_degree)):
        for source_degree in range(source_degree_count):
            value = arb(0)
            for polynomial_degree in range(source_degree_count):
                for log_degree in range(
                    abs(degree - polynomial_degree),
                    degree + polynomial_degree + 1,
                    2,
                ):
                    coefficient = _wigner_zero_square(
                        polynomial_degree, log_degree, degree
                    )
                    if not coefficient:
                        continue
                    sign = -1 if log_degree % 2 else 1
                    log_plus = sign * (
                        q_plus[log_degree + 1] - q_plus[log_degree - 1]
                    )
                    log_minus = sign * (
                        q_minus[log_degree + 1] - q_minus[log_degree - 1]
                    )
                    value += (
                        ordinary[polynomial_degree][source_degree]
                        * (log_plus - log_minus)
                        * arb(coefficient.numerator)
                        / coefficient.denominator
                    )
            value *= -(
                (-1 if degree % 2 else 1)
                * (a * (2 * degree + 1)).sqrt()
                / 2
            )
            matrix[row, source_degree] = value
    return matrix


def build_arb_adjacent_full_map(
    target_length,
    source_length,
    source_degree_count: int,
    first_degree: int,
    last_degree: int,
    precision: int = 512,
) -> ArbAdjacentFullMap:
    """Enclose the exact touching-block coefficients in one orientation.

    The target is the interval to the left of the source.  Rows are target
    degrees ``first_degree <= n < last_degree``; columns are normalized local
    source degrees.  Reflection gives the opposite orientation by multiplying
    entry ``(n,k)`` by ``(-1)^(n+k)``.
    """

    if source_degree_count < 1 or first_degree < source_degree_count:
        raise ValueError("the target band must start above the source degree")
    if last_degree <= first_degree:
        raise ValueError("the target band must be nonempty")
    try:
        from flint import acb, arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        # Q_n(cosh eta) is exponentially small.  Direct endpoint evaluation
        # therefore needs about n*eta/log(2) guard bits for direct evaluation.
        ctx.prec = max(precision, 128)
        a = (
            arb(str(target_length))
            if isinstance(target_length, (int, float))
            else arb(target_length)
        )
        b = (
            arb(str(source_length))
            if isinstance(source_length, (int, float))
            else arb(source_length)
        )
        if not a.lower() > 0 or not b.lower() > 0:
            raise ValueError("interval lengths must be strictly positive")
        eta = (1 + 2 * b / a).acosh()
        working_precision = max(
            precision,
            math.ceil(
                (last_degree + source_degree_count + 2)
                * float(eta.upper())
                / math.log(2)
            )
            + precision
            + 128,
        )
        ctx.prec = working_precision
        a = (
            arb(str(target_length))
            if isinstance(target_length, (int, float))
            else arb(target_length)
        )
        b = (
            arb(str(source_length))
            if isinstance(source_length, (int, float))
            else arb(source_length)
        )

        matrix = _build_adjacent_full_matrix(
            arb,
            arb_mat,
            acb,
            a,
            b,
            source_degree_count,
            first_degree,
            last_degree,
            None,
        )

        midpoint = np.empty((matrix.nrows(), matrix.ncols()), dtype=float)
        radius = np.empty_like(midpoint)
        for row in range(matrix.nrows()):
            for column in range(matrix.ncols()):
                midpoint[row, column] = float(matrix[row, column].mid())
                radius[row, column] = _arb_radius_as_float(matrix[row, column])
    finally:
        ctx.prec = previous_precision

    return ArbAdjacentFullMap(
        midpoint=midpoint,
        radius=radius,
        target_length=float(a.mid()),
        source_length=float(b.mid()),
        source_degree_count=source_degree_count,
        first_degree=first_degree,
        last_degree=last_degree,
        precision=precision,
        working_precision=working_precision,
    )


def certify_adjacent_analytic_tail(
    target_length,
    source_length,
    source_degree_count: int,
    first_degree: int,
    precision: int = 512,
) -> AdjacentAnalyticTailBound:
    """Bound the recombined analytic potential above ``first_degree``.

    If ``z=cosh(eta)=1+2b/a``, Heine's integral bounds the ordinary
    Legendre coefficient of ``log(u+b)`` by ``Q_{m-1}(z)``.  Positivity of
    the Legendre product linearization gives

      sum_m (3j(j,m,n;0,0,0))^2 <= 1/(2(n-j)+1).

    Consequently every source column has an explicit geometric envelope.
    This retains the exact low-degree polynomial coefficients instead of the
    exponentially bad supremum of that polynomial outside its source block.
    """

    if source_degree_count < 1 or first_degree <= source_degree_count + 1:
        raise ValueError("first_degree must exceed the source degree by two")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = (
            arb(str(target_length))
            if isinstance(target_length, (int, float))
            else arb(target_length)
        )
        b = (
            arb(str(source_length))
            if isinstance(source_length, (int, float))
            else arb(source_length)
        )
        if not a.lower() > 0 or not b.lower() > 0:
            raise ValueError("interval lengths must be strictly positive")
        eta = (1 + 2 * b / a).acosh()
        ordinary = _ordinary_reflected_legendre_map(
            arb, a, b, source_degree_count
        )
        column_square = arb(0)
        for source_degree in range(source_degree_count):
            envelope = arb(0)
            for polynomial_degree in range(source_degree_count):
                log_degree = first_degree - polynomial_degree
                q_upper = (
                    arb.pi()
                    * eta.exp()
                    / (2 * (log_degree - 1) * eta.sinh())
                ).sqrt() * (-log_degree * eta).exp()
                envelope += (
                    ordinary[polynomial_degree][source_degree].abs_upper()
                    * q_upper
                    / (2 * log_degree + 1)
                )
            envelope *= (a * (2 * first_degree + 1)).sqrt() / 2
            column_square += envelope**2
        ratio = (-eta).exp() * (
            arb(2 * first_degree + 3) / (2 * first_degree + 1)
        ).sqrt()
        if not ratio.upper() < 1:
            raise ArithmeticError("the analytic tail ratio was not below one")
        total = (column_square / (1 - ratio**2)).sqrt()
    finally:
        ctx.prec = previous_precision

    return AdjacentAnalyticTailBound(
        target_length=float(a.mid()),
        source_length=float(b.mid()),
        source_degree_count=source_degree_count,
        first_degree=first_degree,
        geometric_ratio_upper=math.nextafter(float(ratio.upper()), math.inf),
        frobenius_upper=math.nextafter(float(total.upper()), math.inf),
        precision=precision,
    )
