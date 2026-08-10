"""Outward-rounded infinite-tail budget for the parity Schur certificate."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_trial_variation import (
    certify_active_prime_operator_remainder_variation,
)
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_remainder_bound,
)


@dataclass(frozen=True)
class ArbParityTailBudget:
    parity: int
    jet_tail_upper: float
    prime_remainder_upper: float
    potential_upper: float
    smooth_upper: float
    omitted_weighted_upper: float
    correction_upper: float
    variation_upper: float
    jet_correction_norm_upper: float
    active_primes: tuple[int, ...]


def _upper(value) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def certify_parity_tail_budget(
    parity: int,
    half_width: float = 0.4,
    low_dimension: int = 88,
    finite_dimension: int = 4096,
    smooth_dimension: int = 512,
    jet_count: int = 6,
    jet_end: int = 1_000_000,
    spectral_shift: float = 0.005,
    partitions: int = 128,
    precision: int = 768,
    jet_correction_norm_upper: float = 0.0103,
    active_primes: tuple[int, ...] = (2,),
) -> ArbParityTailBudget:
    if parity not in (0, 1):
        raise ValueError("parity must be zero or one")
    degrees = np.arange(parity, low_dimension, 2)
    variation = certify_active_prime_operator_remainder_variation(
        half_width,
        degrees,
        active_primes,
        jet_count,
        partitions,
        precision,
    )
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = arb(str(half_width))
        scalar = -a.log() - (arb(2) * arb.pi()).log() - arb.const_euler()
        if not scalar.upper() < 0:
            raise ArithmeticError("could not certify the scalar sign")
        prime_balls = [arb(prime) for prime in active_primes]
        loss = -scalar + sum(
            (arb(2) * prime.log() / prime.sqrt() for prime in prime_balls),
            arb(0),
        ) + arb(6) * a
        shift = arb(str(spectral_shift))

        def denominator(index: int):
            return arb(index + 1).digamma() + arb.const_euler() - loss - shift

        jet_tail = arb(0)
        for prime in prime_balls:
            cut = arb(1) - prime.log() / a
            cut_weight = (arb(1) - cut * cut).sqrt().sqrt()
            prime_coefficient = prime.log() / prime.sqrt()
            for jet in range(jet_count):
                endpoint_square = arb(0)
                for degree_value in degrees:
                    degree = int(degree_value)
                    if degree < jet:
                        continue
                    endpoint = (arb(2 * degree + 1) / 2).sqrt()
                    for factor in range(
                        degree - jet + 1, degree + jet + 1
                    ):
                        endpoint *= factor
                    endpoint /= arb(2) ** jet * math.factorial(jet) ** 2
                    endpoint_square += endpoint * endpoint
                if jet == 0:
                    scalar_tail = (
                        (arb(8) / (3 * arb.pi())).sqrt()
                        / (cut_weight * arb(jet_end - 1).sqrt())
                    )
                else:
                    scalar_tail = (
                        arb(2) ** (jet + 1)
                        * math.factorial(jet)
                        / cut_weight
                        / (arb.pi() * (2 * jet + 1)).sqrt()
                        / arb(jet_end - 1) ** arb(str(jet + 0.5))
                    )
                jet_tail += (
                    arb(2)
                    * prime_coefficient
                    * endpoint_square.sqrt()
                    * scalar_tail
                )
        jet_tail /= denominator(jet_end).sqrt()

        prime_remainder = (
            arb(2) ** (jet_count + 1)
            * arb(str(variation.upper))
            / (arb.pi() * (2 * jet_count + 1)).sqrt()
            / arb(finite_dimension - 1) ** arb(str(jet_count + 0.5))
            / denominator(finite_dimension).sqrt()
        )

        eigenvalues = [arb(int(degree) * (int(degree) + 1)) for degree in degrees]
        weights = [arb(2 * int(degree) + 1).sqrt() for degree in degrees]
        potential = arb(0)
        expansion_order = 3
        for order in range(expansion_order):
            norm = sum(
                ((weights[k] * eigenvalues[k] ** order) ** 2 for k in range(len(degrees))),
                arb(0),
            ).sqrt()
            potential += (
                arb(3).sqrt()
                * norm
                / arb(4 * order + 2).sqrt()
                * arb(finite_dimension - 1) ** (-(2 * order + 1))
            )
        remainder_norm = sum(
            (
                (weights[k] * eigenvalues[k] ** expansion_order) ** 2
                for k in range(len(degrees))
            ),
            arb(0),
        ).sqrt()
        ratio = eigenvalues[-1] / (finite_dimension * finite_dimension)
        potential += (
            arb(3).sqrt()
            * remainder_norm
            / (1 - ratio)
            / arb(4 * expansion_order + 2).sqrt()
            * arb(finite_dimension - 1) ** (-(2 * expansion_order + 1))
        )
        potential /= denominator(finite_dimension).sqrt()

        if low_dimension + 24 < smooth_dimension:
            smooth_remainder = math.nextafter(
                smooth_kernel_series_remainder_bound(half_width, 23), math.inf
            )
            smooth = arb(str(smooth_remainder)) / denominator(
                smooth_dimension
            ).sqrt()
        else:
            weighted_l1 = (
                arb.pi().sqrt() * arb("0.75").gamma() / arb("1.25").gamma()
            )
            smooth_r4 = arb(1) if half_width <= 0.4 else arb("1.1")
            smooth_variation = (
                a * a * arb.pi().sqrt() / 24
                + a**3 * smooth_r4 * arb(2).sqrt() * weighted_l1
            )
            smooth = (
                arb(4)
                * smooth_variation
                / (arb(3) * arb.pi()).sqrt()
                / arb(smooth_dimension - 1) ** arb("1.5")
                / denominator(smooth_dimension).sqrt()
            )

        omitted = jet_tail + prime_remainder + potential + smooth
        correction = (
            arb(2) * arb(str(jet_correction_norm_upper)).sqrt() * omitted
            + omitted * omitted
        )
    finally:
        ctx.prec = previous_precision

    return ArbParityTailBudget(
        parity=parity,
        jet_tail_upper=_upper(jet_tail),
        prime_remainder_upper=_upper(prime_remainder),
        potential_upper=_upper(potential),
        smooth_upper=_upper(smooth),
        omitted_weighted_upper=_upper(omitted),
        correction_upper=_upper(correction),
        variation_upper=variation.upper,
        jet_correction_norm_upper=jet_correction_norm_upper,
        active_primes=active_primes,
    )
