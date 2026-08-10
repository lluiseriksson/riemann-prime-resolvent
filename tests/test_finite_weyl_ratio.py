import numpy as np
import pytest

from experiments.theta_pencil.finite_weyl_ratio import (
    audit_resolvent_shift,
    audit_two_channel_shift,
    exact_unshift_error,
    finite_weyl_function,
    projective_cross_ratio,
    shifted_herglotz_value,
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


def test_shifted_herglotz_map_and_exact_error_formula():
    value = 0.4 + 0.7j
    shift = -8.0
    shifted = shifted_herglotz_value(value, shift)
    assert shifted.imag > 0.0
    assert unshift_herglotz_value(shifted, shift) == pytest.approx(value)
    error = 2.0e-7 - 3.0e-7j
    direct = unshift_herglotz_value(shifted + error, shift) - value
    assert exact_unshift_error(value, error, shift) == pytest.approx(direct)
