"""Unconditional localized positivity certificate at ``a = 0.56``."""

from __future__ import annotations

from dataclasses import dataclass

from experiments.theta_pencil.second_window_schur_certificate import (
    SecondWindowSchurCertificate,
    certify_second_window_schur,
)


@dataclass(frozen=True)
class Support056Certificate:
    schur: SecondWindowSchurCertificate
    even_schur_lower: float
    odd_schur_lower: float
    even_coercive_lower: float
    odd_coercive_lower: float
    global_coercive_lower: float


def certify_support_056() -> Support056Certificate:
    """Prove strict positivity at the second registered two-prime anchor."""

    schur = certify_second_window_schur(
        half_width=0.56,
        even_shift=0.0,
        odd_shift=0.0,
        expected_negative_count=0,
    )
    if any(
        (
            schur.even.negative_count,
            schur.odd.negative_count,
            schur.even.unresolved_count,
            schur.odd.unresolved_count,
        )
    ) or min(
        schur.even.first_positive_lower,
        schur.odd.first_positive_lower,
        schur.even.coercive_lower,
        schur.odd.coercive_lower,
    ) <= 0:
        raise ArithmeticError("the a=0.56 Schur positivity did not close")
    return Support056Certificate(
        schur=schur,
        even_schur_lower=schur.even.first_positive_lower,
        odd_schur_lower=schur.odd.first_positive_lower,
        even_coercive_lower=schur.even.coercive_lower,
        odd_coercive_lower=schur.odd.coercive_lower,
        global_coercive_lower=min(
            schur.even.coercive_lower, schur.odd.coercive_lower
        ),
    )
