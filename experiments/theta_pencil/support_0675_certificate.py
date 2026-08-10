"""Unconditional localized positivity frontier at ``a = 0.675``."""

from __future__ import annotations

from dataclasses import dataclass

from experiments.theta_pencil.second_window_schur_certificate import (
    SecondWindowSchurCertificate,
    certify_second_window_schur,
)


@dataclass(frozen=True)
class Support0675Certificate:
    schur: SecondWindowSchurCertificate
    global_coercive_lower: float
    monotone_support_upper: float


def certify_support_0675(
    component_cache_path: str | None = None,
) -> Support0675Certificate:
    """Prove positivity through 0.675 with the joint two-prime floor."""

    schur = certify_second_window_schur(
        half_width=0.675,
        even_shift=0.0,
        odd_shift=0.0,
        maximum_smooth_power=39,
        tail_balance=0.05,
        retain_self_tail=True,
        residual_balance=0.01,
        self_remainder_end=16384,
        expected_negative_count=0,
        component_cache_path=component_cache_path,
        joint_pointwise_floor=True,
        pointwise_subdivisions=1024,
    )
    parity_data = (schur.even, schur.odd)
    if any(
        parity.negative_count != 0
        or parity.unresolved_count != 0
        or parity.first_positive_lower <= 0
        or parity.coercive_lower <= 0
        for parity in parity_data
    ):
        raise ArithmeticError("the a=0.675 Schur positivity did not close")
    return Support0675Certificate(
        schur=schur,
        global_coercive_lower=min(
            schur.even.coercive_lower, schur.odd.coercive_lower
        ),
        monotone_support_upper=0.675,
    )
