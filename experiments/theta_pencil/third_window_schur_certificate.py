"""Rigorous thirteen-block Schur pipeline at support ``a = 0.7``."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_third_window_flux_gram import (
    build_arb_third_window_flux_gram,
)
from experiments.theta_pencil.arb_third_window_near_tail_gram import (
    build_arb_third_window_near_tail_gram,
)
from experiments.theta_pencil.arb_third_window_other_tail import (
    certify_third_window_other_tail,
)
from experiments.theta_pencil.arb_third_window_self_gram import (
    build_arb_third_window_self_gram,
)
from experiments.theta_pencil.arb_third_window_singular_gram import (
    build_arb_third_window_singular_gram,
)
from experiments.theta_pencil.arb_third_window_source import (
    build_arb_third_window_source,
)
from experiments.theta_pencil.interval_inertia import certify_interval_inertia
from experiments.theta_pencil.second_window_schur_certificate import (
    SecondWindowSchurParity,
    _coercive_lower_from_schur,
    _coupling_gram_upper,
    _load_component_cache,
    _matrix_from_export,
    _save_component_cache,
)
from experiments.theta_pencil.third_window_pointwise_floor import (
    certify_third_window_pointwise_floor,
)


@dataclass(frozen=True)
class ThirdWindowSchurCertificate:
    half_width: float
    even: SecondWindowSchurParity
    odd: SecondWindowSchurParity
    complement_floor: float
    tail_complement_floor: float
    smooth_remainder: float
    other_tail_norm: float
    tail_balance: float
    residual_balance: float
    low_degree_count: int
    tail_start: int
    explicit_end: int
    component_cache_hit: bool
    precision: int


def _metadata(
    half_width,
    low_degree_count,
    tail_start,
    explicit_end,
    maximum_smooth_power,
    self_remainder_end,
    precision,
    pointwise_subdivisions,
):
    return {
        "format": 1,
        "architecture": "third-window-thirteen-block",
        "half_width": repr(half_width),
        "low_degree_count": low_degree_count,
        "tail_start": tail_start,
        "explicit_end": explicit_end,
        "maximum_smooth_power": maximum_smooth_power,
        "retain_self_tail": True,
        "self_remainder_end": self_remainder_end,
        "precision": precision,
        "pointwise_subdivisions": pointwise_subdivisions,
        "smooth_target_rule": "maximum_power+source_degree_count+2",
        "singular_moment_order": 8,
    }


def certify_third_window_schur(
    half_width: float = 0.7,
    low_degree_count: int = 12,
    tail_start: int = 176,
    explicit_end: int = 8192,
    maximum_smooth_power: int = 47,
    tail_balance: float = 0.2,
    residual_balance: float = 0.0001,
    self_remainder_end: int = 32768,
    pointwise_subdivisions: int = 1024,
    precision: int = 512,
    expected_negative_count: int = 0,
    component_cache_path: str | None = None,
) -> ThirdWindowSchurCertificate:
    """Build or load every rigorous component and adjudicate both parities."""

    if min(tail_balance, residual_balance) <= 0:
        raise ValueError("the balance parameters must be positive")
    if tail_start <= low_degree_count or explicit_end <= tail_start:
        raise ValueError("invalid Schur degree ranges")
    if expected_negative_count not in (0, 1):
        raise ValueError("expected_negative_count must be zero or one")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    metadata = _metadata(
        half_width,
        low_degree_count,
        tail_start,
        explicit_end,
        maximum_smooth_power,
        self_remainder_end,
        precision,
        pointwise_subdivisions,
    )
    cached = (
        _load_component_cache(component_cache_path, metadata)
        if component_cache_path is not None
        else None
    )
    cache_hit = cached is not None
    if cached is None:
        source = build_arb_third_window_source(
            half_width,
            low_degree_count,
            low_degree_count,
            low_degree_count,
            maximum_smooth_power,
            precision,
        )
        band = build_arb_third_window_near_tail_gram(
            half_width,
            low_degree_count,
            low_degree_count,
            low_degree_count,
            low_degree_count,
            tail_start,
            precision,
            maximum_smooth_power,
        )
        flux = build_arb_third_window_flux_gram(
            half_width,
            low_degree_count,
            low_degree_count,
            low_degree_count,
            tail_start,
            explicit_end,
            precision,
        )
        singular = build_arb_third_window_singular_gram(
            half_width,
            low_degree_count,
            low_degree_count,
            low_degree_count,
            tail_start,
            explicit_end,
            8,
            precision,
        )
        self_tail = build_arb_third_window_self_gram(
            low_degree_count,
            low_degree_count,
            low_degree_count,
            tail_start,
            explicit_end,
            self_remainder_end,
            precision,
        )
        other = certify_third_window_other_tail(
            half_width,
            low_degree_count,
            low_degree_count,
            low_degree_count,
            tail_start,
            explicit_end,
            precision,
            include_self_blocks=False,
        )
        floor = certify_third_window_pointwise_floor(
            half_width,
            low_degree_count,
            maximum_smooth_power,
            pointwise_subdivisions,
            min(precision, 512),
        )
        if component_cache_path is not None:
            _save_component_cache(
                component_cache_path,
                metadata,
                source,
                band,
                flux,
                singular,
                other,
                self_tail,
                floor,
            )
    else:
        source, band, flux, singular, other, self_tail, floor = cached

    smooth_remainder = math.nextafter(source.smooth_remainder, math.inf)
    previous_precision = ctx.prec
    results = []
    try:
        ctx.prec = precision
        for parity, name in ((0, "even"), (1, "odd")):
            matrices = [
                _matrix_from_export(
                    arb,
                    arb_mat,
                    getattr(component, f"{name}_midpoint"),
                    getattr(component, f"{name}_radius"),
                )
                for component in (source, band, flux, singular, self_tail)
            ]
            source_ball, band_ball, flux_ball, singular_ball, self_ball = matrices
            low_complement = (
                arb(str(floor.complement_floor))
                - 2 * arb(str(smooth_remainder))
            )
            harmonic_low = sum(
                (arb(1) / degree for degree in range(1, low_degree_count + 1)),
                arb(0),
            )
            harmonic_tail = sum(
                (arb(1) / degree for degree in range(1, tail_start + 1)),
                arb(0),
            )
            tail_complement = (
                harmonic_tail
                + arb(str(floor.complement_floor))
                - harmonic_low
                - 2 * arb(str(smooth_remainder))
            )
            if not low_complement.lower() > 0 or not tail_complement.lower() > 0:
                raise ArithmeticError("the split Schur denominators were not positive")
            # Writing Q for degrees [d, t) and R for degrees >= t, the
            # complement obeys
            #
            #   D >= H + B I >= d_low Q + d_tail R.
            #
            # This is a form inequality and does not require D to preserve Q
            # and R.  Inversion reverses it, so
            #
            #   D^-1 <= d_low^-1 Q + d_tail^-1 R.
            #
            # The two source-to-complement Grams may therefore be charged at
            # their separate denominators even though D mixes degrees.
            tail_coupling = _coupling_gram_upper(
                arb,
                arb_mat(source_ball.nrows(), source_ball.ncols()),
                flux_ball,
                singular_ball,
                other.spectral_norm_upper,
                tail_balance,
                self_ball,
                residual_balance,
            )
            schur = arb_mat(source_ball)
            for index in range(schur.nrows()):
                schur[index, index] -= arb(str(smooth_remainder))
            schur -= band_ball / low_complement
            schur -= tail_coupling / tail_complement
            coupling = band_ball + tail_coupling
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
            if (
                inertia.negative_count != expected_negative_count
                or inertia.positive_count
                != schur.nrows() - expected_negative_count
                or inertia.unresolved_count != 0
            ):
                raise ArithmeticError(
                    f"the {name} third-window Schur inertia did not close: "
                    f"negative={inertia.negative_count}, "
                    f"positive={inertia.positive_count}, "
                    f"unresolved={inertia.unresolved_count}"
                )
            first_positive = min(
                lower for lower, _ in inertia.real_intervals if lower > 0
            )
            # The full-complement reconstruction must use its global floor,
            # namely the lower-band denominator.  The stronger tail floor is
            # used only inside the weighted Schur correction above.
            complement_float, coupling_norm, coercive = _coercive_lower_from_schur(
                arb, first_positive, low_complement, coupling
            )
            results.append(
                SecondWindowSchurParity(
                    parity=parity,
                    spectral_shift=0.0,
                    negative_count=inertia.negative_count,
                    positive_count=inertia.positive_count,
                    unresolved_count=inertia.unresolved_count,
                    first_positive_lower=first_positive,
                    complement_lower=complement_float,
                    coupling_norm_upper=coupling_norm,
                    coercive_lower=coercive,
                    entry_radius=entry_radius,
                    inertia_method=inertia.method,
                )
            )
    finally:
        ctx.prec = previous_precision

    return ThirdWindowSchurCertificate(
        half_width=half_width,
        even=results[0],
        odd=results[1],
        complement_floor=floor.complement_floor,
        tail_complement_floor=math.nextafter(
            float(tail_complement.lower()), -math.inf
        ),
        smooth_remainder=smooth_remainder,
        other_tail_norm=other.spectral_norm_upper,
        tail_balance=tail_balance,
        residual_balance=residual_balance,
        low_degree_count=low_degree_count,
        tail_start=tail_start,
        explicit_end=explicit_end,
        component_cache_hit=cache_hit,
        precision=precision,
    )
