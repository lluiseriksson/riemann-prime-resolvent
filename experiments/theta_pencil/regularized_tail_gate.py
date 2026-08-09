"""Pre-registered gate for the final cut-basis logarithmic tail."""

from __future__ import annotations

import math


def maximum_regularized_map_bound(
    first_degree: int,
    schur_margin: float,
    tail_floor: float,
    spectral_shift: float,
) -> float:
    """Largest M allowed when ||Dg|| <= M controls the remaining tail."""

    if first_degree < 1:
        raise ValueError("first_degree must be positive")
    if schur_margin <= 0.0:
        raise ValueError("schur_margin must be positive")
    if tail_floor <= spectral_shift:
        raise ValueError("tail_floor must exceed spectral_shift")
    return (
        first_degree
        * (first_degree + 1)
        * math.sqrt(schur_margin * (tail_floor - spectral_shift))
    )
