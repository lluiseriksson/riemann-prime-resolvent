"""Arb enclosure of the finite endpoint-jet Schur correction.

The implementation streams the six scalar jet coefficients.  It uses the
Legendre derivative identity instead of storing the full truncated-power
coefficient table, so memory is independent of the terminal degree.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float


@dataclass(frozen=True)
class ArbJetCorrection:
    midpoint: np.ndarray
    radius: np.ndarray
    first_degree: int
    last_degree: int
    precision: int


def build_arb_prime_jet_correction(
    half_width: float,
    low_degrees: np.ndarray,
    first_degree: int,
    last_degree: int,
    jet_count: int,
    spectral_shift: float = 0.005,
    precision: int = 192,
    progress_stride: int | None = None,
) -> ArbJetCorrection:
    """Enclose ``J D^-1 J*`` for ``first_degree <= n < last_degree``.

    Only the registered first-prime window ``a=2/5`` is supported.  Every
    transcendental constant and every recurrence operation is evaluated in
    Arb.  ``last_degree`` is exclusive, as in ``prime_jet_weighted_correction``.
    """
    if half_width != 0.4:
        raise ValueError("the exact Arb implementation currently registers a = 2/5")
    low = np.asarray(low_degrees, dtype=int)
    if low.ndim != 1 or len(low) == 0:
        raise ValueError("low_degrees must be a nonempty vector")
    if np.any(low % 2 != low[0] % 2):
        raise ValueError("low degrees must have one parity")
    if not 1 <= jet_count <= first_degree:
        raise ValueError("require 1 <= jet_count <= first_degree")
    if last_degree <= first_degree:
        raise ValueError("last_degree must exceed first_degree")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = arb(2) / 5
        cut = arb(1) - arb.const_log2() / a
        sqrt_two = arb(2).sqrt()
        prime_factor = -arb(2) * arb.const_log2() / sqrt_two

        scalar = -a.log() - (arb(2) * arb.pi()).log() - arb.const_euler()
        if not scalar.upper() < 0:
            raise ArithmeticError("could not certify the sign of the scalar term")
        loss = -scalar + arb(2) * arb.const_log2() / sqrt_two + arb(12) / 5
        shift = arb(str(spectral_shift))

        normalizations = {
            int(n): (arb(2 * int(n) + 1) / 2).sqrt()
            for n in low
        }
        endpoint = [[arb(0) for _ in range(jet_count)] for _ in low]
        for row, degree_value in enumerate(low):
            degree = int(degree_value)
            for jet in range(jet_count):
                if degree < jet:
                    continue
                ratio = arb(1)
                for factor in range(degree - jet + 1, degree + jet + 1):
                    ratio *= factor
                ratio /= arb(2) ** jet * math.factorial(jet) ** 2
                endpoint[row][jet] = normalizations[degree] * ratio

        # Direct certified evaluation avoids the dependency explosion of an
        # interval-valued three-term recurrence.  Arb selects asymptotic or
        # hypergeometric algorithms appropriate to the degree.
        standard_values: dict[int, object] = {0: arb(1)}
        step_values: dict[int, object] = {
            0: (cut + 1) / sqrt_two,
        }
        harmonic = arb(0)
        gram = [[arb(0) for _ in range(jet_count)] for _ in range(jet_count)]
        parity = int(low[0] % 2)
        maximum_needed = last_degree - 1 + jet_count + 1

        def normalization(degree: int):
            return (arb(2 * degree + 1) / 2).sqrt()

        def coefficient(jet: int, degree: int, memo: dict[tuple[int, int], object]):
            key = (jet, degree)
            if key in memo:
                return memo[key]
            if jet == 0:
                value = step_values[degree]
            else:
                value = -arb(jet) * normalization(degree) / (2 * degree + 1) * (
                    coefficient(jet - 1, degree + 1, memo)
                    / normalization(degree + 1)
                    - coefficient(jet - 1, degree - 1, memo)
                    / normalization(degree - 1)
                )
            memo[key] = value
            return value

        for degree in range(1, maximum_needed + 1):
            standard_values[degree] = cut.legendre_p(degree)

            # P_{r+1} has just become available, so form the step coefficient r.
            r = degree - 1
            if r >= 1 and r + 1 in standard_values:
                step_values[r] = normalization(r) * (
                    standard_values[r + 1] - standard_values[r - 1]
                ) / (2 * r + 1)

            harmonic += arb(1) / degree
            center = degree - jet_count - 1
            if (
                center >= first_degree
                and center < last_degree
                and center % 2 == parity
            ):
                memo: dict[tuple[int, int], object] = {}
                vector = [coefficient(jet, center, memo) for jet in range(jet_count)]
                # ``arb`` supports in-place mutation; copy rather than aliasing
                # the running harmonic sum before removing the look-ahead.
                denominator = arb(harmonic)
                # harmonic currently is H_{center+jet_count+1}; undo the few
                # look-ahead terms exactly to obtain H_center.
                for undo in range(center + 1, degree + 1):
                    denominator -= arb(1) / undo
                denominator -= loss + shift
                if not denominator.lower() > 0:
                    raise ArithmeticError("tail denominator was not certified positive")
                for left in range(jet_count):
                    for right in range(left, jet_count):
                        gram[left][right] += vector[left] * vector[right] / denominator

                if progress_stride and center % progress_stride < 2:
                    print(f"ARB-JET degree={center}", flush=True)

            # Only a fixed window around the next center is ever needed.
            floor = center - jet_count - 2
            for old in tuple(step_values):
                if old < floor:
                    del step_values[old]
            for old in tuple(standard_values):
                if old < degree - 2:
                    del standard_values[old]

        for left in range(jet_count):
            for right in range(left):
                gram[left][right] = gram[right][left]

        endpoint_matrix = arb_mat(endpoint)
        gram_matrix = arb_mat(gram)
        correction = prime_factor**2 * endpoint_matrix * gram_matrix * endpoint_matrix.transpose()
        midpoint = np.empty((len(low), len(low)), dtype=float)
        radius = np.empty_like(midpoint)
        for row in range(len(low)):
            for column in range(len(low)):
                midpoint[row, column] = float(correction[row, column].mid())
                radius[row, column] = _arb_radius_as_float(correction[row, column])
    finally:
        ctx.prec = previous_precision

    return ArbJetCorrection(
        midpoint=midpoint,
        radius=radius,
        first_degree=first_degree,
        last_degree=last_degree,
        precision=precision,
    )
