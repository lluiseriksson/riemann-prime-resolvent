import pytest

from experiments.theta_pencil.legendre_tail_bound import (
    active_prime_weight,
    bounded_perturbation_norm,
    harmonic,
    required_legendre_tail,
)


def test_harmonic_values() -> None:
    assert harmonic(0) == 0.0
    assert harmonic(4) == pytest.approx(25.0 / 12.0)


def test_active_prime_weight_obeys_support() -> None:
    assert active_prime_weight(0.3) == 0.0
    assert active_prime_weight(0.4) == pytest.approx(0.49012907173427356)


def test_registered_tail_dimensions() -> None:
    assert required_legendre_tail(0.3)[0] == 11
    assert required_legendre_tail(0.4)[0] == 74
    assert required_legendre_tail(0.5)[0] == 168
    assert required_legendre_tail(0.4)[1] > 0.008


def test_tail_bound_rejects_unproved_window() -> None:
    with pytest.raises(ValueError):
        bounded_perturbation_norm(0.55)
