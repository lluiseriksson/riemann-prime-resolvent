"""Localized positivity certificate immediately below ``log(3) / 2``."""

from __future__ import annotations

from dataclasses import dataclass

from experiments.theta_pencil.arb_temple_certificate import certify_temple_trial
from experiments.theta_pencil.support_05_endpoint_certificate import (
    Support05EndpointCertificate,
    certify_first_prime_endpoint,
)
from experiments.theta_pencil.support_window import in_first_prime_window


# This terminating decimal is rigorously smaller than log(3) / 2.  In
# particular, the prime-three translation has empty overlap and must not be
# included in the first-prime-window operator.
HALF_WIDTH_BELOW_PRIME_THREE = 0.5493061443340548


@dataclass(frozen=True)
class SupportNearPrimeThreeCertificate:
    endpoint: Support05EndpointCertificate
    even_temple_lower: float
    odd_temple_lower: float
    global_lower: float


def certify_support_near_prime_three() -> SupportNearPrimeThreeCertificate:
    """Prove localized positivity at ``HALF_WIDTH_BELOW_PRIME_THREE``."""

    half_width = HALF_WIDTH_BELOW_PRIME_THREE
    if not in_first_prime_window(half_width):
        raise ArithmeticError("the registered support is not below log(3) / 2")

    endpoint = certify_first_prime_endpoint(
        half_width,
        even_shift=0.001,
        odd_shift=0.05,
        precision=1024,
    )
    even = certify_temple_trial(
        half_width=half_width,
        trial_parity=0,
        dimension=512,
        residual_end=131072,
        second_floor=0.001,
        variation_partitions=256,
        precision=1024,
        prime_precision=10240,
    )
    odd = certify_temple_trial(
        half_width=half_width,
        trial_parity=1,
        dimension=256,
        residual_end=8192,
        second_floor=0.05,
        variation_partitions=64,
        precision=1024,
        prime_precision=10240,
    )
    if even.temple_lower <= 0 or odd.temple_lower <= 0:
        raise ArithmeticError("the near-prime-three Kato--Temple bound is not positive")
    return SupportNearPrimeThreeCertificate(
        endpoint=endpoint,
        even_temple_lower=even.temple_lower,
        odd_temple_lower=odd.temple_lower,
        global_lower=min(even.temple_lower, odd.temple_lower),
    )
