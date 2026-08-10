"""Support-independent band design for harmonic Schur denominators."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class HarmonicSchurStratification:
    first_degree: int
    last_degree: int
    base_denominator: float
    relative_overcharge: float
    boundaries: tuple[int, ...]
    denominator_starts: tuple[float, ...]
    maximum_denominator_ratio: float
    band_count_logarithmic_upper: int


def build_harmonic_schur_stratification(
    first_degree: int,
    last_degree: int,
    base_denominator: float,
    relative_overcharge: float,
) -> HarmonicSchurStratification:
    """Greedily keep each band's inverse-denominator loss below ``1+eps``.

    Here ``d_n = d_first + H_n - H_first``.  If a band starts at ``m``
    and ``d_n <= (1+eps)d_m`` throughout it, charging the whole band at
    ``d_m`` overestimates the degreewise Schur correction by at most the
    factor ``1+eps`` in Loewner order.
    """

    if first_degree < 1 or last_degree <= first_degree:
        raise ValueError("require 1 <= first_degree < last_degree")
    if not math.isfinite(base_denominator) or base_denominator <= 0.0:
        raise ValueError("base_denominator must be finite and positive")
    if not math.isfinite(relative_overcharge) or relative_overcharge <= 0.0:
        raise ValueError("relative_overcharge must be finite and positive")

    harmonic = [0.0]
    for degree in range(1, last_degree + 1):
        harmonic.append(harmonic[-1] + 1.0 / degree)

    def denominator(degree: int) -> float:
        return base_denominator + harmonic[degree] - harmonic[first_degree]

    factor = 1.0 + relative_overcharge
    boundaries = [first_degree]
    starts = []
    maximum_ratio = 1.0
    start = first_degree
    while start < last_degree:
        start_denominator = denominator(start)
        starts.append(start_denominator)
        end = start + 1
        while (
            end < last_degree
            and denominator(end) <= factor * start_denominator
        ):
            end += 1
        last_in_band = end - 1
        maximum_ratio = max(
            maximum_ratio,
            denominator(last_in_band) / start_denominator,
        )
        boundaries.append(end)
        start = end

    total_ratio = denominator(last_degree - 1) / base_denominator
    logarithmic_upper = (
        math.ceil(math.log(max(1.0, total_ratio)) / math.log(factor)) + 1
    )
    return HarmonicSchurStratification(
        first_degree=first_degree,
        last_degree=last_degree,
        base_denominator=base_denominator,
        relative_overcharge=relative_overcharge,
        boundaries=tuple(boundaries),
        denominator_starts=tuple(starts),
        maximum_denominator_ratio=maximum_ratio,
        band_count_logarithmic_upper=logarithmic_upper,
    )
