import numpy as np

from experiments.theta_pencil.arb_source_schur import certify_source_schur_box
from experiments.theta_pencil.parity_inertia_budget import run_parity_inertia_audit


def test_small_source_schur_is_enclosed():
    audit = run_parity_inertia_audit(
        1,
        low_dimension=80,
        finite_dimension=100,
        smooth_dimension=90,
        jet_count=3,
        jet_end=300,
        partitions=8,
    )
    source = certify_source_schur_box(
        1,
        audit.jet_schur_matrix,
        low_dimension=80,
        finite_dimension=100,
        smooth_dimension=90,
        jet_count=3,
        jet_end=300,
        target_radius=1.0e-8,
        precision=192,
        prime_precision=2048,
    )
    assert source.contained_in_target_box
    assert source.maximum_target_distance < 3.0e-10


def test_small_second_window_source_executes_combined_prime_schur():
    source = certify_source_schur_box(
        0,
        np.zeros((4, 4)),
        half_width=0.62,
        low_dimension=8,
        finite_dimension=32,
        smooth_dimension=16,
        spectral_shift=0.001,
        jet_count=3,
        jet_end=80,
        target_radius=1.0e9,
        precision=192,
        prime_precision=512,
        active_primes=(2, 3),
        perturbation_loss=1.0,
    )
    assert source.active_primes == (2, 3)
    assert np.all(np.isfinite(source.midpoint))
    assert np.all(np.isfinite(source.radius))
