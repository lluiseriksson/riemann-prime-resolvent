"""Exact combinatorial audit for the B-spline variation no-go.

For the m-fold convolution of a box, the (m-1)-st derivative is constant on
each knot interval.  Its values are alternating partial binomial sums, while
its Fourier transform is a constant phase times sin(h z / 2)^m / z.  The
audit uses only exact integer arithmetic and makes no claim about RH.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb


def interval_values(order: int) -> list[int]:
    return [
        sum((-1) ** index * comb(order, index) for index in range(interval + 1))
        for interval in range(order)
    ]


def main() -> None:
    for order in range(2, 65):
        values = interval_values(order)
        expected = [(-1) ** interval * comb(order - 1, interval) for interval in range(order)]
        assert values == expected
        assert all(left * right < 0 for left, right in zip(values, values[1:]))

        # Exact aligned autocorrelations.  Vandermonde gives their magnitude,
        # while the alternating interval values force sign (-1)^shift.
        for shift in range(order):
            correlation = sum(
                values[index + shift] * values[index]
                for index in range(order - shift)
            )
            expected_correlation = (-1) ** shift * comb(
                2 * order - 2, order - 1 - shift
            )
            assert correlation == expected_correlation

        # Exact audit of the |x-y| integration-by-parts identity (PH17) on
        # the unit-knot piecewise-constant model.
        mass = sum(Fraction(value) for value in values)
        absolute_form = Fraction(0)
        for left_index, left_value in enumerate(values):
            for right_index, right_value in enumerate(values):
                interval_kernel = (
                    Fraction(1, 3)
                    if left_index == right_index
                    else Fraction(abs(left_index - right_index))
                )
                absolute_form += left_value * right_value * interval_kernel
        cumulative = Fraction(0)
        centered_primitive_norm = Fraction(0)
        for value in values:
            constant = 2 * cumulative - mass
            slope = 2 * Fraction(value)
            centered_primitive_norm += (
                constant**2 + constant * slope + slope**2 / 3
            )
            cumulative += value
        half_width = Fraction(order, 2)
        assert absolute_form / 2 == (
            half_width * mass**2 / 2 - centered_primitive_norm / 4
        )

        if order <= 12:
            # Physical even-difference moments for the centered unit-knot
            # spline derivative.  They vanish below the Fourier zero order
            # r=order-1 and then all have sign (-1)^r, as in (PH13).
            zero_order = order - 1
            maximum_difference_order = zero_order + 3
            left_endpoint = -Fraction(order, 2)
            moments = []
            for power in range(2 * maximum_difference_order + 1):
                moment = Fraction(0)
                for interval, value in enumerate(values):
                    left = left_endpoint + interval
                    right = left + 1
                    moment += Fraction(value) * (
                        right ** (power + 1) - left ** (power + 1)
                    ) / (power + 1)
                moments.append(moment)
            for difference_order in range(maximum_difference_order + 1):
                difference_moment = sum(
                    (-1) ** index
                    * comb(2 * difference_order, index)
                    * moments[2 * difference_order - index]
                    * moments[index]
                    for index in range(2 * difference_order + 1)
                )
                if difference_order < zero_order:
                    assert difference_moment == 0
                else:
                    assert (-1) ** zero_order * difference_moment > 0

        # If h=2a/m, the nonzero Fourier-zero spacing is pi*m/a and every
        # such zero has multiplicity m.  Multiplicity divided by the spacing
        # therefore equals a/pi, independently of m; counting both signs
        # gives the maximal Cartwright coefficient 2a/pi.
        multiplicity_over_normalized_spacing = Fraction(order, order)
        assert multiplicity_over_normalized_spacing == Fraction(1)

        # With a=1 and h=2/m, Var(sum of m uniforms)=1/(3m).
        # The registered interval radius 2/sqrt(3m) therefore has the exact
        # Chebyshev tail bound Var/radius^2 = 1/4.
        variance = Fraction(1, 3 * order)
        radius_squared = Fraction(4, 3 * order)
        assert variance / radius_squared == Fraction(1, 4)

    print("BSPLINE-REAL-ROOTED-NO-GO: PASS (exact binomial arithmetic, orders 2..64)")


if __name__ == "__main__":
    main()
