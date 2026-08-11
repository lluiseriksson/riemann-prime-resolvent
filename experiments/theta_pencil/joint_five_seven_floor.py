"""Joint pointwise floor for the prime-power translations 5 and 7.

At support one both shifts exceed one.  Their union graph on ``[-1, 1]``
therefore has only isolated vertices, two-vertex prime-5 edges, and
four-vertex paths with edge weights ``c5, c7, c5``.  This module encloses
the least eigenvalue of the two nontrivial component families with Arb.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from experiments.theta_pencil.gauss_stieltjes_potential import harmonic
from experiments.theta_pencil.second_window_pointwise_floor import (
    _float_lower,
    _least_eigenvalue_lower,
    _potential_lower,
)
from experiments.theta_pencil.support_05_comparison import _smooth_lower_loss


EULER_GAMMA = 0.577215664901532860606512090082402431
REGISTERED_JOINT_FLOOR_TARGET = -0.267


@dataclass(frozen=True)
class JointFiveSevenFloor:
    chain_lower: float
    four_path_lower: float
    two_path_lower: float
    four_path_interval: tuple[float, float]
    two_path_interval: tuple[float, float]
    subdivisions_per_interval: int
    precision: int


@dataclass(frozen=True)
class SupportOneJointBlockFloor:
    joint_five_seven: JointFiveSevenFloor
    joint_dyadic_lower: float
    prime_three_lower: float
    scalar_lower: float
    smooth_loss_upper: float
    harmonic_floor: float
    complement_floor: float
    local_degree: int
    precision: int


def _potential_float(value: float) -> float:
    return -0.5 * math.log1p(-(value * value))


def four_path_matrix_float(parameter: float) -> np.ndarray:
    """Return the exact four-path matrix at a nonsingular parameter."""

    h_five = math.log(5.0)
    h_seven = math.log(7.0)
    delta = h_seven - h_five
    if not -1.0 < parameter < 1.0 - h_seven:
        raise ValueError("four-path parameter lies outside its open interval")
    points = (
        parameter + h_five,
        parameter,
        parameter + h_seven,
        parameter + delta,
    )
    matrix = np.diag([_potential_float(point) for point in points])
    c_five = h_five / math.sqrt(5.0)
    c_seven = h_seven / math.sqrt(7.0)
    for left, right, coefficient in (
        (0, 1, c_five),
        (1, 2, c_seven),
        (2, 3, c_five),
    ):
        matrix[left, right] = -coefficient
        matrix[right, left] = -coefficient
    return matrix


def two_path_matrix_float(parameter: float) -> np.ndarray:
    """Return the prime-5 two-path matrix at a nonsingular parameter."""

    h_five = math.log(5.0)
    h_seven = math.log(7.0)
    delta = h_seven - h_five
    if not 1.0 - h_seven < parameter < delta - 1.0:
        raise ValueError("two-path parameter lies outside its open interval")
    coefficient = h_five / math.sqrt(5.0)
    return np.array(
        [
            [_potential_float(parameter), -coefficient],
            [-coefficient, _potential_float(parameter + h_five)],
        ]
    )


def _cell_ball(arb, left, right, cell: int, subdivisions: int):
    lower = left + (right - left) * cell / subdivisions
    upper = left + (right - left) * (cell + 1) / subdivisions
    return (lower + upper) / 2 + arb(0, (upper - lower) / 2)


def certify_joint_five_seven_floor(
    subdivisions_per_interval: int = 4096,
    precision: int = 512,
) -> JointFiveSevenFloor:
    """Certify the essential floor of ``V + T_5 + T_7`` with Arb."""

    if subdivisions_per_interval < 1:
        raise ValueError("subdivisions_per_interval must be positive")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        one = arb(1)
        h_five = arb(5).log()
        h_seven = arb(7).log()
        delta = h_seven - h_five
        c_five = h_five / arb(5).sqrt()
        c_seven = h_seven / arb(7).sqrt()

        four_left, four_right = -one, one - h_seven
        two_left, two_right = four_right, delta - one
        if not four_right.lower() > four_left.upper():
            raise ArithmeticError("the four-path parameter interval collapsed")
        if not two_right.lower() > two_left.upper():
            raise ArithmeticError("the two-path parameter interval collapsed")

        four_lower = None
        for cell in range(subdivisions_per_interval):
            parameter = _cell_ball(
                arb, four_left, four_right, cell, subdivisions_per_interval
            )
            points = (
                parameter + h_five,
                parameter,
                parameter + h_seven,
                parameter + delta,
            )
            matrix = arb_mat(4, 4)
            for index, point in enumerate(points):
                matrix[index, index] = _potential_lower(arb, point)
            for left, right, coefficient in (
                (0, 1, c_five),
                (1, 2, c_seven),
                (2, 3, c_five),
            ):
                matrix[left, right] = -coefficient
                matrix[right, left] = -coefficient
            candidate = _least_eigenvalue_lower(matrix)
            if four_lower is None or candidate < four_lower:
                four_lower = candidate

        two_lower = None
        for cell in range(subdivisions_per_interval):
            parameter = _cell_ball(
                arb, two_left, two_right, cell, subdivisions_per_interval
            )
            matrix = arb_mat(2, 2)
            matrix[0, 0] = _potential_lower(arb, parameter)
            matrix[1, 1] = _potential_lower(arb, parameter + h_five)
            matrix[0, 1] = -c_five
            matrix[1, 0] = -c_five
            candidate = _least_eigenvalue_lower(matrix)
            if two_lower is None or candidate < two_lower:
                two_lower = candidate

        if four_lower is None or two_lower is None:
            raise ArithmeticError("a joint-chain family was not evaluated")
        chain_lower = min(arb(0), four_lower, two_lower)
    finally:
        ctx.prec = previous_precision

    return JointFiveSevenFloor(
        chain_lower=_float_lower(chain_lower),
        four_path_lower=_float_lower(four_lower),
        two_path_lower=_float_lower(two_lower),
        four_path_interval=(-1.0, 1.0 - math.log(7.0)),
        two_path_interval=(
            1.0 - math.log(7.0),
            math.log(7.0 / 5.0) - 1.0,
        ),
        subdivisions_per_interval=subdivisions_per_interval,
        precision=precision,
    )


def certify_support_one_joint_block_floor(
    local_degree: int = 58,
    maximum_smooth_power: int = 95,
    subdivisions_per_interval: int = 4096,
    precision: int = 512,
) -> SupportOneJointBlockFloor:
    """Combine the joint 2+4 and 5+7 blocks with the prime-3 edge."""

    joint_five_seven = certify_joint_five_seven_floor(
        subdivisions_per_interval, precision
    )
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        joint_dyadic = -arb(2).log() * (1 + arb(17).sqrt()) / 4
        prime_three = -arb(3).log() / arb(3).sqrt()
        scalar = -(2 * arb.pi()).log() - arb.const_euler()
        smooth_loss = arb(str(_smooth_lower_loss(1.0, maximum_smooth_power)))
        harmonic_ball = sum(
            (arb(1) / degree for degree in range(1, local_degree + 1)),
            arb(0),
        )
        joint_five_seven_ball = arb(str(joint_five_seven.chain_lower))
        complement = (
            harmonic_ball
            + scalar
            - smooth_loss
            + joint_dyadic
            + prime_three
            + joint_five_seven_ball
        )
        if not complement.lower() > 0:
            raise ArithmeticError("the support-one joint-block floor is not positive")
    finally:
        ctx.prec = previous_precision

    return SupportOneJointBlockFloor(
        joint_five_seven=joint_five_seven,
        joint_dyadic_lower=_float_lower(joint_dyadic),
        prime_three_lower=_float_lower(prime_three),
        scalar_lower=_float_lower(scalar),
        smooth_loss_upper=math.nextafter(
            float(smooth_loss.upper()), math.inf
        ),
        harmonic_floor=_float_lower(harmonic_ball),
        complement_floor=_float_lower(complement),
        local_degree=local_degree,
        precision=precision,
    )


def registered_joint_floor_target_margin() -> tuple[int, float]:
    """Return the exact float design margin for the pre-registered target."""

    joint_dyadic = -math.log(2.0) * (1.0 + math.sqrt(17.0)) / 4.0
    prime_three = -math.log(3.0) / math.sqrt(3.0)
    scalar = -math.log(2.0 * math.pi) - EULER_GAMMA
    smooth_loss = _smooth_lower_loss(1.0, 95)
    bounded = (
        scalar
        - smooth_loss
        + joint_dyadic
        + prime_three
        + REGISTERED_JOINT_FLOOR_TARGET
    )
    return 58, harmonic(58) + bounded
