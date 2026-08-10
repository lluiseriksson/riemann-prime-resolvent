"""Separable boundary-potential floors for arbitrary active prime powers."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from experiments.theta_pencil.second_window_pointwise_floor import (
    _float_lower,
    _float_upper,
    _least_eigenvalue_lower,
    _potential_lower,
)
from experiments.theta_pencil.prime_power_arithmetic import prime_power_base
from experiments.theta_pencil.support_05_comparison import _smooth_lower_loss


@dataclass(frozen=True)
class PrimePowerChainFloor:
    prime_power: int
    prime_base: int
    allocation: float
    displacement_lower: float
    displacement_upper: float
    coefficient_upper: float
    chain_lower: float
    maximum_chain_length: int
    residue_segments: int


@dataclass(frozen=True)
class SeparablePrimeComplementFloor:
    half_width: float
    components: tuple[PrimePowerChainFloor, ...]
    allocation_sum_upper: float
    unused_potential_lower: float
    scalar_lower: float
    smooth_loss_upper: float
    harmonic_floor: float
    complement_floor: float
    subdivisions_per_segment: int
    maximum_smooth_power: int
    precision: int


def _residue_cuts(arb, displacement):
    """Partition the base residue interval where the chain length is constant."""

    left = -arb(1)
    right = left + displacement
    approximate_displacement = float(displacement.mid())
    maximum_steps = math.ceil(2.0 / approximate_displacement) + 1
    cuts = [left, right]
    for step in range(1, maximum_steps + 1):
        candidate = arb(1) - step * displacement
        if candidate.lower() > left.upper() and candidate.upper() < right.lower():
            cuts.append(candidate)
        elif not (
            candidate.upper() <= left.lower() or candidate.lower() >= right.upper()
        ):
            raise ArithmeticError("a residue cut met an unresolved chain threshold")
    cuts.sort(key=lambda value: float(value.mid()))
    if not all((cuts[index + 1] - cuts[index]).lower() > 0 for index in range(len(cuts) - 1)):
        raise ArithmeticError("the single-translation residue cuts did not order")
    return tuple(cuts)


def _certify_single_chain_floor(
    arb,
    arb_mat,
    half_width,
    prime_power: int,
    allocation,
    subdivisions_per_segment: int,
) -> PrimePowerChainFloor:
    prime_base = prime_power_base(prime_power)
    displacement = arb(prime_power).log() / half_width
    if not displacement.lower() > 0 or not displacement.upper() < 2:
        raise ValueError("every supplied prime power must have positive overlap")
    coefficient = arb(prime_base).log() / arb(prime_power).sqrt()
    cuts = _residue_cuts(arb, displacement)
    component_lower = None
    maximum_chain_length = 0

    for segment_left, segment_right in zip(cuts[:-1], cuts[1:]):
        sample = float(((segment_left + segment_right) / 2).mid())
        h_float = float(displacement.mid())
        chain_length = 1
        while sample + chain_length * h_float < 1.0:
            chain_length += 1
        maximum_chain_length = max(maximum_chain_length, chain_length)

        for cell in range(subdivisions_per_segment):
            lower = segment_left + (segment_right - segment_left) * cell / subdivisions_per_segment
            upper = segment_left + (segment_right - segment_left) * (cell + 1) / subdivisions_per_segment
            residue = (lower + upper) / 2 + arb(0, (upper - lower) / 2)
            matrix = arb_mat(chain_length, chain_length)
            for index in range(chain_length):
                physical = residue + index * displacement
                matrix[index, index] = allocation * _potential_lower(arb, physical)
            for index in range(chain_length - 1):
                matrix[index, index + 1] = -coefficient
                matrix[index + 1, index] = -coefficient
            candidate = _least_eigenvalue_lower(matrix)
            if component_lower is None or candidate < component_lower:
                component_lower = candidate

    if component_lower is None:
        raise ArithmeticError("no residue chain was certified")
    return PrimePowerChainFloor(
        prime_power=prime_power,
        prime_base=prime_base,
        allocation=_float_lower(allocation),
        displacement_lower=_float_lower(displacement),
        displacement_upper=_float_upper(displacement),
        coefficient_upper=_float_upper(coefficient),
        chain_lower=_float_lower(component_lower),
        maximum_chain_length=maximum_chain_length,
        residue_segments=len(cuts) - 1,
    )


def certify_separable_prime_complement_floor(
    half_width: float,
    allocations: dict[int, float],
    local_degree: int = 16,
    maximum_smooth_power: int = 39,
    subdivisions_per_segment: int = 512,
    precision: int = 512,
) -> SeparablePrimeComplementFloor:
    """Certify a scalable complement floor by splitting the boundary potential.

    If ``V`` is the nonnegative boundary potential and ``T_n`` the symmetric
    translation belonging to a prime power ``n``, choose ``theta_n >= 0``
    with sum at most one.  Then

    ``V + sum T_n >= sum inf(theta_n V + T_n)``.

    Each summand fibers over residues modulo ``log(n) / half_width`` into
    finite tridiagonal chains.  This avoids a joint cut partition, which need
    not remain finite once several incommensurate translations can compose.
    """

    if half_width <= 0 or local_degree < 1 or subdivisions_per_segment < 1:
        raise ValueError("invalid support, degree, or subdivision count")
    if maximum_smooth_power < 3:
        raise ValueError("maximum_smooth_power must be at least three")
    if not allocations or any(value < 0 for value in allocations.values()):
        raise ValueError("allocations must be a nonempty nonnegative mapping")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = arb(str(half_width))
        allocation_rationals = {
            prime_power: Fraction(str(allocation))
            for prime_power, allocation in sorted(allocations.items())
        }
        allocation_sum_rational = sum(allocation_rationals.values(), Fraction(0))
        if not 0 <= allocation_sum_rational <= 1:
            raise ValueError("the boundary-potential allocations must sum to at most one")
        allocation_balls = {
            prime_power: arb(value.numerator) / value.denominator
            for prime_power, value in allocation_rationals.items()
        }
        allocation_sum = sum(allocation_balls.values(), arb(0))
        components = tuple(
            _certify_single_chain_floor(
                arb,
                arb_mat,
                a,
                prime_power,
                allocation,
                subdivisions_per_segment,
            )
            for prime_power, allocation in allocation_balls.items()
        )
        scalar = -a.log() - (2 * arb.pi()).log() - arb.const_euler()
        smooth_loss_float = _smooth_lower_loss(half_width, maximum_smooth_power)
        smooth_loss = arb(str(smooth_loss_float))
        harmonic = sum(
            (arb(1) / degree for degree in range(1, local_degree + 1)),
            arb(0),
        )
        chain_sum = sum(
            (arb(str(component.chain_lower)) for component in components), arb(0)
        )
        complement = harmonic + scalar - smooth_loss + chain_sum
        if not complement.lower() > 0:
            raise ArithmeticError("the separable prime complement floor is not positive")
    finally:
        ctx.prec = previous_precision

    return SeparablePrimeComplementFloor(
        half_width=half_width,
        components=components,
        allocation_sum_upper=_float_upper(allocation_sum),
        unused_potential_lower=float(1 - allocation_sum_rational),
        scalar_lower=_float_lower(scalar),
        smooth_loss_upper=_float_upper(smooth_loss),
        harmonic_floor=_float_lower(harmonic),
        complement_floor=_float_lower(complement),
        subdivisions_per_segment=subdivisions_per_segment,
        maximum_smooth_power=maximum_smooth_power,
        precision=precision,
    )
