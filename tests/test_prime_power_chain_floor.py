import pytest

from experiments.theta_pencil.prime_power_chain_floor import (
    certify_separable_prime_complement_floor,
)
from experiments.theta_pencil.prime_power_arithmetic import prime_power_base


def test_prime_power_base_rejects_composites_with_two_prime_factors():
    assert prime_power_base(2) == 2
    assert prime_power_base(4) == 2
    assert prime_power_base(9) == 3
    with pytest.raises(ValueError, match="prime power"):
        prime_power_base(6)


def test_separable_chain_floor_crosses_prime_power_four_threshold():
    pytest.importorskip("flint")
    result = certify_separable_prime_complement_floor(
        0.7,
        {2: 0.325, 3: 0.5, 4: 0.175},
        subdivisions_per_segment=128,
        precision=384,
    )
    assert tuple(component.prime_power for component in result.components) == (2, 3, 4)
    assert result.components[0].maximum_chain_length == 3
    assert result.components[1].maximum_chain_length == 2
    assert result.components[2].maximum_chain_length == 2
    assert result.complement_floor > 0.30
    assert result.complement_floor < 0.36
