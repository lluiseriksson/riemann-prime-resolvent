import math

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("scipy")

from scipy.linalg import eigh

from experiments.theta_pencil.semilocal_weil_matrix import (
    build_weil_matrices,
    fourier_archimedean_matrix,
)


def test_first_window_basis_obeys_both_weil_constraints() -> None:
    _, _, _, residual, condition = build_weil_matrices(
        4.5, 1025, 6, 0.98, "legendre"
    )
    assert residual < 1e-12
    assert condition < 20.0


def test_registered_finite_matrix_has_required_sign() -> None:
    gram, arch, total, _, _ = build_weil_matrices(
        5.0, 2049, 8, 0.995, "legendre"
    )
    assert eigh(arch, gram, eigvals_only=True)[-1] < -0.3
    assert eigh(total, gram, eigvals_only=True)[-1] < -0.2


def test_archimedean_formula_agrees_with_fourier_representation() -> None:
    gram, arch, total, _, _ = build_weil_matrices(
        4.5, 2049, 3, 0.98, "legendre"
    )
    fourier = fourier_archimedean_matrix(
        4.5, 2049, 3, 0.98, "legendre"
    )
    discrepancy = eigh(arch - fourier, gram, eigvals_only=True)
    assert np.max(np.abs(discrepancy)) < 1e-6
    fourier_total = fourier_archimedean_matrix(
        4.5, 2049, 3, 0.98, "legendre", include_prime_two=True
    )
    total_discrepancy = eigh(total - fourier_total, gram, eigvals_only=True)
    assert np.max(np.abs(total_discrepancy)) < 2e-4


def test_support_must_reach_two() -> None:
    with pytest.raises(ValueError, match="does not activate"):
        build_weil_matrices(4.01, 1025, 4, 0.99, "legendre")


def test_prime_two_is_the_only_active_prime() -> None:
    support_radius = 0.999 * 0.5 * math.log(5.0)
    assert math.log(2.0) < support_radius < math.log(3.0)
