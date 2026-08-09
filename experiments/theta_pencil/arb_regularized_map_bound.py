"""Arb proof of the regularized logarithmic-tail operator bound at a=1/2."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from experiments.theta_pencil.regularized_tail_gate import (
    maximum_regularized_map_bound,
)


@dataclass(frozen=True)
class RegularizedMapBound:
    local_d_a2_upper: float
    local_vd_frobenius_upper: float
    local_polynomial_frobenius_upper: float
    derivative_upper: float
    adjacent_upper: float
    distant_upper: float
    global_upper: float
    even_gate: float
    precision: int


def _legendre_monomials(degree_count: int) -> list[list[Fraction]]:
    rows = [[Fraction(1)]]
    if degree_count > 1:
        rows.append([Fraction(0), Fraction(1)])
    for degree in range(1, degree_count - 1):
        following = [Fraction(0)] * (len(rows[-1]) + 1)
        for index, value in enumerate(rows[-1]):
            following[index + 1] += Fraction(2 * degree + 1, degree + 1) * value
        for index, value in enumerate(rows[-2]):
            following[index] -= Fraction(degree, degree + 1) * value
        rows.append(following)
    return rows


def certify_regularized_map_bound(
    degree_count: int = 16,
    precision: int = 256,
) -> RegularizedMapBound:
    """Prove ||f -> D(L f)|| < 2537 on the local polynomial space.

    The proof uses Green's identity after the six endpoint fluxes have been
    removed.  A touching cross block is transferred to the source Legendre
    operator.  Its commutator kernel is an integration-by-parts derivative
    of v/(Au+Bv)^2, whose Mellin norm is pi/2.  The separated edge--edge
    block is bounded by its elementary Hilbert--Schmidt supremum.
    """

    if degree_count != 16:
        raise ValueError("the registered constants are for degree_count=16")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        d = degree_count
        polynomials = _legendre_monomials(d)

        def log_square_moment(power: int):
            # Integral x^(2 power) log^2(1-x^2) dx.  This is the second
            # beta derivative at (power+1/2,1), written at half integers.
            odd_sum = sum(
                (arb(1) / (2 * index - 1) for index in range(1, power + 2)),
                arb(0),
            )
            odd_square_sum = sum(
                (
                    arb(1) / (2 * index - 1) ** 2
                    for index in range(1, power + 2)
                ),
                arb(0),
            )
            digamma_difference = 2 * arb.const_log2() - 2 * odd_sum
            trigamma_difference = -arb.pi() ** 2 / 3 + 4 * odd_square_sum
            return (
                arb(2)
                / (2 * power + 1)
                * (digamma_difference**2 + trigamma_difference)
            )

        vd_frobenius_square = arb(0)
        for degree, polynomial in enumerate(polynomials):
            integral = arb(0)
            for left, left_value in enumerate(polynomial):
                for right, right_value in enumerate(polynomial):
                    if (left + right) % 2:
                        continue
                    rational = left_value * right_value
                    integral += (
                        arb(rational.numerator)
                        / rational.denominator
                        * log_square_moment((left + right) // 2)
                    )
            # phi_n^2 contributes (2n+1)/2 and V^2 contributes 1/4.
            integral *= arb(2 * degree + 1) / 8
            eigenvalue = degree * (degree + 1)
            vd_frobenius_square += eigenvalue**2 * integral
        vd_frobenius = vd_frobenius_square.sqrt()
        if not vd_frobenius.upper() < 506:
            raise ArithmeticError("the V D Frobenius bound did not close")

        derivative = arb_mat(d, d)
        for source in range(d):
            for target in range(source):
                if (source - target) % 2:
                    derivative[target, source] = arb(
                        (2 * source + 1) * (2 * target + 1)
                    ).sqrt()
        derivative_gram = derivative.transpose() * derivative
        derivative_eigenvalues = derivative_gram.eig(
            multiple=True, algorithm="rump"
        )
        derivative_upper = max(
            value.real.upper() for value in derivative_eigenvalues
        ).sqrt()
        if not derivative_upper.upper() < 87:
            raise ArithmeticError("the polynomial derivative bound did not close")

        multiply_x = arb_mat(d, d)
        for source in range(d):
            if source + 1 < d:
                multiply_x[source + 1, source] = arb(source + 1) / arb(
                    (2 * source + 1) * (2 * source + 3)
                ).sqrt()
            if source > 0:
                multiply_x[source - 1, source] = arb(source) / arb(
                    (2 * source - 1) * (2 * source + 1)
                ).sqrt()
        polynomial_part = -2 * multiply_x * derivative
        for index in range(d):
            polynomial_part[index, index] -= 1
        polynomial_frobenius = sum(
            (
                polynomial_part[row, column] ** 2
                for row in range(d)
                for column in range(d)
            ),
            arb(0),
        ).sqrt()
        if not polynomial_frobenius.upper() < 246:
            raise ArithmeticError("the polynomial Frobenius bound did not close")

        harmonic = arb(0)
        d_a2 = arb(0)
        for degree in range(1, d):
            harmonic += arb(1) / degree
            d_a2 = max(d_a2, arb(degree * (degree + 1)) * harmonic)
        if not d_a2.upper() < 797:
            raise ArithmeticError("the D A2 bound did not close")

        log_two = arb.const_log2()
        edge = 2 - 2 * log_two
        center = 4 * log_two - 2
        lengths = ((edge, center), (center, edge))
        commutator = arb(0)
        boundary = arb(0)
        for target_length, source_length in lengths:
            commutator = max(
                commutator,
                (target_length + source_length)
                / source_length
                * arb.pi()
                / 2
                * derivative_upper,
            )
            boundary_function_square = (
                (target_length + source_length) ** 2
                / (6 * source_length**2)
                - source_length / (6 * (target_length + source_length))
            )
            boundary = max(
                boundary,
                boundary_function_square.sqrt() * arb(d) / arb(2).sqrt(),
            )
        touching = arb.pi() / 2 * (d - 1) * d + commutator + boundary
        if not touching.upper() < 697:
            raise ArithmeticError("the adjacent cross-block bound did not close")

        # Direct pointwise derivative bound for the separated edge--edge
        # kernel, followed by sqrt(area)=2 for its Hilbert--Schmidt norm.
        separated_supremum = (
            edge**2 / (4 * center**2) + edge**3 / (8 * center**3)
        )
        separated = 2 * separated_supremum
        if not separated.upper() < 1:
            raise ArithmeticError("the separated cross-block bound did not close")

        # The block-norm comparison matrix has diagonal <1549, adjacent
        # entries <697 and the separated edge entry <1.  Its norm is at most
        # diagonal + sqrt(2)*adjacent + separated.
        global_bound = arb(1549) + arb(2).sqrt() * 697 + 1
        if not global_bound.upper() < 2537:
            raise ArithmeticError("the global regularized map bound did not close")

        perturbation_floor = arb("0.14076327914588865") - arb(25) / 12
        harmonic_128 = sum(
            (arb(1) / degree for degree in range(1, 129)), arb(0)
        )
        tail_floor = harmonic_128 + perturbation_floor
    finally:
        ctx.prec = previous_precision

    even_gate = maximum_regularized_map_bound(
        128, 0.007, float(tail_floor.lower()), 0.01
    )
    if not float(global_bound.upper()) < even_gate:
        raise ArithmeticError("the regularized bound does not pass the even gate")
    return RegularizedMapBound(
        local_d_a2_upper=float(d_a2.upper()),
        local_vd_frobenius_upper=float(vd_frobenius.upper()),
        local_polynomial_frobenius_upper=float(polynomial_frobenius.upper()),
        derivative_upper=float(derivative_upper.upper()),
        adjacent_upper=float(touching.upper()),
        distant_upper=float(separated.upper()),
        global_upper=float(global_bound.upper()),
        even_gate=even_gate,
        precision=precision,
    )
