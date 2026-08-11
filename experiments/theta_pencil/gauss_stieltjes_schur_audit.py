"""Design audit for the support-one Gauss--Stieltjes lower operator.

The output is intentionally descriptive.  Prime translations are evaluated
by polynomial-exact double Gauss quadrature, while the smooth kernel is an
exact-power truncation accompanied by its analytic norm remainder.  An
interval proof must replace the source matrices by Arb enclosures.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np
from numpy.polynomial.legendre import leggauss, legvander

from experiments.theta_pencil.gauss_stieltjes_potential import (
    gauss_stieltjes_lower_matrix,
    harmonic,
)
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_matrix,
    smooth_kernel_series_remainder_bound,
)
from experiments.theta_pencil.support_05_comparison import _smooth_lower_loss


EULER_GAMMA = 0.577215664901532860606512090082402431


@dataclass(frozen=True)
class ParityAudit:
    parity: int
    finite_eigenvalues: tuple[float, ...]
    low_eigenvalues: tuple[float, ...]
    single_floor_schur_eigenvalues: tuple[float, ...]


@dataclass(frozen=True)
class SupportOneAudit:
    dimension: int
    low_dimension: int
    quadrature_order: int
    stieltjes_order: int
    chebyshev_order: int
    smooth_order: int
    chebyshev_error: float
    smooth_remainder_bound: float
    complement_floor: float
    active_prime_powers: tuple[int, ...]
    even: ParityAudit
    odd: ParityAudit


def _von_mangoldt(value: int) -> float:
    if value < 2:
        return 0.0
    for prime in range(2, value + 1):
        if any(prime % divisor == 0 for divisor in range(2, math.isqrt(prime) + 1)):
            continue
        power = prime
        while power < value:
            power *= prime
        if power == value:
            return math.log(prime)
    return 0.0


def prime_translation_floor(half_width: float = 1.0) -> float:
    """Sum of the exact path-graph lower losses for active prime powers."""

    upper = int(math.floor(math.exp(2.0 * half_width) + 1e-13))
    result = 0.0
    for prime_power in range(2, upper + 1):
        coefficient = _von_mangoldt(prime_power)
        if coefficient == 0.0 or math.log(prime_power) >= 2.0 * half_width:
            continue
        chain = math.ceil(2.0 * half_width / math.log(prime_power))
        result += (
            2.0
            * coefficient
            / math.sqrt(prime_power)
            * math.cos(math.pi / (chain + 1))
        )
    return result


def support_one_complement_floor(
    tail_start: int = 256, smooth_order: int = 95
) -> float:
    """Degree-tail lower bound from A2, smooth loss, and path spectra."""

    scalar = -math.log(2.0 * math.pi) - EULER_GAMMA
    return (
        harmonic(tail_start)
        + scalar
        - _smooth_lower_loss(1.0, smooth_order)
        - prime_translation_floor(1.0)
    )


def _normalized_legendre_values(nodes: np.ndarray, size: int) -> np.ndarray:
    values = legvander(nodes, size - 1).T
    values *= np.sqrt((2.0 * np.arange(size) + 1.0) / 2.0)[:, None]
    return values


def _translation_matrix(shift: float, size: int, order: int) -> np.ndarray:
    if not 0.0 < shift < 2.0:
        return np.zeros((size, size), dtype=float)
    nodes, weights = leggauss(order)
    right = 1.0 - shift
    points = (right + 1.0) * nodes / 2.0 + (right - 1.0) / 2.0
    weights = weights * (right + 1.0) / 2.0
    source = _normalized_legendre_values(points, size)
    target = _normalized_legendre_values(points + shift, size)
    one_way = (target * weights) @ source.T
    return one_way + one_way.T


def build_support_one_lower_matrix(
    dimension: int = 128,
    stieltjes_order: int = 12,
    chebyshev_order: int = 384,
    smooth_order: int = 95,
    quadrature_order: int | None = None,
) -> tuple[np.ndarray, float, tuple[int, ...]]:
    """Build the double-precision finite source for ``L_{m,J}`` at a=1."""

    if dimension < 2:
        raise ValueError("dimension must be at least two")
    order = quadrature_order or max(192, dimension + 32)
    potential, metadata = gauss_stieltjes_lower_matrix(
        dimension, stieltjes_order, chebyshev_order
    )
    matrix = np.diag([harmonic(index) for index in range(dimension)])
    matrix += potential
    matrix += (-math.log(2.0 * math.pi) - EULER_GAMMA) * np.eye(dimension)

    active = []
    for prime_power in range(2, 8):
        coefficient = _von_mangoldt(prime_power)
        if coefficient == 0.0:
            continue
        active.append(prime_power)
        matrix -= coefficient / math.sqrt(prime_power) * _translation_matrix(
            math.log(prime_power), dimension, order
        )
    matrix += smooth_kernel_series_matrix(1.0, dimension, smooth_order)
    return 0.5 * (matrix + matrix.T), metadata.uniform_error, tuple(active)


def run_support_one_audit(
    dimension: int = 128,
    low_dimension: int = 16,
    stieltjes_order: int = 12,
    chebyshev_order: int = 384,
    smooth_order: int = 95,
    complement_floor: float | None = None,
) -> SupportOneAudit:
    if not 1 < low_dimension < dimension:
        raise ValueError("low dimension must lie strictly inside the section")
    matrix, chebyshev_error, active = build_support_one_lower_matrix(
        dimension,
        stieltjes_order,
        chebyshev_order,
        smooth_order,
    )
    floor = (
        support_one_complement_floor(256, smooth_order)
        if complement_floor is None
        else complement_floor
    )
    if floor <= 0.0:
        raise ValueError("the registered common complement floor must be positive")
    audits = []
    for parity in (0, 1):
        indices = np.arange(parity, dimension, 2)
        low = indices[indices < low_dimension]
        high = indices[indices >= low_dimension]
        finite = matrix[np.ix_(indices, indices)]
        source = matrix[np.ix_(low, low)]
        cross = matrix[np.ix_(low, high)]
        schur = source - cross @ cross.T / floor
        audits.append(
            ParityAudit(
                parity=parity,
                finite_eigenvalues=tuple(
                    float(value) for value in np.linalg.eigvalsh(finite)[:6]
                ),
                low_eigenvalues=tuple(
                    float(value) for value in np.linalg.eigvalsh(source)[:6]
                ),
                single_floor_schur_eigenvalues=tuple(
                    float(value) for value in np.linalg.eigvalsh(schur)[:6]
                ),
            )
        )
    return SupportOneAudit(
        dimension=dimension,
        low_dimension=low_dimension,
        quadrature_order=max(192, dimension + 32),
        stieltjes_order=stieltjes_order,
        chebyshev_order=chebyshev_order,
        smooth_order=smooth_order,
        chebyshev_error=chebyshev_error,
        smooth_remainder_bound=smooth_kernel_series_remainder_bound(
            1.0, smooth_order
        ),
        complement_floor=floor,
        active_prime_powers=active,
        even=audits[0],
        odd=audits[1],
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, default=128)
    parser.add_argument("--low-dimension", type=int, default=16)
    parser.add_argument("--stieltjes-order", type=int, default=12)
    parser.add_argument("--chebyshev-order", type=int, default=384)
    parser.add_argument("--smooth-order", type=int, default=95)
    args = parser.parse_args()
    print(
        run_support_one_audit(
            dimension=args.dimension,
            low_dimension=args.low_dimension,
            stieltjes_order=args.stieltjes_order,
            chebyshev_order=args.chebyshev_order,
            smooth_order=args.smooth_order,
        )
    )


if __name__ == "__main__":
    main()
