from types import SimpleNamespace

import pytest

from experiments.theta_pencil import support_054_certificate as certificate


def test_support_054_composes_registered_gap_and_temple_parameters(monkeypatch):
    calls = []
    endpoint = SimpleNamespace(half_width=0.54)

    def fake_endpoint(*args, **kwargs):
        calls.append(("endpoint", args, kwargs))
        return endpoint

    def fake_temple(**kwargs):
        calls.append(("temple", (), kwargs))
        lower = 7e-9 if kwargs["trial_parity"] == 0 else 2e-5
        return SimpleNamespace(temple_lower=lower)

    monkeypatch.setattr(certificate, "certify_first_prime_endpoint", fake_endpoint)
    monkeypatch.setattr(certificate, "certify_temple_trial", fake_temple)
    result = certificate.certify_support_054()

    assert result.endpoint is endpoint
    assert result.global_lower == 7e-9
    assert calls[0][1] == (0.54,)
    assert calls[0][2]["even_shift"] == 0.0011
    even = calls[1][2]
    odd = calls[2][2]
    assert even["dimension"] == 512
    assert even["residual_end"] == 131072
    assert even["second_floor"] == 0.0011
    assert even["variation_partitions"] == 256
    assert odd["dimension"] == 256
    assert odd["residual_end"] == 8192
    assert odd["second_floor"] == 0.1


def test_support_054_rejects_a_nonpositive_sector(monkeypatch):
    monkeypatch.setattr(
        certificate,
        "certify_first_prime_endpoint",
        lambda *args, **kwargs: SimpleNamespace(half_width=0.54),
    )

    def fake_temple(**kwargs):
        return SimpleNamespace(
            temple_lower=0.0 if kwargs["trial_parity"] == 0 else 1.0
        )

    monkeypatch.setattr(certificate, "certify_temple_trial", fake_temple)
    with pytest.raises(ArithmeticError, match="not positive"):
        certificate.certify_support_054()
