"""Finite-dimensional falsifier for the first semilocal Weil window.

The formulas are equations (A.4)--(A.6) of Connes--Consani,
arXiv:2006.13771, transferred to logarithmic coordinates.  The experiment
uses H = (-d^2/dt^2 + 1/4) phi, so the two Weil constraints hold by
integration by parts for every basis vector.

A nonpositive finite matrix is evidence only.  A positive generalized
eigenvalue is a genuine counterexample to the registered finite-dimensional
claim once its numerical error is certified.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np
from scipy.linalg import eigh
from scipy.signal import correlate
from scipy.special import digamma
from numpy.polynomial.legendre import Legendre


EULER_GAMMA = 0.577215664901532860606512090082402431


@dataclass(frozen=True)
class WeilMatrixResult:
    q_cutoff: float
    support_radius: float
    grid_points: int
    basis_size: int
    basis_family: str
    constraint_residual: float
    gram_condition: float
    arch_eigenvalues: np.ndarray
    total_eigenvalues: np.ndarray


def _bump_jet(r: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return psi, psi', psi'' for exp(-1/(1-r^2)) on |r| < 1."""
    psi = np.zeros_like(r)
    first = np.zeros_like(r)
    second = np.zeros_like(r)
    inside = np.abs(r) < 1.0
    ri = r[inside]
    denominator = 1.0 - ri * ri
    value = np.exp(-1.0 / denominator)
    exponent_first = -2.0 * ri / denominator**2
    exponent_second = -2.0 / denominator**2 - 8.0 * ri**2 / denominator**3
    psi[inside] = value
    first[inside] = value * exponent_first
    second[inside] = value * (exponent_first**2 + exponent_second)
    return psi, first, second


def polynomial_constrained_basis(
    t: np.ndarray, half_width: float, size: int
) -> np.ndarray:
    """Rows are Q(phi_j), Q=-d^2/dt^2+1/4, with compact support."""
    r = t / half_width
    psi, psi_first, psi_second = _bump_jet(r)
    rows = []
    for degree in range(size):
        power = r**degree
        first_power = degree * r ** (degree - 1) if degree >= 1 else np.zeros_like(r)
        second_power = (
            degree * (degree - 1) * r ** (degree - 2)
            if degree >= 2
            else np.zeros_like(r)
        )
        phi = power * psi
        phi_rr = second_power * psi + 2.0 * first_power * psi_first + power * psi_second
        rows.append(-phi_rr / half_width**2 + 0.25 * phi)
    return np.asarray(rows)


def translated_constrained_basis(
    t: np.ndarray, half_width: float, size: int, overlap: float = 1.5
) -> np.ndarray:
    """Localized Q(bump) basis with a registered overlap ratio."""
    if size < 2:
        raise ValueError("translated basis needs at least two vectors")
    width = 2.0 * overlap * half_width / (size - 1 + 2.0 * overlap)
    centers = np.linspace(-half_width + width, half_width - width, size)
    rows = []
    for center in centers:
        r = (t - center) / width
        psi, _, psi_second = _bump_jet(r)
        rows.append(-psi_second / width**2 + 0.25 * psi)
    return np.asarray(rows)


def legendre_constrained_basis(
    t: np.ndarray, half_width: float, size: int
) -> np.ndarray:
    """Global smooth basis using Legendre polynomials times the flat bump."""
    r = t / half_width
    psi, psi_first, psi_second = _bump_jet(r)
    rows = []
    for degree in range(size):
        polynomial = Legendre.basis(degree)
        value = polynomial(r)
        first = polynomial.deriv(1)(r)
        second = polynomial.deriv(2)(r)
        phi = value * psi
        phi_rr = second * psi + 2.0 * first * psi_first + value * psi_second
        rows.append(-phi_rr / half_width**2 + 0.25 * phi)
    return np.asarray(rows)


def _simpson_weights(intervals: int) -> np.ndarray:
    if intervals % 2:
        raise ValueError("Simpson integration needs an even interval count")
    weights = np.ones(intervals + 1)
    weights[1:-1:2] = 4.0
    weights[2:-1:2] = 2.0
    return weights


def _correlation_matrices(basis: np.ndarray, dt: float) -> np.ndarray:
    """Return C[k,i,j] = integral H_i(u) H_j(u-k*dt) du."""
    size, points = basis.shape
    positive_lags = points
    matrices = np.empty((positive_lags, size, size))
    center = points - 1
    for i in range(size):
        for j in range(size):
            full = correlate(basis[i], basis[j], mode="full", method="fft")
            matrices[:, i, j] = dt * full[center : center + positive_lags]
    return matrices


