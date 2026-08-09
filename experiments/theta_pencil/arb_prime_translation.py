"""Arb enclosure of the prime-2 Legendre matrix without quadrature.

The translated low polynomial is expanded exactly at the two overlap cuts.
Large endpoint-jet terms cancel, so production dimensions deliberately use
thousands of bits; Arb retains a certified enclosure through that cancellation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ArbPrimeMatrix:
    midpoint: np.ndarray
    radius: np.ndarray
    precision: int


def _arb_radius_as_float(value) -> float:
    """Work around a high-precision python-flint radius conversion edge case."""
    rendered = value.rad().str(20)
    if rendered == "0":
        return 0.0
    midpoint = rendered.lstrip("[").split()[0]
    return float(midpoint)


def build_arb_prime_two_matrix(
    half_width: float,
    low_dimension: int,
    maximum_degree: int,
    precision: int = 8192,
) -> ArbPrimeMatrix:
    """Enclose rows ``m < low_dimension`` and columns ``n < maximum_degree``."""
    if half_width != 0.4:
        raise ValueError("the exact Arb implementation currently registers a = 2/5")
    if not 1 <= low_dimension <= maximum_degree:
        raise ValueError("require 1 <= low_dimension <= maximum_degree")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        two = arb(2)
        cut = 1 - arb(5) * two.log() / 2
        jet_count = low_dimension
        padded = maximum_degree + jet_count

        legendre = [arb(0)] * (padded + 2)
        legendre[0] = 1
        legendre[1] = cut
        for degree in range(1, padded + 1):
            legendre[degree + 1] = (
                (2 * degree + 1) * cut * legendre[degree]
                - degree * legendre[degree - 1]
            ) / (degree + 1)

        rows: list[list] = []
        step = [arb(0)] * padded
        step[0] = (cut + 1) / two.sqrt()
        for degree in range(1, padded):
            step[degree] = (
                (arb(2 * degree + 1) / 2).sqrt()
                * (legendre[degree + 1] - legendre[degree - 1])
                / (2 * degree + 1)
            )
        rows.append(step)
        for _ in range(1, jet_count):
            previous = rows[-1]
            following = [-cut * value for value in previous]
            for degree in range(padded - 1):
                link = arb(degree + 1) / arb(
                    (2 * degree + 1) * (2 * degree + 3)
                ).sqrt()
                following[degree] += link * previous[degree + 1]
                following[degree + 1] += link * previous[degree]
            rows.append(following)

        endpoint = []
        for degree in range(low_dimension):
            normalization = (arb(2 * degree + 1) / 2).sqrt()
            endpoint_row = []
            for jet in range(jet_count):
                if degree < jet:
                    endpoint_row.append(arb(0))
                    continue
                derivative = arb(1)
                for factor in range(degree - jet + 1, degree + jet + 1):
                    derivative *= factor
                derivative /= 2**jet * math.factorial(jet) ** 2
                endpoint_row.append(normalization * derivative)
            endpoint.append(endpoint_row)

        product = arb_mat(endpoint) * arb_mat(
            [row[:maximum_degree] for row in rows]
        )
        coefficient = -2 * two.log() / two.sqrt()
        midpoint = np.empty((low_dimension, maximum_degree), dtype=float)
        radius = np.empty_like(midpoint)
        for left in range(low_dimension):
            for right in range(maximum_degree):
                if (left + right) % 2:
                    midpoint[left, right] = 0.0
                    radius[left, right] = 0.0
                    continue
                value = coefficient * product[left, right]
                midpoint[left, right] = float(value.mid())
                radius[left, right] = _arb_radius_as_float(value)
    finally:
        ctx.prec = previous_precision
    return ArbPrimeMatrix(midpoint=midpoint, radius=radius, precision=precision)
