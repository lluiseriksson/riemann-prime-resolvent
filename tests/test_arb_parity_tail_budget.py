from experiments.theta_pencil.arb_parity_tail_budget import (
    certify_parity_tail_budget,
)


def test_small_parity_tail_budget_is_positive_and_finite():
    result = certify_parity_tail_budget(
        1,
        low_dimension=20,
        finite_dimension=128,
        smooth_dimension=96,
        jet_count=3,
        jet_end=1000,
        partitions=8,
        precision=384,
        jet_correction_norm_upper=0.1,
    )
    assert result.omitted_weighted_upper > 0.0
    assert result.correction_upper > result.omitted_weighted_upper**2


def test_second_window_tail_budget_includes_both_prime_cuts():
    result = certify_parity_tail_budget(
        0,
        half_width=0.62,
        low_dimension=12,
        finite_dimension=4096,
        smooth_dimension=4096,
        jet_count=3,
        jet_end=10_000,
        partitions=8,
        precision=384,
        jet_correction_norm_upper=0.1,
        active_primes=(2, 3),
    )
    assert result.active_primes == (2, 3)
    assert result.omitted_weighted_upper > 0.0
    assert result.correction_upper > result.omitted_weighted_upper**2
