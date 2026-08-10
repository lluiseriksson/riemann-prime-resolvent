"""Signed Gram matrix for the adjacent second-Green singular tail."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_cut_dominant import (
    _local_legendre_coefficients,
)
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_second_green_tail import (
    _singular_polynomial,
    _source_decomposition,
)


@dataclass(frozen=True)
class ArbAdjacentSingularGram:
    midpoint: np.ndarray
    radius: np.ndarray
    explicit_frobenius_upper: float
    remainder_norm_upper: float
    total_frobenius_upper: float
    degree_count: int
    first_degree: int
    last_degree: int
    moment_order: int
    precision: int


def _float_upper(value) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def _build_adjacent_singular_map(arb, arb_mat, target_length, source_length, degree_count):
    """Return the signed low-degree singular map without float export."""

    source_rows = _local_legendre_coefficients(
        arb, source_length, degree_count, reversed_=False
    )
    target_rows = _local_legendre_coefficients(
        arb, target_length, degree_count, reversed_=True
    )
    decompositions = [
        _source_decomposition(row, source_length, arb) for row in source_rows
    ]
    singular_polynomials = [
        _singular_polynomial(reflected, target_length, arb)
        for _, reflected in decompositions
    ]
    singular_map = arb_mat(degree_count, degree_count)
    for target_degree, target in enumerate(target_rows):
        for source_degree, singular in enumerate(singular_polynomials):
            integral = arb(0)
            for left, left_value in enumerate(target):
                for right, right_value in enumerate(singular):
                    integral += (
                        left_value
                        * right_value
                        * target_length ** (left + right + 1)
                        / (left + right + 1)
                    )
            singular_map[target_degree, source_degree] = integral
    return singular_map


def build_arb_adjacent_singular_gram(
    target_length: float,
    source_length: float,
    degree_count: int = 16,
    first_degree: int = 128,
    last_degree: int = 4096,
    moment_order: int = 8,
    precision: int = 512,
) -> ArbAdjacentSingularGram:
    """Enclose the signed ``sum r_n^* r_n / lambda_n^2`` Gram.

    The explicit rows retain their signs before the outer product.  Only the
    tail beyond ``last_degree`` is replaced by a scalar Frobenius remainder.
    """

    if target_length <= 0 or source_length <= 0:
        raise ValueError("interval lengths must be positive")
    if degree_count < 1 or first_degree <= degree_count:
        raise ValueError("first_degree must exceed degree_count")
    if last_degree <= first_degree or moment_order < 1:
        raise ValueError("invalid last degree or moment order")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = arb(str(target_length))
        b = arb(str(source_length))
        singular_map = _build_adjacent_singular_map(
            arb, arb_mat, a, b, degree_count
        )

        gram = arb_mat(degree_count, degree_count)
        explicit_square = arb(0)
        for degree in range(first_degree, last_degree):
            eigenvalue = degree * (degree + 1)
            row = arb_mat(1, degree_count)
            for source in range(degree_count):
                row[0, source] = sum(
                    (
                        -arb((2 * degree + 1) * (2 * low + 1)).sqrt()
                        / (eigenvalue - low * (low + 1))
                        * singular_map[low, source]
                        / eigenvalue
                        for low in range(degree_count)
                    ),
                    arb(0),
                )
                explicit_square += row[0, source].abs_upper() ** 2
            gram += row.transpose() * row

        remainder = arb(0)
        for order in range(moment_order):
            moment_square = arb(0)
            for source in range(degree_count):
                moment = sum(
                    (
                        arb(2 * low + 1).sqrt()
                        * (low * (low + 1)) ** order
                        * singular_map[low, source]
                        for low in range(degree_count)
                    ),
                    arb(0),
                )
                moment_square += moment.abs_upper() ** 2
            exponent = 4 * order + 7
            scalar_tail = (
                arb(1) / last_degree**exponent
                + arb(1)
                / ((exponent - 1) * last_degree ** (exponent - 1))
            )
            remainder += (3 * scalar_tail * moment_square).sqrt()

        maximum_eigenvalue = (degree_count - 1) * degree_count
        absolute_moment_square = arb(0)
        for source in range(degree_count):
            absolute_moment = sum(
                (
                    arb(2 * low + 1).sqrt()
                    * (low * (low + 1)) ** moment_order
                    * singular_map[low, source].abs_upper()
                    for low in range(degree_count)
                ),
                arb(0),
            )
            absolute_moment_square += absolute_moment**2
        exponent = 4 * moment_order + 7
        scalar_tail = (
            arb(1) / last_degree**exponent
            + arb(1) / ((exponent - 1) * last_degree ** (exponent - 1))
        )
        ratio = arb(maximum_eigenvalue) / (
            last_degree * (last_degree + 1)
        )
        remainder += (
            3 * scalar_tail * absolute_moment_square
        ).sqrt() / (1 - ratio)

        midpoint = np.empty((degree_count, degree_count), dtype=float)
        radius = np.empty_like(midpoint)
        for row in range(degree_count):
            for column in range(degree_count):
                midpoint[row, column] = float(gram[row, column].mid())
                radius[row, column] = _arb_radius_as_float(gram[row, column])
        explicit = explicit_square.sqrt()
        total = explicit + remainder
    finally:
        ctx.prec = previous_precision

    return ArbAdjacentSingularGram(
        midpoint=midpoint,
        radius=radius,
        explicit_frobenius_upper=_float_upper(explicit),
        remainder_norm_upper=_float_upper(remainder),
        total_frobenius_upper=_float_upper(total),
        degree_count=degree_count,
        first_degree=first_degree,
        last_degree=last_degree,
        moment_order=moment_order,
        precision=precision,
    )
