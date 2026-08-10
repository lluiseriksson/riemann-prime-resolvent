import math

from experiments.theta_pencil.calibrated_parity_diagnostic import (
    run_calibrated_parity_diagnostic,
)


def test_calibrated_parity_diagnostic_predicts_an_uncalibrated_height():
    result = run_calibrated_parity_diagnostic(
        half_widths=(0.4,),
        imaginary_height=3.0,
        grid_points=513,
        basis_size=8,
        precision_bits=100,
    )
    assert result.kinematic_baseline == -3.0 * result.target_balance
    assert result.kinematic_baseline_error > 0.0
    assert result.target_schwarz_pick_excess == result.kinematic_baseline_error
    assert result.target_schwarz_pick_upper_slack > 0.0
    assert -1.0 < result.target_second_schur_parameter < 1.0
    row = result.rows[0]
    assert row.calibrated_shift < row.galerkin_ground_state
    assert row.gap_multiple > 0.0
    assert math.isfinite(row.predicted_parity_ratio)
    assert row.predicted_schwarz_pick_excess == (
        row.predicted_parity_ratio - result.kinematic_baseline
    )
    assert -1.0 < row.predicted_second_schur_parameter < 1.0
    assert row.target_error > 0.0
