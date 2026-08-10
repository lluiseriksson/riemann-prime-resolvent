from experiments.theta_pencil.screw_weyl_shift_diagnostic import (
    run_screw_weyl_shift_diagnostic,
)


def test_screw_weyl_ratio_is_not_formally_shift_invariant():
    result = run_screw_weyl_shift_diagnostic(
        half_width=0.4,
        grid_points=513,
        basis_size=6,
        spectral_parameter=0.7 + 0.8j,
        shifts=(-1.0, -2.0),
    )
    assert result.relative_characteristic_spread > 5.0e-4
    assert result.maximum_resolvent_identity_residual < 1.0e-12
    assert result.maximum_parity_identity_residual < 1.0e-12
    assert result.maximum_mobius_cross_ratio_defect > 1.0e-6
