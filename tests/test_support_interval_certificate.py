from fractions import Fraction

from experiments.theta_pencil.smooth_legendre_series import (
    smooth_remainder_series_coefficients,
)
from experiments.theta_pencil.support_interval_certificate import (
    _smooth_series_supremum,
    certify_support_054_interval,
)


def test_smooth_supremum_majorants_dominate_retained_series():
    argument = Fraction(109, 100)
    coefficients = smooth_remainder_series_coefficients(23)
    retained = sum(
        (abs(value) * argument**power for power, value in enumerate(coefficients)),
        Fraction(0),
    )
    retained_radial = sum(
        (
            (power + 1) * abs(value) * argument**power
            for power, value in enumerate(coefficients)
        ),
        Fraction(0),
    )
    assert _smooth_series_supremum(1.09, radial_derivative=False) > float(
        retained
    )
    assert _smooth_series_supremum(1.09, radial_derivative=True) > float(
        retained_radial
    )


def test_support_054_interval_certificate_has_strict_margin():
    result = certify_support_054_interval()
    assert result.certified_interval_lower > 1.4e-9
    assert result.certified_interval_lower < result.point_lower
    assert result.relative_eta > 0
    assert result.required_logarithm > 1e18
    assert result.decimal_radius_exponent > 1_000_000_000_000_000_000
    assert result.neighborhood_upper < 0.55
