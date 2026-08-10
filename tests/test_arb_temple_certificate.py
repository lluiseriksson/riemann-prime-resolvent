import numpy as np
import pytest

from experiments.theta_pencil.arb_prime_translation import ArbPrimeAction
from experiments.theta_pencil.arb_temple_certificate import (
    _minimum_prime_precision,
    _trial_build_residual_end,
    certify_temple_trial,
)


def test_long_tail_does_not_expand_auxiliary_dense_quadrature():
    assert _trial_build_residual_end(512, 131072) == 8192
    assert _trial_build_residual_end(24, 128) == 128


def test_prime_precision_preflight_scales_with_jet_growth():
    assert _minimum_prime_precision(24, 128) == 1264
    assert _minimum_prime_precision(256, 16384) == 5120
    assert _minimum_prime_precision(512, 131072) == 10240


def test_cached_prime_action_is_validated_before_use():
    malformed = ArbPrimeAction(
        midpoint=np.zeros(127), radius=np.zeros(127), precision=1536
    )
    with pytest.raises(ValueError, match="wrong degree cutoff"):
        certify_temple_trial(
            dimension=24,
            residual_end=128,
            variation_partitions=8,
            precision=384,
            prime_precision=1536,
            prime_action=malformed,
        )


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
