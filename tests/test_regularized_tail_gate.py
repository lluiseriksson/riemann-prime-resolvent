from experiments.theta_pencil.regularized_tail_gate import (
    maximum_regularized_map_bound,
)


def test_degree_128_gate_has_large_certification_budget():
    even = maximum_regularized_map_bound(128, 0.007, 3.4905, 0.01)
    odd = maximum_regularized_map_bound(128, 0.06, 3.4905, 0.3)
    assert even > 2500
    assert odd > 7200