def _select_basis(
    t: np.ndarray, half_width: float, size: int, family: str
) -> np.ndarray:
    if family == "polynomial":
        return polynomial_constrained_basis(t, half_width, size)
    if family == "legendre":
        return legendre_constrained_basis(t, half_width, size)
    if family == "translated":
        return translated_constrained_basis(t, half_width, size)
    raise ValueError("basis_family must be 'polynomial', 'legendre', or 'translated'")


def _interpolate_matrix(matrices: np.ndarray, position: float) -> np.ndarray:
    lower = int(math.floor(position))
    fraction = position - lower
    if lower < 0 or lower + 1 >= len(matrices):
        raise ValueError("requested lag lies outside the registered support")
    return (1.0 - fraction) * matrices[lower] + fraction * matrices[lower + 1]


def build_weil_matrices(
    q_cutoff: float = 4.5,
    grid_points: int = 4097,
    basis_size: int = 8,
    support_margin: float = 0.98,
    basis_family: str = "polynomial",
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
    """Return Gram, archimedean, total matrices and two diagnostics.

    The convolution support radius is strictly below (1/2) log(q_cutoff).
    In the registered 4 < q <= 5 window only p=2 can be sampled; p=3 is in
    the semilocal set but outside the support.
    """
    if not 4.0 < q_cutoff <= 5.0:
        raise ValueError("the first arithmetic window requires 4 < q <= 5")
    if grid_points < 257 or grid_points % 2 == 0:
        raise ValueError("grid_points must be an odd integer at least 257")
    if not 0.0 < support_margin < 1.0:
        raise ValueError("support_margin must lie strictly between 0 and 1")

    support_radius = support_margin * 0.5 * math.log(q_cutoff)
    if support_radius <= math.log(2.0):
        raise ValueError("the chosen support does not activate the prime 2")
    half_width = support_radius / 2.0
    t = np.linspace(-half_width, half_width, grid_points)
    dt = float(t[1] - t[0])
    basis = _select_basis(t, half_width, basis_size, basis_family)

    constraint_plus = np.trapezoid(basis * np.exp(t / 2.0), t, axis=1)
    constraint_minus = np.trapezoid(basis * np.exp(-t / 2.0), t, axis=1)
    constraint_residual = float(
        max(np.max(np.abs(constraint_plus)), np.max(np.abs(constraint_minus)))
    )

    correlations = _correlation_matrices(basis, dt)
    gram = 0.5 * (correlations[0] + correlations[0].T)

    lags = np.arange(grid_points) * dt
    weights = _simpson_weights(grid_points - 1)
    arch = np.zeros_like(gram)
    for index, lag in enumerate(lags):
        if index == 0:
            integrand = 0.5 * gram
        else:
            symmetric = correlations[index] + correlations[index].T
            denominator = -math.expm1(-2.0 * lag)
            integrand = (
                math.exp(-lag / 2.0) * symmetric
                - 2.0 * math.exp(-lag) * gram
            ) / denominator
        arch += weights[index] * integrand
    arch *= dt / 3.0
    # The compactly supported correlations vanish beyond support_radius, but
    # the principal-value subtraction -2 exp(-t) h(0) does not.  Its exact
    # remaining integral is -2 atanh(exp(-support_radius)) h(0).
    arch -= 2.0 * math.atanh(math.exp(-support_radius)) * gram
    arch += (math.log(4.0 * math.pi) + EULER_GAMMA) * gram
    arch = 0.5 * (arch + arch.T)

    prime_lag = math.log(2.0)
    prime_correlation = _interpolate_matrix(correlations, prime_lag / dt)
    prime = (math.log(2.0) / math.sqrt(2.0)) * (
        prime_correlation + prime_correlation.T
    )
    total = arch + prime
    total = 0.5 * (total + total.T)

    gram_eigenvalues = np.linalg.eigvalsh(gram)
    gram_condition = float(gram_eigenvalues[-1] / gram_eigenvalues[0])
    return gram, arch, total, constraint_residual, gram_condition


def fourier_archimedean_matrix(
    q_cutoff: float = 4.5,
    grid_points: int = 4097,
    basis_size: int = 8,
    support_margin: float = 0.98,
    basis_family: str = "polynomial",
    frequency_max: float = 640.0,
    frequency_points: int = 16385,
    include_prime_two: bool = False,
) -> np.ndarray:
    """Independent Fourier-side evaluation of the archimedean matrix.

    It uses W_R(H*H*) = -pi^(-1) integral theta'(s) |Hhat(s)|^2 ds,
    with theta'(s) = (Re digamma(1/4+is/2)-log(pi))/2.
    """
    if frequency_points % 2 == 0:
        raise ValueError("frequency_points must be odd for Simpson integration")
    support_radius = support_margin * 0.5 * math.log(q_cutoff)
    half_width = support_radius / 2.0
    t = np.linspace(-half_width, half_width, grid_points)
    dt = float(t[1] - t[0])
    basis = _select_basis(t, half_width, basis_size, basis_family)
    t_weights = _simpson_weights(grid_points - 1) * (dt / 3.0)
    weighted_basis = basis * t_weights

    frequencies = np.linspace(0.0, frequency_max, frequency_points)
    ds = float(frequencies[1] - frequencies[0])
    frequency_weights = _simpson_weights(frequency_points - 1)
    matrix = np.zeros((basis_size, basis_size))
    chunk_size = 128
    for start in range(0, frequency_points, chunk_size):
        stop = min(start + chunk_size, frequency_points)
        chunk = frequencies[start:stop]
        transforms = weighted_basis @ np.exp(-1j * np.outer(t, chunk))
        theta_prime = 0.5 * (
            np.real(digamma(0.25 + 0.5j * chunk)) - math.log(math.pi)
        )
        symbol = (-2.0 / math.pi) * theta_prime
        if include_prime_two:
            symbol += (
                2.0
                * math.log(2.0)
                / (math.pi * math.sqrt(2.0))
                * np.cos(chunk * math.log(2.0))
            )
        scalar = symbol * frequency_weights[start:stop]
        matrix += np.real(
            np.einsum("ik,jk,k->ij", transforms, np.conjugate(transforms), scalar)
        )
    return 0.5 * (matrix + matrix.T) * (ds / 3.0)


def run_audit(
    q_cutoff: float = 4.5,
    grid_points: int = 4097,
    basis_size: int = 8,
    support_margin: float = 0.98,
    basis_family: str = "polynomial",
) -> WeilMatrixResult:
    gram, arch, total, residual, condition = build_weil_matrices(
        q_cutoff=q_cutoff,
        grid_points=grid_points,
        basis_size=basis_size,
        support_margin=support_margin,
        basis_family=basis_family,
    )
    arch_eigenvalues = eigh(arch, gram, eigvals_only=True)
    total_eigenvalues = eigh(total, gram, eigvals_only=True)
    return WeilMatrixResult(
        q_cutoff=q_cutoff,
        support_radius=support_margin * 0.5 * math.log(q_cutoff),
        grid_points=grid_points,
        basis_size=basis_size,
        basis_family=basis_family,
        constraint_residual=residual,
        gram_condition=condition,
        arch_eigenvalues=arch_eigenvalues,
        total_eigenvalues=total_eigenvalues,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=float, default=4.5)
    parser.add_argument("--grid", type=int, default=4097)
    parser.add_argument("--basis", type=int, default=8)
    parser.add_argument("--margin", type=float, default=0.98)
    parser.add_argument(
        "--family",
        choices=("polynomial", "legendre", "translated"),
        default="polynomial",
    )
    parser.add_argument("--fourier-check", action="store_true")
    args = parser.parse_args()
    result = run_audit(args.q, args.grid, args.basis, args.margin, args.family)
    print(result)
    print("arch generalized eigenvalues:")
    print(np.array2string(result.arch_eigenvalues, precision=12))
    print("total generalized eigenvalues:")
    print(np.array2string(result.total_eigenvalues, precision=12))
    if args.fourier_check:
        gram, arch, _, _, _ = build_weil_matrices(
            args.q, args.grid, args.basis, args.margin, args.family
        )
        fourier_arch = fourier_archimedean_matrix(
            args.q, args.grid, args.basis, args.margin, args.family
        )
        discrepancy = eigh(arch - fourier_arch, gram, eigvals_only=True)
        print("direct-minus-Fourier generalized eigenvalues:")
        print(np.array2string(discrepancy, precision=12))


if __name__ == "__main__":
    main()
