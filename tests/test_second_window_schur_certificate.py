import numpy as np
import pytest

from experiments.theta_pencil.second_window_schur_certificate import (
    _assemble_parity_schur,
    _coercive_lower_from_schur,
)


def test_synthetic_schur_assembly_matches_scalar_formula():
    flint = pytest.importorskip("flint")
    source = flint.arb_mat([[2, 0], [0, 3]])
    band = flint.arb_mat([[0.1, 0], [0, 0.2]])
    flux = flint.arb_mat([[0.01, 0], [0, 0.02]])
    singular = flint.arb_mat([[0.03, 0], [0, 0.04]])
    result = _assemble_parity_schur(
        flint.arb,
        flint.arb_mat,
        source,
        band,
        flux,
        singular,
        0.5,
        0.01,
        1.5,
        0.02,
        0.1,
    )
    denominator = 1.5 - 0.5 - 0.02
    structured = 2 * np.array([0.04, 0.06])
    scalar = 11 * 0.02**2
    expected = np.array([2, 3]) - 0.51 - (
        np.array([0.1, 0.2]) + 1.1 * structured + scalar
    ) / denominator
    actual = np.diag([float(result[i, i].mid()) for i in range(2)])
    assert np.max(
        np.abs(actual - np.diag(expected))
    ) < 1e-14


def test_schur_reconstruction_returns_conservative_full_lower():
    flint = pytest.importorskip("flint")
    gram = flint.arb_mat([[4]])
    complement, coupling, lower = _coercive_lower_from_schur(
        flint.arb, 2.0, flint.arb(3), gram
    )
    full = np.array([[2.0 + 4.0 / 3.0, 2.0], [2.0, 3.0]])
    assert complement <= 3.0
    assert coupling >= 2.0
    assert 0.0 < lower <= np.linalg.eigvalsh(full)[0]
