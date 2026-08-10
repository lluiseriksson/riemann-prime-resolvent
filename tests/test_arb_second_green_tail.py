import pytest

from experiments.theta_pencil.arb_second_green_tail import (
    _source_decomposition,
    certify_first_window_second_green_tails,
    certify_second_green_adjacent_tail,
)


def test_polynomial_division_identity_for_source_monomials():
    flint = pytest.importorskip("flint")
    arb = flint.arb
    source = [arb(2), arb(-3), arb(5)]
    polynomial, reflected = _source_decomposition(source, arb(7) / 5, arb)
    for numerator, denominator in ((1, 4), (2, 3), (5, 7)):
        u = arb(numerator) / denominator
        integrals = [((u + arb(7) / 5) / u).log()]
        for power in range(1, len(source)):
            integrals.append((arb(7) / 5) ** power / power - u * integrals[-1])
        direct = sum(
            (coefficient * integral for coefficient, integral in zip(source, integrals)),
            arb(0),
        )
        reconstructed = sum(
            (coefficient * u**power for power, coefficient in enumerate(polynomial)),
            arb(0),
        ) + sum(
            (coefficient * u**power for power, coefficient in enumerate(reflected)),
            arb(0),
        ) * ((u + arb(7) / 5).log() - u.log())
        assert (direct - reconstructed).contains(0)


def test_second_green_tail_is_small_on_a_tiny_block():
    pytest.importorskip("flint")
    result = certify_second_green_adjacent_tail(
        0.7,
        0.6,
        degree_count=3,
        first_degree=16,
        derivative_order=3,
        explicit_end=64,
        subdivisions=16,
        precision=192,
    )
    assert result.singular_frobenius_upper < 2
    assert result.analytic_frobenius_upper < 1
    assert result.total_upper < 3


def test_first_window_wrapper_keeps_exact_logarithmic_geometry():
    pytest.importorskip("flint")
    result = certify_first_window_second_green_tails(
        0.54,
        degree_count=3,
        first_degree=16,
        derivative_order=3,
        explicit_end=64,
        subdivisions=16,
        precision=192,
        moment_order=3,
    )
    assert result.edge_to_center.target_length > result.center_to_edge.target_length
    assert result.maximum_adjacent_upper == max(
        result.edge_to_center.total_upper,
        result.center_to_edge.total_upper,
    )
