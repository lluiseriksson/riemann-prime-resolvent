"""Joint pointwise graph floor in the first prime-power-four window."""

from __future__ import annotations

from dataclasses import dataclass

from experiments.theta_pencil.cut_adapted_prime_basis import third_prime_partition
from experiments.theta_pencil.second_window_pointwise_floor import (
    _float_lower,
    _float_upper,
    _least_eigenvalue_lower,
    _potential_lower,
)
from experiments.theta_pencil.support_05_comparison import _smooth_lower_loss


@dataclass(frozen=True)
class ThirdWindowPointwiseFloor:
    half_width: float
    component_lowers: tuple[float, ...]
    graph_lower: float
    scalar_lower: float
    smooth_loss_upper: float
    harmonic_floor: float
    complement_floor: float
    subdivisions: int
    maximum_smooth_power: int
    precision: int


def certify_third_window_pointwise_floor(
    half_width: float = 0.7,
    local_degree: int = 16,
    maximum_smooth_power: int = 47,
    subdivisions: int = 1024,
    precision: int = 512,
) -> ThirdWindowPointwiseFloor:
    """Certify boundary potential plus the exact 2/3/4 translation graph."""

    partition = third_prime_partition(half_width)
    if local_degree < 1 or subdivisions < 1:
        raise ValueError("local_degree and subdivisions must be positive")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        one = arb(1)
        a = arb(str(half_width))
        h_two = arb.const_log2() / a
        h_three = arb(3).log() / a
        breakpoints = (
            -one,
            one - 2 * h_two,
            -one + 2 * h_two - h_three,
            one - h_three,
            -one - h_two + h_three,
            one - 3 * h_two + h_three,
            -one + h_two,
            one - h_two,
            -one + 3 * h_two - h_three,
            one + h_two - h_three,
            -one + h_three,
            one - 2 * h_two + h_three,
            -one + 2 * h_two,
            one,
        )
        lengths = tuple(
            breakpoints[index + 1] - breakpoints[index] for index in range(13)
        )
        if not all(length.lower() > 0 for length in lengths):
            raise ArithmeticError("the third-window Arb cuts did not order")

        components = (
            (0, 2, 4, 6, 8, 10, 12),
            (1, 5, 7, 11),
            (3, 9),
        )
        weighted_edges = tuple(
            (left, right, arb.const_log2() / arb(2).sqrt())
            for left, right in partition.prime_two_pairs
        ) + tuple(
            (left, right, arb(3).log() / arb(3).sqrt())
            for left, right in partition.prime_three_pairs
        ) + tuple(
            (left, right, arb.const_log2() / arb(4).sqrt())
            for left, right in partition.prime_four_pairs
        )
        component_lowers = [None for _ in components]
        for cell in range(subdivisions):
            lower = -one + arb(2 * cell) / subdivisions
            upper = -one + arb(2 * (cell + 1)) / subdivisions
            local = (lower + upper) / 2 + arb(0, (upper - lower) / 2)
            potentials = []
            for block in range(13):
                physical = (
                    (breakpoints[block] + breakpoints[block + 1]) / 2
                    + lengths[block] * local / 2
                )
                potentials.append(_potential_lower(arb, physical))

            for component_index, blocks in enumerate(components):
                positions = {block: index for index, block in enumerate(blocks)}
                matrix = arb_mat(len(blocks), len(blocks))
                for block, index in positions.items():
                    matrix[index, index] = potentials[block]
                for left, right, coefficient in weighted_edges:
                    if left not in positions:
                        continue
                    left_index = positions[left]
                    right_index = positions[right]
                    matrix[left_index, right_index] -= coefficient
                    matrix[right_index, left_index] -= coefficient
                candidate = _least_eigenvalue_lower(matrix)
                if (
                    component_lowers[component_index] is None
                    or candidate < component_lowers[component_index]
                ):
                    component_lowers[component_index] = candidate

        graph_lower = min(component_lowers)
        scalar = -a.log() - (2 * arb.pi()).log() - arb.const_euler()
        smooth_loss = arb(
            str(_smooth_lower_loss(half_width, maximum_smooth_power))
        )
        harmonic = sum(
            (arb(1) / degree for degree in range(1, local_degree + 1)),
            arb(0),
        )
        complement = harmonic + graph_lower + scalar - smooth_loss
        if not complement.lower() > 0:
            raise ArithmeticError("the third-window complement floor is not positive")
    finally:
        ctx.prec = previous_precision

    return ThirdWindowPointwiseFloor(
        half_width=half_width,
        component_lowers=tuple(_float_lower(value) for value in component_lowers),
        graph_lower=_float_lower(graph_lower),
        scalar_lower=_float_lower(scalar),
        smooth_loss_upper=_float_upper(smooth_loss),
        harmonic_floor=_float_lower(harmonic),
        complement_floor=_float_lower(complement),
        subdivisions=subdivisions,
        maximum_smooth_power=maximum_smooth_power,
        precision=precision,
    )
