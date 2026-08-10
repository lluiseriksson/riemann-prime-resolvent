import numpy as np

from experiments.theta_pencil.arb_prime_jet_correction import (
    build_arb_active_prime_jet_correction,
    build_arb_prime_jet_correction,
)
from experiments.theta_pencil.legendre_tail_bound import bounded_perturbation_norm
from experiments.theta_pencil.prime_jet_tail import (
    endpoint_jet_matrix,
    prime_jet_weighted_correction,
    truncated_power_coefficients,
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


def test_combined_prime_correction_retains_cross_terms():
    half_width = 0.62
    low = np.arange(1, 8, 2)
    first = 20
    last = 80
    jets = 3
    loss = 1.0
    shift = 0.005
    exact = build_arb_active_prime_jet_correction(
        half_width,
        (2, 3),
        low,
        first,
        last,
        jets,
        shift,
        256,
        perturbation_loss=loss,
    )
    high = np.arange(first + ((first - low[0]) % 2), last, 2)
    endpoint = endpoint_jet_matrix(low, jets)
    cross = np.zeros((len(low), len(high)))
    for prime in (2, 3):
        cut = 1.0 - np.log(prime) / half_width
        powers = truncated_power_coefficients(cut, last, jets)
        cross += (
            -2.0
            * np.log(prime)
            / np.sqrt(prime)
            * endpoint
            @ powers[:, high]
        )
    harmonic = np.array([sum(1.0 / k for k in range(1, n + 1)) for n in high])
    floating = (cross / (harmonic - loss - shift)) @ cross.T
    assert np.max(exact.radius) < 1.0e-50
    assert np.max(np.abs(exact.midpoint - floating)) < 2.0e-13
