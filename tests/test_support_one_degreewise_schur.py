from fractions import Fraction

from experiments.theta_pencil.rational_joint_five_seven_certificate import (
    certify_rational_support_one_tail,
)
from experiments.theta_pencil.support_one_degreewise_schur import (
    support_one_bounded_part_lower,
    support_one_degreewise_denominator_lowers,
)


def test_degreewise_denominators_start_at_registered_tail_margin():
    certificate = certify_rational_support_one_tail()
    denominators = support_one_degreewise_denominator_lowers(64)
    assert denominators[0] == certificate.complement_margin
    assert all(
        right > left for left, right in zip(denominators[:-1], denominators[1:])
    )
    assert denominators[1] - denominators[0] == Fraction(1, 59)


def test_bounded_part_recovers_preceding_margin():
    certificate = certify_rational_support_one_tail()
    beta = support_one_bounded_part_lower()
    harmonic_57 = certificate.harmonic_floor - Fraction(1, 58)
    assert harmonic_57 + beta == certificate.preceding_margin
