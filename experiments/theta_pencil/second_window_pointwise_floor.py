"""Joint boundary-potential/prime-graph floor in the second window."""

from __future__ import annotations

import math
from dataclasses import dataclass

from experiments.theta_pencil.cut_adapted_prime_basis import second_prime_partition
from experiments.theta_pencil.support_05_comparison import _smooth_lower_loss


@dataclass(frozen=True)
class SecondWindowPointwiseFloor:
    half_width: float
    edge_graph_lower: float
    bridge_graph_lower: float
    center_lower: float
    graph_lower: float
    scalar_lower: float
    smooth_loss_upper: float
    bounded_perturbation_lower: float
    harmonic_floor: float
    complement_floor: float
    subdivisions: int
    maximum_smooth_power: int
    precision: int


def _float_lower(value) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def _float_upper(value) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def _potential_lower(arb, physical_ball):
    """Lower-bound ``-log(1-x^2)/2`` on one physical interval ball."""

    minimum_absolute = physical_ball.abs_lower()
    if not minimum_absolute.lower() >= 0:
        raise ArithmeticError("the absolute-value lower bound was unresolved")
    if not minimum_absolute.upper() < 1:
        raise ArithmeticError("a support cell collapsed onto the singular endpoint")
    return -(1 - minimum_absolute**2).log() / 2


def _least_eigenvalue_lower(matrix):
    eigenvalues = matrix.eig(multiple=True, algorithm="rump")
    return min(value.real.lower() for value in eigenvalues)


def certify_second_window_pointwise_floor(
    half_width: float,
    local_degree: int = 16,
    maximum_smooth_power: int = 39,
    subdivisions: int = 1024,
    precision: int = 512,
) -> SecondWindowPointwiseFloor:
    """Certify a common complement floor using the full two-prime graph.

    The four equal edge intervals form the path ``4--0--6--2`` with weights
    ``p2,p3,p2``.  The two bridge intervals form one prime-two edge and the
    centre is isolated.  On each local-coordinate cell, replacing every
    boundary potential by its Arb lower bound gives a Loewner-lower constant
    matrix.  Its least eigenvalue therefore bounds the whole fiber.
    """

    second_prime_partition(half_width)
    if local_degree < 1 or subdivisions < 1:
        raise ValueError("local_degree and subdivisions must be positive")
    if maximum_smooth_power < 3:
        raise ValueError("maximum_smooth_power must be at least three")
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
            one - h_three,
            h_three - h_two - one,
            one - h_two,
            h_two - one,
            one - h_three + h_two,
            h_three - one,
            one,
        )
        lengths = tuple(
            breakpoints[index + 1] - breakpoints[index] for index in range(7)
        )
        if not all(length.lower() > 0 for length in lengths):
            raise ArithmeticError("the second-window partition ordering failed")

        prime_two = arb.const_log2() / arb(2).sqrt()
        prime_three = arb(3).log() / arb(3).sqrt()
        component_lowers = [None, None, None]
        edge_ids = (4, 0, 6, 2)
        for cell in range(subdivisions):
            lower = -one + arb(2 * cell) / subdivisions
            upper = -one + arb(2 * (cell + 1)) / subdivisions
            midpoint = (lower + upper) / 2
            t = midpoint + arb(0, (upper - lower) / 2)
            potentials = []
            for block in range(7):
                physical = (
                    (breakpoints[block] + breakpoints[block + 1]) / 2
                    + lengths[block] * t / 2
                )
                potentials.append(_potential_lower(arb, physical))

            edge = arb_mat(4, 4)
            for index, block in enumerate(edge_ids):
                edge[index, index] = potentials[block]
            for left, right, coefficient in (
                (0, 1, prime_two),
                (1, 2, prime_three),
                (2, 3, prime_two),
            ):
                edge[left, right] = -coefficient
                edge[right, left] = -coefficient

            bridge = arb_mat(
                [[potentials[1], -prime_two], [-prime_two, potentials[5]]]
            )
            candidates = (
                _least_eigenvalue_lower(edge),
                _least_eigenvalue_lower(bridge),
                potentials[3].lower(),
            )
            for index, candidate in enumerate(candidates):
                if component_lowers[index] is None or candidate < component_lowers[index]:
                    component_lowers[index] = candidate

        edge_lower, bridge_lower, center_lower = component_lowers
        graph_lower = min(component_lowers)
        scalar = -a.log() - (2 * arb.pi()).log() - arb.const_euler()
        smooth_loss_float = _smooth_lower_loss(
            half_width, maximum_smooth_power
        )
        smooth_loss = arb(str(smooth_loss_float))
        bounded = graph_lower + scalar - smooth_loss
        harmonic = sum(
            (arb(1) / degree for degree in range(1, local_degree + 1)),
            arb(0),
        )
        complement = harmonic + bounded
        if not complement.lower() > 0:
            raise ArithmeticError("the joint pointwise complement floor is not positive")
    finally:
        ctx.prec = previous_precision

    return SecondWindowPointwiseFloor(
        half_width=half_width,
        edge_graph_lower=_float_lower(edge_lower),
        bridge_graph_lower=_float_lower(bridge_lower),
        center_lower=_float_lower(center_lower),
        graph_lower=_float_lower(graph_lower),
        scalar_lower=_float_lower(scalar),
        smooth_loss_upper=_float_upper(smooth_loss),
        bounded_perturbation_lower=_float_lower(bounded),
        harmonic_floor=_float_lower(harmonic),
        complement_floor=_float_lower(complement),
        subdivisions=subdivisions,
        maximum_smooth_power=maximum_smooth_power,
        precision=precision,
    )
