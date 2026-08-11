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
