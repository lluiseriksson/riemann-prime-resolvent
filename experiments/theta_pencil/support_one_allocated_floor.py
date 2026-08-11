"""Allocated boundary-potential floor for the support-one complement.

The rational split 173/500 + 327/500 = 1 pairs the boundary potential with
the prime-power translations 5 and 7.  Since both shifts exceed one, every
nontrivial residue fiber is a two-vertex path and admits an elementary
pointwise floor.  Prime powers 2, 3, and 4 retain their exact path spectra.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from experiments.theta_pencil.gauss_stieltjes_potential import harmonic
from experiments.theta_pencil.support_05_comparison import _smooth_lower_loss


EULER_GAMMA = 0.577215664901532860606512090082402431
THETA_FIVE = Fraction(173, 500)
THETA_SEVEN = Fraction(327, 500)


@dataclass(frozen=True)
class AllocatedSupportOneFloor:
    theta_five: float
    theta_seven: float
    prime_two_floor: float
    prime_three_floor: float
    prime_four_floor: float
    prime_five_floor: float
    prime_seven_raw_floor: float
    prime_seven_floor: float
    smooth_loss: float
    bounded_part_floor: float
    tail_start: int
    complement_margin: float


def boundary_potential(value: float) -> float:
    if not 0.0 < abs(value) < 1.0:
        raise ValueError("boundary-potential argument must lie inside the interval")
    return -0.5 * math.log1p(-(value * value))


def two_vertex_allocated_floor(prime_power: int, allocation: Fraction) -> float:
    """Pointwise floor for a shift log(n)>1 paired with theta*V."""

    if prime_power not in (5, 7):
        raise ValueError("the registered two-vertex formula is for 5 and 7")
    shift = math.log(prime_power)
    minimum_potential = boundary_potential(shift - 1.0)
    coefficient = math.log(prime_power) / math.sqrt(prime_power)
    return float(allocation) * minimum_potential - coefficient


def registered_support_one_floor(
    smooth_order: int = 95,
) -> AllocatedSupportOneFloor:
    """Return the rational-allocation high-complement design constants."""

    if THETA_FIVE + THETA_SEVEN != 1:
        raise AssertionError("the registered potential allocation must sum to one")
    coefficient_two = math.log(2.0) / math.sqrt(2.0)
    floor_two = -2.0 * coefficient_two * math.cos(math.pi / 4.0)
    floor_three = -math.log(3.0) / math.sqrt(3.0)
    floor_four = -math.log(2.0) / 2.0
    floor_five = two_vertex_allocated_floor(5, THETA_FIVE)
    raw_seven = two_vertex_allocated_floor(7, THETA_SEVEN)
    floor_seven = min(0.0, raw_seven)
    smooth = _smooth_lower_loss(1.0, smooth_order)
    scalar = -math.log(2.0 * math.pi) - EULER_GAMMA
    bounded = (
        scalar
        - smooth
        + floor_two
        + floor_three
        + floor_four
        + floor_five
        + floor_seven
    )
    index = 0
    while harmonic(index) + bounded <= 0.0:
        index += 1
    margin = harmonic(index) + bounded
    return AllocatedSupportOneFloor(
        theta_five=float(THETA_FIVE),
        theta_seven=float(THETA_SEVEN),
        prime_two_floor=floor_two,
        prime_three_floor=floor_three,
        prime_four_floor=floor_four,
        prime_five_floor=floor_five,
        prime_seven_raw_floor=raw_seven,
        prime_seven_floor=floor_seven,
        smooth_loss=smooth,
        bounded_part_floor=bounded,
        tail_start=index,
        complement_margin=margin,
    )


def certify_registered_support_one_floor(
    subdivisions_per_segment: int = 4096,
    precision: int = 512,
):
    """Run the source-level Arb chain certificate for the rational split."""

    from experiments.theta_pencil.prime_power_chain_floor import (
        certify_separable_prime_complement_floor,
    )

    return certify_separable_prime_complement_floor(
        half_width=1.0,
        allocations={
            2: 0.0,
            3: 0.0,
            4: 0.0,
            5: float(THETA_FIVE),
            7: float(THETA_SEVEN),
        },
        local_degree=99,
        maximum_smooth_power=95,
        subdivisions_per_segment=subdivisions_per_segment,
        precision=precision,
    )


def main() -> None:
    print(registered_support_one_floor())


if __name__ == "__main__":
    main()
