from experiments.theta_pencil.safe_shift_signal_diagnostic import (
    safe_shift_signal_row,
)


def test_first_coefficient_splits_over_operator_components():
    row = safe_shift_signal_row(0.4, grid_points=1025, basis_size=10)
    assert row.coefficient_additivity_residual < 1.0e-11
    assert row.prime_first_coefficient_abs > 0.0
    assert 0.0 <= row.component_cancellation_ratio <= 1.0
    assert row.scaled_total_signal_abs <= (
        row.total_first_coefficient_abs / abs(row.shift)
    ) * (1.0 + 1.0e-15)
    assert row.first_approximation_error >= 0.0
    assert row.second_approximation_error < row.first_approximation_error
