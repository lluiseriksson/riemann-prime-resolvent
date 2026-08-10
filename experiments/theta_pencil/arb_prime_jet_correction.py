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
from experiments.theta_pencil.prime_power_arithmetic import prime_power_base
from experiments.theta_pencil.support_window import (
    in_first_prime_window,
    prime_overlap_positive,
)


@dataclass(frozen=True)
class ArbJetCorrection:
    midpoint: np.ndarray
    radius: np.ndarray
    first_degree: int
    last_degree: int
    precision: int


def build_arb_active_prime_jet_correction(
    half_width: float,
    active_primes: tuple[int, ...],
    low_degrees: np.ndarray,
    first_degree: int,
    last_degree: int,
    jet_count: int,
    spectral_shift: float = 0.005,
    precision: int = 192,
    progress_stride: int | None = None,
    perturbation_loss: float | None = None,
) -> ArbJetCorrection:
    """Enclose the combined-prime ``J D^-1 J*`` over a degree band.

    Cross terms between different prime cuts are retained in one Gram matrix.
    Every transcendental constant and recurrence operation is evaluated in
    Arb. ``last_degree`` is exclusive.
    """
    if not active_primes:
        raise ValueError("at least one active prime is required")
    if any(prime < 2 for prime in active_primes):
        raise ValueError("active primes must be at least two")
    if any(
        not prime_overlap_positive(half_width, prime)
        for prime in active_primes
    ):
        raise ValueError("every active prime must have positive overlap")
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
        a = arb(str(half_width))
        sqrt_two = arb(2).sqrt()
        prime_balls = [arb(prime) for prime in active_primes]
        mangoldt_balls = [
            arb(prime_power_base(prime)).log() for prime in active_primes
        ]
        cuts = [arb(1) - prime.log() / a for prime in prime_balls]
        prime_factors = [
            -arb(2) * mangoldt / prime.sqrt()
            for prime, mangoldt in zip(prime_balls, mangoldt_balls)
        ]

        scalar = -a.log() - (arb(2) * arb.pi()).log() - arb.const_euler()
        if not scalar.upper() < 0:
            raise ArithmeticError("could not certify the sign of the scalar term")
        loss = (
            arb(str(perturbation_loss))
            if perturbation_loss is not None
            else -scalar
            + sum(
                (
                    arb(2) * mangoldt / prime.sqrt()
                    for prime, mangoldt in zip(prime_balls, mangoldt_balls)
                ),
                arb(0),
            )
            + arb(6) * a
        )
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

        combined_endpoint = [
            row * len(active_primes) for row in endpoint
        ]
        standard_values = [{0: arb(1)} for _ in active_primes]
        step_values = [
            {0: (cut + 1) / sqrt_two} for cut in cuts
        ]
        harmonic = arb(0)
        combined_size = len(active_primes) * jet_count
        gram = [
            [arb(0) for _ in range(combined_size)]
            for _ in range(combined_size)
        ]
        parity = int(low[0] % 2)
        maximum_needed = last_degree - 1 + jet_count + 1

        def normalization(degree: int):
            return (arb(2 * degree + 1) / 2).sqrt()

        def coefficient(
            prime_index: int,
            jet: int,
            degree: int,
            memo: dict[tuple[int, int, int], object],
        ):
            key = (prime_index, jet, degree)
            if key in memo:
                return memo[key]
            if jet == 0:
                value = step_values[prime_index][degree]
            else:
                value = -arb(jet) * normalization(degree) / (2 * degree + 1) * (
                    coefficient(prime_index, jet - 1, degree + 1, memo)
                    / normalization(degree + 1)
                    - coefficient(prime_index, jet - 1, degree - 1, memo)
                    / normalization(degree - 1)
                )
            memo[key] = value
            return value

        for degree in range(1, maximum_needed + 1):
            r = degree - 1
            for prime_index, cut in enumerate(cuts):
                standard_values[prime_index][degree] = cut.legendre_p(degree)
                if r >= 1:
                    step_values[prime_index][r] = normalization(r) * (
                        standard_values[prime_index][r + 1]
                        - standard_values[prime_index][r - 1]
                    ) / (2 * r + 1)

            harmonic += arb(1) / degree
            center = degree - jet_count - 1
            if (
                center >= first_degree
                and center < last_degree
                and center % 2 == parity
            ):
                memo: dict[tuple[int, int, int], object] = {}
                vector = []
                for prime_index, prime_factor in enumerate(prime_factors):
                    vector.extend(
                        prime_factor
                        * coefficient(prime_index, jet, center, memo)
                        for jet in range(jet_count)
                    )
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
                for left in range(combined_size):
                    for right in range(left, combined_size):
                        gram[left][right] += vector[left] * vector[right] / denominator

                if progress_stride and center % progress_stride < 2:
                    print(f"ARB-JET degree={center}", flush=True)

            # Only a fixed window around the next center is ever needed.
            floor = center - jet_count - 2
            for prime_index in range(len(active_primes)):
                for old in tuple(step_values[prime_index]):
                    if old < floor:
                        del step_values[prime_index][old]
                for old in tuple(standard_values[prime_index]):
                    if old < degree - 2:
                        del standard_values[prime_index][old]

        for left in range(combined_size):
            for right in range(left):
                gram[left][right] = gram[right][left]

        endpoint_matrix = arb_mat(combined_endpoint)
        gram_matrix = arb_mat(gram)
        correction = endpoint_matrix * gram_matrix * endpoint_matrix.transpose()
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
    """Backward-compatible prime-two jet correction."""

    if not in_first_prime_window(half_width):
        raise ValueError(
            "the exact Arb jet implementation requires log(2)/2 < a <= log(3)/2"
        )
    return build_arb_active_prime_jet_correction(
        half_width,
        (2,),
        low_degrees,
        first_degree,
        last_degree,
        jet_count,
        spectral_shift,
        precision,
        progress_stride,
    )
