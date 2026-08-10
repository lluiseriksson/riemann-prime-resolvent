"""Open two-prime support interval about ``a = 0.56``."""

from __future__ import annotations

from experiments.theta_pencil.support_0551_interval_certificate import (
    TwoPrimeSupportIntervalCertificate,
    _certify_two_prime_support_interval,
)


def certify_support_056_interval(
    point_lower: float = 8.267012903894029e-10,
    precision: int = 256,
) -> TwoPrimeSupportIntervalCertificate:
    """Continue the certified ``a = 0.56`` lower bound to an open interval."""

    return _certify_two_prime_support_interval(
        center_text="0.56",
        lower_text="0.555",
        upper_text="0.57",
        point_lower=point_lower,
        precision=precision,
    )
