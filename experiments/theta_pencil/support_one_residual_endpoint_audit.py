"""Endpoint audit for a frozen support-one residual Schur trial.

This is a floating design gate.  It detects whether the leading endpoint jump
survives in ``e_low - Y`` before any expensive Arb action grid is launched.
The signed-band calculation contains only that leading jet and is not a bound
for the complete operator, whose higher jets may cancel it on finite bands.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.special import digamma

from experiments.theta_pencil.legendre_jump_tail import (
    bernstein_jump_tail_bound,
)
from experiments.theta_pencil.prime_jet_tail import (
    endpoint_jet_matrix,
    truncated_power_coefficients,
)
from experiments.theta_pencil.screw_weil_operator import von_mangoldt
from experiments.theta_pencil.semilocal_weil_matrix import EULER_GAMMA
from experiments.theta_pencil.support_one_degreewise_schur import (
    support_one_bounded_part_lower,
    support_one_degreewise_denominator_lowers,
)


ACTIVE_SUPPORT_ONE_PRIME_POWERS = (2, 3, 4, 5, 7)


@dataclass(frozen=True)
class FloatingResidualEndpointParity:
    parity: str
    residual_endpoint_norm: float
    raw_endpoint_norm: float
    residual_to_raw_ratio: float
    triangular_weighted_norm_upper: float
    triangular_correction_upper: float
    signed_leading_jet_band_norm: float


@dataclass(frozen=True)
class FloatingResidualEndpointAudit:
    first_degree: int
    last_degree: int
    even: FloatingResidualEndpointParity
    odd: FloatingResidualEndpointParity
    context: str = (
        "floating leading-endpoint-jet gate; the triangular value is a valid "
        "upper bound for this jet, while the signed band is diagnostic and "
        "does not include higher jets or analytic remainders"
    )


def _parity_audit(
    payload,
    parity_name: str,
    parity: int,
    finite_dimension: int,
    first_degree: int,
    last_degree: int,
    denominator_floor: float,
) -> FloatingResidualEndpointParity:
    action_vectors = np.array(
        payload[f"{parity_name}_action_vectors"], dtype=float
    )
    right_factor = np.array(payload[f"{parity_name}_right_factor"], dtype=float)
    low_indices = np.array(payload[f"{parity_name}_low_indices"], dtype=int)
    residual_vectors = -(action_vectors @ right_factor)
    residual_vectors[low_indices, np.arange(len(low_indices))] += 1.0
    raw_vectors = np.zeros_like(residual_vectors)
    raw_vectors[low_indices, np.arange(len(low_indices))] = 1.0

    endpoint = endpoint_jet_matrix(np.arange(finite_dimension), 1)[:, 0]
    residual_endpoint = endpoint @ residual_vectors
    raw_endpoint = endpoint @ raw_vectors
    residual_norm = float(np.linalg.norm(residual_endpoint))
    raw_norm = float(np.linalg.norm(raw_endpoint))

    triangular = 0.0
    for prime_power in ACTIVE_SUPPORT_ONE_PRIME_POWERS:
        cut = 1.0 - math.log(prime_power)
        cut_weight = (1.0 - cut * cut) ** 0.25
        scalar_tail = bernstein_jump_tail_bound(
            1.0, cut_weight, first_degree
        )
        triangular += (
            2.0
            * von_mangoldt(prime_power)
            / math.sqrt(prime_power)
            * residual_norm
            * scalar_tail
            / math.sqrt(denominator_floor)
        )

    high_degrees = np.arange(
        first_degree + ((first_degree - parity) % 2), last_degree, 2
    )
    action = np.zeros((len(high_degrees), len(low_indices)))
    for prime_power in ACTIVE_SUPPORT_ONE_PRIME_POWERS:
        cut = 1.0 - math.log(prime_power)
        row = truncated_power_coefficients(cut, last_degree, 1)[
            0, high_degrees
        ]
        coefficient = -2.0 * von_mangoldt(prime_power) / math.sqrt(
            prime_power
        )
        action += np.outer(coefficient * row, residual_endpoint)
    beta = float(support_one_bounded_part_lower())
    denominators = digamma(high_degrees + 1.0) + EULER_GAMMA + beta
    gram = action.T @ (action / denominators[:, None])
    band_norm = float(np.linalg.eigvalsh(0.5 * (gram + gram.T))[-1])
    return FloatingResidualEndpointParity(
        parity=parity_name,
        residual_endpoint_norm=residual_norm,
        raw_endpoint_norm=raw_norm,
        residual_to_raw_ratio=residual_norm / raw_norm,
        triangular_weighted_norm_upper=triangular,
        triangular_correction_upper=triangular * triangular,
        signed_leading_jet_band_norm=band_norm,
    )


def run_support_one_residual_endpoint_audit(
    trial: Path,
    first_degree: int = 256,
    last_degree: int = 4096,
) -> FloatingResidualEndpointAudit:
    """Measure the uncancelled endpoint value of one frozen trial."""

    if first_degree < 59 or last_degree <= first_degree:
        raise ValueError("require 59 <= first_degree < last_degree")
    denominator_floor = float(
        support_one_degreewise_denominator_lowers(first_degree + 1)[-1]
    )
    with np.load(trial, allow_pickle=False) as payload:
        metadata = json.loads(str(payload["metadata"].item()))
        if metadata.get("architecture") != "support-one-residual-schur-trial":
            raise ValueError("the input is not a support-one residual trial")
        finite_dimension = int(metadata["finite_dimension"])
        if first_degree < finite_dimension:
            raise ValueError("the endpoint band must start after the trial support")
        even = _parity_audit(
            payload,
            "even",
            0,
            finite_dimension,
            first_degree,
            last_degree,
            denominator_floor,
        )
        odd = _parity_audit(
            payload,
            "odd",
            1,
            finite_dimension,
            first_degree,
            last_degree,
            denominator_floor,
        )
    return FloatingResidualEndpointAudit(
        first_degree=first_degree,
        last_degree=last_degree,
        even=even,
        odd=odd,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trial", type=Path, required=True)
    parser.add_argument("--first-degree", type=int, default=256)
    parser.add_argument("--last-degree", type=int, default=4096)
    args = parser.parse_args()
    result = run_support_one_residual_endpoint_audit(
        args.trial, args.first_degree, args.last_degree
    )
    print(json.dumps(asdict(result), indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
