import math

import numpy as np
import pytest

pytest.importorskip("scipy")

from experiments.theta_pencil.screw_weil_operator import (
    build_screw_weil_components,
    run_audit,
)


def test_dirichlet_gram_is_well_conditioned() -> None:
    result = run_audit(half_width=0.4, grid_points=2049, basis_size=8)
    assert result.gram_condition == pytest.approx(1.0, abs=2e-12)


@pytest.mark.parametrize(
    ("half_width", "expected"),
    [(0.3, ()), (0.4, (2,)), (0.55, (2, 3))],
)
def test_prime_power_support_thresholds(
    half_width: float, expected: tuple[int, ...]
) -> None:
    result = run_audit(half_width=half_width, grid_points=2049, basis_size=4)
    assert result.active_prime_powers == expected


def test_source_normalized_component_identity() -> None:
    components = build_screw_weil_components(
        half_width=0.4, grid_points=2049, basis_size=6
    )
    assembled = components.polar - components.archimedean - components.prime
    assert np.max(np.abs(assembled - assembled.T)) < 1e-12
    assert np.linalg.eigvalsh(components.gram)[0] > 0.999999999


def test_polar_component_is_the_cross_gram_from_weil_convolution() -> None:
    half_width = 0.4
    grid_points = 2049
    basis_size = 6
    components = build_screw_weil_components(
        half_width=half_width,
        grid_points=grid_points,
        basis_size=basis_size,
    )
    coordinate = np.linspace(-half_width, half_width, grid_points)
    spacing = float(coordinate[1] - coordinate[0])
    from experiments.theta_pencil.semilocal_weil_matrix import _simpson_weights
    from experiments.theta_pencil.screw_weil_operator import dirichlet_basis

    weights = _simpson_weights(grid_points - 1) * (spacing / 3.0)
    basis = dirichlet_basis(coordinate, half_width, basis_size)
    plus = basis @ (weights * np.exp(coordinate / 2.0))
    minus = basis @ (weights * np.exp(-coordinate / 2.0))
    expected = np.outer(plus, minus) + np.outer(minus, plus)
    assert components.polar == pytest.approx(expected)

    odd = np.zeros(basis_size)
    odd[1] = 1.0
    assert float(odd @ components.polar @ odd) < 0.0


def test_lowest_ritz_value_is_grid_stable_at_first_two_primes() -> None:
    # This eigenvalue is an 8-digit cancellation.  Coarser grids are useful
    # falsifiers but are not fine enough to certify its leading digits.
    coarse = run_audit(half_width=0.55, grid_points=8193, basis_size=12)
    fine = run_audit(half_width=0.55, grid_points=16385, basis_size=12)
    assert coarse.eigenvalues[0] > 0.0
    assert fine.eigenvalues[0] > 0.0
    assert math.isclose(
        coarse.eigenvalues[0], fine.eigenvalues[0], rel_tol=0.01, abs_tol=1e-11
    )
