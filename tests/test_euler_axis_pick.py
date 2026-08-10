import numpy as np
import pytest

from experiments.theta_pencil.euler_axis_pick import (
    centered_zero_orbit_gate_margin,
    euler_axis_log_derivative_kernel,
    euler_axis_pick_matrix,
    reciprocal_log_derivative_congruence_residual,
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


def test_reciprocal_pick_kernel_is_diagonally_congruent_to_log_kernel():
    heights = (1.0, 2.0, 3.0)
    log_derivatives = (0.046, 0.092, 0.138)
    kernel = euler_axis_log_derivative_kernel(heights, log_derivatives)
    assert np.allclose(kernel, np.full((3, 3), 0.046))
    assert reciprocal_log_derivative_congruence_residual(
        heights, log_derivatives, 21.0
    ) < 1.0e-15


def test_every_admissible_off_line_zero_orbit_has_positive_gate_margin():
    for alpha, gamma, eta in (
        (0.49, 1.01, 0.5001),
        (-0.49, 14.134725, 1.0),
        (0.1, 3.0e12, 10.0),
    ):
        assert centered_zero_orbit_gate_margin(alpha, gamma, eta) > 0.0
    with pytest.raises(ValueError):
        centered_zero_orbit_gate_margin(0.5, 14.0, 1.0)
