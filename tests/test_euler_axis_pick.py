import numpy as np
import pytest

from experiments.theta_pencil.euler_axis_pick import (
    euler_axis_pick_matrix,
    two_point_log_derivative_gate,
    two_point_pick_determinant,
)


def test_two_point_factorization_matches_direct_determinant():
    heights = (2.0, 3.0)
    values = (0.50238247, 0.33752251)
    matrix = euler_axis_pick_matrix(heights, values)
    assert np.linalg.det(matrix) == pytest.approx(
        two_point_pick_determinant(*(
            heights[0], values[0], heights[1], values[1]
        ))
    )


def test_rank_one_reciprocal_data_have_zero_pick_determinant():
    assert two_point_pick_determinant(2.0, 0.5, 5.0, 0.2) == pytest.approx(0.0)


def test_differential_gate_is_the_log_derivative_scaling_defect():
    assert two_point_log_derivative_gate(3.0, 0.14, 0.02) == pytest.approx(0.08)
    with pytest.raises(ValueError):
        two_point_log_derivative_gate(0.0, 1.0, 1.0)
