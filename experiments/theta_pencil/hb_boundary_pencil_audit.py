"""Lightweight algebra audit for Proposition 4.9.

This script checks only the elementary factorization and the finite-dimensional
spectral-projector limit used in the boundary Hermite--Biehler pencil.  The
real-zero input is Suzuki's Theorem 1.5, not a numerical claim made here.
The script is intentionally local-light: one process, negligible memory, and
well below one second on the desk machine.
"""

from __future__ import annotations

from fractions import Fraction

Gaussian = tuple[Fraction, Fraction]


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] - right[0], left[1] - right[1]


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gdiv(left: Gaussian, right: Gaussian) -> Gaussian:
    denominator = right[0] ** 2 + right[1] ** 2
    return (
        (left[0] * right[0] + left[1] * right[1]) / denominator,
        (left[1] * right[0] - left[0] * right[1]) / denominator,
    )


def parity_factorization(
    y: Fraction, deficiency: Fraction, even: Fraction, odd: Fraction
) -> None:
    left = (y + deficiency) ** 2 * (even + odd) ** 2 - (
        y - deficiency
    ) ** 2 * (even - odd) ** 2
    right = 4 * (y * even + deficiency * odd) * (
        deficiency * even + y * odd
    )
    assert left == right


def projector_limit() -> None:
    # Diagonal model for epsilon (A + epsilon I)^(-1) -> P_ker(A).
    eigenvalues = [Fraction(0), Fraction(0), Fraction(7, 10), Fraction(21, 10)]
    vector = [Fraction(2), Fraction(-3), Fraction(5), Fraction(11)]
    projection = vector[:2] + [Fraction(0), Fraction(0)]
    errors = []
    for epsilon in [Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000)]:
        scaled_resolvent = [
            epsilon * value / (eigenvalue + epsilon)
            for eigenvalue, value in zip(eigenvalues, vector, strict=True)
        ]
        error = sum(abs(x - y) for x, y in zip(scaled_resolvent, projection, strict=True))
        errors.append(error)
    assert errors[2] < errors[1] < errors[0]


def simple_kernel_cayley_check() -> None:
    one: Gaussian = Fraction(1), Fraction(0)
    imaginary_unit: Gaussian = Fraction(0), Fraction(1)
    for z in [Fraction(-7, 3), Fraction(2, 5), Fraction(11, 2)]:
        for c in [Fraction(1, 7), Fraction(3, 2), Fraction(9)]:
            z_gaussian: Gaussian = z, Fraction(0)
            ic: Gaussian = Fraction(0), c
            base_theta = gdiv(gsub(z_gaussian, ic), gadd(z_gaussian, ic))
            even_m = gmul(
                imaginary_unit,
                gdiv(gadd(one, base_theta), gsub(one, base_theta)),
            )
            odd_theta = -base_theta[0], -base_theta[1]
            odd_m = gmul(
                imaginary_unit,
                gdiv(gadd(one, odd_theta), gsub(one, odd_theta)),
            )
            assert even_m == (z / c, Fraction(0))
            assert odd_m == (-c / z, Fraction(0))


def scalar_amplitude_stieltjes_check() -> None:
    # Build the amplitude polynomial independently, differentiate it, and
    # compare its logarithmic derivative with the Stieltjes partial fractions.
    def multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
        product = [Fraction(0)] * (len(left) + len(right) - 1)
        for left_index, left_value in enumerate(left):
            for right_index, right_value in enumerate(right):
                product[left_index + right_index] += left_value * right_value
        return product

    def evaluate(coefficients: list[Fraction], point: Fraction) -> Fraction:
        value = Fraction(0)
        for coefficient in reversed(coefficients):
            value = value * point + coefficient
        return value

    order_at_zero = 3
    squared_zeros = [Fraction(4), Fraction(9), Fraction(25), Fraction(121)]
    amplitude = [Fraction(0)] * order_at_zero + [Fraction(1)]
    for zero in squared_zeros:
        amplitude = multiply(amplitude, [zero * zero, 2 * zero, Fraction(1)])
    derivative = [index * value for index, value in enumerate(amplitude)][1:]
    for x in [Fraction(1, 3), Fraction(2), Fraction(17, 2)]:
        phi = sum(Fraction(1, 1) / (x + zero) for zero in squared_zeros)
        log_derivative_amplitude = evaluate(derivative, x) / evaluate(amplitude, x)
        assert (log_derivative_amplitude - order_at_zero / x) / 2 == phi


