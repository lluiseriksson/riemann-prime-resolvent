from fractions import Fraction

import numpy as np

from experiments.theta_pencil.rational_joint_five_seven_certificate import (
    certify_rational_support_one_tail,
)
from experiments.theta_pencil.support_one_degreewise_schur import (
    _build_rectangular_support_one_blocks,
    _build_high_component,
    _smooth_high_component_labels,
    run_support_one_absolute_tail_budget,
    run_support_one_endpoint_jet_band_audit,
    run_support_one_finite_schur_audit,
    schur_residual_lower_matrix,
    support_one_bounded_part_lower,
    support_one_degreewise_denominator_lowers,
)
from experiments.theta_pencil.legendre_feshbach import build_legendre_weil_components
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_kernel_series_matrix,
)


def test_degreewise_denominators_start_at_registered_tail_margin():
    certificate = certify_rational_support_one_tail()
    denominators = support_one_degreewise_denominator_lowers(64)
    assert denominators[0] == certificate.complement_margin
    assert all(
        right > left for left, right in zip(denominators[:-1], denominators[1:])
    )
    assert denominators[1] - denominators[0] == Fraction(1, 59)


def test_bounded_part_recovers_preceding_margin():
    certificate = certify_rational_support_one_tail()
    beta = support_one_bounded_part_lower()
    harmonic_57 = certificate.harmonic_floor - Fraction(1, 58)
    assert harmonic_57 + beta == certificate.preceding_margin


def test_absolute_tail_budget_keeps_its_scope_and_square_accounting():
    result = run_support_one_absolute_tail_budget(
        first_degree=64,
        jet_count=1,
        partitions=4,
        maximum_smooth_power=5,
    )
    assert result.denominator_floor > 0
    for parity in (result.even, result.odd):
        assert parity.total_weighted_norm > 0
        assert parity.correction_norm_upper == parity.total_weighted_norm**2
    assert "failure of this estimate" in result.context


def test_endpoint_jet_band_retains_the_algebraic_rank_bound():
    result = run_support_one_endpoint_jet_band_audit(
        first_degree=64,
        last_degree=80,
        jet_count=2,
    )
    for parity in (result.even, result.odd):
        assert parity.gram_rank <= parity.rank_bound == 2
        assert parity.signed_gram_norm > 0
        assert parity.separate_prime_gram_norm > 0
        assert parity.signed_to_separate_ratio > 0
    assert "rank <= jet_count is algebraic" in result.context


def test_rectangular_builder_matches_the_full_point_components():
    source, cross = _build_rectangular_support_one_blocks(4, 12, 64, 5)
    components = build_legendre_weil_components(1.0, 12, 64)
    target = (
        components.dominant
        + components.scalar
        + components.prime
        + smooth_kernel_series_matrix(1.0, 12, 5)
    )
    assert abs(source - target[:4, :4]).max() < 1.0e-12
    assert abs(cross - target[:4, 4:]).max() < 1.0e-12
    high = sum(
        (
            _build_high_component(label, 4, 12, 64, 5)
            for label in (
                "base",
                "2",
                "3",
                "4",
                "5",
                "7",
                *_smooth_high_component_labels(5),
            )
        ),
        np.zeros((8, 8)),
    )
    assert abs(high - target[4:, 4:]).max() < 1.0e-12


def test_small_full_high_block_schur_pipeline_keeps_scope_explicit():
    result = run_support_one_finite_schur_audit(
        source_dimension=4,
        finite_dimension=12,
        quadrature_order=64,
        maximum_smooth_power=5,
    )
    assert result.tail_least_eigenvalue > 0
    assert result.even.dimension == result.odd.dimension == 2
    assert "infinite cross tail" in result.context


def test_residual_schur_matrix_is_below_the_exact_complement():
    source = np.array([[3.0, 0.2], [0.2, 2.0]])
    cross = np.array([[0.4, -0.1], [0.3, 0.2]])
    high = np.array([[2.0, 0.1], [0.1, 1.5]])
    trial = np.array([[0.1, 0.05], [-0.02, 0.08]])
    floor = float(np.linalg.eigvalsh(high)[0])
    lower, residual = schur_residual_lower_matrix(
        source, cross, high, trial, floor
    )
    exact = source - cross @ np.linalg.solve(high, cross.T)
    assert np.linalg.eigvalsh(exact - lower)[0] > -1.0e-14
    assert np.linalg.norm(residual) > 0
