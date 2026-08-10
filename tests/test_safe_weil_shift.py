import math

import pytest
from scipy.linalg import eigh

from experiments.theta_pencil.safe_weil_shift import (
    archimedean_multiplier_floor,
    explicit_safe_shift,
    inverse_mobius_error_scale,
    localized_weil_lower_bound,
    prime_weight_upper_bound,
)
from experiments.theta_pencil.screw_weil_operator import build_screw_weil_matrix


def test_archimedean_floor_matches_digamma_value():
    scipy = pytest.importorskip("scipy.special")
    assert archimedean_multiplier_floor() == pytest.approx(
        float(scipy.digamma(0.25) - math.log(math.pi))
    )


def test_elementary_prime_weight_bound_covers_direct_small_sum():
    half_width = 0.72
    direct = (
        math.log(2.0) / math.sqrt(2.0)
        + math.log(3.0) / math.sqrt(3.0)
        + math.log(2.0) / 2.0
    )
    assert prime_weight_upper_bound(half_width) >= direct


def test_chebyshev_branch_removes_the_support_factor():
    for half_width in (8.0, 12.0, 16.0):
        bound = prime_weight_upper_bound(half_width)
        assert bound == pytest.approx(
            8.0 * math.log(2.0) * math.exp(half_width)
        )


def test_safe_shift_lies_below_galerkin_spectrum():
    half_width = 0.72
    gram, weil, _, _ = build_screw_weil_matrix(
        half_width=half_width,
        grid_points=1025,
        basis_size=10,
        basis_family="dirichlet",
    )
    ground = float(eigh(weil, gram, eigvals_only=True)[0])
    assert explicit_safe_shift(half_width) < localized_weil_lower_bound(half_width)
    assert explicit_safe_shift(half_width) < ground


def test_inverse_mobius_scale_has_expected_large_support_asymptotic():
    coefficient = 2.0 + 16.0 * math.log(2.0)
    values = [
        inverse_mobius_error_scale(half_width)
        * coefficient**2
        * math.exp(2.0 * half_width)
        for half_width in (8.0, 12.0, 16.0)
    ]
    assert values[-1] == pytest.approx(1.0, rel=2.0e-5)
    errors = [abs(value - 1.0) for value in values]
    assert errors[0] > errors[1] > errors[2]
