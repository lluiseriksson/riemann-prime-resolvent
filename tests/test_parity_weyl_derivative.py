import numpy as np
import pytest

from experiments.theta_pencil.parity_weyl_derivative import (
    imaginary_axis_parity_ratio_audit,
    parity_ratio_from_target_derivative,
    parity_weyl_derivative_audit,
    schwarz_pick_excess_from_second_schur_parameter,
    schwarz_pick_extremal_weyl,
    schwarz_pick_parity_interval,
    second_schur_parameter_from_parity_ratio,
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


def test_schwarz_pick_interval_has_the_exact_eta_kappa_endpoints():
    derivative = -0.9968019520324009
    kappa = parity_ratio_from_target_derivative(derivative)
    lower, upper = schwarz_pick_parity_interval(derivative, 3.0)
    assert lower == pytest.approx(-3.0 * kappa)
    assert upper == pytest.approx(-kappa / 3.0)
    assert lower < -0.0047202431666865455 < upper
    assert schwarz_pick_parity_interval(derivative, 1.0) == pytest.approx(
        (-kappa, -kappa)
    )
    with pytest.raises(ValueError):
        schwarz_pick_parity_interval(derivative, 0.9)


def test_second_schur_parameter_exactly_reconstructs_the_parity_excess():
    derivative = -0.9968019520324009
    eta = 3.0
    target_ratio = -0.0047202431666865455
    lower, _ = schwarz_pick_parity_interval(derivative, eta)
    q_value = second_schur_parameter_from_parity_ratio(
        derivative, eta, target_ratio
    )
    assert q_value == pytest.approx(0.9866317619939311)
    excess = schwarz_pick_excess_from_second_schur_parameter(
        derivative, eta, q_value
    )
    assert excess == pytest.approx(target_ratio - lower)
    assert second_schur_parameter_from_parity_ratio(
        derivative, eta, lower
    ) == pytest.approx(1.0)


def test_second_schur_coordinate_rejects_the_basepoint():
    with pytest.raises(ValueError):
        second_schur_parameter_from_parity_ratio(-0.5, 1.0, -1.0 / 3.0)


def test_extremal_weyl_is_the_calibrated_parity_endpoint_mixture():
    derivative = -0.9968019520324009
    kappa = parity_ratio_from_target_derivative(derivative)
    assert schwarz_pick_extremal_weyl(derivative, 1j) == pytest.approx(1j)
    step = 1.0e-6
    numerical_derivative = (
        schwarz_pick_extremal_weyl(derivative, 1j + step)
        - schwarz_pick_extremal_weyl(derivative, 1j - step)
    ) / (2.0 * step)
    assert numerical_derivative == pytest.approx(derivative)
    for eta in (1.5, 3.0, 10.0):
        value = schwarz_pick_extremal_weyl(derivative, 1j * eta)
        ratio = (1.0 + 1j * eta * value) / (
            1j * (value - 1j * eta)
        )
        assert ratio == pytest.approx(-eta * kappa)