def parity_sector_squared_node_no_go() -> None:
    # PSD rank-one Loewner data at positive squared nodes can have a negative
    # kernel-rational zero. Passing back through t=z^2 gives imaginary
    # z-zeros, so sectorwise Loewner reality is insufficient.
    matrix = [[Fraction(4), Fraction(2)], [Fraction(2), Fraction(1)]]
    kernel = [Fraction(1), Fraction(-2)]
    assert all(
        sum(matrix[row][column] * kernel[column] for column in range(2)) == 0
        for row in range(2)
    )
    assert matrix[0][0] >= 0
    assert matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2 == 0
    nodes = [Fraction(1), Fraction(4)]
    negative_zero = Fraction(-2)
    rational_value = sum(
        residue / (negative_zero - node)
        for residue, node in zip(kernel, nodes, strict=True)
    )
    assert rational_value == 0


def small_deficiency_pure_parity_limit() -> None:
    # If H(-z)=s H(z) and the boundary phase is exp(i theta)=s, the
    # coefficient of c^k in W is exactly 2 z H.  Terms carrying the explicit
    # deficiency factor ic start one order later.  This is the algebra in
    # (PE5); Hurwitz supplies the analytic real-zero conclusion.
    for parity in (Fraction(-1), Fraction(1)):
        for z in (Fraction(-7, 3), Fraction(2, 5), Fraction(11, 2)):
            for h_value in (Fraction(-5, 4), Fraction(3, 7)):
                reflected_h = parity * h_value
                leading = z * h_value + parity * z * reflected_h
                assert leading == 2 * z * h_value


def kernel_jet_normalization() -> None:
    # A parity-preserving projector whose first nonzero polynomial jet is k=1.
    # The first moment is the squared norm of that projected jet, and the
    # scalar-residue norm has no odd power immediately after c^(2k).
    monomial_zero = [Fraction(1), Fraction(0), Fraction(0)]
    monomial_one = [Fraction(0), Fraction(3), Fraction(0)]
    monomial_two = [Fraction(0), Fraction(0), Fraction(5)]
    monomial_three = [Fraction(0), Fraction(7), Fraction(0)]

    def project(vector: list[Fraction]) -> list[Fraction]:
        return [Fraction(0), vector[1], Fraction(0)]

    def inner(left: list[Fraction], right: list[Fraction]) -> Fraction:
        return sum(x * y for x, y in zip(left, right, strict=True))

    assert project(monomial_zero) == [0, 0, 0]
    jet = project(monomial_one)
    assert inner(jet, monomial_zero) == 0
    assert inner(jet, monomial_one) == inner(jet, jet) == 9
    assert inner(jet, project(monomial_two)) == 0

    # P exp(cx) through degree three.
    # Its only surviving coordinates are 3c + 7c^3/6, so the norm square
    # starts with 9c^2 and has no c^3 term.
    leading_residue = inner(jet, jet)
    cubic_residue = 2 * inner(jet, project(monomial_two)) / 2
    quartic_residue = (
        inner(project(monomial_two), project(monomial_two)) / 4
        + 2 * inner(jet, project(monomial_three)) / 6
    )
    assert leading_residue == 9
    assert cubic_residue == 0
    assert quartic_residue == 7


def main() -> None:
    for y in [Fraction(1, 7), Fraction(1), Fraction(5, 2), Fraction(13)]:
        for deficiency in [Fraction(1, 5), Fraction(1), Fraction(11, 3)]:
            for even, odd in [
                (Fraction(2), Fraction(3)),
                (Fraction(-5, 4), Fraction(7, 9)),
                (Fraction(0), Fraction(11, 6)),
            ]:
                parity_factorization(y, deficiency, even, odd)
    projector_limit()
    simple_kernel_cayley_check()
    scalar_amplitude_stieltjes_check()
    parity_sector_squared_node_no_go()
    small_deficiency_pure_parity_limit()
    kernel_jet_normalization()
    print("HB-PENCIL-AUDIT: PASS (exact rational algebra; spectral sanity check)")


if __name__ == "__main__":
    main()
