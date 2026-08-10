"""Full interval Schur certificate in the second prime window."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_second_window_flux_gram import (
    build_arb_second_window_flux_gram,
)
from experiments.theta_pencil.arb_second_window_near_tail_gram import (
    build_arb_second_window_near_tail_gram,
)
from experiments.theta_pencil.arb_second_window_other_tail import (
    certify_second_window_other_tail,
)
from experiments.theta_pencil.arb_second_window_singular_gram import (
    build_arb_second_window_singular_gram,
)
from experiments.theta_pencil.arb_second_window_source import (
    build_arb_second_window_source,
)
from experiments.theta_pencil.arb_source_schur import _roundtrip_ball
from experiments.theta_pencil.interval_inertia import certify_interval_inertia
from experiments.theta_pencil.support_05_comparison import (
    certify_second_window_complement_floor,
)


@dataclass(frozen=True)
class SecondWindowSchurParity:
    parity: int
    spectral_shift: float
    negative_count: int
    positive_count: int
    unresolved_count: int
    first_positive_lower: float
    entry_radius: float


@dataclass(frozen=True)
class SecondWindowSchurCertificate:
    half_width: float
    even: SecondWindowSchurParity
    odd: SecondWindowSchurParity
    complement_floor: float
    smooth_remainder: float
    other_tail_norm: float
    tail_balance: float
    low_degree_count: int
    tail_start: int
    explicit_end: int
    precision: int


def _matrix_from_export(arb, arb_mat, midpoint, radius):
    result = arb_mat(midpoint.shape[0], midpoint.shape[1])
    for row in range(result.nrows()):
        for column in range(result.ncols()):
            result[row, column] = _roundtrip_ball(
                arb, midpoint[row, column], radius[row, column]
            )
    return result


def _assemble_parity_schur(
    arb,
    arb_mat,
    source,
    band_gram,
    flux_gram,
    singular_gram,
    spectral_shift,
    smooth_remainder,
    complement_floor,
    other_tail_norm,
    tail_balance,
):
    """Assemble one rigorous lower Schur matrix from Arb components."""

    size = source.nrows()
    shift = arb(str(spectral_shift))
    smooth = arb(str(smooth_remainder))
    denominator = arb(str(complement_floor)) - shift - 2 * smooth
    if not denominator.lower() > 0:
        raise ArithmeticError("the common Schur denominator is unresolved")
    result = arb_mat(source)
    for index in range(size):
        result[index, index] -= shift + smooth
    structured = 2 * (flux_gram + singular_gram)
    balance = arb(str(tail_balance))
    other = arb(str(other_tail_norm))
    tail_upper = (1 + balance) * structured
    scalar_tail = (1 + 1 / balance) * other**2
    for index in range(size):
        tail_upper[index, index] += scalar_tail
    result -= (band_gram + tail_upper) / denominator
    return result


def certify_second_window_schur(
    half_width: float = 0.551,
    even_shift: float = 0.001,
    odd_shift: float = 0.05,
    low_degree_count: int = 16,
    tail_start: int = 640,
    explicit_end: int = 4096,
    maximum_smooth_power: int = 23,
    tail_balance: float = 0.1,
    precision: int = 512,
    comparison_subdivisions: int = 80,
    expected_negative_count: int = 1,
) -> SecondWindowSchurCertificate:
    """Certify that at most one eigenvalue lies below each shift.

    The finite band ``d <= n < tail_start`` is accumulated exactly with all
    seven source blocks and the truncated smooth kernel in each row.  Above
    ``tail_start``, endpoint flux and adjacent singular Grams retain their
    directions.  The remaining map enters only through its certified norm.
    """

    if tail_balance <= 0:
        raise ValueError("tail_balance must be positive")
    if expected_negative_count not in (0, 1):
        raise ValueError("expected_negative_count must be zero or one")
    if tail_start <= low_degree_count or explicit_end <= tail_start:
        raise ValueError("invalid Schur degree ranges")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    source = build_arb_second_window_source(
        half_width,
        low_degree_count,
        low_degree_count,
        low_degree_count,
        maximum_smooth_power,
        precision,
    )
    band = build_arb_second_window_near_tail_gram(
        half_width,
        low_degree_count,
        low_degree_count,
        low_degree_count,
        low_degree_count,
        tail_start,
        precision,
        maximum_smooth_power,
    )
    flux = build_arb_second_window_flux_gram(
        half_width,
        low_degree_count,
        low_degree_count,
        low_degree_count,
        tail_start,
        explicit_end,
        precision,
    )
    singular = build_arb_second_window_singular_gram(
        half_width,
        low_degree_count,
        low_degree_count,
        low_degree_count,
        tail_start,
        explicit_end,
        8,
        precision,
    )
    other = certify_second_window_other_tail(
        half_width,
        low_degree_count,
        low_degree_count,
        low_degree_count,
        tail_start,
        explicit_end,
        precision,
    )
    floor = certify_second_window_complement_floor(
        half_width,
        low_degree_count,
        min(precision, 512),
        comparison_subdivisions,
    )
    smooth_remainder = math.nextafter(source.smooth_remainder, math.inf)

    previous_precision = ctx.prec
    results = []
    try:
        ctx.prec = precision
        for parity, name, shift in (
            (0, "even", even_shift),
            (1, "odd", odd_shift),
        ):
            source_ball = _matrix_from_export(
                arb,
                arb_mat,
                getattr(source, f"{name}_midpoint"),
                getattr(source, f"{name}_radius"),
            )
            band_ball = _matrix_from_export(
                arb,
                arb_mat,
                getattr(band, f"{name}_midpoint"),
                getattr(band, f"{name}_radius"),
            )
            flux_ball = _matrix_from_export(
                arb,
                arb_mat,
                getattr(flux, f"{name}_midpoint"),
                getattr(flux, f"{name}_radius"),
            )
            singular_ball = _matrix_from_export(
                arb,
                arb_mat,
                getattr(singular, f"{name}_midpoint"),
                getattr(singular, f"{name}_radius"),
            )
            schur = _assemble_parity_schur(
                arb,
                arb_mat,
                source_ball,
                band_ball,
                flux_ball,
                singular_ball,
                shift,
                smooth_remainder,
                floor.complement_floor,
                other.spectral_norm_upper,
                tail_balance,
            )
            midpoint = np.empty((schur.nrows(), schur.ncols()), dtype=float)
            radius = np.empty_like(midpoint)
            for row in range(schur.nrows()):
                for column in range(schur.ncols()):
                    midpoint[row, column] = float(schur[row, column].mid())
                    radius[row, column] = _arb_radius_as_float(
                        schur[row, column]
                    )
            entry_radius = math.nextafter(float(np.max(radius)), math.inf)
            inertia = certify_interval_inertia(
                midpoint, entry_radius, min(precision, 768)
            )
            positive_lowers = [
                lower for lower, _ in inertia.real_intervals if lower > 0
            ]
            if (
                inertia.negative_count != expected_negative_count
                or inertia.positive_count
                != schur.nrows() - expected_negative_count
                or inertia.unresolved_count != 0
            ):
                raise ArithmeticError(
                    f"the {name} Schur inertia did not close: "
                    f"negative={inertia.negative_count}, "
                    f"positive={inertia.positive_count}, "
                    f"unresolved={inertia.unresolved_count}"
                )
            results.append(
                SecondWindowSchurParity(
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

    return SecondWindowSchurCertificate(
        half_width=half_width,
        even=results[0],
        odd=results[1],
        complement_floor=floor.complement_floor,
        smooth_remainder=smooth_remainder,
        other_tail_norm=other.spectral_norm_upper,
        tail_balance=tail_balance,
        low_degree_count=low_degree_count,
        tail_start=tail_start,
        explicit_end=explicit_end,
        precision=precision,
    )
