from types import SimpleNamespace

import experiments.theta_pencil.support_0675_certificate as certificate


def test_support_0675_uses_joint_floor_and_registered_balance(monkeypatch):
    fake = SimpleNamespace(
        even=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=3.3e-12,
            coercive_lower=1.5e-13,
        ),
        odd=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=2.4e-9,
            coercive_lower=1.1e-10,
        ),
    )
    calls = []

    def fake_schur(**kwargs):
        calls.append(kwargs)
        return fake

    monkeypatch.setattr(certificate, "certify_second_window_schur", fake_schur)
    result = certificate.certify_support_0675("components.npz")
    assert calls[0]["joint_pointwise_floor"] is True
    assert calls[0]["tail_balance"] == 0.05
    assert calls[0]["component_cache_path"] == "components.npz"
    assert result.monotone_support_upper == 0.675
