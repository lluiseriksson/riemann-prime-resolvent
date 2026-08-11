"""Degree-resolved support-one Schur design audit.

The rational support-one tail certificate proves a global lower bound for the
bounded part of the Legendre operator.  Keeping the harmonic diagonal
unabsorbed upgrades its single degree-58 floor to one exact denominator per
Legendre degree.  The finite matrix calculation in this module is only a
floating design audit; the denominators themselves are exact Fractions.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np

from experiments.theta_pencil.legendre_feshbach import (
    build_legendre_weil_components,
)
from experiments.theta_pencil.legendre_jump_tail import (
    potential_operator_tail_bound,
    wang_normalized_tail_bound,
)
from experiments.theta_pencil.prime_jet_tail import (
    active_prime_jet_tail_weighted_norm,
    active_prime_remainder_variation_bound,
)
from experiments.theta_pencil.rational_joint_five_seven_certificate import (
    certify_rational_support_one_tail,
)
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_matrix,
    smooth_kernel_series_remainder_bound,
)


@dataclass(frozen=True)
class FloatingDegreewiseSchurParity:
    parity: int
    dimension: int
    negative_count: int
    positive_count: int
    unresolved_count: int
    least_eigenvalues: tuple[float, ...]


@dataclass(frozen=True)
class FloatingSupportOneDegreewiseSchur:
    source_dimension: int
    finite_dimension: int
    quadrature_order: int
    maximum_smooth_power: int
    denominator_lower_minimum: float
    denominator_lower_maximum: float
    smooth_remainder: float
    even: FloatingDegreewiseSchurParity
    odd: FloatingDegreewiseSchurParity
    context: str = (
        "floating finite degreewise-majorant audit; the infinite cross tail "
        "and interval entry enclosures are omitted"
    )


@dataclass(frozen=True)
class FloatingSupportOneAbsoluteTailParity:
    parity: int
    endpoint_jet_weighted_norm: float
    prime_remainder_weighted_norm: float
    potential_weighted_norm: float
    smooth_weighted_norm: float
    total_weighted_norm: float
    correction_norm_upper: float


@dataclass(frozen=True)
class FloatingSupportOneAbsoluteTail:
    first_degree: int
    jet_count: int
    partitions: int
    denominator_floor: float
    even: FloatingSupportOneAbsoluteTailParity
    odd: FloatingSupportOneAbsoluteTailParity
    context: str = (
        "floating absolute-norm tail design audit; a large upper bound is a "
        "failure of this estimate, not a lower bound for the true correction"
    )


def support_one_bounded_part_lower() -> Fraction:
    """Return the exact lower bound for the non-harmonic operator part."""

    certificate = certify_rational_support_one_tail()
    return certificate.complement_margin - certificate.harmonic_floor


def support_one_degreewise_denominator_lowers(
    finite_dimension: int,
    source_dimension: int = 58,
) -> tuple[Fraction, ...]:
    """Exact diagonal Schur minorant for degrees in ``[source, finite)``.

    If ``L = diag(H_n) + B`` and the rational certificate gives
    ``B >= beta I``, then ``L >= diag(H_n + beta)``.  The first returned
    denominator is exactly the registered degree-58 complement margin.
    """

    if source_dimension != 58:
        raise ValueError("the registered rational certificate starts at degree 58")
    if finite_dimension <= source_dimension:
        raise ValueError("finite_dimension must exceed source_dimension")
    beta = support_one_bounded_part_lower()
    harmonic = sum(
        (Fraction(1, degree) for degree in range(1, source_dimension + 1)),
        Fraction(0),
    )
    denominators = []
    for degree in range(source_dimension, finite_dimension):
        if degree > source_dimension:
            harmonic += Fraction(1, degree)
        denominator = harmonic + beta
        if denominator <= 0:
            raise ArithmeticError("a registered degreewise denominator is nonpositive")
        denominators.append(denominator)
    return tuple(denominators)


def _atomic_save_matrix(path: Path, metadata: dict, matrix: np.ndarray) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as stream:
        np.savez(
            stream,
            metadata=np.array(json.dumps(metadata, sort_keys=True)),
            matrix=np.asarray(matrix, dtype=np.float64),
        )
    os.replace(temporary, path)


def _load_or_build_matrix(
    cache: Path | None,
    finite_dimension: int,
    quadrature_order: int,
    maximum_smooth_power: int,
) -> np.ndarray:
    metadata = {
        "format": 1,
        "architecture": "support-one-degreewise-schur",
        "finite_dimension": finite_dimension,
        "quadrature_order": quadrature_order,
        "maximum_smooth_power": maximum_smooth_power,
    }
    if cache is not None and cache.exists():
        with np.load(cache, allow_pickle=False) as payload:
            observed = json.loads(str(payload["metadata"].item()))
            if observed != metadata:
                raise ValueError("the degreewise Schur cache metadata do not match")
            matrix = np.array(payload["matrix"], dtype=float)
        if matrix.shape != (finite_dimension, finite_dimension):
            raise ValueError("the cached matrix has the wrong shape")
        return matrix

    components = build_legendre_weil_components(
        1.0, finite_dimension, quadrature_order
    )
    expected = (2, 3, 4, 5, 7)
    if components.active_prime_powers != expected:
        raise ArithmeticError(
            f"unexpected support-one prime powers: {components.active_prime_powers}"
        )
    matrix = (
        components.dominant
        + components.scalar
        + components.prime
        + smooth_kernel_series_matrix(
            1.0, finite_dimension, maximum_smooth_power
        )
    )
    matrix = 0.5 * (matrix + matrix.T)
    if cache is not None:
        cache.parent.mkdir(parents=True, exist_ok=True)
        _atomic_save_matrix(cache, metadata, matrix)
    return matrix


def run_support_one_degreewise_schur_audit(
    source_dimension: int = 58,
    finite_dimension: int = 256,
    quadrature_order: int = 1024,
    maximum_smooth_power: int = 95,
    zero_tolerance: float = 1.0e-12,
    matrix_cache: Path | None = None,
) -> FloatingSupportOneDegreewiseSchur:
    """Apply the exact degreewise denominators to a floating finite source."""

    if zero_tolerance < 0:
        raise ValueError("zero_tolerance must be nonnegative")
    matrix = _load_or_build_matrix(
        matrix_cache,
        finite_dimension,
        quadrature_order,
        maximum_smooth_power,
    )
    denominators_exact = support_one_degreewise_denominator_lowers(
        finite_dimension, source_dimension
    )
    denominators = np.array([float(value) for value in denominators_exact])
    cross = matrix[:source_dimension, source_dimension:]
    schur = matrix[:source_dimension, :source_dimension] - (
        cross / denominators
    ) @ cross.T
    schur = 0.5 * (schur + schur.T)

    results = []
    for parity in (0, 1):
        indices = np.arange(parity, source_dimension, 2)
        eigenvalues = np.linalg.eigvalsh(schur[np.ix_(indices, indices)])
        results.append(
            FloatingDegreewiseSchurParity(
                parity=parity,
                dimension=len(indices),
                negative_count=int(np.count_nonzero(eigenvalues < -zero_tolerance)),
                positive_count=int(np.count_nonzero(eigenvalues > zero_tolerance)),
                unresolved_count=int(
                    np.count_nonzero(np.abs(eigenvalues) <= zero_tolerance)
                ),
                least_eigenvalues=tuple(float(value) for value in eigenvalues[:5]),
            )
        )
    return FloatingSupportOneDegreewiseSchur(
        source_dimension=source_dimension,
        finite_dimension=finite_dimension,
        quadrature_order=quadrature_order,
        maximum_smooth_power=maximum_smooth_power,
        denominator_lower_minimum=float(denominators_exact[0]),
        denominator_lower_maximum=float(denominators_exact[-1]),
        smooth_remainder=math.nextafter(
            smooth_kernel_series_remainder_bound(1.0, maximum_smooth_power),
            math.inf,
        ),
        even=results[0],
        odd=results[1],
    )


def run_support_one_absolute_tail_budget(
    first_degree: int = 256,
    jet_count: int = 1,
    partitions: int = 128,
    maximum_smooth_power: int = 95,
) -> FloatingSupportOneAbsoluteTail:
    """Audit a triangle-inequality bound for the cross tail above a cutoff."""

    if first_degree <= 58:
        raise ValueError("first_degree must exceed the 58-mode source")
    if jet_count < 1:
        raise ValueError("jet_count must be positive")
    if partitions < 1:
        raise ValueError("partitions must be positive")
    active_prime_powers = (2, 3, 4, 5, 7)
    denominator = float(
        support_one_degreewise_denominator_lowers(first_degree + 1)[-1]
    )
    results = []
    for parity in (0, 1):
        low_degrees = np.arange(parity, 58, 2)
        endpoint = active_prime_jet_tail_weighted_norm(
            1.0,
            active_prime_powers,
            low_degrees,
            first_degree,
            jet_count,
            denominator,
        )
        variation = active_prime_remainder_variation_bound(
            1.0,
            active_prime_powers,
            low_degrees,
            jet_count,
            partitions,
        )
        prime_remainder = wang_normalized_tail_bound(
            variation, first_degree, jet_count
        ) / math.sqrt(denominator)
        potential = potential_operator_tail_bound(
            low_degrees, first_degree, 3
        ) / math.sqrt(denominator)
        smooth = smooth_kernel_series_remainder_bound(
            1.0, maximum_smooth_power
        ) / math.sqrt(denominator)
        total = endpoint + prime_remainder + potential + smooth
        results.append(
            FloatingSupportOneAbsoluteTailParity(
                parity=parity,
                endpoint_jet_weighted_norm=endpoint,
                prime_remainder_weighted_norm=prime_remainder,
                potential_weighted_norm=potential,
                smooth_weighted_norm=smooth,
                total_weighted_norm=total,
                correction_norm_upper=total * total,
            )
        )
    return FloatingSupportOneAbsoluteTail(
        first_degree=first_degree,
        jet_count=jet_count,
        partitions=partitions,
        denominator_floor=denominator,
        even=results[0],
        odd=results[1],
    )


def _atomic_write_json(path: Path, payload: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dimension", type=int, default=58)
    parser.add_argument("--finite-dimension", type=int, default=256)
    parser.add_argument("--quadrature-order", type=int, default=1024)
    parser.add_argument("--maximum-smooth-power", type=int, default=95)
    parser.add_argument("--zero-tolerance", type=float, default=1.0e-12)
    parser.add_argument("--matrix-cache", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--absolute-tail-only", action="store_true")
    parser.add_argument("--tail-first-degree", type=int, default=256)
    parser.add_argument("--jet-count", type=int, default=1)
    parser.add_argument("--partitions", type=int, default=128)
    args = parser.parse_args()
    if args.absolute_tail_only:
        result = run_support_one_absolute_tail_budget(
            first_degree=args.tail_first_degree,
            jet_count=args.jet_count,
            partitions=args.partitions,
            maximum_smooth_power=args.maximum_smooth_power,
        )
    else:
        result = run_support_one_degreewise_schur_audit(
            source_dimension=args.source_dimension,
            finite_dimension=args.finite_dimension,
            quadrature_order=args.quadrature_order,
            maximum_smooth_power=args.maximum_smooth_power,
            zero_tolerance=args.zero_tolerance,
            matrix_cache=args.matrix_cache,
        )
    payload = asdict(result)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_json(args.output, payload)
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
