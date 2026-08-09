"""Parity-resolved inertia budget for the first prime support window.

This is a floating-point design audit.  Positive margins identify an interval
certificate worth building; they are not themselves rigorous spectral bounds.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

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
from experiments.theta_pencil.legendre_tail_bound import bounded_perturbation_norm
from experiments.theta_pencil.prime_jet_tail import (
    piecewise_prime_remainder_variation_bound,
    prime_jet_tail_weighted_norm,
    prime_jet_weighted_correction,
)
from experiments.theta_pencil.semilocal_weil_matrix import EULER_GAMMA


@dataclass(frozen=True)
class ParityInertiaAudit:
    parity: int
    raw_eigenvalues: np.ndarray
    jet_eigenvalues: np.ndarray
    jet_correction_norm: float
    omitted_weighted_norm: float
    omitted_correction_bound: float
    floating_margin: float


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
) -> ParityInertiaAudit:
    if parity not in (0, 1):
        raise ValueError("parity must be zero or one")
    if not 0 < low_dimension < smooth_dimension <= finite_dimension:
        raise ValueError("dimensions must satisfy low < smooth <= finite")

    loss = bounded_perturbation_norm(half_width)
    low_components = build_legendre_weil_components(
        half_width, low_dimension, max(512, 2 * low_dimension)
    )
    low_matrix = low_components.total - spectral_floor * np.eye(low_dimension)

    quadrature_order = (finite_dimension + low_dimension + 2) // 2 + 2
    nodes, weights = leggauss(quadrature_order)
    shift = math.log(2.0) / half_width
    cut = 1.0 - shift
    x = (cut + 1.0) * nodes / 2.0 + (cut - 1.0) / 2.0
    scaled_weights = weights * (cut + 1.0) / 2.0
    at_x = normalized_legendre_values(x, finite_dimension)
    at_shift = normalized_legendre_values(x + shift, finite_dimension)
    prime_coefficient = math.log(2.0) / math.sqrt(2.0)
    cross = boundary_potential_matrix(finite_dimension)[:low_dimension, low_dimension:]
    cross -= prime_coefficient * (
        (at_shift[:low_dimension] * scaled_weights)
        @ at_x[low_dimension:].T
        + (at_x[:low_dimension] * scaled_weights)
        @ at_shift[low_dimension:].T
    )

    smooth_components = build_legendre_weil_components(
        half_width, smooth_dimension, max(512, 2 * smooth_dimension)
    )
    cross[:, : smooth_dimension - low_dimension] += smooth_components.smooth[
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

    jet_correction = prime_jet_weighted_correction(
        half_width,
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
    jet_tail = prime_jet_tail_weighted_norm(
        half_width, low_degrees, jet_end, jet_count, end_denominator
    )
    variation = piecewise_prime_remainder_variation_bound(
        half_width, low_degrees, jet_count, partitions
    )
    finite_denominator = float(denominators[0])
    prime_remainder = wang_normalized_tail_bound(
        variation, finite_dimension, jet_count
    ) / math.sqrt(float(_harmonic_array(np.array([finite_dimension]))[0] - loss - spectral_floor))
    potential = potential_operator_tail_bound(
        low_degrees, finite_dimension, 3
    ) / math.sqrt(float(_harmonic_array(np.array([finite_dimension]))[0] - loss - spectral_floor))
    smooth_variation = smooth_kernel_variation_bound(half_width)
    smooth = wang_normalized_tail_bound(
        smooth_variation, smooth_dimension, 1
    ) / math.sqrt(
        float(_harmonic_array(np.array([smooth_dimension]))[0] - loss - spectral_floor)
    )
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
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partitions", type=int, default=128)
    args = parser.parse_args()
    for parity in (0, 1):
        print(run_parity_inertia_audit(parity, partitions=args.partitions))


if __name__ == "__main__":
    main()

