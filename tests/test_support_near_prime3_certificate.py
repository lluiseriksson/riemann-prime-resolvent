from types import SimpleNamespace

import pytest

from experiments.theta_pencil import support_near_prime3_certificate as certificate
from experiments.theta_pencil.support_window import in_first_prime_window


def test_registered_support_is_strictly_below_prime_three_boundary():
    assert in_first_prime_window(certificate.HALF_WIDTH_BELOW_PRIME_THREE)


def test_near_prime_three_composes_registered_parameters(monkeypatch):
    calls = []
    endpoint = SimpleNamespace(half_width=certificate.HALF_WIDTH_BELOW_PRIME_THREE)

    def fake_endpoint(*args, **kwargs):
        calls.append(("endpoint", args, kwargs))
        return endpoint

    def fake_temple(**kwargs):
        calls.append(("temple", (), kwargs))
        lower = 5e-10 if kwargs["trial_parity"] == 0 else 1e-5
        return SimpleNamespace(temple_lower=lower)

    monkeypatch.setattr(certificate, "certify_first_prime_endpoint", fake_endpoint)
    monkeypatch.setattr(certificate, "certify_temple_trial", fake_temple)
    result = certificate.certify_support_near_prime_three()

    assert result.endpoint is endpoint
    assert result.global_lower == 5e-10
    assert calls[0][1] == (certificate.HALF_WIDTH_BELOW_PRIME_THREE,)
    assert calls[0][2]["even_shift"] == 0.001
    assert calls[0][2]["odd_shift"] == 0.05
    even = calls[1][2]
    odd = calls[2][2]
    assert even["dimension"] == 512
    assert even["residual_end"] == 131072
    assert even["second_floor"] == 0.001
    assert even["variation_partitions"] == 256
    assert odd["dimension"] == 256
    assert odd["residual_end"] == 8192
    assert odd["second_floor"] == 0.05


def test_near_prime_three_rejects_a_nonpositive_sector(monkeypatch):
    monkeypatch.setattr(
        certificate,
        "certify_first_prime_endpoint",
        lambda *args, **kwargs: SimpleNamespace(half_width=args[0]),
    )

    def fake_temple(**kwargs):
        return SimpleNamespace(
            temple_lower=0.0 if kwargs["trial_parity"] == 0 else 1.0
        )

    monkeypatch.setattr(certificate, "certify_temple_trial", fake_temple)
    with pytest.raises(ArithmeticError, match="not positive"):
        certificate.certify_support_near_prime_three()
