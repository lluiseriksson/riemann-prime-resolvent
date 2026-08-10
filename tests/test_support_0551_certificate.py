from types import SimpleNamespace

import experiments.theta_pencil.support_0551_certificate as certificate


def test_support_0551_requires_both_zero_shift_inertias(monkeypatch):
    fake = SimpleNamespace(
        even=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=4.4e-8,
        ),
        odd=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=1.3e-5,
        ),
    )
    calls = []

    def fake_schur(**kwargs):
        calls.append(kwargs)
        return fake

    monkeypatch.setattr(certificate, "certify_second_window_schur", fake_schur)
    result = certificate.certify_support_0551()
    assert calls == [
        {
            "half_width": 0.551,
            "even_shift": 0.0,
            "odd_shift": 0.0,
            "expected_negative_count": 0,
        }
    ]
    assert result.even_schur_lower == 4.4e-8
    assert result.odd_schur_lower == 1.3e-5
