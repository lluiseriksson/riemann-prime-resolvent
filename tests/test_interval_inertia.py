import numpy as np
import pytest

from experiments.theta_pencil.interval_inertia import (
    certify_arb_positive_definite_by_congruence,
    certify_interval_inertia,
    entrywise_weyl_budget,
)


def test_ball_inertia_certifies_well_separated_diagonal_matrix():
    pytest.importorskip("flint")
    result = certify_interval_inertia(np.diag([-2.0, 1.0, 3.0]), 1e-5)
    assert result.negative_count == 1
    assert result.positive_count == 2
    assert result.unresolved_count == 0
    assert result.method in {"direct-ball", "point-weyl"}


def test_ball_inertia_accepts_last_bit_midpoint_asymmetry():
    pytest.importorskip("flint")
    matrix = np.array([[2.0, 0.25 + 1e-14], [0.25, 1.0]])
    result = certify_interval_inertia(matrix, 1e-12)
    assert result.negative_count == 0
    assert result.positive_count == 2
    assert result.unresolved_count == 0


def test_congruence_keeps_structured_entry_radii():
    flint = pytest.importorskip("flint")
    matrix = flint.arb_mat(2, 2)
    matrix[0, 0] = flint.arb(1.0e-8, 1.0e-12)
    matrix[1, 1] = flint.arb(1.0, 1.0e-4)
    result = certify_arb_positive_definite_by_congruence(matrix, 256)
    assert result.original_spectral_lower > 0.0
    assert result.transformation_gram_lower > 0.0


def test_weyl_entry_budget():
    assert entrywise_weyl_budget(0.0022, 44) == pytest.approx(5e-5)
