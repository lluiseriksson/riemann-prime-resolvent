"""Rigorous multiband repair of the thirteen-block Schur certificate."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.interval_inertia import (
    certify_arb_positive_definite_by_congruence,
)
from experiments.theta_pencil.second_window_schur_certificate import (
    SecondWindowSchurParity,
    _coercive_lower_from_schur,
    _coupling_gram_upper,
    _load_component_cache,
    _matrix_from_export,
)
from experiments.theta_pencil.third_window_schur_certificate import _metadata


@dataclass(frozen=True)
class ThirdWindowMultibandSchurCertificate:
    half_width: float
    even: SecondWindowSchurParity
    odd: SecondWindowSchurParity
    band_boundaries: tuple[int, ...]
    band_denominator_lowers: tuple[float, ...]
    complement_floor: float
    smooth_remainder: float
    other_tail_norm: float
    tail_balance: float
    residual_balance: float
    low_degree_count: int
    tail_start: int
    explicit_end: int
    precision: int


def _load_registered_bands(
    path: str | Path,
    half_width: float,
    degree: int,
    tail_start: int,
    maximum_smooth_power: int,
    precision: int,
):
    with np.load(path, allow_pickle=False) as payload:
        metadata = json.loads(str(payload["metadata"].item()))
        required = {
            "format": 1,
            "architecture": "third-window-near-tail-bands",
            "half_width": repr(half_width),
            "degree": degree,
            "precision": precision,
            "maximum_smooth_power": maximum_smooth_power,
        }
        if any(metadata.get(key) != value for key, value in required.items()):
            raise ValueError("the registered near-band metadata do not match")
        boundaries = tuple(int(value) for value in metadata["boundaries"])
        if (
            len(boundaries) < 2
            or boundaries[0] != degree
            or boundaries[-1] > tail_start
            or any(right <= left for left, right in zip(boundaries[:-1], boundaries[1:]))
        ):
            raise ValueError("the registered near-band boundaries are invalid")
        bands = []
        for index in range(len(boundaries) - 1):
            bands.append(
                {
                    f"{parity}_{part}": payload[
                        f"band_{index}_{parity}_{part}"
                    ].copy()
                    for parity in ("even", "odd")
                    for part in ("midpoint", "radius")
                }
            )
    return boundaries, bands


def certify_third_window_multiband_schur(
    component_cache_path: str | Path,
    band_cache_path: str | Path,
    half_width: float = 0.72,
    low_degree_count: int = 12,
    tail_start: int = 176,
    explicit_end: int = 8192,
    maximum_smooth_power: int = 47,
    tail_balance: float = 0.2,
    residual_balance: float = 0.0001,
    self_remainder_end: int = 32768,
    pointwise_subdivisions: int = 1024,
    precision: int = 512,
) -> ThirdWindowMultibandSchurCertificate:
    """Adjudicate cached components with degree-dependent denominators."""

    if min(tail_balance, residual_balance) <= 0:
        raise ValueError("the balance parameters must be positive")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    components = _load_component_cache(
        component_cache_path,
        _metadata(
            half_width,
            low_degree_count,
            tail_start,
            explicit_end,
            maximum_smooth_power,
            self_remainder_end,
            precision,
            pointwise_subdivisions,
        ),
    )
    if components is None:
        raise FileNotFoundError(component_cache_path)
    source, aggregate, flux, singular, other, self_tail, floor = components
    boundaries, exported_bands = _load_registered_bands(
        band_cache_path,
        half_width,
        low_degree_count,
        tail_start,
        maximum_smooth_power,
        precision,
    )

    smooth_remainder = math.nextafter(source.smooth_remainder, math.inf)
    previous_precision = ctx.prec
    results = []
    denominator_lowers = None
    try:
        ctx.prec = precision
        harmonic_low = sum(
            (arb(1) / degree for degree in range(1, low_degree_count + 1)),
            arb(0),
        )
        low_complement = (
            arb(str(floor.complement_floor))
            - 2 * arb(str(smooth_remainder))
        )

        starts = list(boundaries[:-1])
        if boundaries[-1] < tail_start:
            starts.append(boundaries[-1])
        denominators = [
            sum((arb(1) / degree for degree in range(1, start + 1)), arb(0))
            - harmonic_low
            + low_complement
            for start in starts
        ]
        tail_complement = (
            sum((arb(1) / degree for degree in range(1, tail_start + 1)), arb(0))
            - harmonic_low
            + low_complement
        )
        if any(not value.lower() > 0 for value in denominators) or not (
            tail_complement.lower() > 0
        ):
            raise ArithmeticError("a multiband Schur denominator was not positive")
        denominator_lowers = tuple(
            math.nextafter(float(value.lower()), -math.inf)
            for value in denominators
        )

        for parity, name in ((0, "even"), (1, "odd")):
            source_ball, aggregate_ball, flux_ball, singular_ball, self_ball = [
                _matrix_from_export(
                    arb,
                    arb_mat,
                    getattr(component, f"{name}_midpoint"),
                    getattr(component, f"{name}_radius"),
                )
                for component in (source, aggregate, flux, singular, self_tail)
            ]
            band_balls = [
                _matrix_from_export(
                    arb,
                    arb_mat,
                    band[f"{name}_midpoint"],
                    band[f"{name}_radius"],
                )
                for band in exported_bands
            ]
            registered_sum = sum(
                band_balls,
                arb_mat(source_ball.nrows(), source_ball.ncols()),
            )
            if boundaries[-1] < tail_start:
                band_balls.append(aggregate_ball - registered_sum)

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
            for band_ball, denominator in zip(band_balls, denominators):
                schur -= band_ball / denominator
            schur -= tail_coupling / tail_complement

            positivity = certify_arb_positive_definite_by_congruence(
                schur, precision
            )
            coupling = aggregate_ball + tail_coupling
            complement_float, coupling_norm, coercive = _coercive_lower_from_schur(
                arb,
                positivity.original_spectral_lower,
                low_complement,
                coupling,
            )
            entry_radius = 0.0
            for row in range(schur.nrows()):
                for column in range(schur.ncols()):
                    entry_radius = max(
                        entry_radius,
                        _arb_radius_as_float(schur[row, column]),
                    )
            results.append(
                SecondWindowSchurParity(
                    parity=parity,
                    spectral_shift=0.0,
                    negative_count=0,
                    positive_count=schur.nrows(),
                    unresolved_count=0,
                    first_positive_lower=positivity.original_spectral_lower,
                    complement_lower=complement_float,
                    coupling_norm_upper=coupling_norm,
                    coercive_lower=coercive,
                    entry_radius=math.nextafter(entry_radius, math.inf),
                    inertia_method=positivity.method,
                )
            )
    finally:
        ctx.prec = previous_precision

    full_boundaries = boundaries
    if boundaries[-1] < tail_start:
        full_boundaries = boundaries + (tail_start,)
    return ThirdWindowMultibandSchurCertificate(
        half_width=half_width,
        even=results[0],
        odd=results[1],
        band_boundaries=full_boundaries,
        band_denominator_lowers=denominator_lowers,
        complement_floor=floor.complement_floor,
        smooth_remainder=smooth_remainder,
        other_tail_norm=other.spectral_norm_upper,
        tail_balance=tail_balance,
        residual_balance=residual_balance,
        low_degree_count=low_degree_count,
        tail_start=tail_start,
        explicit_end=explicit_end,
        precision=precision,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--component-cache", type=Path, required=True)
    parser.add_argument("--band-cache", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = certify_third_window_multiband_schur(
        args.component_cache, args.band_cache
    )
    rendered = json.dumps(asdict(certificate), indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_suffix(args.output.suffix + ".tmp")
        temporary.write_text(rendered, encoding="utf-8")
        temporary.replace(args.output)
    print(rendered, end="", flush=True)


if __name__ == "__main__":
    main()
