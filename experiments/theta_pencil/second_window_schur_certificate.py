"""Full interval Schur certificate in the second prime window."""

from __future__ import annotations

import math
import json
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

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
from experiments.theta_pencil.arb_second_window_self_gram import (
    build_arb_second_window_self_gram,
)
from experiments.theta_pencil.arb_second_window_source import (
    build_arb_second_window_source,
)
from experiments.theta_pencil.arb_source_schur import _roundtrip_ball
from experiments.theta_pencil.interval_inertia import certify_interval_inertia
from experiments.theta_pencil.support_05_comparison import (
    certify_second_window_complement_floor,
)
from experiments.theta_pencil.second_window_pointwise_floor import (
    certify_second_window_pointwise_floor,
)


@dataclass(frozen=True)
class SecondWindowSchurParity:
    parity: int
    spectral_shift: float
    negative_count: int
    positive_count: int
    unresolved_count: int
    first_positive_lower: float
    complement_lower: float
    coupling_norm_upper: float
    coercive_lower: float
    entry_radius: float
    inertia_method: str = "direct-ball"


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
    retain_self_tail: bool
    residual_balance: float
    component_cache_hit: bool
    complement_floor_method: str
    precision: int


def _component_metadata(
    half_width,
    low_degree_count,
    tail_start,
    explicit_end,
    maximum_smooth_power,
    retain_self_tail,
    self_remainder_end,
    precision,
    comparison_subdivisions,
):
    return {
        "format": 1,
        "smooth_target_rule": "maximum_power+source_degree_count+2",
        "half_width": repr(half_width),
        "low_degree_count": low_degree_count,
        "tail_start": tail_start,
        "explicit_end": explicit_end,
        "maximum_smooth_power": maximum_smooth_power,
        "retain_self_tail": retain_self_tail,
        "self_remainder_end": self_remainder_end,
        "precision": precision,
        "comparison_subdivisions": comparison_subdivisions,
        "singular_moment_order": 8,
    }


