from types import SimpleNamespace

from experiments.theta_pencil import support_051_certificate as certificate


def test_support_051_composes_registered_gap_and_temple_parameters(monkeypatch):
    calls = []
    endpoint = SimpleNamespace(half_width=0.51)

    def fake_endpoint(*args, **kwargs):
        calls.append(("endpoint", args, kwargs))
        return endpoint

    def fake_temple(**kwargs):
        calls.append(("temple", (), kwargs))
        lower = 2e-7 if kwargs["trial_parity"] == 0 else 1e-4
        return SimpleNamespace(temple_lower=lower)

    monkeypatch.setattr(certificate, "certify_first_prime_endpoint", fake_endpoint)
    monkeypatch.setattr(certificate, "certify_temple_trial", fake_temple)
    result = certificate.certify_support_051()

    assert result.endpoint is endpoint
    assert result.global_lower == 2e-7
    assert calls[0][1] == (0.51,)
    assert calls[0][2]["even_shift"] == 0.003
    even = calls[1][2]
    odd = calls[2][2]
    assert even["residual_end"] == 16384
    assert even["second_floor"] == 0.003
    assert odd["residual_end"] == 8192
    assert odd["second_floor"] == 0.1
