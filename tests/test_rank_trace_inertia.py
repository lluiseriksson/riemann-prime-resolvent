from fractions import Fraction

import numpy as np

from experiments.theta_pencil.rank_trace_inertia import (
    audit_floating_symmetric_matrix,
    combine_block_audits,
    positive_inertia_from_moments,
    rank_trace_lower_bound,
    support_one_finite_schur_audit,
    support_one_source_audit,
)


def test_rank_trace_bound_is_exact_on_one_online_atom():
    result = rank_trace_lower_bound(1, 0, 0, 1)
    assert result.continuous_lower == 1
    assert result.forced_integer_lower == 1


def test_positive_inertia_moment_bound_forces_two_directions():
    result = positive_inertia_from_moments(3, 5)
    assert result.continuous_lower == Fraction(9, 5)
    assert result.forced_integer_lower == 2


def test_nonpositive_trace_does_not_force_a_positive_direction():
    result = positive_inertia_from_moments(-1, 7)
    assert result.forced_integer_lower == 0


def test_floating_audit_distinguishes_moment_bound_from_full_inertia():
    result = audit_floating_symmetric_matrix(np.diag([-1.0, 2.0, 3.0]))
    assert result.moment_forced_positive_count == 2
    assert result.observed_negative_count == 1
    assert result.observed_positive_count == 2
    assert result.observed_unresolved_count == 0


def test_direct_sum_recomputes_the_joint_moment_bound():
    left = audit_floating_symmetric_matrix(np.diag([1.0, 2.0]))
    right = audit_floating_symmetric_matrix(np.diag([-1.0, 3.0]))
    combined = combine_block_audits(left, right)
    assert combined.dimension == 4
    assert combined.trace == 5.0
    assert combined.frobenius_squared == 15.0
    assert combined.moment_forced_positive_count == 2
    assert combined.observed_positive_count == 3


def test_support_one_source_audit_keeps_both_parities():
    even, odd = support_one_source_audit(8, 64)
    assert even.dimension == 4
    assert odd.dimension == 4
    assert even.moment_forced_positive_count <= even.dimension
    assert odd.moment_forced_positive_count <= odd.dimension


def test_support_one_finite_schur_audit_keeps_scope_explicit():
    result = support_one_finite_schur_audit(8, 16, 64)
    assert result.source_dimension == 8
    assert result.finite_dimension == 16
    assert result.tail_least_eigenvalue > 0.0
    assert result.combined.dimension == 8
    assert "infinite cross tail is omitted" in result.context
