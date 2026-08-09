"""Mode-resolved finite sections of the scaled Weil--Suzuki operator.

The dominant operator is assembled from its closed Legendre matrix.  Only the
bounded scalar, prime-translation, and smooth-kernel terms are quadrature
approximations.  The resulting Feshbach complement is a numerical diagnostic,
not an infinite-dimensional positivity certificate.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np
from numpy.polynomial.legendre import leggauss, legvander
from scipy.linalg import eigh

from experiments.theta_pencil.legendre_log_matrix import dominant_operator_matrix
from experiments.theta_pencil.semilocal_weil_matrix import EULER_GAMMA
from experiments.theta_pencil.screw_weil_operator import von_mangoldt


@dataclass(frozen=True)
class LegendreWeilComponents:
    dominant: np.ndarray
    scalar: np.ndarray
    prime: np.ndarray
    smooth: np.ndarray
    active_prime_powers: tuple[int, ...]

    @property
    def total(self) -> np.ndarray:
        matrix = self.dominant + self.scalar + self.prime + self.smooth
        return 0.5 * (matrix + matrix.T)


@dataclass(frozen=True)
class FeshbachAudit:
    half_width: float
    dimension: int
    low_modes: int
    full_ritz: float
    low_block_ritz: float
    tail_ritz: float
    cross_norm: float
    scalar_schur_bound: float
    exact_finite_schur_ritz: float


def normalized_legendre_values(nodes: np.ndarray, size: int) -> np.ndarray:
    """Rows are normalized Legendre polynomials evaluated at nodes."""
    values = legvander(nodes, size - 1).T
    values *= np.sqrt((2.0 * np.arange(size) + 1.0) / 2.0)[:, None]
    return values


def smooth_remainder_second_array(values: np.ndarray) -> np.ndarray:
    """Stable evaluation of the even extension of Suzuki's r''."""
    t = np.abs(np.asarray(values, dtype=float))
    result = np.empty_like(t)
    small = t < 1.0e-4
    z = t[small]
    result[small] = (
        -7.0 / 4.0
        - z / 48.0
        - 9.0 * z**2 / 32.0
        + 7.0 * z**3 / 11520.0
        - z**4 / 512.0
    )
    z = t[~small]
    result[~small] = (
        -np.exp(z / 2.0)
        - np.exp(-z / 2.0)
        + np.exp(-z / 2.0) / (-np.expm1(-2.0 * z))
        - 1.0 / (2.0 * z)
    )
    return result


def _translation_matrix(shift: float, size: int, quadrature_order: int) -> np.ndarray:
    if not 0.0 < shift < 2.0:
        return np.zeros((size, size), dtype=float)
    nodes, weights = leggauss(quadrature_order)
    left = -1.0
    right = 1.0 - shift
    x = (right - left) * nodes / 2.0 + (right + left) / 2.0
    scaled_weights = weights * (right - left) / 2.0
    at_x = normalized_legendre_values(x, size)
    at_shift = normalized_legendre_values(x + shift, size)
    one_way = (at_shift * scaled_weights) @ at_x.T
    return one_way + one_way.T


def build_legendre_weil_components(
    half_width: float,
    size: int,
    quadrature_order: int | None = None,
) -> LegendreWeilComponents:
    """Build a Legendre finite section of Suzuki equation (405)."""
    if half_width <= 0.0:
        raise ValueError("half_width must be positive")
    if size < 1:
        raise ValueError("size must be positive")
    order = quadrature_order or max(256, 2 * size)
    if order < size:
        raise ValueError("quadrature_order must be at least size")

    identity = np.eye(size)
    dominant = dominant_operator_matrix(size)
    scalar_coefficient = (
        -math.log(half_width) - math.log(2.0 * math.pi) - EULER_GAMMA
    )
    scalar = scalar_coefficient * identity

    prime = np.zeros((size, size), dtype=float)
    active: list[int] = []
    upper = int(math.floor(math.exp(2.0 * half_width) + 1e-13))
    for n in range(2, upper + 1):
        mangoldt = von_mangoldt(n)
        shift = math.log(n) / half_width
        if mangoldt == 0.0 or shift >= 2.0:
            continue
        active.append(n)
        prime -= (mangoldt / math.sqrt(n)) * _translation_matrix(
            shift, size, order
        )

    nodes, weights = leggauss(order)
    basis = normalized_legendre_values(nodes, size)
    differences = half_width * (nodes[:, None] - nodes[None, :])
    weighted_kernel = (
        weights[:, None]
        * smooth_remainder_second_array(differences)
        * weights[None, :]
    )
    smooth = -half_width * (basis @ weighted_kernel @ basis.T)

    return LegendreWeilComponents(
        dominant=dominant,
        scalar=scalar,
        prime=0.5 * (prime + prime.T),
        smooth=0.5 * (smooth + smooth.T),
        active_prime_powers=tuple(active),
    )


def feshbach_audit(
    half_width: float,
    dimension: int,
    low_modes: int,
    quadrature_order: int | None = None,
) -> FeshbachAudit:
    """Compare a scalar tail bound with the exact finite Schur complement."""
    if not 0 < low_modes < dimension:
        raise ValueError("low_modes must lie strictly between zero and dimension")
    components = build_legendre_weil_components(
        half_width, dimension, quadrature_order
    )
    dominant_eigenvalues, transform = eigh(components.dominant)
    matrix = transform.T @ components.total @ transform
    low = matrix[:low_modes, :low_modes]
    cross = matrix[:low_modes, low_modes:]
    tail = matrix[low_modes:, low_modes:]
    low_ritz = float(eigh(low, eigvals_only=True, subset_by_index=[0, 0])[0])
    tail_ritz = float(eigh(tail, eigvals_only=True, subset_by_index=[0, 0])[0])
    cross_norm = float(np.linalg.svd(cross, compute_uv=False)[0])
    schur = low - np.linalg.solve(tail, cross.T).T @ cross.T
    return FeshbachAudit(
        half_width=half_width,
        dimension=dimension,
        low_modes=low_modes,
        full_ritz=float(eigh(matrix, eigvals_only=True, subset_by_index=[0, 0])[0]),
        low_block_ritz=low_ritz,
        tail_ritz=tail_ritz,
        cross_norm=cross_norm,
        scalar_schur_bound=low_ritz - cross_norm**2 / tail_ritz,
        exact_finite_schur_ritz=float(
            eigh(schur, eigvals_only=True, subset_by_index=[0, 0])[0]
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--half-width", type=float, default=0.4)
    parser.add_argument("--dimension", type=int, default=128)
    parser.add_argument("--low-modes", type=int, default=74)
    parser.add_argument("--quadrature", type=int, default=512)
    args = parser.parse_args()
    print(
        feshbach_audit(
            args.half_width, args.dimension, args.low_modes, args.quadrature
        )
    )


if __name__ == "__main__":
    main()

