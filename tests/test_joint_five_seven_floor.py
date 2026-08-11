import math

import numpy as np

from experiments.theta_pencil.joint_five_seven_floor import (
    REGISTERED_JOINT_FLOOR_TARGET,
    four_path_matrix_float,
    registered_joint_floor_target_margin,
    two_path_matrix_float,
)


def test_centered_four_path_is_above_registered_target():
    centered = -0.5 * math.log(7.0)
    least = float(np.linalg.eigvalsh(four_path_matrix_float(centered))[0])
    assert -0.263 < least < -0.262
    assert least > REGISTERED_JOINT_FLOOR_TARGET


def test_two_path_is_not_the_observed_minimum():
    left = 1.0 - math.log(7.0)
    right = math.log(7.0 / 5.0) - 1.0
    midpoint = 0.5 * (left + right)
    least = float(np.linalg.eigvalsh(two_path_matrix_float(midpoint))[0])
    assert -0.199 < least < -0.198


def test_registered_joint_target_moves_tail_to_58():
    degree, margin = registered_joint_floor_target_margin()
    assert degree == 58
    assert 0.0006 < margin < 0.0007
