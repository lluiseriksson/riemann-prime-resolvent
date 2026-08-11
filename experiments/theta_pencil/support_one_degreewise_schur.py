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
from numpy.polynomial.legendre import leggauss
from scipy.special import digamma

from experiments.theta_pencil.legendre_feshbach import (
    normalized_legendre_values,
)
from experiments.theta_pencil.legendre_log_matrix import dominant_operator_matrix
from experiments.theta_pencil.legendre_jump_tail import (
    potential_operator_tail_bound,
    wang_normalized_tail_bound,
)
from experiments.theta_pencil.prime_jet_tail import (
    prime_jet_cross_matrix_for_prime,
    active_prime_jet_tail_weighted_norm,
    active_prime_remainder_variation_bound,
)
from experiments.theta_pencil.rational_joint_five_seven_certificate import (
    certify_rational_support_one_tail,
)
from experiments.theta_pencil.smooth_legendre_series import (
    absolute_power_matrix,
    smooth_kernel_series_matrix,
    smooth_kernel_series_remainder_bound,
    smooth_remainder_series_coefficients,
)
from experiments.theta_pencil.semilocal_weil_matrix import EULER_GAMMA
from experiments.theta_pencil.screw_weil_operator import von_mangoldt


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
class FloatingSupportOneFiniteSchur:
    source_dimension: int
    finite_dimension: int
    quadrature_order: int
    maximum_smooth_power: int
    tail_least_eigenvalue: float
    even: FloatingDegreewiseSchurParity
    odd: FloatingDegreewiseSchurParity
    context: str = (
        "floating finite Schur audit with the full high-high block; the "
        "infinite cross tail, smooth remainder and interval enclosures are omitted"
    )


@dataclass(frozen=True)
class FloatingSupportOneResidualSchurParity:
    parity: int
    trial_rank: int
    residual_norm: float
    next_solution_singular_value: float
    negative_count: int
    positive_count: int
    unresolved_count: int
    least_eigenvalues: tuple[float, ...]


