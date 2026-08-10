"""Unconditional localized positivity frontier at ``a = 0.7``."""

from __future__ import annotations

from dataclasses import dataclass

from experiments.theta_pencil.third_window_schur_certificate import (
    ThirdWindowSchurCertificate,
    certify_third_window_schur,
)


@dataclass(frozen=True)
class Support070Certificate:
    schur: ThirdWindowSchurCertificate
    global_coercive_lower: float
    monotone_support_upper: float


def certify_support_070(
    component_cache_path: str | None = None,
) -> Support070Certificate:
    """Prove positivity through support 0.7 in the thirteen-block window."""

    schur = certify_third_window_schur(
        component_cache_path=component_cache_path
    )
    if any(
        parity.negative_count != 0
        or parity.unresolved_count != 0
        or parity.first_positive_lower <= 0
        or parity.coercive_lower <= 0
        for parity in (schur.even, schur.odd)
    ):
        raise ArithmeticError("the a=0.7 Schur positivity did not close")
    return Support070Certificate(
        schur=schur,
        global_coercive_lower=min(
            schur.even.coercive_lower, schur.odd.coercive_lower
        ),
        monotone_support_upper=0.7,
    )
