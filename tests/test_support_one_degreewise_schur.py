from fractions import Fraction

from experiments.theta_pencil.rational_joint_five_seven_certificate import (
    certify_rational_support_one_tail,
)
from experiments.theta_pencil.support_one_degreewise_schur import (
    run_support_one_absolute_tail_budget,
    run_support_one_endpoint_jet_band_audit,
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


def test_absolute_tail_budget_keeps_its_scope_and_square_accounting():
    result = run_support_one_absolute_tail_budget(
        first_degree=64,
        jet_count=1,
        partitions=4,
        maximum_smooth_power=5,
    )
    assert result.denominator_floor > 0
    for parity in (result.even, result.odd):
        assert parity.total_weighted_norm > 0
        assert parity.correction_norm_upper == parity.total_weighted_norm**2
    assert "failure of this estimate" in result.context


def test_endpoint_jet_band_retains_the_algebraic_rank_bound():
    result = run_support_one_endpoint_jet_band_audit(
        first_degree=64,
        last_degree=80,
        jet_count=2,
    )
    for parity in (result.even, result.odd):
        assert parity.gram_rank <= parity.rank_bound == 2
        assert parity.signed_gram_norm > 0
        assert parity.separate_prime_gram_norm > 0
        assert parity.signed_to_separate_ratio > 0
    assert "rank <= jet_count is algebraic" in result.context
