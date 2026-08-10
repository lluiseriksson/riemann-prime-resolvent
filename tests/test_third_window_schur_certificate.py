from types import SimpleNamespace

import experiments.theta_pencil.third_window_schur_certificate as certificate


def test_third_window_cache_metadata_records_every_expensive_parameter():
    metadata = certificate._metadata(0.7, 16, 640, 4096, 47, 16384, 512, 1024)
    assert metadata["architecture"] == "third-window-thirteen-block"
    assert metadata["maximum_smooth_power"] == 47
    assert metadata["smooth_target_rule"].endswith("+2")
    assert metadata["retain_self_tail"] is True


def test_third_window_certificate_result_shape_is_explicit():
    parity = SimpleNamespace(coercive_lower=1e-20)
    result = certificate.ThirdWindowSchurCertificate(
        half_width=0.7,
        even=parity,
        odd=parity,
        complement_floor=0.6,
        tail_complement_floor=2.0,
        smooth_remainder=1e-16,
        other_tail_norm=1e-12,
        tail_balance=0.05,
        residual_balance=0.01,
        low_degree_count=16,
        tail_start=640,
        explicit_end=4096,
        component_cache_hit=True,
        precision=512,
    )
    assert result.even.coercive_lower > 0
    assert result.component_cache_hit is True
