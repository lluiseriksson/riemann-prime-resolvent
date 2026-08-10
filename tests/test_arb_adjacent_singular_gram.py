import numpy as np
import pytest

from experiments.theta_pencil.arb_adjacent_singular_gram import (
    build_arb_adjacent_singular_gram,
)
from experiments.theta_pencil.arb_second_green_tail import (
    certify_second_green_adjacent_tail,
)


def test_signed_adjacent_gram_matches_scalar_weighted_audit():
    pytest.importorskip("flint")
    result = build_arb_adjacent_singular_gram(
        0.7,
        0.2,
        degree_count=3,
        first_degree=8,
        last_degree=32,
        moment_order=3,
        precision=256,
    )
    scalar = certify_second_green_adjacent_tail(
        0.7,
        0.2,
        degree_count=3,
        first_degree=8,
        derivative_order=3,
        explicit_end=32,
        subdivisions=16,
        precision=256,
        moment_order=3,
    )
    assert np.max(np.abs(result.midpoint - result.midpoint.T)) < 1e-15
    assert np.linalg.eigvalsh(result.midpoint)[0] > -1e-14
    assert result.total_frobenius_upper == pytest.approx(
        scalar.weighted_singular_frobenius_upper, rel=2e-15
    )
    assert result.remainder_norm_upper > 0
