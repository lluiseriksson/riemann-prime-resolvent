from experiments.theta_pencil.arb_temple_certificate import certify_temple_trial


def test_small_arb_temple_pipeline_is_finite():
    result = certify_temple_trial(
        dimension=24,
        residual_end=128,
        variation_partitions=8,
        precision=384,
        prime_precision=1536,
    )
    assert result.rayleigh_lower > 0.0
    assert result.finite_residual_upper > 0.0
    assert result.total_residual_upper > 0.0
    # This deliberately small regression case is not expected to certify the
    # final positive Temple lower bound.
    assert result.temple_lower < result.rayleigh_lower

