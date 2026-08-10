from experiments.theta_pencil.support_0551_interval_certificate import (
    certify_support_0551_interval,
)


def test_support_0551_interval_stays_inside_two_prime_window():
    result = certify_support_0551_interval()
    assert result.neighborhood_lower > 0.5493
    assert result.neighborhood_upper < 0.6932
    assert result.certified_interval_lower > 2.6e-10
    assert result.certified_interval_lower < result.point_lower
    assert result.prime_coefficient_sum_upper > 1.12
    assert result.required_logarithm > 1e20
    assert result.decimal_radius_exponent > 10**19
