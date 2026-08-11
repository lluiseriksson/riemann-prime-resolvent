import math

from experiments.theta_pencil.gauss_stieltjes_schur_audit import (
    prime_translation_floor,
    support_one_complement_floor,
)


def test_support_one_path_floor_and_complement_margin():
    assert math.isclose(
        prime_translation_floor(1.0),
        3.1292522910020812,
        rel_tol=2e-15,
    )
    floor = support_one_complement_floor(256, 95)
    assert 0.1385 < floor < 0.1386
