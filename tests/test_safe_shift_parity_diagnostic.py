import math

from experiments.theta_pencil.safe_shift_parity_diagnostic import (
    run_safe_shift_parity_diagnostic,
)


def test_safe_shift_parity_diagnostic_reports_target_and_finite_row():
    result = run_safe_shift_parity_diagnostic(
        half_widths=(0.4,),
        imaginary_height=3.0,
        grid_points=513,
        basis_size=8,
        precision_bits=100,
    )
    assert -0.00473 < result.target_parity_ratio < -0.00471
    assert result.base_imaginary_value > 20.0
    assert len(result.rows) == 1
    row = result.rows[0]
    assert row.shift < row.galerkin_ground_state
    assert math.isfinite(row.target_error)
    assert row.target_error > 0.0
