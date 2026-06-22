import math


def elementary_tail_bound(delta: float, cutoff: float) -> float:
    return cutoff ** (-delta) * (math.log(cutoff) / delta + 1 / delta**2) / (1 + 2 * delta)


def test_tail_bound_positive_and_decreasing_in_examples():
    delta = 0.5
    values = [elementary_tail_bound(delta, x) for x in (100, 1000, 10000)]
    assert all(v > 0 for v in values)
    assert values[0] > values[1] > values[2]


def test_error_budget_triangle():
    spectral, model, prime, target = 1.2, 1.1, 0.9, 0.8
    assert abs(spectral - target) <= (
        abs(spectral - model) + abs(model - prime) + abs(prime - target) + 1e-15
    )
