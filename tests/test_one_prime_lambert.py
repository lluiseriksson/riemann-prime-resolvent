import math

import pytest

from experiments.theta_pencil.one_prime_lambert import (
    alpha,
    lambert_moment_correction,
    sigma_direct,
    sigma_lambert,
)


def test_alpha_matches_closed_form() -> None:
    for ell in range(12):
        expected = (-4.0) ** (-ell) * math.comb(2 * ell, ell)
        assert alpha(ell) == pytest.approx(expected, rel=0.0, abs=1e-16)


@pytest.mark.parametrize("p", [2, 3, 5])
@pytest.mark.parametrize("t", [-0.25, 0.0, 0.25, 0.75])
def test_lambert_expansion_matches_power_sum(p: int, t: float) -> None:
    direct = sigma_direct(p, t, terms=120)
    expanded = sigma_lambert(p, t, terms=120)
    assert expanded == pytest.approx(direct, rel=2e-14, abs=2e-15)


def test_prime_two_moment_corrections_are_stable() -> None:
    for k in range(4):
        coarse = lambert_moment_correction(2, k, terms=60)
        fine = lambert_moment_correction(2, k, terms=120)
        assert fine == pytest.approx(coarse, rel=2e-14, abs=2e-14)


@pytest.mark.parametrize("function", [sigma_direct, sigma_lambert])
def test_rejects_invalid_prime(function) -> None:
    with pytest.raises(ValueError):
        function(1, 0.0)
