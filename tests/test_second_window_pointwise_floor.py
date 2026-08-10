import pytest

from experiments.theta_pencil.second_window_pointwise_floor import (
    certify_second_window_pointwise_floor,
)


def test_joint_two_prime_graph_improves_the_0675_complement():
    pytest.importorskip("flint")
    result = certify_second_window_pointwise_floor(
        0.675, subdivisions=128, precision=384
    )
    assert result.edge_graph_lower > -0.54
    assert result.bridge_graph_lower > result.edge_graph_lower
    assert result.complement_floor > 0.68
    assert result.complement_floor < 0.71
