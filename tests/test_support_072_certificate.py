from types import SimpleNamespace

import experiments.theta_pencil.support_072_certificate as certificate


def test_support_072_checks_both_parity_sectors(monkeypatch):
    fake = SimpleNamespace(
        even=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=2.5e-14,
            coercive_lower=9.8e-17,
        ),
        odd=SimpleNamespace(
            negative_count=0,
            unresolved_count=0,
            first_positive_lower=4.3e-11,
            coercive_lower=1.6e-13,
        ),
    )
    calls = []

    def fake_schur(**kwargs):
        calls.append(kwargs)
        return fake

    monkeypatch.setattr(
        certificate, "certify_third_window_multiband_schur", fake_schur
    )
    result = certificate.certify_support_072("components.npz", "bands.npz")
    assert calls == [
        {
            "component_cache_path": "components.npz",
            "band_cache_path": "bands.npz",
        }
    ]
    assert result.global_coercive_lower == 9.8e-17
    assert result.monotone_support_upper == 0.72
