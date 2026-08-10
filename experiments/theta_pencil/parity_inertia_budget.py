"""Parity-resolved inertia budget for the first prime support window.

This is a floating-point design audit.  Positive margins identify an interval
certificate worth building; they are not themselves rigorous spectral bounds.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, field

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import eigh
from scipy.special import digamma

from experiments.theta_pencil.legendre_feshbach import (
    build_legendre_weil_components,
    normalized_legendre_values,
)
from experiments.theta_pencil.legendre_jump_tail import (
    potential_operator_tail_bound,
    smooth_kernel_variation_bound,
    wang_normalized_tail_bound,
)
from experiments.theta_pencil.legendre_log_matrix import (
    boundary_potential_matrix,
)
from experiments.theta_pencil.prime_jet_tail import (
    active_prime_jet_tail_weighted_norm,
    active_prime_jet_weighted_correction,
    active_prime_remainder_variation_bound,
)
from experiments.theta_pencil.semilocal_weil_matrix import EULER_GAMMA
from experiments.theta_pencil.screw_weil_operator import von_mangoldt
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_matrix,
    smooth_kernel_series_remainder_bound,
)


@dataclass(frozen=True)
class ParityInertiaAudit:
    parity: int
    raw_eigenvalues: np.ndarray
    jet_eigenvalues: np.ndarray
    jet_correction_norm: float
    omitted_weighted_norm: float
    omitted_correction_bound: float
    floating_margin: float
    jet_schur_matrix: np.ndarray = field(repr=False)


def _harmonic_array(degrees: np.ndarray) -> np.ndarray:
    return digamma(degrees + 1.0) + EULER_GAMMA


def run_parity_inertia_audit(
    parity: int,
    half_width: float = 0.4,
    low_dimension: int = 88,
    finite_dimension: int = 4096,
    smooth_dimension: int = 512,
    spectral_floor: float = 0.005,
    jet_count: int = 6,
    jet_end: int = 1_000_000,
    partitions: int = 128,
    active_primes: tuple[int, ...] = (2,),
) -> ParityInertiaAudit:
    if parity not in (0, 1):
        raise ValueError("parity must be zero or one")
    if not 0 < low_dimension < smooth_dimension <= finite_dimension:
        raise ValueError("dimensions must satisfy low < smooth <= finite")

    scalar_coefficient = (
        -math.log(half_width) - math.log(2.0 * math.pi) - EULER_GAMMA
    )
    loss = (
        abs(scalar_coefficient)
        + 2.0
        * math.fsum(
            von_mangoldt(prime) / math.sqrt(prime)
            for prime in active_primes
        )
        + 6.0 * half_width
    )
    low_components = build_legendre_weil_components(
        half_width, low_dimension, max(512, 2 * low_dimension)
    )
    if low_components.active_prime_powers != active_primes:
        raise ValueError(
            "active_primes must equal the prime powers in the support window"
        )
    smooth_series = smooth_kernel_series_matrix(
        half_width, smooth_dimension, maximum_power=23
    )
    low_matrix = (
        low_components.dominant
        + low_components.scalar
        + low_components.prime
        + smooth_series[:low_dimension, :low_dimension]
        - spectral_floor * np.eye(low_dimension)
    )

    quadrature_order = (finite_dimension + low_dimension + 2) // 2 + 2
    nodes, weights = leggauss(quadrature_order)
    cross = boundary_potential_matrix(finite_dimension)[:low_dimension, low_dimension:]
    for prime in active_primes:
        translation = math.log(prime) / half_width
        cut = 1.0 - translation
        x = (cut + 1.0) * nodes / 2.0 + (cut - 1.0) / 2.0
        scaled_weights = weights * (cut + 1.0) / 2.0
        at_x = normalized_legendre_values(x, finite_dimension)
        at_shift = normalized_legendre_values(
            x + translation, finite_dimension
        )
        prime_coefficient = von_mangoldt(prime) / math.sqrt(prime)
        cross -= prime_coefficient * (
            (at_shift[:low_dimension] * scaled_weights)
            @ at_x[low_dimension:].T
            + (at_x[:low_dimension] * scaled_weights)
            @ at_shift[low_dimension:].T
        )

    cross[:, : smooth_dimension - low_dimension] += smooth_series[
        :low_dimension, low_dimension:smooth_dimension
    ]

    high_degrees = np.arange(low_dimension, finite_dimension)
    denominators = _harmonic_array(high_degrees) - loss - spectral_floor
    low_degrees = np.arange(parity, low_dimension, 2)
    high_columns = np.where(high_degrees % 2 == parity)[0]
    selected_cross = cross[np.ix_(low_degrees, high_columns)]
    schur = low_matrix[np.ix_(low_degrees, low_degrees)] - (
        selected_cross / denominators[high_columns]
    ) @ selected_cross.T
    raw_eigenvalues = eigh(schur, eigvals_only=True, subset_by_index=[0, 2])

    jet_correction = active_prime_jet_weighted_correction(
        half_width,
        active_primes,
        low_degrees,
        finite_dimension,
        jet_end,
        jet_count,
        loss,
        spectral_floor,
    )
    with_jets = schur - jet_correction
    jet_eigenvalues = eigh(with_jets, eigvals_only=True, subset_by_index=[0, 2])
    jet_norm = float(eigh(jet_correction, eigvals_only=True)[-1])

    end_denominator = (
        float(digamma(jet_end + 1) + EULER_GAMMA) - loss - spectral_floor
    )
    jet_tail = active_prime_jet_tail_weighted_norm(
        half_width,
        active_primes,
        low_degrees,
        jet_end,
        jet_count,
        end_denominator,
    )
    variation = active_prime_remainder_variation_bound(
        half_width, active_primes, low_degrees, jet_count, partitions
    )
    finite_denominator = float(denominators[0])
    prime_remainder = wang_normalized_tail_bound(
        variation, finite_dimension, jet_count
    ) / math.sqrt(float(_harmonic_array(np.array([finite_dimension]))[0] - loss - spectral_floor))
    potential = potential_operator_tail_bound(
        low_degrees, finite_dimension, 3
    ) / math.sqrt(float(_harmonic_array(np.array([finite_dimension]))[0] - loss - spectral_floor))
    smooth_denominator = math.sqrt(
        float(
            _harmonic_array(np.array([smooth_dimension]))[0]
            - loss
            - spectral_floor
        )
    )
    if low_dimension + 24 < smooth_dimension:
        smooth = smooth_kernel_series_remainder_bound(
            half_width, 23
        ) / smooth_denominator
    else:
        smooth_r4_bound = 1.0 if half_width <= 0.4 else 1.1
        smooth = wang_normalized_tail_bound(
            smooth_kernel_variation_bound(half_width, smooth_r4_bound),
            smooth_dimension,
            1,
        ) / smooth_denominator
    omitted_weighted = jet_tail + prime_remainder + potential + smooth
    omitted_correction = (
        2.0 * math.sqrt(jet_norm) * omitted_weighted + omitted_weighted**2
    )
    target_index = 1 if parity == 0 else 0
    margin = float(jet_eigenvalues[target_index] - omitted_correction)
    return ParityInertiaAudit(
        parity=parity,
        raw_eigenvalues=raw_eigenvalues,
        jet_eigenvalues=jet_eigenvalues,
        jet_correction_norm=jet_norm,
        omitted_weighted_norm=omitted_weighted,
        omitted_correction_bound=omitted_correction,
        floating_margin=margin,
        jet_schur_matrix=with_jets,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partitions", type=int, default=128)
    args = parser.parse_args()
    for parity in (0, 1):
        print(run_parity_inertia_audit(parity, partitions=args.partitions))


if __name__ == "__main__":
    main()
