"""Float-design audit for paying endpoint jets with source dimensions.

The registered degree-58 finite matrix is re-sliced at larger even source
dimensions.  The optional leading-jet charge is deliberately isolated: its
inertia is a design diagnostic, not a certificate for the complete residual.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.special import digamma

from experiments.theta_pencil.prime_jet_tail import (
    endpoint_jet_matrix,
    truncated_power_coefficients,
)
from experiments.theta_pencil.rational_joint_five_seven_certificate import (
    certify_rational_support_one_tail,
)
from experiments.theta_pencil.screw_weil_operator import von_mangoldt
from experiments.theta_pencil.semilocal_weil_matrix import EULER_GAMMA
from experiments.theta_pencil.support_one_degreewise_schur import (
    _load_or_build_blocks,
    _load_or_build_high_component,
    _smooth_high_component_labels,
    support_one_bounded_part_lower,
)


@dataclass(frozen=True)
class FloatingSourceBufferParity:
    parity: int
    dimension: int
    raw_positive_count: int
    finite_schur_positive_count: int
    isolated_leading_jet_positive_count: int
    endpoint_defect_norm: float
    leading_jet_band_norm: float
    first_finite_schur_positive: float


@dataclass(frozen=True)
class FloatingSourceBufferRow:
    source_dimension: int
    even: FloatingSourceBufferParity
    odd: FloatingSourceBufferParity


@dataclass(frozen=True)
class FloatingSourceBufferAudit:
    finite_dimension: int
    first_tail_degree: int
    last_tail_degree: int
    rows: tuple[FloatingSourceBufferRow, ...]
    context: str = (
        "floating finite-section design audit; the isolated leading-jet "
        "charge omits all higher jets and remainders and is not an operator "
        "lower bound"
    )


def _positive_count(eigenvalues: np.ndarray, tolerance: float) -> int:
    return int(np.count_nonzero(eigenvalues > tolerance))


def run_support_one_source_buffer_audit(
    matrix_cache: Path,
    component_cache_dir: Path,
    source_dimensions: tuple[int, ...] = (58, 60, 62, 64),
    finite_dimension: int = 256,
    quadrature_order: int = 1024,
    maximum_smooth_power: int = 95,
    first_tail_degree: int = 256,
    last_tail_degree: int = 4096,
    zero_tolerance: float = 1.0e-12,
) -> FloatingSourceBufferAudit:
    """Re-slice one registered finite matrix at larger source cutoffs."""

    if any(value < 58 or value % 2 for value in source_dimensions):
        raise ValueError("source dimensions must be even and at least 58")
    if any(value >= finite_dimension for value in source_dimensions):
        raise ValueError("source dimensions must be below the finite dimension")
    if (
        first_tail_degree < finite_dimension
        or last_tail_degree <= first_tail_degree
    ):
        raise ValueError("the leading-jet band must start after the finite section")

    source58, cross58 = _load_or_build_blocks(
        matrix_cache,
        component_cache_dir,
        58,
        finite_dimension,
        quadrature_order,
        maximum_smooth_power,
    )
    high58 = sum(
        (
            _load_or_build_high_component(
                label,
                component_cache_dir,
                58,
                finite_dimension,
                quadrature_order,
                maximum_smooth_power,
            )
            for label in (
                "base",
                "2",
                "3",
                "4",
                "5",
                "7",
                *_smooth_high_component_labels(maximum_smooth_power),
            )
        ),
        np.zeros((finite_dimension - 58,) * 2),
    )
    full = np.block([[source58, cross58], [cross58.T, high58]])
    complement_floor = float(
        certify_rational_support_one_tail().complement_margin
    )
    beta = float(support_one_bounded_part_lower())
    rows = []
    for source_dimension in source_dimensions:
        source = full[:source_dimension, :source_dimension]
        cross = full[:source_dimension, source_dimension:]
        high = full[source_dimension:, source_dimension:]
        parity_rows = []
        for parity in (0, 1):
            low_indices = np.arange(parity, source_dimension, 2)
            high_global = np.arange(
                source_dimension + ((source_dimension - parity) % 2),
                finite_dimension,
                2,
            )
            high_indices = high_global - source_dimension
            parity_source = source[np.ix_(low_indices, low_indices)]
            parity_cross = cross[np.ix_(low_indices, high_indices)]
            parity_high = high[np.ix_(high_indices, high_indices)]
            raw_values = np.linalg.eigvalsh(parity_source)
            trial = np.linalg.solve(parity_high, parity_cross.T)
            schur = parity_source - parity_cross @ trial
            schur_values = np.linalg.eigvalsh(0.5 * (schur + schur.T))

            low_endpoint = endpoint_jet_matrix(low_indices, 1)[:, 0]
            high_endpoint = endpoint_jet_matrix(high_global, 1)[:, 0]
            endpoint_defect = low_endpoint - high_endpoint @ trial
            tail_degrees = np.arange(
                first_tail_degree + ((first_tail_degree - parity) % 2),
                last_tail_degree,
                2,
            )
            action = np.zeros((len(tail_degrees), len(low_indices)))
            for prime_power in (2, 3, 4, 5, 7):
                cut = 1.0 - math.log(prime_power)
                row = truncated_power_coefficients(
                    cut, last_tail_degree, 1
                )[0, tail_degrees]
                coefficient = -2.0 * von_mangoldt(
                    prime_power
                ) / math.sqrt(prime_power)
                action += np.outer(coefficient * row, endpoint_defect)
            denominators = (
                digamma(tail_degrees + 1.0) + EULER_GAMMA + beta
            )
            leading_gram = action.T @ (action / denominators[:, None])
            charged = schur - leading_gram / complement_floor
            charged_values = np.linalg.eigvalsh(0.5 * (charged + charged.T))
            positive = schur_values[schur_values > zero_tolerance]
            parity_rows.append(
                FloatingSourceBufferParity(
                    parity=parity,
                    dimension=len(low_indices),
                    raw_positive_count=_positive_count(
                        raw_values, zero_tolerance
                    ),
                    finite_schur_positive_count=_positive_count(
                        schur_values, zero_tolerance
                    ),
                    isolated_leading_jet_positive_count=_positive_count(
                        charged_values, zero_tolerance
                    ),
                    endpoint_defect_norm=float(np.linalg.norm(endpoint_defect)),
                    leading_jet_band_norm=float(
                        np.linalg.eigvalsh(
                            0.5 * (leading_gram + leading_gram.T)
                        )[-1]
                    ),
                    first_finite_schur_positive=float(positive[0]),
                )
            )
        rows.append(
            FloatingSourceBufferRow(
                source_dimension=source_dimension,
                even=parity_rows[0],
                odd=parity_rows[1],
            )
        )
    return FloatingSourceBufferAudit(
        finite_dimension=finite_dimension,
        first_tail_degree=first_tail_degree,
        last_tail_degree=last_tail_degree,
        rows=tuple(rows),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-cache", type=Path, required=True)
    parser.add_argument("--component-cache-dir", type=Path, required=True)
    parser.add_argument(
        "--source-dimensions",
        type=int,
        nargs="+",
        default=(58, 60, 62, 64),
    )
    parser.add_argument("--finite-dimension", type=int, default=256)
    parser.add_argument("--first-tail-degree", type=int, default=256)
    parser.add_argument("--last-tail-degree", type=int, default=4096)
    args = parser.parse_args()
    result = run_support_one_source_buffer_audit(
        matrix_cache=args.matrix_cache,
        component_cache_dir=args.component_cache_dir,
        source_dimensions=tuple(args.source_dimensions),
        finite_dimension=args.finite_dimension,
        first_tail_degree=args.first_tail_degree,
        last_tail_degree=args.last_tail_degree,
    )
    print(json.dumps(asdict(result), indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
