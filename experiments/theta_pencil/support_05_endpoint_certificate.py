"""Single-source interval certificate for the endpoint support a=1/2."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_cut_dominant_cross import (
    build_arb_cut_dominant_cross,
)
from experiments.theta_pencil.arb_cut_smooth import build_arb_cut_smooth_matrix
from experiments.theta_pencil.arb_cut_source import build_arb_cut_finite_source
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_regularized_map_bound import (
    certify_regularized_map_bound,
)
from experiments.theta_pencil.arb_source_schur import _roundtrip_ball
from experiments.theta_pencil.interval_inertia import certify_interval_inertia
from experiments.theta_pencil.support_05_comparison import (
    certify_support_05_comparison,
)


@dataclass(frozen=True)
class EndpointParityCertificate:
    parity: int
    spectral_shift: float
    negative_count: int
    positive_count: int
    unresolved_count: int
    first_positive_lower: float
    entry_radius: float


@dataclass(frozen=True)
class Support05EndpointCertificate:
    even: EndpointParityCertificate
    odd: EndpointParityCertificate
    complement_floor: float
    regularized_tail_norm: float
    smooth_remainder: float
    low_degree_count: int
    explicit_degree_end: int
    precision: int


def _arb_parity_transform(arb, arb_mat, degree_count: int, parity: int):
    center_degrees = tuple(range(parity, degree_count, 2))
    size = degree_count + len(center_degrees)
    transform = arb_mat(3 * degree_count, size)
    inverse_sqrt_two = arb(1) / arb(2).sqrt()
    for degree in range(degree_count):
        reflection = -1 if degree % 2 else 1
        transform[degree, degree] = inverse_sqrt_two
        transform[2 * degree_count + degree, degree] = (
            (reflection if parity == 0 else -reflection) * inverse_sqrt_two
        )
    for column, degree in enumerate(center_degrees, start=degree_count):
        transform[degree_count + degree, column] = arb(1)
    return transform


def _arb_flux_upper(
    arb,
    arb_mat,
    degree_count: int,
    parity: int,
    first_degree: int,
    explicit_end: int,
):
    """Parity flux Gram: explicit rational sum plus PSD tail upper."""

    log_two = arb.const_log2()
    lengths = (2 - 2 * log_two, 4 * log_two - 2, 2 - 2 * log_two)
    total = 3 * degree_count
    minus = []
    plus = []
    for block, length in enumerate(lengths):
        left = [arb(0) for _ in range(total)]
        right = [arb(0) for _ in range(total)]
        for degree in range(degree_count):
            normalization = (arb(2 * degree + 1) / length).sqrt()
            left[block * degree_count + degree] = (
                (-1 if degree % 2 else 1) * normalization
            )
            right[block * degree_count + degree] = normalization
        minus.append(left)
        plus.append(right)

    def subtract(left, right):
        return [a - b for a, b in zip(left, right)]

    flux = []
    flux.append(
        (
            [
                (lengths[0] / 2).sqrt() * value
                for value in subtract(plus[0], minus[1])
            ],
            [-(lengths[0] / 2).sqrt() * value for value in minus[0]],
        )
    )
    flux.append(
        (
            [
                (lengths[1] / 2).sqrt() * value
                for value in subtract(plus[1], minus[2])
            ],
            [
                (lengths[1] / 2).sqrt() * value
                for value in subtract(plus[0], minus[1])
            ],
        )
    )
    flux.append(
        (
            [(lengths[2] / 2).sqrt() * value for value in plus[2]],
            [
                (lengths[2] / 2).sqrt() * value
                for value in subtract(plus[1], minus[2])
            ],
        )
    )

    transform = _arb_parity_transform(arb, arb_mat, degree_count, parity)
    projected = []
    for positive, negative in flux:
        positive_row = arb_mat([positive]) * transform
        negative_row = arb_mat([negative]) * transform
        projected.append((positive_row, negative_row))
    size = transform.ncols()
    gram = arb_mat(size, size)
    even_weight = arb(0)
    odd_weight = arb(0)
    for degree in range(first_degree, explicit_end):
        weight = arb(2 * degree + 1) / (
            2 * degree**2 * (degree + 1) ** 2
        )
        if degree % 2:
            odd_weight += weight
        else:
            even_weight += weight
    for positive, negative in projected:
        for sign, weight in ((1, even_weight), (-1, odd_weight)):
            row = positive - sign * negative
            gram += weight * row.transpose() * row
        # Remaining scalar weight is 1/(2 explicit_end^2); after
        # |p +/- m|^2 <= 2(|p|^2+|m|^2), its PSD upper is this expression.
        gram += (
            positive.transpose() * positive + negative.transpose() * negative
        ) / explicit_end**2
    return gram


def certify_support_05_endpoint(
    precision: int = 3072,
    low_degree_count: int = 16,
    explicit_degree_end: int = 128,
    flux_explicit_end: int = 4096,
) -> Support05EndpointCertificate:
    """Certify the two second-eigenvalue floors required by Kato--Temple."""

    if low_degree_count != 16 or explicit_degree_end != 128:
        raise ValueError("the registered endpoint certificate uses degrees 16 and 128")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    source = build_arb_cut_finite_source(0.5, low_degree_count, 23, 768)
    smooth = build_arb_cut_smooth_matrix(0.5, 40, 23, 768)
    cross = build_arb_cut_dominant_cross(
        0.5, low_degree_count, explicit_degree_end, precision
    )
    comparison = certify_support_05_comparison(256, 300)
    regularized = certify_regularized_map_bound(16, 256)

    previous_precision = ctx.prec
    results = []
    try:
        ctx.prec = precision
        d = low_degree_count
        high_count = explicit_degree_end - d
        low_indices = [
            block * 40 + degree
            for block in range(3)
            for degree in range(d)
        ]
        smooth_high_indices = [
            block * 40 + degree
            for block in range(3)
            for degree in range(d, 40)
        ]
        smooth_columns = [
            block * high_count + degree - d
            for block in range(3)
            for degree in range(d, 40)
        ]
        coupling = arb_mat(3 * d, 3 * high_count)
        for row in range(3 * d):
            for column in range(3 * high_count):
                coupling[row, column] = _roundtrip_ball(
                    arb, cross.midpoint[row, column], cross.radius[row, column]
                )
        for row, smooth_row in enumerate(low_indices):
            for column, smooth_column in zip(
                smooth_columns, smooth_high_indices
            ):
                coupling[row, column] += _roundtrip_ball(
                    arb,
                    smooth.midpoint[smooth_row, smooth_column],
                    smooth.radius[smooth_row, smooth_column],
                )

        # H_16 plus the rigorously lower-bounded common perturbation floor.
        harmonic_16 = sum((arb(1) / k for k in range(1, 17)), arb(0))
        perturbation_lower = math.nextafter(
            comparison.even_third_floor - 25.0 / 12.0, -math.inf
        )
        complement_floor_ball = harmonic_16 + arb(str(perturbation_lower))
        complement_floor = float(complement_floor_ball.lower())
        smooth_remainder = math.nextafter(source.smooth_remainder, math.inf)
        regularized_upper = math.nextafter(regularized.global_upper, math.inf)
        regularized_tail_norm = regularized_upper / (
            explicit_degree_end * (explicit_degree_end + 1)
        )

        for parity, name, shift in ((0, "even", 0.01), (1, "odd", 0.3)):
            transform = _arb_parity_transform(arb, arb_mat, d, parity)
            projected_coupling = transform.transpose() * coupling
            flux_upper = _arb_flux_upper(
                arb,
                arb_mat,
                d,
                parity,
                explicit_degree_end,
                flux_explicit_end,
            )
            size = transform.ncols()
            source_midpoint = getattr(source, f"{name}_midpoint")
            source_radius = getattr(source, f"{name}_radius")
            schur = arb_mat(size, size)
            for row in range(size):
                for column in range(size):
                    schur[row, column] = _roundtrip_ball(
                        arb,
                        source_midpoint[row, column],
                        source_radius[row, column],
                    )
                schur[row, row] -= arb(str(shift)) + arb(str(smooth_remainder))
            tail_upper = 2 * flux_upper
            for index in range(size):
                tail_upper[index, index] += 2 * arb(str(regularized_tail_norm)) ** 2
            denominator = complement_floor_ball - arb(str(shift))
            if not denominator.lower() > 0:
                raise ArithmeticError("the common Schur denominator is unresolved")
            schur -= (
                projected_coupling * projected_coupling.transpose() + tail_upper
            ) / denominator

            midpoint = np.empty((size, size))
            radius = np.empty_like(midpoint)
            for row in range(size):
                for column in range(size):
                    midpoint[row, column] = float(schur[row, column].mid())
                    radius[row, column] = _arb_radius_as_float(schur[row, column])
            entry_radius = math.nextafter(float(np.max(radius)), math.inf)
            inertia = certify_interval_inertia(
                midpoint, entry_radius, min(precision, 768)
            )
            positive_lowers = [
                lower for lower, _ in inertia.real_intervals if lower > 0
            ]
            if (
                inertia.negative_count != 1
                or inertia.positive_count != size - 1
                or inertia.unresolved_count != 0
            ):
                raise ArithmeticError(f"the {name} endpoint inertia did not close")
            results.append(
                EndpointParityCertificate(
                    parity=parity,
                    spectral_shift=shift,
                    negative_count=inertia.negative_count,
                    positive_count=inertia.positive_count,
                    unresolved_count=inertia.unresolved_count,
                    first_positive_lower=min(positive_lowers),
                    entry_radius=entry_radius,
                )
            )
    finally:
        ctx.prec = previous_precision

    return Support05EndpointCertificate(
        even=results[0],
        odd=results[1],
        complement_floor=complement_floor,
        regularized_tail_norm=regularized_tail_norm,
        smooth_remainder=smooth_remainder,
        low_degree_count=low_degree_count,
        explicit_degree_end=explicit_degree_end,
        precision=precision,
    )
