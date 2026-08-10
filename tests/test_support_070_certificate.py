from types import SimpleNamespace

import experiments.theta_pencil.support_070_certificate as certificate


def test_support_070_checks_both_parity_sectors(monkeypatch):
    fake = SimpleNamespace(
        even=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=1.5e-13,
            coercive_lower=1.0e-15,
        ),
        odd=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=2.5e-10,
            coercive_lower=1.7e-12,
        ),
    )
    calls = []

    def fake_schur(**kwargs):
        calls.append(kwargs)
        return fake

    monkeypatch.setattr(certificate, "certify_third_window_schur", fake_schur)
    result = certificate.certify_support_070("components.npz")
    assert calls == [{"component_cache_path": "components.npz"}]
    assert result.global_coercive_lower == 1.0e-15
    assert result.monotone_support_upper == 0.7
