"""Rigorous piecewise variation bound for a fixed Legendre trial vector."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float


@dataclass(frozen=True)
class ArbVariationBound:
    midpoint: float
    radius: float
    upper: float
    partitions: int
    precision: int


def certify_prime_operator_remainder_variation(
    half_width: float,
    low_degrees: np.ndarray,
    derivative_order: int = 6,
    partitions: int = 128,
    precision: int = 768,
) -> ArbVariationBound:
    """Vector-valued version used by the parity Schur tail certificate."""
    degrees = np.asarray(low_degrees, dtype=int)
    if half_width != 0.4:
        raise ValueError("the exact Arb implementation currently registers a = 2/5")
    if len(degrees) < 1 or derivative_order < 1 or partitions < 1:
        raise ValueError("invalid degrees, derivative order, or partition count")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        derivative_rows = []
        endpoint_square = arb(0)
        for degree_value in degrees:
            degree = int(degree_value)
            row = [arb(0) for _ in range(degree + 1)]
            row[degree] = (arb(2 * degree + 1) / 2).sqrt()
            for _ in range(derivative_order + 1):
                row = _differentiate_standard_legendre(row, arb)
            derivative_rows.append(row)

            if degree >= derivative_order:
                endpoint = (arb(2 * degree + 1) / 2).sqrt()
                for factor in range(degree - derivative_order + 1, degree + derivative_order + 1):
                    endpoint *= factor
                endpoint /= arb(2) ** derivative_order * math.factorial(derivative_order)
                endpoint_square += endpoint * endpoint

        maximum_derivative_degree = max(len(row) - 1 for row in derivative_rows)
        order = maximum_derivative_degree + 1
        nodes_weights = [arb.legendre_p_root(order, k, weight=True) for k in range(order)]
        a = arb(2) / 5
        translation = arb.const_log2() / a
        cut = arb(1) - translation
        length = cut + 1
        total = arb(0)
        for part in range(partitions):
            left = -arb(1) + length * part / partitions
            right = -arb(1) + length * (part + 1) / partitions
            midpoint = (right + left) / 2
            scale = (right - left) / 2
            square_integral = arb(0)
            for node, weight in nodes_weights:
                source = midpoint + scale * node + translation
                squared_norm = arb(0)
                for row in derivative_rows:
                    value = _legendre_series_value(row, source, arb)
                    squared_norm += value * value
                square_integral += scale * weight * squared_norm
            arcsine_mass = right.asin() - left.asin()
            total += (arcsine_mass * square_integral).sqrt()

        cut_weight = (arb(1) - cut * cut).sqrt().sqrt()
        prime_factor = arb(2) * arb.const_log2() / arb(2).sqrt()
        bound = prime_factor * (total + endpoint_square.sqrt() / cut_weight)
        midpoint = float(bound.mid())
        radius = _arb_radius_as_float(bound)
        upper = math.nextafter(float(bound.upper()), math.inf)
    finally:
        ctx.prec = previous_precision
    return ArbVariationBound(
        midpoint=midpoint,
        radius=radius,
        upper=upper,
        partitions=partitions,
        precision=precision,
    )


def _differentiate_standard_legendre(coefficients, arb):
    """Differentiate coefficients in the unnormalized P_n basis."""
    if len(coefficients) <= 1:
        return [arb(0)]
    result = [arb(0) for _ in range(len(coefficients) - 1)]
    for output in range(len(result)):
        factor = 2 * output + 1
        for source in range(output + 1, len(coefficients), 2):
            result[output] += factor * coefficients[source]
    return result


def _legendre_series_value(coefficients, point, arb):
    if not coefficients:
        return arb(0)
    previous = arb(1)
    value = coefficients[0] * previous
    if len(coefficients) == 1:
        return value
    current = point
    value += coefficients[1] * current
    for degree in range(1, len(coefficients) - 1):
        following = (
            arb(2 * degree + 1) * point * current - degree * previous
        ) / (degree + 1)
        value += coefficients[degree + 1] * following
        previous, current = current, following
    return value


def certify_prime_remainder_variation(
    half_width: float,
    coefficients: np.ndarray,
    partitions: int = 32,
    precision: int = 1024,
) -> ArbVariationBound:
    """Upper-bound the weighted variation after removing both jump steps.

    On each subinterval Cauchy--Schwarz uses the exact arcsine mass and an
    Arb Gauss--Legendre evaluation of the polynomial ``phi''**2``.  The rule
    order integrates that polynomial exactly.
    """
    vector = np.asarray(coefficients, dtype=float)
    if half_width != 0.4:
        raise ValueError("the exact Arb implementation currently registers a = 2/5")
    if len(vector) < 3 or partitions < 1:
        raise ValueError("need at least three coefficients and one partition")
    if np.any(vector[1::2] != 0.0):
        raise ValueError("the registered trial variation requires an even vector")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        standard = [
            arb(float(value)) * (arb(2 * degree + 1) / 2).sqrt()
            for degree, value in enumerate(vector)
        ]
        first = _differentiate_standard_legendre(standard, arb)
        second = _differentiate_standard_legendre(first, arb)
        order = len(vector) - 2
        nodes_weights = [arb.legendre_p_root(order, k, weight=True) for k in range(order)]

        a = arb(2) / 5
        translation = arb.const_log2() / a
        cut = arb(1) - translation
        length = cut + 1
        total = arb(0)
        for part in range(partitions):
            left = -arb(1) + length * part / partitions
            right = -arb(1) + length * (part + 1) / partitions
            midpoint = (right + left) / 2
            scale = (right - left) / 2
            square_integral = arb(0)
            for node, weight in nodes_weights:
                source = midpoint + scale * node + translation
                value = _legendre_series_value(second, source, arb)
                square_integral += scale * weight * value * value
            arcsine_mass = right.asin() - left.asin()
            total += (arcsine_mass * square_integral).sqrt()

        endpoint_derivative = arb(0)
        for degree in range(1, len(standard)):
            endpoint_derivative += standard[degree] * degree * (degree + 1) / 2
        cut_weight = (arb(1) - cut * cut).sqrt().sqrt()
        prime_factor = arb(2) * arb.const_log2() / arb(2).sqrt()
        bound = prime_factor * (total + abs(endpoint_derivative) / cut_weight)
        midpoint = float(bound.mid())
        radius = _arb_radius_as_float(bound)
        upper = math.nextafter(float(bound.upper()), math.inf)
    finally:
        ctx.prec = previous_precision
    return ArbVariationBound(
        midpoint=midpoint,
        radius=radius,
        upper=upper,
        partitions=partitions,
        precision=precision,
    )
