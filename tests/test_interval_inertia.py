import numpy as np
import pytest

from experiments.theta_pencil.interval_inertia import (
    certify_interval_inertia,
    entrywise_weyl_budget,
)


def test_ball_inertia_certifies_well_separated_diagonal_matrix():
    pytest.importorskip("flint")
    result = certify_interval_inertia(np.diag([-2.0, 1.0, 3.0]), 1e-5)
    assert result.negative_count == 1
    assert result.positive_count == 2
    assert result.unresolved_count == 0


def test_weyl_entry_budget():
    assert entrywise_weyl_budget(0.0022, 44) == pytest.approx(5e-5)

