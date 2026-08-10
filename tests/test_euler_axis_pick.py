import numpy as np
import pytest

from experiments.theta_pencil.euler_axis_pick import (
    centered_zero_orbit_profile,
    centered_zero_orbit_gate_margin,
    euler_axis_log_derivative_kernel,
    euler_axis_pick_matrix,
    off_line_orbit_defect_ceiling,
    local_three_point_curvature_gate,
    normalized_log_derivative_correlation,
    reciprocal_log_derivative_congruence_residual,
    two_point_log_derivative_gate,
    two_point_pick_determinant,
    zero_orbit_mixture_lower_slack,
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


def test_hyperbolic_correlation_is_the_diagonal_normalization():
    heights = (1.0, 2.0, 3.0)
    log_derivatives = (0.05, 0.09, 0.13)
    kernel = euler_axis_log_derivative_kernel(heights, log_derivatives)
    diagonal = np.sqrt(np.diag(kernel))
    direct = kernel / (diagonal[:, None] * diagonal[None, :])
    assert np.allclose(
        normalized_log_derivative_correlation(heights, log_derivatives),
        direct,
    )


def test_local_three_point_gate_is_the_h6_determinant_coefficient():
    slope = 0.5
    curvature = 0.2
    target = local_three_point_curvature_gate(slope, curvature)
    assert target == pytest.approx(2.21)
    for step in (0.01, 0.005):
        points = np.array((-step, 0.0, step))
        values = slope * points + 0.5 * curvature * points**2
        correlation = np.cosh(values[:, None] - values[None, :]) / np.cosh(
            points[:, None] - points[None, :]
        )
        assert np.linalg.det(correlation) / step**6 == pytest.approx(
            target, rel=5.0e-4
        )


def test_off_line_orbit_has_the_exact_negative_lower_curvature_slack():
    mass, slope, curvature, slack = centered_zero_orbit_profile(
        0.25, 14.0, 3.0
    )
    assert mass > 0.0
    assert -1.0 < slope < 1.0
    assert slack < 0.0
    assert curvature + 2.0 * (1.0 - slope * slope) == pytest.approx(slack)
    _, _, _, on_line_slack = centered_zero_orbit_profile(0.0, 14.0, 3.0)
    assert on_line_slack == 0.0


def test_verified_height_makes_each_off_line_defect_tiny():
    ceiling = off_line_orbit_defect_ceiling(3.0e12)
    assert ceiling == pytest.approx(1.0 / (3.0e12) ** 2)
    assert ceiling < 1.12e-25


def test_orbit_mixture_slack_is_component_defect_plus_four_variances():
    profiles = (
        centered_zero_orbit_profile(0.0, 14.0, 3.0),
        centered_zero_orbit_profile(0.2, 3.0e12, 3.0),
        centered_zero_orbit_profile(0.0, 21.0, 3.0),
    )
    direct, decomposed = zero_orbit_mixture_lower_slack(
        tuple(row[0] for row in profiles),
        tuple(row[1] for row in profiles),
        tuple(row[2] for row in profiles),
    )
    assert direct == pytest.approx(decomposed)
    assert direct > 0.0
