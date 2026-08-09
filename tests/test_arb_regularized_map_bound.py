import pytest

from experiments.theta_pencil.arb_regularized_map_bound import (
    certify_regularized_map_bound,
)


def test_regularized_map_bound_passes_degree_128_gate():
    pytest.importorskip("flint")
    result = certify_regularized_map_bound(16, 192)
    assert result.local_d_a2_upper < 797
    assert result.local_vd_frobenius_upper < 506
    assert result.local_polynomial_frobenius_upper < 246
    assert result.derivative_upper < 87
    assert result.adjacent_upper < 697
    assert result.distant_upper < 1
    assert result.global_upper < 2537
    assert result.global_upper < result.even_gate
