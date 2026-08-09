"""Localized Weil operator in the continuous-kernel/Suzuki normalization.

This implements the defining Weil functional in arXiv:2606.09096, lines
107--119, on convolution squares supported in [-2a, 2a].  Its generalized
eigenvalues approximate the localized self-adjoint operator A_a, but no finite
compression establishes positivity of A_a.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np
from numpy.polynomial.legendre import Legendre
from scipy.linalg import eigh

from experiments.theta_pencil.semilocal_weil_matrix import (
    EULER_GAMMA,
    _bump_jet,
    _correlation_matrices,
    _interpolate_matrix,
    _simpson_weights,
)


@dataclass(frozen=True)
class ScrewAuditResult:
    half_width: float
    grid_points: int
    basis_size: int
    gram_condition: float
    active_prime_powers: tuple[int, ...]
    eigenvalues: np.ndarray


@dataclass(frozen=True)
class ScrewComponents:
    """Matrices entering the source-normalized Weil functional."""

    gram: np.ndarray
    polar: np.ndarray
    archimedean: np.ndarray
    prime: np.ndarray
    active_prime_powers: tuple[int, ...]
    gram_condition: float


def raw_legendre_basis(t: np.ndarray, half_width: float, size: int) -> np.ndarray:
    r = t / half_width
    bump, _, _ = _bump_jet(r)
    return np.asarray([Legendre.basis(degree)(r) * bump for degree in range(size)])


def dirichlet_basis(t: np.ndarray, half_width: float, size: int) -> np.ndarray:
    """First Dirichlet Laplacian modes, orthonormal on (-a,a)."""
    coordinate = (t + half_width) / (2.0 * half_width)
    return np.asarray(
        [
            np.sin(mode * math.pi * coordinate) / math.sqrt(half_width)
            for mode in range(1, size + 1)
        ]
    )


def von_mangoldt(n: int) -> float:
    """Return Lambda(n) by recognizing an integer prime power."""
    if n < 2:
        return 0.0
    for prime in range(2, n + 1):
        if any(prime % divisor == 0 for divisor in range(2, int(math.sqrt(prime)) + 1)):
            continue
        power = prime
        while power < n:
            power *= prime
        if power == n:
            return math.log(prime)
    return 0.0


def build_screw_weil_components(
    half_width: float = 0.4,
    grid_points: int = 4097,
    basis_size: int = 12,
    basis_family: str = "dirichlet",
) -> ScrewComponents:
    if half_width <= 0.0:
        raise ValueError("half_width must be positive")
    if grid_points < 257 or grid_points % 2 == 0:
        raise ValueError("grid_points must be odd and at least 257")

    t = np.linspace(-half_width, half_width, grid_points)
    dt = float(t[1] - t[0])
    if basis_family == "dirichlet":
        basis = dirichlet_basis(t, half_width, basis_size)
    elif basis_family == "legendre":
        basis = raw_legendre_basis(t, half_width, basis_size)
    else:
        raise ValueError("basis_family must be 'dirichlet' or 'legendre'")
    correlations = _correlation_matrices(basis, dt)
    gram = 0.5 * (correlations[0] + correlations[0].T)
    support_radius = 2.0 * half_width

    lags = np.arange(grid_points) * dt
    weights = _simpson_weights(grid_points - 1)
    local_arch = np.zeros_like(gram)
    for index, lag in enumerate(lags):
        if index == 0:
            integrand = 0.5 * gram
        else:
            symmetric = correlations[index] + correlations[index].T
            integrand = (
                math.exp(-lag / 2.0) * symmetric
                - 2.0 * math.exp(-lag) * gram
            ) / (-math.expm1(-2.0 * lag))
        local_arch += weights[index] * integrand
    local_arch *= dt / 3.0
    local_arch -= 2.0 * math.atanh(math.exp(-support_radius)) * gram
    local_arch += (math.log(4.0 * math.pi) + EULER_GAMMA) * gram

    t_weights = _simpson_weights(grid_points - 1) * (dt / 3.0)
    plus = basis @ (t_weights * np.exp(t / 2.0))
    minus = basis @ (t_weights * np.exp(-t / 2.0))
    polar = np.outer(plus, plus) + np.outer(minus, minus)

    prime_matrix = np.zeros_like(gram)
    active = []
    upper = int(math.floor(math.exp(support_radius) + 1e-13))
    for n in range(2, upper + 1):
        mangoldt = von_mangoldt(n)
        if mangoldt == 0.0 or math.log(n) >= support_radius:
            continue
        active.append(n)
        correlation = _interpolate_matrix(correlations, math.log(n) / dt)
        prime_matrix += (mangoldt / math.sqrt(n)) * (correlation + correlation.T)

    gram_eigenvalues = np.linalg.eigvalsh(gram)
    condition = float(gram_eigenvalues[-1] / gram_eigenvalues[0])
    return ScrewComponents(
        gram=gram,
        polar=0.5 * (polar + polar.T),
        archimedean=0.5 * (local_arch + local_arch.T),
        prime=0.5 * (prime_matrix + prime_matrix.T),
        active_prime_powers=tuple(active),
        gram_condition=condition,
    )


def build_screw_weil_matrix(
    half_width: float = 0.4,
    grid_points: int = 4097,
    basis_size: int = 12,
    basis_family: str = "dirichlet",
) -> tuple[np.ndarray, np.ndarray, tuple[int, ...], float]:
    components = build_screw_weil_components(
        half_width, grid_points, basis_size, basis_family
    )
    weil = components.polar - components.archimedean - components.prime
    weil = 0.5 * (weil + weil.T)
    return (
        components.gram,
        weil,
        components.active_prime_powers,
        components.gram_condition,
    )


def run_audit(
    half_width: float = 0.4,
    grid_points: int = 4097,
    basis_size: int = 12,
    basis_family: str = "dirichlet",
) -> ScrewAuditResult:
    gram, weil, active, condition = build_screw_weil_matrix(
        half_width, grid_points, basis_size, basis_family
    )
    return ScrewAuditResult(
        half_width=half_width,
        grid_points=grid_points,
        basis_size=basis_size,
        gram_condition=condition,
        active_prime_powers=active,
        eigenvalues=eigh(weil, gram, eigvals_only=True),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--half-width", type=float, default=0.4)
    parser.add_argument("--grid", type=int, default=4097)
    parser.add_argument("--basis", type=int, default=12)
    parser.add_argument(
        "--family", choices=("dirichlet", "legendre"), default="dirichlet"
    )
    args = parser.parse_args()
    result = run_audit(args.half_width, args.grid, args.basis, args.family)
    print(result)
    print(np.array2string(result.eigenvalues, precision=12))


if __name__ == "__main__":
    main()
