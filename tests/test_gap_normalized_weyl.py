import numpy as np
import pytest

from experiments.theta_pencil.gap_normalized_weyl import (
    gap_normalized_weyl_value,
)


def test_gap_normalized_shift_is_admissible_and_affine_invariant():
    operator = np.array([[1.4, 0.2], [0.2, 3.1]])
    metric = np.array([[1.2, 0.1], [0.1, 0.9]])
    plus = np.array([1.0, 0.3])
    minus = np.array([-0.2, 0.8])
    observation = np.array([0.7 + 0.4j, -0.1 + 0.6j])
    z = 0.6 + 0.9j
    original = gap_normalized_weyl_value(
        operator,
        metric,
        plus,
        minus,
        observation,
        z,
        gap_multiple=0.7,
    )
    assert original.shift < original.ground_eigenvalue
    assert original.ground_eigenvalue - original.shift == pytest.approx(
        0.7 * original.first_gap
    )

    alpha = 3.5
    beta = -2.1
    transformed = gap_normalized_weyl_value(
        alpha * operator + beta * metric,
        metric,
        plus,
        minus,
        observation,
        z,
        gap_multiple=0.7,
    )
    assert transformed.ground_eigenvalue == pytest.approx(
        alpha * original.ground_eigenvalue + beta
    )
    assert transformed.first_gap == pytest.approx(alpha * original.first_gap)
    assert transformed.canonical_weyl == pytest.approx(original.canonical_weyl)


def test_gap_normalized_shift_rejects_a_degenerate_ground_state():
    with pytest.raises(ValueError, match="simple"):
        gap_normalized_weyl_value(
            np.eye(2),
            np.eye(2),
            np.ones(2),
            np.array([1.0, -1.0]),
            np.array([1.0 + 1.0j, 0.5 - 0.2j]),
            0.4 + 0.8j,
            gap_multiple=1.0,
        )
