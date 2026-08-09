from experiments.theta_pencil.local_metric_obstruction import (
    local_metric_potential,
    theta_density_jet,
)


def test_theta_density_is_even_to_machine_precision() -> None:
    for x in (0.0, 0.25, 0.75, 1.25):
        positive = theta_density_jet(x)
        negative = theta_density_jet(-x)
        assert positive[0] == negative[0]
        assert positive[1] == -negative[1]
        assert positive[2] == negative[2]


def test_local_metric_potential_is_not_constant() -> None:
    values = [local_metric_potential(x) for x in (0.0, 0.5, 1.0, 1.5)]
    assert max(values) - min(values) > 100.0
