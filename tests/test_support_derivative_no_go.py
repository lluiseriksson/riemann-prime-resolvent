import math

import pytest

from experiments.theta_pencil.support_derivative_no_go import (
    build_derivative_no_go_witness,
    phase_locked_frequency,
    polynomial_bump_overlap,
)


def test_polynomial_overlap_derivative_matches_centered_difference():
    h = math.log(2.0) / 0.4
    _, derivative = polynomial_bump_overlap(h)
    step = 1e-5
    left, _ = polynomial_bump_overlap(h - step)
    right, _ = polynomial_bump_overlap(h + step)
    assert derivative == pytest.approx((right - left) / (2 * step), rel=2e-8)


def test_phase_lock_makes_the_first_order_term_negative():
    h = math.log(2.0) / 0.4
    frequency = phase_locked_frequency(h, 20)
    assert math.sin(frequency * h) == pytest.approx(1.0, abs=2e-14)
    witness = build_derivative_no_go_witness(0.4, 20)
    assert witness.overlap > 0.0
    assert witness.support_derivative < 0.0


def test_derivative_outgrows_the_logarithmic_form_scale():
    ratios = [
        -build_derivative_no_go_witness(0.4, index).derivative_to_logarithmic_scale
        for index in (10, 100, 1000)
    ]
    assert ratios[0] > 0.0
    assert ratios[1] > 5.0 * ratios[0]
    assert ratios[2] > 5.0 * ratios[1]
