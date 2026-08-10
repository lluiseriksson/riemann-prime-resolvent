import numpy as np
import pytest

from experiments.theta_pencil.parity_weyl_derivative import (
    imaginary_axis_parity_ratio_audit,
    parity_ratio_from_target_derivative,
    parity_weyl_derivative_audit,
)


def test_parity_sector_identity_for_a_reflection_symmetric_pencil():
    operator = np.array([[2.0, 0.4], [0.4, 2.0]])
    metric = np.eye(2)
    plus = np.array([3.0, 1.0])
    minus = plus[::-1].copy()
    audit = parity_weyl_derivative_audit(
        operator,
        metric,
        plus,
        minus,
        shift=-0.7,
    )
    assert abs(audit.parity_cross_mass) < 1.0e-15
    assert audit.parity_identity_residual < 1.0e-15
    expected = -(
        audit.even_resolvent_mass - audit.odd_resolvent_mass
    ) / (audit.even_resolvent_mass + audit.odd_resolvent_mass)
    assert audit.canonical_derivative == pytest.approx(expected)


def test_target_derivative_converts_to_the_riemann_balance():
    derivative = -0.9968019520324009
    assert parity_ratio_from_target_derivative(derivative) == pytest.approx(
        0.0016015849565571757
    )
    with pytest.raises(ValueError):
        parity_ratio_from_target_derivative(-1.0)


def test_imaginary_axis_ratio_is_a_real_even_odd_resolvent_quotient():
    a = 0.6
    eta = 2.3
    points = np.array([-a, a])
    operator = np.array([[2.0, 0.4], [0.4, 2.0]])
    plus = np.exp(points)
    minus = np.exp(-points)
    positive_observation = np.exp(eta * points)
    negative_observation = np.exp(-eta * points)
    audit = imaginary_axis_parity_ratio_audit(
        operator,
        np.eye(2),
        plus,
        minus,
        positive_observation,
        negative_observation,
        shift=-0.7,
    )
    assert abs(audit.even_cross_mass) < 1.0e-15
    assert abs(audit.odd_cross_mass) < 1.0e-15
    assert audit.parity_identity_residual < 1.0e-15
