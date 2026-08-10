from types import SimpleNamespace

import experiments.theta_pencil.support_06_certificate as certificate


def test_support_06_requires_both_parities(monkeypatch):
    fake = SimpleNamespace(
        even=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=2.0e-10,
            coercive_lower=4.8e-12,
        ),
        odd=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=5.9e-7,
            coercive_lower=1.3e-8,
        ),
    )
    monkeypatch.setattr(
        certificate, "certify_second_window_schur", lambda **kwargs: fake
    )
    result = certificate.certify_support_06()
    assert result.global_coercive_lower == 4.8e-12
    assert result.monotone_support_upper == 0.6