@dataclass(frozen=True)
class FloatingSupportOneResidualSchur:
    source_dimension: int
    finite_dimension: int
    trial_rank: int
    complement_floor: float
    even: FloatingSupportOneResidualSchurParity
    odd: FloatingSupportOneResidualSchurParity
    context: str = (
        "floating trial-inverse design audit; the residual Schur inequality "
        "is exact, but all reported matrix data still require Arb enclosures"
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


@dataclass(frozen=True)
class FloatingSupportOneEndpointJetBandParity:
    parity: int
    block_dimension: int
    gram_rank: int
    rank_bound: int
    signed_gram_norm: float
    separate_prime_gram_norm: float
    signed_to_separate_ratio: float


@dataclass(frozen=True)
class FloatingSupportOneEndpointJetBand:
    first_degree: int
    last_degree: int
    jet_count: int
    even: FloatingSupportOneEndpointJetBandParity
    odd: FloatingSupportOneEndpointJetBandParity
    context: str = (
        "floating finite endpoint-jet band; rank <= jet_count is algebraic, "
        "but the reported norms and numerical ranks are design diagnostics"
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


def _atomic_save_blocks(
    path: Path, metadata: dict, source: np.ndarray, cross: np.ndarray
) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as stream:
        np.savez(
            stream,
            metadata=np.array(json.dumps(metadata, sort_keys=True)),
            source=np.asarray(source, dtype=np.float64),
            cross=np.asarray(cross, dtype=np.float64),
        )
    os.replace(temporary, path)


def _atomic_save_high(path: Path, metadata: dict, high: np.ndarray) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as stream:
        np.savez(
            stream,
            metadata=np.array(json.dumps(metadata, sort_keys=True)),
            high=np.asarray(high, dtype=np.float64),
        )
    os.replace(temporary, path)


def _build_rectangular_support_one_blocks(
    source_dimension: int,
    finite_dimension: int,
    quadrature_order: int,
    maximum_smooth_power: int,
    component_cache_dir: Path | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Build only the source and cross blocks needed by the Schur majorant."""

    if not 0 < source_dimension < finite_dimension:
        raise ValueError("require 0 < source_dimension < finite_dimension")
    if quadrature_order < finite_dimension:
        raise ValueError("quadrature_order must be at least finite_dimension")
    source, cross = _load_or_build_rectangular_component(
        "base",
        component_cache_dir,
        source_dimension,
        finite_dimension,
        quadrature_order,
        maximum_smooth_power,
    )
    for prime_power in (2, 3, 4, 5, 7):
        prime_source, prime_cross = _load_or_build_rectangular_component(
            str(prime_power),
            component_cache_dir,
            source_dimension,
            finite_dimension,
            quadrature_order,
            maximum_smooth_power,
        )
        source += prime_source
        cross += prime_cross
    return 0.5 * (source + source.T), cross


def _build_rectangular_component(
    label: str,
    source_dimension: int,
    finite_dimension: int,
    quadrature_order: int,
    maximum_smooth_power: int,
) -> tuple[np.ndarray, np.ndarray]:
    if label == "base":
        dominant = dominant_operator_matrix(finite_dimension)
        # A |x-y|^p kernel changes Legendre degree by at most p+1.  Hence the
        # truncated smooth series has no cross entry beyond
        # source_dimension + maximum_smooth_power.  Building only that exact
        # band avoids an unused finite_dimension-square calculation.
        smooth_dimension = min(
            finite_dimension, source_dimension + maximum_smooth_power + 1
        )
        smooth = smooth_kernel_series_matrix(
            1.0, smooth_dimension, maximum_smooth_power
        )
        scalar = -math.log(2.0 * math.pi) - EULER_GAMMA
        source = dominant[:source_dimension, :source_dimension].copy()
        source += smooth[:source_dimension, :source_dimension]
        source += scalar * np.eye(source_dimension)
        cross = dominant[:source_dimension, source_dimension:].copy()
        smooth_cross_end = smooth_dimension - source_dimension
        cross[:, :smooth_cross_end] += smooth[
            :source_dimension, source_dimension:smooth_dimension
        ]
        return 0.5 * (source + source.T), cross

    prime_power = int(label)
    if prime_power not in (2, 3, 4, 5, 7):
        raise ValueError("the support-one component must be base, 2, 3, 4, 5 or 7")
    mangoldt = von_mangoldt(prime_power)
    shift = math.log(prime_power)
    if mangoldt == 0.0 or not 0.0 < shift < 2.0:
        raise ArithmeticError("the requested prime-power component is inactive")
    nodes, weights = leggauss(quadrature_order)
    right = 1.0 - shift
    x = (right + 1.0) * nodes / 2.0 + (right - 1.0) / 2.0
    scaled_weights = weights * (right + 1.0) / 2.0
    at_x = normalized_legendre_values(x, finite_dimension)
    at_shift = normalized_legendre_values(x + shift, finite_dimension)
    coefficient = -mangoldt / math.sqrt(prime_power)
    low_x = at_x[:source_dimension]
    low_shift = at_shift[:source_dimension]
    source = coefficient * (
        (low_shift * scaled_weights) @ low_x.T
        + (low_x * scaled_weights) @ low_shift.T
    )
    high_x = at_x[source_dimension:]
    high_shift = at_shift[source_dimension:]
    cross = coefficient * (
        (low_shift * scaled_weights) @ high_x.T
        + (low_x * scaled_weights) @ high_shift.T
    )
    return 0.5 * (source + source.T), cross


def _load_or_build_rectangular_component(
    label: str,
    cache_dir: Path | None,
    source_dimension: int,
    finite_dimension: int,
    quadrature_order: int,
    maximum_smooth_power: int,
) -> tuple[np.ndarray, np.ndarray]:
    metadata = {
        "format": 1,
        "architecture": "support-one-degreewise-rectangular-component",
        "component": label,
        "source_dimension": source_dimension,
        "finite_dimension": finite_dimension,
        "quadrature_order": quadrature_order,
        "maximum_smooth_power": maximum_smooth_power,
    }
    path = None if cache_dir is None else cache_dir / f"component-{label}.npz"
    if path is not None and path.exists():
        with np.load(path, allow_pickle=False) as payload:
            observed = json.loads(str(payload["metadata"].item()))
            if observed != metadata:
                raise ValueError(f"the cached {label} component metadata do not match")
            source = np.array(payload["source"], dtype=float)
            cross = np.array(payload["cross"], dtype=float)
        if source.shape != (source_dimension, source_dimension):
            raise ValueError(f"the cached {label} source has the wrong shape")
        if cross.shape != (source_dimension, finite_dimension - source_dimension):
            raise ValueError(f"the cached {label} cross has the wrong shape")
        return source, cross

    source, cross = _build_rectangular_component(
        label,
        source_dimension,
        finite_dimension,
        quadrature_order,
        maximum_smooth_power,
    )
    if path is not None:
        cache_dir.mkdir(parents=True, exist_ok=True)
        _atomic_save_blocks(path, metadata, source, cross)
    return source, cross


def _build_high_component(
    label: str,
    source_dimension: int,
    finite_dimension: int,
    quadrature_order: int,
    maximum_smooth_power: int,
) -> np.ndarray:
    high_dimension = finite_dimension - source_dimension
    if label == "base":
        dominant = dominant_operator_matrix(finite_dimension)
        high = dominant[source_dimension:, source_dimension:].copy()
        high += (-math.log(2.0 * math.pi) - EULER_GAMMA) * np.eye(
            high_dimension
        )
        return 0.5 * (high + high.T)

    if label.startswith("smooth-"):
        bounds = label.removeprefix("smooth-").split("-")
        if len(bounds) != 2:
            raise ValueError("invalid smooth high-component label")
        first_power, last_power = (int(value) for value in bounds)
        if not 0 <= first_power <= last_power:
            raise ValueError("invalid smooth power range")
        coefficients = smooth_remainder_series_coefficients(
            maximum_smooth_power
        )
        high = np.zeros((high_dimension, high_dimension))
        for power in range(first_power, min(last_power, maximum_smooth_power) + 1):
            matrix = absolute_power_matrix(power, finite_dimension)
            high += -float(coefficients[power]) * matrix[
                source_dimension:, source_dimension:
            ]
        return 0.5 * (high + high.T)

    prime_power = int(label)
    if prime_power not in (2, 3, 4, 5, 7):
        raise ValueError("the support-one component must be base, 2, 3, 4, 5 or 7")
    mangoldt = von_mangoldt(prime_power)
    shift = math.log(prime_power)
    nodes, weights = leggauss(quadrature_order)
    right = 1.0 - shift
    x = (right + 1.0) * nodes / 2.0 + (right - 1.0) / 2.0
    scaled_weights = weights * (right + 1.0) / 2.0
    high_x = normalized_legendre_values(x, finite_dimension)[source_dimension:]
    high_shift = normalized_legendre_values(
        x + shift, finite_dimension
    )[source_dimension:]
    coefficient = -mangoldt / math.sqrt(prime_power)
    high = coefficient * (
        (high_shift * scaled_weights) @ high_x.T
        + (high_x * scaled_weights) @ high_shift.T
    )
    return 0.5 * (high + high.T)


def _smooth_high_component_labels(
    maximum_smooth_power: int, chunk_size: int = 16
) -> tuple[str, ...]:
    if maximum_smooth_power < 0 or chunk_size < 1:
        raise ValueError("invalid smooth high-component partition")
    return tuple(
        f"smooth-{start}-{min(start + chunk_size - 1, maximum_smooth_power)}"
        for start in range(0, maximum_smooth_power + 1, chunk_size)
    )


def _load_or_build_high_component(
    label: str,
    cache_dir: Path | None,
    source_dimension: int,
    finite_dimension: int,
    quadrature_order: int,
    maximum_smooth_power: int,
) -> np.ndarray:
    metadata = {
        "format": 1,
        "architecture": "support-one-finite-schur-high-component",
        "component": label,
        "source_dimension": source_dimension,
        "finite_dimension": finite_dimension,
        "quadrature_order": quadrature_order,
        "maximum_smooth_power": maximum_smooth_power,
    }
    path = None if cache_dir is None else cache_dir / f"high-component-{label}.npz"
    if path is not None and path.exists():
        with np.load(path, allow_pickle=False) as payload:
            observed = json.loads(str(payload["metadata"].item()))
            if observed != metadata:
                raise ValueError(f"the cached high {label} metadata do not match")
            high = np.array(payload["high"], dtype=float)
        expected = finite_dimension - source_dimension
        if high.shape != (expected, expected):
            raise ValueError(f"the cached high {label} block has the wrong shape")
        return high
    high = _build_high_component(
        label,
        source_dimension,
        finite_dimension,
        quadrature_order,
        maximum_smooth_power,
    )
    if path is not None:
        cache_dir.mkdir(parents=True, exist_ok=True)
        _atomic_save_high(path, metadata, high)
    return high


def _load_or_build_blocks(
    cache: Path | None,
    component_cache_dir: Path | None,
    source_dimension: int,
    finite_dimension: int,
    quadrature_order: int,
    maximum_smooth_power: int,
) -> tuple[np.ndarray, np.ndarray]:
    metadata = {
        "format": 2,
        "architecture": "support-one-degreewise-schur-rectangular",
        "source_dimension": source_dimension,
        "finite_dimension": finite_dimension,
        "quadrature_order": quadrature_order,
        "maximum_smooth_power": maximum_smooth_power,
    }
    if cache is not None and cache.exists():
        with np.load(cache, allow_pickle=False) as payload:
            observed = json.loads(str(payload["metadata"].item()))
            if observed != metadata:
                raise ValueError("the degreewise Schur cache metadata do not match")
            source = np.array(payload["source"], dtype=float)
            cross = np.array(payload["cross"], dtype=float)
        if source.shape != (source_dimension, source_dimension):
            raise ValueError("the cached source block has the wrong shape")
        if cross.shape != (source_dimension, finite_dimension - source_dimension):
            raise ValueError("the cached cross block has the wrong shape")
        return source, cross

    source, cross = _build_rectangular_support_one_blocks(
        source_dimension,
        finite_dimension,
        quadrature_order,
        maximum_smooth_power,
        component_cache_dir,
    )
    if cache is not None:
        cache.parent.mkdir(parents=True, exist_ok=True)
        _atomic_save_blocks(cache, metadata, source, cross)
    return source, cross


def run_support_one_degreewise_schur_audit(
    source_dimension: int = 58,
    finite_dimension: int = 256,
    quadrature_order: int = 1024,
    maximum_smooth_power: int = 95,
    zero_tolerance: float = 1.0e-12,
    matrix_cache: Path | None = None,
    component_cache_dir: Path | None = None,
) -> FloatingSupportOneDegreewiseSchur:
    """Apply the exact degreewise denominators to a floating finite source."""

    if zero_tolerance < 0:
        raise ValueError("zero_tolerance must be nonnegative")
    source, cross = _load_or_build_blocks(
        matrix_cache,
        component_cache_dir,
        source_dimension,
        finite_dimension,
        quadrature_order,
        maximum_smooth_power,
    )
    denominators_exact = support_one_degreewise_denominator_lowers(
        finite_dimension, source_dimension
    )
    denominators = np.array([float(value) for value in denominators_exact])
    schur = source - (cross / denominators) @ cross.T
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


def run_support_one_finite_schur_audit(
    source_dimension: int = 58,
    finite_dimension: int = 256,
    quadrature_order: int = 1024,
    maximum_smooth_power: int = 95,
    zero_tolerance: float = 1.0e-12,
    matrix_cache: Path | None = None,
    component_cache_dir: Path | None = None,
) -> FloatingSupportOneFiniteSchur:
    """Keep the full finite high block instead of its diagonal minorant."""

    source, cross = _load_or_build_blocks(
        matrix_cache,
        component_cache_dir,
        source_dimension,
        finite_dimension,
        quadrature_order,
        maximum_smooth_power,
    )
    high = sum(
        (
            _load_or_build_high_component(
                label,
                component_cache_dir,
                source_dimension,
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
        np.zeros((finite_dimension - source_dimension,) * 2),
    )
    tail_least = float(np.linalg.eigvalsh(high)[0])
    if tail_least <= 0:
        raise ArithmeticError("the finite high block is not positive definite")
    schur = source - np.linalg.solve(high, cross.T).T @ cross.T
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
    return FloatingSupportOneFiniteSchur(
        source_dimension=source_dimension,
        finite_dimension=finite_dimension,
        quadrature_order=quadrature_order,
        maximum_smooth_power=maximum_smooth_power,
        tail_least_eigenvalue=tail_least,
        even=results[0],
        odd=results[1],
    )


def schur_residual_lower_matrix(
    source: np.ndarray,
    cross: np.ndarray,
    high: np.ndarray,
    trial_inverse_cross: np.ndarray,
    complement_floor: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the residual lower Schur matrix and residual map.

    If ``high >= complement_floor * I`` and ``R = cross.T - high @ Y``, then

    ``source - cross @ high^-1 @ cross.T`` is bounded below by
    ``source - cross@Y - Y.T@cross.T + Y.T@high@Y - R.T@R/floor``.
    """

    source = np.asarray(source, dtype=float)
    cross = np.asarray(cross, dtype=float)
    high = np.asarray(high, dtype=float)
    trial = np.asarray(trial_inverse_cross, dtype=float)
    if complement_floor <= 0:
        raise ValueError("complement_floor must be positive")
    if source.ndim != 2 or source.shape[0] != source.shape[1]:
        raise ValueError("source must be square")
    if high.ndim != 2 or high.shape[0] != high.shape[1]:
        raise ValueError("high must be square")
    if cross.shape != (source.shape[0], high.shape[0]):
        raise ValueError("cross has the wrong shape")
    if trial.shape != (high.shape[0], source.shape[0]):
        raise ValueError("trial inverse cross has the wrong shape")
    residual = cross.T - high @ trial
    lower = (
        source
        - cross @ trial
        - trial.T @ cross.T
        + trial.T @ high @ trial
        - residual.T @ residual / complement_floor
    )
    return 0.5 * (lower + lower.T), residual


def run_support_one_residual_schur_audit(
    trial_rank: int = 20,
    source_dimension: int = 58,
    finite_dimension: int = 256,
    quadrature_order: int = 1024,
    maximum_smooth_power: int = 95,
    zero_tolerance: float = 1.0e-12,
    matrix_cache: Path | None = None,
    component_cache_dir: Path | None = None,
) -> FloatingSupportOneResidualSchur:
    """Size a low-rank trial inverse for a future Arb residual proof."""

    source, cross = _load_or_build_blocks(
        matrix_cache,
        component_cache_dir,
        source_dimension,
        finite_dimension,
        quadrature_order,
        maximum_smooth_power,
    )
    high = sum(
        (
            _load_or_build_high_component(
                label,
                component_cache_dir,
                source_dimension,
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
        np.zeros((finite_dimension - source_dimension,) * 2),
    )
    complement_floor = float(
        certify_rational_support_one_tail().complement_margin
    )
    results = []
    for parity in (0, 1):
        low_indices = np.arange(parity, source_dimension, 2)
        high_indices = np.arange(
            parity, finite_dimension - source_dimension, 2
        )
        parity_source = source[np.ix_(low_indices, low_indices)]
        parity_cross = cross[np.ix_(low_indices, high_indices)]
        parity_high = high[np.ix_(high_indices, high_indices)]
        exact_trial = np.linalg.solve(parity_high, parity_cross.T)
        left, singular_values, right = np.linalg.svd(
            exact_trial, full_matrices=False
        )
        if not 1 <= trial_rank <= len(singular_values):
            raise ValueError("trial_rank must fit each parity source block")
        trial = (
            left[:, :trial_rank] * singular_values[:trial_rank]
        ) @ right[:trial_rank]
        lower, residual = schur_residual_lower_matrix(
            parity_source,
            parity_cross,
            parity_high,
            trial,
            complement_floor,
        )
        eigenvalues = np.linalg.eigvalsh(lower)
        next_singular = (
            float(singular_values[trial_rank])
            if trial_rank < len(singular_values)
            else 0.0
        )
        results.append(
            FloatingSupportOneResidualSchurParity(
                parity=parity,
                trial_rank=trial_rank,
                residual_norm=float(np.linalg.svd(residual, compute_uv=False)[0]),
                next_solution_singular_value=next_singular,
                negative_count=int(np.count_nonzero(eigenvalues < -zero_tolerance)),
                positive_count=int(np.count_nonzero(eigenvalues > zero_tolerance)),
                unresolved_count=int(
                    np.count_nonzero(np.abs(eigenvalues) <= zero_tolerance)
                ),
                least_eigenvalues=tuple(float(value) for value in eigenvalues[:5]),
            )
        )
    return FloatingSupportOneResidualSchur(
        source_dimension=source_dimension,
        finite_dimension=finite_dimension,
        trial_rank=trial_rank,
        complement_floor=complement_floor,
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


def run_support_one_endpoint_jet_band_audit(
    first_degree: int = 256,
    last_degree: int = 4096,
    jet_count: int = 1,
) -> FloatingSupportOneEndpointJetBand:
    """Keep the signed finite-rank jet Gram over one degree band.

    For each parity the combined-prime cross matrix factors as ``E_J P_J``,
    where ``E_J`` has one column per endpoint jet.  Hence its weighted Gram
    has rank at most ``J`` independently of the number of prime powers.
    """

    if first_degree <= 58 or last_degree <= first_degree:
        raise ValueError("the degree band must start above 58 and be nonempty")
    if jet_count < 1:
        raise ValueError("jet_count must be positive")
    active_prime_powers = (2, 3, 4, 5, 7)
    beta = float(support_one_bounded_part_lower())
    results = []
    for parity in (0, 1):
        low_degrees = np.arange(parity, 58, 2)
        high_degrees = np.arange(
            first_degree + ((first_degree - parity) % 2), last_degree, 2
        )
        denominators = (
            digamma(high_degrees + 1.0) + EULER_GAMMA + beta
        )
        pieces = [
            prime_jet_cross_matrix_for_prime(
                1.0,
                prime_power,
                low_degrees,
                high_degrees,
                jet_count,
            )
            for prime_power in active_prime_powers
        ]
        combined = sum(pieces, np.zeros_like(pieces[0]))
        signed_gram = (combined / denominators) @ combined.T
        separate_gram = sum(
            ((piece / denominators) @ piece.T for piece in pieces),
            np.zeros((len(low_degrees), len(low_degrees))),
        )
        signed_norm = float(np.linalg.eigvalsh(signed_gram)[-1])
        separate_norm = float(np.linalg.eigvalsh(separate_gram)[-1])
        results.append(
            FloatingSupportOneEndpointJetBandParity(
                parity=parity,
                block_dimension=len(low_degrees),
                gram_rank=int(np.linalg.matrix_rank(signed_gram, tol=1.0e-10)),
                rank_bound=min(jet_count, len(low_degrees)),
                signed_gram_norm=signed_norm,
                separate_prime_gram_norm=separate_norm,
                signed_to_separate_ratio=signed_norm / separate_norm,
            )
        )
    return FloatingSupportOneEndpointJetBand(
        first_degree=first_degree,
        last_degree=last_degree,
        jet_count=jet_count,
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
    parser.add_argument("--component-cache-dir", type=Path)
    parser.add_argument(
        "--build-component-only", choices=("base", "2", "3", "4", "5", "7")
    )
    parser.add_argument(
        "--build-high-component-only",
        choices=(
            "base",
            "2",
            "3",
            "4",
            "5",
            "7",
            "smooth-0-15",
            "smooth-16-31",
            "smooth-32-47",
            "smooth-48-63",
            "smooth-64-79",
            "smooth-80-95",
        ),
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--absolute-tail-only", action="store_true")
    parser.add_argument("--endpoint-jet-band-only", action="store_true")
    parser.add_argument("--finite-schur", action="store_true")
    parser.add_argument("--residual-schur-rank", type=int)
    parser.add_argument("--tail-first-degree", type=int, default=256)
    parser.add_argument("--tail-last-degree", type=int, default=4096)
    parser.add_argument("--jet-count", type=int, default=1)
    parser.add_argument("--partitions", type=int, default=128)
    args = parser.parse_args()
    if args.build_component_only is not None:
        if args.component_cache_dir is None:
            raise ValueError("--build-component-only requires --component-cache-dir")
        source, cross = _load_or_build_rectangular_component(
            args.build_component_only,
            args.component_cache_dir,
            args.source_dimension,
            args.finite_dimension,
            args.quadrature_order,
            args.maximum_smooth_power,
        )
        print(
            json.dumps(
                {
                    "component": args.build_component_only,
                    "source_shape": source.shape,
                    "cross_shape": cross.shape,
                    "source_frobenius": float(np.linalg.norm(source)),
                    "cross_frobenius": float(np.linalg.norm(cross)),
                },
                indent=2,
                sort_keys=True,
            ),
            flush=True,
        )
        return
    if args.build_high_component_only is not None:
        if args.component_cache_dir is None:
            raise ValueError(
                "--build-high-component-only requires --component-cache-dir"
            )
        high = _load_or_build_high_component(
            args.build_high_component_only,
            args.component_cache_dir,
            args.source_dimension,
            args.finite_dimension,
            args.quadrature_order,
            args.maximum_smooth_power,
        )
        print(
            json.dumps(
                {
                    "component": args.build_high_component_only,
                    "high_shape": high.shape,
                    "high_frobenius": float(np.linalg.norm(high)),
                },
                indent=2,
                sort_keys=True,
            ),
            flush=True,
        )
        return
    if sum(
        (
            args.absolute_tail_only,
            args.endpoint_jet_band_only,
            args.finite_schur,
            args.residual_schur_rank is not None,
        )
    ) > 1:
        raise ValueError("select at most one specialized audit")
    if args.absolute_tail_only:
        result = run_support_one_absolute_tail_budget(
            first_degree=args.tail_first_degree,
            jet_count=args.jet_count,
            partitions=args.partitions,
            maximum_smooth_power=args.maximum_smooth_power,
        )
    elif args.endpoint_jet_band_only:
        result = run_support_one_endpoint_jet_band_audit(
            first_degree=args.tail_first_degree,
            last_degree=args.tail_last_degree,
            jet_count=args.jet_count,
        )
    elif args.finite_schur:
        result = run_support_one_finite_schur_audit(
            source_dimension=args.source_dimension,
            finite_dimension=args.finite_dimension,
            quadrature_order=args.quadrature_order,
            maximum_smooth_power=args.maximum_smooth_power,
            zero_tolerance=args.zero_tolerance,
            matrix_cache=args.matrix_cache,
            component_cache_dir=args.component_cache_dir,
        )
    elif args.residual_schur_rank is not None:
        result = run_support_one_residual_schur_audit(
            trial_rank=args.residual_schur_rank,
            source_dimension=args.source_dimension,
            finite_dimension=args.finite_dimension,
            quadrature_order=args.quadrature_order,
            maximum_smooth_power=args.maximum_smooth_power,
            zero_tolerance=args.zero_tolerance,
            matrix_cache=args.matrix_cache,
            component_cache_dir=args.component_cache_dir,
        )
    else:
        result = run_support_one_degreewise_schur_audit(
            source_dimension=args.source_dimension,
            finite_dimension=args.finite_dimension,
            quadrature_order=args.quadrature_order,
            maximum_smooth_power=args.maximum_smooth_power,
            zero_tolerance=args.zero_tolerance,
            matrix_cache=args.matrix_cache,
            component_cache_dir=args.component_cache_dir,
        )
    payload = asdict(result)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_json(args.output, payload)
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
