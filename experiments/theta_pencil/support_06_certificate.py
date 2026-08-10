"""Unconditional localized positivity frontier at ``a = 0.60``."""

from __future__ import annotations

from dataclasses import dataclass

from experiments.theta_pencil.second_window_schur_certificate import (
    SecondWindowSchurCertificate,
    certify_second_window_schur,
)


@dataclass(frozen=True)
class Support06Certificate:
    schur: SecondWindowSchurCertificate
    global_coercive_lower: float
    monotone_support_upper: float


def certify_support_06() -> Support06Certificate:
    """Prove positivity at 0.60, hence at every smaller support."""

    schur = certify_second_window_schur(
        half_width=0.6,
        even_shift=0.0,
        odd_shift=0.0,
        expected_negative_count=0,
    )
    parity_data = (schur.even, schur.odd)
    if any(
        parity.negative_count != 0
        or parity.unresolved_count != 0
        or parity.first_positive_lower <= 0
        or parity.coercive_lower <= 0
        for parity in parity_data
    ):
        raise ArithmeticError("the a=0.60 Schur positivity did not close")
    return Support06Certificate(
        schur=schur,
        global_coercive_lower=min(
            schur.even.coercive_lower, schur.odd.coercive_lower
        ),
        monotone_support_upper=0.6,
    )
