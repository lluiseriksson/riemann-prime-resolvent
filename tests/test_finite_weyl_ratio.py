import numpy as np
import pytest

from experiments.theta_pencil.finite_weyl_ratio import (
    audit_resolvent_shift,
    audit_two_channel_shift,
    canonical_weyl_from_channels,
    canonically_normalized_shifted_value,
    exact_normalized_unshift_error,
    exact_unshift_error,
    finite_weyl_function,
    normalized_unshift_error_bound,
    projective_cross_ratio,
    shifted_herglotz_value,
    undo_canonically_normalized_shift,
    unshift_error_bound,
    unshift_herglotz_value,
)


def test_finite_self_adjoint_weyl_function_is_herglotz():
    operator = np.array([[1.0, 0.4], [0.4, 3.0]])
    vector = np.array([1.0, -0.25])
    for z in (0.2 + 0.1j, -3.0 + 2.0j, 5.0 + 0.75j):
        assert finite_weyl_function(operator, vector, z).imag > 0.0


def test_shift_resolvent_identity_and_gap_bound():
    operator = np.array([[0.5, 0.2], [0.2, 2.0]])
    vector = np.array([1.0, 2.0])
    result = audit_resolvent_shift(operator, vector, -2.0, -0.25)
    assert result.identity_residual < 1.0e-14
    assert result.difference_norm <= result.norm_bound * (1.0 + 1.0e-14)


def test_shift_audit_rejects_a_shift_above_the_ground_state():
    with pytest.raises(ValueError):
        audit_resolvent_shift(np.eye(2), np.ones(2), 0.0, 1.5)


def test_two_channel_ratio_has_exact_nonzero_shift_defect():
    operator = np.diag([1.0, 3.0])
    result = audit_two_channel_shift(
        operator,
        np.array([1.0, 1.0]),
        np.array([1.0, -1.0]),
        np.array([1.0, 0.5]),
        0.0,
        -1.0,
    )
    assert result.lower_ratio == pytest.approx(7.0 / 5.0)
    assert result.upper_ratio == pytest.approx(5.0 / 3.0)
    assert abs(result.cross_difference) > 0.0
    assert result.identity_residual < 1.0e-15
    assert abs(result.lower_ratio_derivative) > 0.0


def test_cross_ratio_is_invariant_under_constant_mobius_map():
    values = (0.2 + 0.3j, -0.4 + 0.8j, 1.1 + 0.2j, 2.0 + 1.5j)
    transformed = tuple((2.0 * value + 1.0) / (0.5 * value + 3.0) for value in values)
    assert projective_cross_ratio(transformed) == pytest.approx(
        projective_cross_ratio(values)
    )


def test_canonical_channel_weyl_value_has_basepoint_normalization():
    value = canonical_weyl_from_channels(3.0 - 2.0j, 0.7 + 0.1j, 1j)
    assert value == pytest.approx(1j)


def test_shifted_herglotz_map_and_exact_error_formula():
    value = 0.4 + 0.7j
    shift = -8.0
    shifted = shifted_herglotz_value(value, shift)
    assert shifted.imag > 0.0
    assert unshift_herglotz_value(shifted, shift) == pytest.approx(value)
    error = 2.0e-7 - 3.0e-7j
    direct = unshift_herglotz_value(shifted + error, shift) - value
    assert exact_unshift_error(value, error, shift) == pytest.approx(direct)


def test_uniform_unshift_error_bound_controls_exact_error():
    value = -0.3 + 0.9j
    shift = -25.0
    error = 1.0e-7 - 2.0e-7j
    bound = unshift_error_bound(abs(value), abs(error), shift)
    assert abs(exact_unshift_error(value, error, shift)) <= bound


def test_uniform_unshift_error_bound_rejects_uncontrolled_denominator():
    with pytest.raises(ValueError, match="inverse denominator"):
        unshift_error_bound(2.0, 0.1, -10.0)


def test_canonical_shift_normalizes_base_point_and_preserves_half_plane():
    c = 21.67508148290566
    for shift in (-0.1, -10.0, -1.0e6):
        base = canonically_normalized_shifted_value(1j * c, shift, c)
        assert base == pytest.approx(1j)
        value = canonically_normalized_shifted_value(0.4 + 0.7j, shift, c)
        assert value.imag > 0.0


def test_canonical_shift_inverse_and_exact_error_formula():
    value = -0.3 + 0.9j
    shift = -1000.0
    c = 21.67508148290566
    shifted = canonically_normalized_shifted_value(value, shift, c)
    assert undo_canonically_normalized_shift(shifted, shift, c) == pytest.approx(
        value
    )
    error = 2.0e-7 - 1.0e-7j
    direct = undo_canonically_normalized_shift(
        shifted + error, shift, c
    ) - value
    assert exact_normalized_unshift_error(value, error, shift, c) == pytest.approx(
        direct
    )
    bound = normalized_unshift_error_bound(abs(value), abs(error), shift, c)
    assert abs(direct) <= bound


def test_canonical_inverse_amplification_stays_bounded_for_large_shift():
    target_bound = 2.0
    raw_error = 1.0e-8
    c = 3.0
    bounds = [
        normalized_unshift_error_bound(target_bound, raw_error, shift, c)
        for shift in (-1.0e2, -1.0e4, -1.0e6)
    ]
    expected_limit = 2.0 * raw_error * target_bound**2 / c
    assert bounds[-1] == pytest.approx(expected_limit, rel=2.0e-6)
