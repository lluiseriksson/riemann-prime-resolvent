import numpy as np

from experiments.theta_pencil.arb_trial_variation import (
    certify_prime_operator_remainder_variation,
    certify_prime_remainder_variation,
)
from experiments.theta_pencil.prime_jet_tail import (
    piecewise_prime_remainder_variation_bound,
)
from experiments.theta_pencil.temple_trial_budget import (
    _prime_remainder_variation,
    run_temple_trial_audit,
)


def test_piecewise_arb_variation_dominates_direct_quadrature():
    audit = run_temple_trial_audit(trial_dimension=24, residual_end=128)
    coefficients = audit.coefficients.copy()
    coefficients[1::2] = 0.0
    certified = certify_prime_remainder_variation(
        0.4, coefficients, partitions=8, precision=384
    )
    direct = _prime_remainder_variation(0.4, coefficients, quadrature_order=256)
    assert certified.upper >= direct
    assert certified.upper < 3.0 * direct
    assert certified.radius < 1.0e-80


def test_operator_variation_is_a_finite_positive_bound():
    degrees = np.arange(1, 20, 2)
    certified = certify_prime_operator_remainder_variation(
        0.4, degrees, derivative_order=3, partitions=8, precision=384
    )
    direct = piecewise_prime_remainder_variation_bound(
        0.4, degrees, derivative_order=3, partitions=8
    )
    assert certified.upper > 0.0
    assert certified.upper < 2.0 * direct
