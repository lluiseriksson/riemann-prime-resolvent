import numpy as np
import pytest

from experiments.theta_pencil.finite_weyl_ratio import (
    audit_resolvent_shift,
    finite_weyl_function,
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
