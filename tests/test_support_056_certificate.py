from types import SimpleNamespace

import experiments.theta_pencil.support_056_certificate as certificate


def test_support_056_requires_two_positive_parity_bounds(monkeypatch):
    fake = SimpleNamespace(
        even=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=2.6e-8,
            coercive_lower=8.2e-10,
        ),
        odd=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=7.9e-6,
            coercive_lower=2.4e-7,
        ),
    )
    monkeypatch.setattr(
        certificate, "certify_second_window_schur", lambda **kwargs: fake
    )
    result = certificate.certify_support_056()
    assert result.global_coercive_lower == 8.2e-10


def test_support_056_interval_is_strictly_positive():
    from experiments.theta_pencil.support_056_interval_certificate import (
        certify_support_056_interval,
    )

    result = certify_support_056_interval()
    assert result.center == 0.56
    assert result.certified_interval_lower > 1.65e-10
    assert result.decimal_radius_exponent > 10**20
