import pytest

from experiments.theta_pencil.third_window_pointwise_floor import (
    certify_third_window_pointwise_floor,
)


def test_joint_prime_power_four_graph_has_positive_high_complement():
    pytest.importorskip("flint")
    result = certify_third_window_pointwise_floor(
        subdivisions=128, precision=384
    )
    assert len(result.component_lowers) == 3
    assert result.graph_lower > -0.58
    assert result.complement_floor > 0.59
    assert result.complement_floor < 0.63
