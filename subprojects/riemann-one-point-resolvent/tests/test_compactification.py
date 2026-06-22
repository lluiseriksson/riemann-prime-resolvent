from __future__ import annotations


def point(x0: float, lam: float) -> float:
    return x0 / (lam + x0)


def weight(x0: float, lam: float) -> float:
    return 1 / (lam + x0)


def test_nonnegative_spectrum_maps_to_unit_interval() -> None:
    for x0 in (0.25, 1.0, 10.0):
        for lam in (0.0, 1.0, 100.0):
            assert 0 <= point(x0, lam) <= 1
            assert weight(x0, lam) >= 0
