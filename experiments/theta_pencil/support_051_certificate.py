"""Top-level unconditional localized positivity certificate at ``a=0.51``."""

from __future__ import annotations

from dataclasses import dataclass

from experiments.theta_pencil.arb_temple_certificate import certify_temple_trial
from experiments.theta_pencil.support_05_endpoint_certificate import (
    Support05EndpointCertificate,
    certify_first_prime_endpoint,
)


@dataclass(frozen=True)
class Support051Certificate:
    endpoint: Support05EndpointCertificate
    even_temple_lower: float
    odd_temple_lower: float
    global_lower: float


def certify_support_051() -> Support051Certificate:
    """Prove ``A_0.51`` is strictly positive on both parity sectors."""

    endpoint = certify_first_prime_endpoint(
        0.51,
        even_shift=0.003,
        odd_shift=0.1,
        precision=1024,
    )
    even = certify_temple_trial(
        half_width=0.51,
        trial_parity=0,
        dimension=256,
        residual_end=16384,
        second_floor=0.003,
        variation_partitions=64,
        precision=1024,
        prime_precision=10240,
    )
    odd = certify_temple_trial(
        half_width=0.51,
        trial_parity=1,
        dimension=256,
        residual_end=8192,
        second_floor=0.1,
        variation_partitions=64,
        precision=1024,
        prime_precision=10240,
    )
    if even.temple_lower <= 0 or odd.temple_lower <= 0:
        raise ArithmeticError("the a=0.51 Kato--Temple bound is not positive")
    return Support051Certificate(
        endpoint=endpoint,
        even_temple_lower=even.temple_lower,
        odd_temple_lower=odd.temple_lower,
        global_lower=min(even.temple_lower, odd.temple_lower),
    )
