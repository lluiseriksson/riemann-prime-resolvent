"""Unconditional localized positivity frontier at ``a = 0.72``."""

from __future__ import annotations

from dataclasses import dataclass

from experiments.theta_pencil.third_window_multiband_schur_certificate import (
    ThirdWindowMultibandSchurCertificate,
    certify_third_window_multiband_schur,
)


@dataclass(frozen=True)
class Support072Certificate:
    schur: ThirdWindowMultibandSchurCertificate
    global_coercive_lower: float
    monotone_support_upper: float


def certify_support_072(
    component_cache_path: str,
    band_cache_path: str,
) -> Support072Certificate:
    """Prove positivity through support 0.72 with the registered band split."""

    schur = certify_third_window_multiband_schur(
        component_cache_path=component_cache_path,
        band_cache_path=band_cache_path,
    )
    if any(
        parity.negative_count != 0
        or parity.unresolved_count != 0
        or parity.first_positive_lower <= 0
        or parity.coercive_lower <= 0
        for parity in (schur.even, schur.odd)
    ):
        raise ArithmeticError("the a=0.72 multiband positivity did not close")
    return Support072Certificate(
        schur=schur,
        global_coercive_lower=min(
            schur.even.coercive_lower, schur.odd.coercive_lower
        ),
        monotone_support_upper=0.72,
    )
