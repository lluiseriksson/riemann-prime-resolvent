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
