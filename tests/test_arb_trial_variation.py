import numpy as np

from experiments.theta_pencil.arb_trial_variation import (
    certify_active_prime_operator_remainder_variation,
    certify_active_prime_remainder_variation,
    certify_prime_operator_remainder_variation,
    certify_prime_operator_remainder_variation_for_prime,
    certify_prime_remainder_variation,
    certify_prime_remainder_variation_for_prime,
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


def test_generic_prime_two_variation_matches_legacy_wrapper():
    coefficients = np.zeros(12)
    coefficients[::2] = np.linspace(0.1, 0.6, 6)
    legacy = certify_prime_remainder_variation(
        0.4, coefficients, partitions=8, precision=384
    )
    generic = certify_prime_remainder_variation_for_prime(
        0.4, 2, coefficients, partitions=8, precision=384
    )
    assert generic == legacy


def test_active_variation_dominates_each_prime_and_their_sum():
    coefficients = np.zeros(12)
    coefficients[1::2] = np.linspace(0.1, 0.6, 6)
    individual = [
        certify_prime_remainder_variation_for_prime(
            0.62, prime, coefficients, partitions=8, precision=384
        )
        for prime in (2, 3)
    ]
    active = certify_active_prime_remainder_variation(
        0.62, coefficients, (2, 3), partitions=8, precision=384
    )
    assert active.upper >= sum(bound.upper for bound in individual)


def test_second_order_prime_three_variation_dominates_direct_quadrature():
    coefficients = np.zeros(12)
    coefficients[::2] = np.linspace(0.1, 0.6, 6)
    certified = certify_prime_remainder_variation_for_prime(
        0.62,
        3,
        coefficients,
        partitions=8,
        precision=384,
        derivative_order=2,
    )
    direct = _prime_remainder_variation(
        0.62,
        coefficients,
        quadrature_order=256,
        prime_power=3,
        derivative_order=2,
    )
    assert certified.upper >= direct
    assert certified.upper < 3.0 * direct


def test_active_operator_variation_dominates_prime_two_and_three_sum():
    degrees = np.arange(1, 12, 2)
    individual = [
        certify_prime_operator_remainder_variation_for_prime(
            0.62, prime, degrees, 3, 8, 384
        )
        for prime in (2, 3)
    ]
    active = certify_active_prime_operator_remainder_variation(
        0.62, degrees, (2, 3), 3, 8, 384
    )
    assert active.upper >= sum(bound.upper for bound in individual)
