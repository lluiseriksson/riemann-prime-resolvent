import numpy as np

from experiments.theta_pencil.arb_prime_jet_correction import (
    build_arb_prime_jet_correction,
)
from experiments.theta_pencil.legendre_tail_bound import bounded_perturbation_norm
from experiments.theta_pencil.prime_jet_tail import (
    prime_jet_weighted_correction,
)


def test_streaming_arb_jet_correction_matches_array_recurrence():
    low = np.arange(1, 12, 2)
    exact = build_arb_prime_jet_correction(
        0.4, low, 100, 260, 4, precision=160
    )
    floating = prime_jet_weighted_correction(
        0.4,
        low,
        100,
        260,
        4,
        bounded_perturbation_norm(0.4),
        0.005,
    )
    assert np.max(exact.radius) < 1.0e-35
    assert np.max(np.abs(exact.midpoint - floating)) < 2.0e-14


def test_high_jet_recurrence_remains_accurate_at_large_degree():
    low = np.arange(1, 12, 2)
    exact = build_arb_prime_jet_correction(
        0.4, low, 4096, 10_000, 6, precision=160
    )
    floating = prime_jet_weighted_correction(
        0.4,
        low,
        4096,
        10_000,
        6,
        bounded_perturbation_norm(0.4),
        0.005,
    )
    assert np.max(np.abs(exact.midpoint - floating)) < 2.0e-14