def _save_component_cache(
    path,
    metadata,
    source,
    band,
    flux,
    singular,
    other,
    self_tail,
    floor,
):
    """Persist exported interval components without weakening their balls."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    arrays = {"metadata": np.array(json.dumps(metadata, sort_keys=True))}
    for prefix, component in (
        ("source", source),
        ("band", band),
        ("flux", flux),
        ("singular", singular),
    ):
        for parity in ("even", "odd"):
            arrays[f"{prefix}_{parity}_midpoint"] = getattr(
                component, f"{parity}_midpoint"
            )
            arrays[f"{prefix}_{parity}_radius"] = getattr(
                component, f"{parity}_radius"
            )
    if self_tail is not None:
        for parity in ("even", "odd"):
            arrays[f"self_{parity}_midpoint"] = getattr(
                self_tail, f"{parity}_midpoint"
            )
            arrays[f"self_{parity}_radius"] = getattr(
                self_tail, f"{parity}_radius"
            )
    arrays["smooth_remainder"] = np.array(source.smooth_remainder)
    arrays["other_tail_norm"] = np.array(other.spectral_norm_upper)
    arrays["complement_floor"] = np.array(floor.complement_floor)
    temporary = target.with_suffix(target.suffix + ".tmp")
    with temporary.open("wb") as stream:
        np.savez_compressed(stream, **arrays)
    temporary.replace(target)


def _load_component_cache(path, expected_metadata):
    """Load a cache only when every proof-relevant parameter agrees."""

    target = Path(path)
    if not target.exists():
        return None
    with np.load(target, allow_pickle=False) as payload:
        metadata = json.loads(str(payload["metadata"].item()))
        if metadata != expected_metadata:
            raise ValueError("the Schur component cache metadata do not match")

        def component(prefix, *, smooth=False):
            values = {}
            for parity in ("even", "odd"):
                values[f"{parity}_midpoint"] = payload[
                    f"{prefix}_{parity}_midpoint"
                ].copy()
                values[f"{parity}_radius"] = payload[
                    f"{prefix}_{parity}_radius"
                ].copy()
            if smooth:
                values["smooth_remainder"] = float(payload["smooth_remainder"])
            return SimpleNamespace(**values)

        source = component("source", smooth=True)
        band = component("band")
        flux = component("flux")
        singular = component("singular")
        self_tail = (
            component("self") if expected_metadata["retain_self_tail"] else None
        )
        other = SimpleNamespace(
            spectral_norm_upper=float(payload["other_tail_norm"])
        )
        floor = SimpleNamespace(
            complement_floor=float(payload["complement_floor"])
        )
    return source, band, flux, singular, other, self_tail, floor


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
    self_gram=None,
    residual_balance=0.01,
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
    coupling_upper = _coupling_gram_upper(
        arb,
        band_gram,
        flux_gram,
        singular_gram,
        other_tail_norm,
        tail_balance,
        self_gram,
        residual_balance,
    )
    result -= coupling_upper / denominator
    return result


def _coupling_gram_upper(
    arb,
    band_gram,
    flux_gram,
    singular_gram,
    other_tail_norm,
    tail_balance,
    self_gram=None,
    residual_balance=0.01,
):
    """Return the positive Gram majorant used in the Schur correction."""

    structured = 2 * (flux_gram + singular_gram)
    balance = arb(str(tail_balance))
    other = arb(str(other_tail_norm))
    if self_gram is None:
        result = band_gram + (1 + balance) * structured
        scalar_tail = (1 + 1 / balance) * other**2
    else:
        residual = arb(str(residual_balance))
        if not residual.lower() > 0:
            raise ValueError("residual_balance must be positive")
        combined = (1 + balance) * structured + (1 + 1 / balance) * self_gram
        result = band_gram + (1 + residual) * combined
        scalar_tail = (1 + 1 / residual) * other**2
    for index in range(result.nrows()):
        result[index, index] += scalar_tail
    return result


def _coercive_lower_from_schur(
    arb,
    schur_lower: float,
    complement_lower,
    coupling_gram_upper,
) -> tuple[float, float, float]:
    """Turn a positive Schur complement into a full operator lower bound.

    If ``D >= d I``, ``S >= s I`` and ``B B* <= G``, block Gaussian
    elimination gives

        q(u,v) >= s ||u||^2 + d ||v + D^-1 B* u||^2.

    Since ``||B||^2 <= tr G``, weighted Cauchy--Schwarz then proves the
    conservative lower bound returned here.  Only outward endpoints of Arb
    balls are exported.
    """

    s = arb(str(math.nextafter(schur_lower, -math.inf)))
    d = complement_lower
    if not s.lower() > 0 or not d.lower() > 0:
        raise ArithmeticError("the Schur coercivity inputs were not positive")
    trace = sum(
        (
            coupling_gram_upper[index, index]
            for index in range(coupling_gram_upper.nrows())
        ),
        arb(0),
    )
    if not trace.lower() >= 0:
        raise ArithmeticError("the coupling Gram trace was not nonnegative")
    coupling_norm = trace.sqrt()
    kappa = coupling_norm / d
    inverse_lower = (1 + kappa) ** 2 / s + 1 / d
    coercive = 1 / inverse_lower
    if not coercive.lower() > 0:
        raise ArithmeticError("the full coercive lower bound was unresolved")
    return (
        math.nextafter(float(d.lower()), -math.inf),
        math.nextafter(float(coupling_norm.upper()), math.inf),
        math.nextafter(float(coercive.lower()), -math.inf),
    )


def certify_second_window_schur(
    half_width: float = 0.551,
    even_shift: float = 0.001,
    odd_shift: float = 0.05,
    low_degree_count: int = 16,
    tail_start: int = 640,
    explicit_end: int = 4096,
    maximum_smooth_power: int = 23,
    tail_balance: float = 0.1,
    retain_self_tail: bool = False,
    residual_balance: float = 0.01,
    self_remainder_end: int = 16384,
    precision: int = 512,
    comparison_subdivisions: int = 80,
    expected_negative_count: int = 1,
    component_cache_path: str | None = None,
    joint_pointwise_floor: bool = False,
    pointwise_subdivisions: int = 1024,
) -> SecondWindowSchurCertificate:
    """Certify that at most one eigenvalue lies below each shift.

    The finite band ``d <= n < tail_start`` is accumulated exactly with all
    seven source blocks and the truncated smooth kernel in each row.  Above
    ``tail_start``, endpoint flux and adjacent singular Grams retain their
    directions.  The remaining map enters only through its certified norm.
    """

    if tail_balance <= 0:
        raise ValueError("tail_balance must be positive")
    if residual_balance <= 0:
        raise ValueError("residual_balance must be positive")
    if pointwise_subdivisions < 1:
        raise ValueError("pointwise_subdivisions must be positive")
    if expected_negative_count not in (0, 1):
        raise ValueError("expected_negative_count must be zero or one")
    if tail_start <= low_degree_count or explicit_end <= tail_start:
        raise ValueError("invalid Schur degree ranges")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    metadata = _component_metadata(
        half_width,
        low_degree_count,
        tail_start,
        explicit_end,
        maximum_smooth_power,
        retain_self_tail,
        self_remainder_end,
        precision,
        comparison_subdivisions,
    )
    cached = (
        _load_component_cache(component_cache_path, metadata)
        if component_cache_path is not None
        else None
    )
    cache_hit = cached is not None
    if cached is None:
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
            include_self_blocks=not retain_self_tail,
        )
        self_tail = None
        if retain_self_tail:
            self_tail = build_arb_second_window_self_gram(
                low_degree_count,
                tail_start,
                explicit_end,
                self_remainder_end,
                precision,
            )
        floor = certify_second_window_complement_floor(
            half_width,
            low_degree_count,
            min(precision, 512),
            comparison_subdivisions,
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
    if joint_pointwise_floor:
        pointwise = certify_second_window_pointwise_floor(
            half_width,
            low_degree_count,
            maximum_smooth_power,
            pointwise_subdivisions,
            min(precision, 512),
        )
        floor = SimpleNamespace(complement_floor=pointwise.complement_floor)
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
            self_ball = None
            if self_tail is not None:
                self_ball = _matrix_from_export(
                    arb,
                    arb_mat,
                    getattr(self_tail, f"{name}_midpoint"),
                    getattr(self_tail, f"{name}_radius"),
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
                self_ball,
                residual_balance,
            )
            complement_lower = (
                arb(str(floor.complement_floor))
                - arb(str(shift))
                - 2 * arb(str(smooth_remainder))
            )
            coupling_upper = _coupling_gram_upper(
                arb,
                band_ball,
                flux_ball,
                singular_ball,
                other.spectral_norm_upper,
                tail_balance,
                self_ball,
                residual_balance,
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
            first_positive_lower = min(positive_lowers)
            (
                complement_lower_float,
                coupling_norm_upper,
                coercive_lower,
            ) = _coercive_lower_from_schur(
                arb,
                first_positive_lower,
                complement_lower,
                coupling_upper,
            )
            results.append(
                SecondWindowSchurParity(
                    parity=parity,
                    spectral_shift=shift,
                    negative_count=inertia.negative_count,
                    positive_count=inertia.positive_count,
                    unresolved_count=inertia.unresolved_count,
                    first_positive_lower=first_positive_lower,
                    complement_lower=complement_lower_float,
                    coupling_norm_upper=coupling_norm_upper,
                    coercive_lower=coercive_lower,
                    entry_radius=entry_radius,
                    inertia_method=inertia.method,
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
        retain_self_tail=retain_self_tail,
        residual_balance=residual_balance,
        component_cache_hit=cache_hit,
        complement_floor_method=(
            "joint-two-prime-pointwise" if joint_pointwise_floor else "prime-two-minus-norm"
        ),
        precision=precision,
    )
