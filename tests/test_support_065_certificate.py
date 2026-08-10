from types import SimpleNamespace

import experiments.theta_pencil.support_065_certificate as certificate


def test_support_065_activates_directional_self_tail(monkeypatch):
    fake = SimpleNamespace(
        even=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=3.4e-11,
            coercive_lower=4.3e-13,
        ),
        odd=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=1.8e-8,
            coercive_lower=2.2e-10,
        ),
    )
    calls = []

    def fake_schur(**kwargs):
        calls.append(kwargs)
        return fake

    monkeypatch.setattr(certificate, "certify_second_window_schur", fake_schur)
    result = certificate.certify_support_065()
    assert calls[0]["retain_self_tail"] is True
    assert calls[0]["maximum_smooth_power"] == 31
    assert result.global_coercive_lower == 4.3e-13
