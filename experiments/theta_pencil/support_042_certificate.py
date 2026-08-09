"""Reproduce the localized Weil--Suzuki positivity certificate at a = 0.42.

This is intentionally a long-running certificate driver.  The floating
Gauss--Legendre matrices are used only as independently computed targets;
Arb reconstructs the exact finite sources from endpoint jets and then checks
that they lie in fixed entrywise boxes around those targets.
"""

from __future__ import annotations

from dataclasses import dataclass

from experiments.theta_pencil.arb_parity_tail_budget import (
    certify_parity_tail_budget,
)
from experiments.theta_pencil.arb_source_schur import certify_source_schur_box
from experiments.theta_pencil.arb_temple_certificate import certify_temple_trial
from experiments.theta_pencil.interval_inertia import certify_interval_inertia
from experiments.theta_pencil.parity_inertia_budget import run_parity_inertia_audit


@dataclass(frozen=True)
class ParitySupportCertificate:
    parity: int
    spectral_floor: float
    source_distance: float
    negative_count: int
    positive_count: int
    first_positive_lower: float
    tail_correction_upper: float
    post_tail_margin: float
    temple_lower: float


@dataclass(frozen=True)
class Support042Certificate:
    half_width: float
    odd: ParitySupportCertificate
    even: ParitySupportCertificate
    global_lower: float


def _run_parity(
    parity: int,
    low_dimension: int,
    spectral_floor: float,
    jet_norm_upper: float,
) -> ParitySupportCertificate:
    audit = run_parity_inertia_audit(
        parity=parity,
        half_width=0.42,
        low_dimension=low_dimension,
        finite_dimension=4096,
        smooth_dimension=512,
        spectral_floor=spectral_floor,
        jet_count=28,
        jet_end=100_000,
        partitions=64,
    )
    source = certify_source_schur_box(
        parity,
        audit.jet_schur_matrix,
        half_width=0.42,
        low_dimension=low_dimension,
        finite_dimension=4096,
        smooth_dimension=512,
        spectral_shift=spectral_floor,
        jet_count=28,
        jet_end=100_000,
        target_radius=1.0e-9,
        precision=768,
        prime_precision=16_384,
    )
    if not source.contained_in_target_box:
        raise ArithmeticError("the exact Schur source escaped the registered box")

    inertia = certify_interval_inertia(
        audit.jet_schur_matrix, entry_radius=1.0e-9, precision=768
    )
    if not (
        inertia.negative_count == 1
        and inertia.positive_count == len(audit.jet_schur_matrix) - 1
        and inertia.unresolved_count == 0
    ):
        raise ArithmeticError("the registered Schur box has unresolved inertia")
    first_positive = min(lower for lower, _ in inertia.real_intervals if lower > 0)

    tail = certify_parity_tail_budget(
        parity=parity,
        half_width=0.42,
        low_dimension=low_dimension,
        finite_dimension=4096,
        smooth_dimension=512,
        jet_count=28,
        jet_end=100_000,
        spectral_shift=spectral_floor,
        partitions=64,
        precision=768,
        jet_correction_norm_upper=jet_norm_upper,
    )
    margin = first_positive - tail.correction_upper
    if margin <= 0:
        raise ArithmeticError("the omitted Schur tail exhausts the inertia margin")

    temple = certify_temple_trial(
        half_width=0.42,
        trial_parity=parity,
        dimension=256,
        residual_end=8192,
        second_floor=spectral_floor,
        variation_partitions=32,
        precision=1024,
        prime_precision=10_240,
    )
    if temple.temple_lower <= 0:
        raise ArithmeticError("the parity Temple lower bound is not positive")

    return ParitySupportCertificate(
        parity=parity,
        spectral_floor=spectral_floor,
        source_distance=source.maximum_target_distance,
        negative_count=inertia.negative_count,
        positive_count=inertia.positive_count,
        first_positive_lower=first_positive,
        tail_correction_upper=tail.correction_upper,
        post_tail_margin=margin,
        temple_lower=temple.temple_lower,
    )


def certify_support_042() -> Support042Certificate:
    """Run the two independent parity certificates and combine their floors."""
    odd = _run_parity(1, 176, 0.5, 0.06)
    even = _run_parity(0, 128, 0.1, 0.03)
    return Support042Certificate(
        half_width=0.42,
        odd=odd,
        even=even,
        global_lower=min(odd.temple_lower, even.temple_lower),
    )


if __name__ == "__main__":
    print(certify_support_042())
