from fractions import Fraction

from experiments.theta_pencil.rational_joint_five_seven_certificate import (
    certify_rational_joint_five_seven_floor,
    certify_rational_support_one_tail,
)


def test_registered_rational_joint_certificate_closes():
    result = certify_rational_joint_five_seven_floor()
    assert result.certified_floor == Fraction(-263, 1000)
    assert all(value > 0 for value in result.four_path_minor_lowers)
    assert all(value > 0 for value in result.two_path_minor_lowers)
    assert float(result.four_path_minor_lowers[-1]) > 0.0004


def test_rational_log_boxes_are_positive_and_narrow():
    result = certify_rational_joint_five_seven_floor()
    assert 0 < result.log_five_lower < result.log_five_upper
    assert 0 < result.log_seven_lower < result.log_seven_upper
    assert result.log_five_upper - result.log_five_lower < Fraction(1, 10**30)
    assert result.log_seven_upper - result.log_seven_lower < Fraction(1, 10**20)


def test_rational_support_one_tail_starts_at_degree_58():
    result = certify_rational_support_one_tail()
    assert result.local_degree == 58
    assert result.complement_margin > Fraction(46, 10_000)
    assert result.preceding_margin < 0
