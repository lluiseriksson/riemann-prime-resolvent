"""Second-Green tail bound for one touching cut-basis block.

After the first endpoint flux is removed, the adjacent logarithmic block is
``D g``.  Polynomial division isolates its only endpoint singularity as
``R_f(U) log(U)`` with polynomial ``R_f``.  Its high Legendre coefficients
are rational.  The remaining function is analytic on the closed interval and
is bounded with Wang's variation estimate using Arb Taylor arithmetic.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from experiments.theta_pencil.arb_cut_dominant import (
    _local_legendre_coefficients,
)
from experiments.theta_pencil.support_window import at_most_prime_three_boundary


@dataclass(frozen=True)
class SecondGreenAdjacentTail:
    target_length: float
    source_length: float
    first_degree: int
    degree_count: int
    derivative_order: int
    singular_explicit_upper: float
    singular_remainder_upper: float
    singular_frobenius_upper: float
    analytic_frobenius_upper: float
    total_upper: float
    weighted_singular_frobenius_upper: float
    weighted_analytic_frobenius_upper: float
    weighted_total_upper: float
    maximum_variation_upper: float
    precision: int
    subdivisions: int


@dataclass(frozen=True)
class SecondGreenSeparatedTail:
    target_length: float
    source_length: float
    gap: float
    first_degree: int
    degree_count: int
    derivative_order: int
    total_upper: float
    maximum_variation_upper: float
    precision: int
    subdivisions: int


@dataclass(frozen=True)
class SecondGreenSeparatedGeometricTail:
    target_length: float
    source_length: float
    gap: float
    first_degree: int
    eta_lower: float
    ratio_upper: float
    total_upper: float
    precision: int


@dataclass(frozen=True)
class SecondGreenAdjacentConstantGeometricTail:
    target_length: float
    source_length: float
    first_degree: int
    eta_lower: float
    ratio_upper: float
    total_upper: float
    precision: int


@dataclass(frozen=True)
class SecondGreenSelfTail:
    degree_count: int
    first_degree: int
    explicit_end: int
    total_upper: float
    precision: int


@dataclass(frozen=True)
class FirstWindowSecondGreenTails:
    half_width: float
    edge_to_center: SecondGreenAdjacentTail
    center_to_edge: SecondGreenAdjacentTail
    maximum_adjacent_upper: float


def _pad(values, size, arb):
    return list(values[:size]) + [arb(0) for _ in range(max(0, size - len(values)))]


def _float_upper(value) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def _add(left, right, size, arb):
    a = _pad(left, size, arb)
    b = _pad(right, size, arb)
    return [a[index] + b[index] for index in range(size)]


def _scale(values, scalar, size, arb):
    a = _pad(values, size, arb)
    return [scalar * value for value in a]


def _multiply(left, right, size, arb):
    result = [arb(0) for _ in range(size)]
    for i, a in enumerate(left[:size]):
        for j, b in enumerate(right[: size - i]):
            result[i + j] += a * b
    return result


def _derivative(values, size, arb):
    return _pad(
        [(index + 1) * values[index + 1] for index in range(len(values) - 1)],
        size,
        arb,
    )


def _inverse(values, size, arb):
    source = _pad(values, size, arb)
    result = [arb(0) for _ in range(size)]
    result[0] = 1 / source[0]
    for degree in range(1, size):
        result[degree] = -result[0] * sum(
            (source[index] * result[degree - index] for index in range(1, degree + 1)),
            arb(0),
        )
    return result


def _logarithm(values, size, arb):
    source = _pad(values, size, arb)
    inverse = _inverse(source, size, arb)
    derivative = _derivative(source, size, arb)
    quotient = _multiply(derivative, inverse, size, arb)
    result = [arb(0) for _ in range(size)]
    result[0] = source[0].log()
    for degree in range(1, size):
        result[degree] = quotient[degree - 1] / degree
    return result


def _polynomial_jet(coefficients, variable, size, arb):
    result = [arb(0) for _ in range(size)]
    for coefficient in reversed(coefficients):
        result = _multiply(result, variable, size, arb)
        result[0] += coefficient
    return result


def _polynomial_derivative(coefficients, arb):
    if len(coefficients) <= 1:
        return [arb(0)]
    return [index * coefficients[index] for index in range(1, len(coefficients))]


def _polynomial_add(left, right, arb):
    size = max(len(left), len(right))
    return _add(left, right, size, arb)


def _polynomial_multiply(left, right, arb):
    return _multiply(left, right, len(left) + len(right) - 1, arb)


def _source_decomposition(source, source_length, arb):
    """Return ``P(U)`` and ``f(-U)`` in ``I_f=P+f(-U) I_0``."""

    degree_count = len(source)
    polynomial = [arb(0) for _ in range(degree_count)]
    reflected = [arb(0) for _ in range(degree_count)]
    for power, coefficient in enumerate(source):
        reflected[power] = coefficient * (-1 if power % 2 else 1)
        for degree in range(power):
            polynomial[degree] += (
                coefficient
                * (-1 if degree % 2 else 1)
                * source_length ** (power - degree)
                / (power - degree)
            )
    return polynomial, reflected


def _singular_polynomial(reflected, target_length, arb):
    """Coefficients of ``R_f=(1/2) D_target[f(-U)]``."""

    first = _polynomial_derivative(reflected, arb)
    second = _polynomial_derivative(first, arb)
    u = [arb(0), arb(1)]
    a_minus_two_u = [target_length, -arb(2)]
    u_a_minus_u = [arb(0), target_length, -arb(1)]
    inside = _polynomial_add(
        _polynomial_multiply(a_minus_two_u, first, arb),
        _polynomial_multiply(u_a_minus_u, second, arb),
        arb,
    )
    return _scale(inside, -arb(1) / 2, len(inside), arb)


def _regular_jet(
    polynomial,
    reflected,
    target_length,
    source_length,
    point,
    output_order,
    arb,
):
    """Taylor jet of ``Dg-R_f log U`` at an Arb interval point."""

    work = output_order + 3
    variable = [point, arb(1)] + [arb(0) for _ in range(work - 2)]
    a_minus_u = _add([target_length], _scale(variable, -1, work, arb), work, arb)
    a_minus_two_u = _add(
        [target_length], _scale(variable, -2, work, arb), work, arb
    )
    u_a_minus_u = _multiply(variable, a_minus_u, work, arb)
    reflected_jet = _polynomial_jet(reflected, variable, work, arb)
    polynomial_jet = _polynomial_jet(polynomial, variable, work, arb)
    log_shifted = _logarithm(
        _add(variable, [source_length], work, arb), work, arb
    )

    # g = s + q log U, where only the logarithmic part is omitted here.
    smooth = _add(
        _scale(polynomial_jet, -arb(1) / 2, work, arb),
        _scale(
            _multiply(reflected_jet, log_shifted, work, arb),
            -arb(1) / 2,
            work,
            arb,
        ),
        work,
        arb,
    )
    q = _scale(reflected_jet, arb(1) / 2, work, arb)
    smooth_first = _derivative(smooth, work, arb)
    smooth_second = _derivative(smooth_first, work, arb)
    d_smooth = _scale(
        _add(
            _multiply(a_minus_two_u, smooth_first, work, arb),
            _multiply(u_a_minus_u, smooth_second, work, arb),
            work,
            arb,
        ),
        -1,
        work,
        arb,
    )
    q_first = _derivative(q, work, arb)
    regular_from_log = _add(
        q,
        _scale(_multiply(a_minus_u, q_first, work, arb), -2, work, arb),
        work,
        arb,
    )
    return _add(d_smooth, regular_from_log, output_order + 1, arb)


def _separated_jet(
    polynomial,
    reflected,
    target_length,
    source_length,
    gap,
    point,
    output_order,
    arb,
):
    """Taylor jet of ``D_target L f`` for a strictly separated block."""

    work = output_order + 3
    variable = [point, arb(1)] + [arb(0) for _ in range(work - 2)]
    shifted = _add(variable, [gap], work, arb)
    a_minus_u = _add(
        [target_length], _scale(variable, -1, work, arb), work, arb
    )
    a_minus_two_u = _add(
        [target_length], _scale(variable, -2, work, arb), work, arb
    )
    u_a_minus_u = _multiply(variable, a_minus_u, work, arb)
    reflected_jet = _polynomial_jet(reflected, shifted, work, arb)
    polynomial_jet = _polynomial_jet(polynomial, shifted, work, arb)
    log_ratio = _add(
        _logarithm(
            _add(shifted, [source_length], work, arb), work, arb
        ),
        _scale(_logarithm(shifted, work, arb), -1, work, arb),
        work,
        arb,
    )
    potential = _scale(
        _add(
            polynomial_jet,
            _multiply(reflected_jet, log_ratio, work, arb),
            work,
            arb,
        ),
        -arb(1) / 2,
        work,
        arb,
    )
    first = _derivative(potential, work, arb)
    second = _derivative(first, work, arb)
    return _scale(
        _add(
            _multiply(a_minus_two_u, first, work, arb),
            _multiply(u_a_minus_u, second, work, arb),
            work,
            arb,
        ),
        -1,
        output_order + 1,
        arb,
    )


def certify_second_green_separated_tail(
    target_length: float,
    source_length: float,
    gap: float,
    degree_count: int = 16,
    first_degree: int = 128,
    derivative_order: int = 12,
    subdivisions: int = 192,
    precision: int = 512,
) -> SecondGreenSeparatedTail:
    """Certify ``Q_N D_target L P_d`` for one separated block.

    Unlike a touching block, a positive gap makes the potential regular at
    both target endpoints.  Green's identity therefore has no endpoint flux,
    and Wang's Legendre coefficient estimate applies directly to
    ``D_target L f``.
    """

    if isinstance(target_length, (int, float)) and target_length <= 0:
        raise ValueError("interval lengths must be positive")
    if isinstance(source_length, (int, float)) and source_length <= 0:
        raise ValueError("interval lengths must be positive")
    if isinstance(gap, (int, float)) and gap <= 0:
        raise ValueError("the separation gap must be positive")
    if degree_count < 1 or first_degree <= degree_count:
        raise ValueError("first_degree must exceed the source degree count")
    if derivative_order < 1 or subdivisions < 1:
        raise ValueError("invalid derivative order or subdivision count")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = (
            arb(str(target_length))
            if isinstance(target_length, (int, float))
            else arb(target_length)
        )
        b = (
            arb(str(source_length))
            if isinstance(source_length, (int, float))
            else arb(source_length)
        )
        separation = (
            arb(str(gap)) if isinstance(gap, (int, float)) else arb(gap)
        )
        if not a.lower() > 0 or not b.lower() > 0 or not separation.lower() > 0:
            raise ValueError("length and gap balls must be strictly positive")
        source_rows = _local_legendre_coefficients(
            arb, b, degree_count, reversed_=False
        )
        decompositions = [
            _source_decomposition(row, b, arb) for row in source_rows
        ]
        variations = []
        requested_derivative = derivative_order + 1
        scale = (a / 2) ** requested_derivative * (a / 2).sqrt()
        for polynomial, reflected in decompositions:
            derivative_supremum = arb(0)
            for part in range(subdivisions):
                lower = a * part / subdivisions
                upper = a * (part + 1) / subdivisions
                midpoint = (lower + upper) / 2
                point = midpoint + arb(0, (upper - lower) / 2)
                jet = _separated_jet(
                    polynomial,
                    reflected,
                    a,
                    b,
                    separation,
                    point,
                    requested_derivative,
                    arb,
                )
                derivative = (
                    math.factorial(requested_derivative)
                    * jet[requested_derivative]
                    * scale
                )
                derivative_supremum = max(
                    derivative_supremum, derivative.abs_upper()
                )
            variations.append(2 * derivative_supremum)

        wang_constant = (
            2 ** (derivative_order + 1)
            / (
                arb.pi().sqrt()
                * arb(2 * derivative_order + 1).sqrt()
                * arb(first_degree - 1) ** (derivative_order + arb("0.5"))
            )
        )
        total = sum(
            (
                (wang_constant * variation).abs_upper() ** 2
                for variation in variations
            ),
            arb(0),
        ).sqrt()
    finally:
        ctx.prec = previous_precision

    return SecondGreenSeparatedTail(
        target_length=float(a.mid()),
        source_length=float(b.mid()),
        gap=float(separation.mid()),
        first_degree=first_degree,
        degree_count=degree_count,
        derivative_order=derivative_order,
        total_upper=_float_upper(total),
        maximum_variation_upper=_float_upper(max(variations)),
        precision=precision,
        subdivisions=subdivisions,
    )


def certify_second_green_separated_geometric_tail(
    target_length: float,
    source_length: float,
    gap: float,
    first_degree: int = 128,
    precision: int = 512,
) -> SecondGreenSeparatedGeometricTail:
    """Bound a separated ``Q_N D L`` block by Legendre ``Q_n`` decay.

    In normalized local coordinates the target coefficient of the kernel
    ``-1 / (2 (gap + u + v))`` is

    ``-sqrt((2n+1)/a) Q_n(1 + 2(gap+v)/a)``.

    Heine's positive integral for ``Q_n(cosh eta)`` and
    ``cosh(t) >= 1+t^2/2`` imply

    ``Q_n(cosh eta) <= sqrt(pi exp(eta)/(2 n sinh(eta))) exp(-(n+1)eta)``.

    The source projection is a contraction, so summing the resulting
    Hilbert--Schmidt envelope bounds every retained source degree at once.
    A geometric majorant handles the infinite polynomially weighted tail.
    """

    if isinstance(target_length, (int, float)) and target_length <= 0:
        raise ValueError("interval lengths must be positive")
    if isinstance(source_length, (int, float)) and source_length <= 0:
        raise ValueError("interval lengths must be positive")
    if isinstance(gap, (int, float)) and gap <= 0:
        raise ValueError("the separation gap must be positive")
    if first_degree < 1:
        raise ValueError("first_degree must be positive")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = (
            arb(str(target_length))
            if isinstance(target_length, (int, float))
            else arb(target_length)
        )
        b = (
            arb(str(source_length))
            if isinstance(source_length, (int, float))
            else arb(source_length)
        )
        separation = (
            arb(str(gap)) if isinstance(gap, (int, float)) else arb(gap)
        )
        if not a.lower() > 0 or not b.lower() > 0 or not separation.lower() > 0:
            raise ValueError("length and gap balls must be strictly positive")

        eta = (1 + 2 * separation / a).acosh()
        if not eta.lower() > 0:
            raise ArithmeticError("the separated-block ellipse was unresolved")
        q = (-2 * eta).exp()
        n = arb(first_degree)
        constant = b / a * arb.pi() * eta.exp() / (2 * eta.sinh())
        first_term = (
            constant
            * n
            * (n + 1) ** 2
            * (2 * n + 1)
            * q ** (first_degree + 1)
        )
        ratio = (
            q
            * (1 + arb(2) / n) ** 2
            * (1 + arb(2) / (2 * n + 1))
        )
        if not ratio.upper() < 1:
            raise ArithmeticError("the geometric Legendre-Q tail ratio is not below one")
        total = (first_term / (1 - ratio)).sqrt()
    finally:
        ctx.prec = previous_precision

    return SecondGreenSeparatedGeometricTail(
        target_length=float(a.mid()),
        source_length=float(b.mid()),
        gap=float(separation.mid()),
        first_degree=first_degree,
        eta_lower=math.nextafter(float(eta.lower()), -math.inf),
        ratio_upper=_float_upper(ratio),
        total_upper=_float_upper(total),
        precision=precision,
    )


def certify_second_green_adjacent_constant_geometric_tail(
    target_length: float,
    source_length: float,
    first_degree: int = 128,
    precision: int = 512,
) -> SecondGreenAdjacentConstantGeometricTail:
    """Bound a touching block with one retained constant source mode.

    Integrating the exact target coefficient over the normalized constant
    source gives a flux term plus

    ``sqrt(a/b)/2 * n(n+1)/sqrt(2n+1) * (Q_(n-1)(z)-Q_(n+1)(z))``,

    where ``z=1+2b/a``.  The first Green flux removes the nondecaying term.
    Bounding the remaining difference by ``Q_(n-1)`` and applying the same
    Heine envelope as the separated-block certificate gives a geometric
    Hilbert--Schmidt tail.  This avoids derivative bounds that are singular
    when the source interval is short.
    """

    if isinstance(target_length, (int, float)) and target_length <= 0:
        raise ValueError("interval lengths must be positive")
    if isinstance(source_length, (int, float)) and source_length <= 0:
        raise ValueError("interval lengths must be positive")
    if first_degree < 2:
        raise ValueError("first_degree must be at least two")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = (
            arb(str(target_length))
            if isinstance(target_length, (int, float))
            else arb(target_length)
        )
        b = (
            arb(str(source_length))
            if isinstance(source_length, (int, float))
            else arb(source_length)
        )
        if not a.lower() > 0 or not b.lower() > 0:
            raise ValueError("interval-length balls must be strictly positive")

        eta = (1 + 2 * b / a).acosh()
        if not eta.lower() > 0:
            raise ArithmeticError("the adjacent-block ellipse was unresolved")
        q = (-2 * eta).exp()
        n = arb(first_degree)
        constant = a / b * arb.pi() * eta.exp() / (8 * eta.sinh())
        first_term = (
            constant
            * n**2
            * (n + 1) ** 2
            / ((2 * n + 1) * (n - 1))
            * q**first_degree
        )
        ratio = q * (1 + arb(2) / n) ** 2
        if not ratio.upper() < 1:
            raise ArithmeticError("the adjacent Legendre-Q tail ratio is not below one")
        total = (first_term / (1 - ratio)).sqrt()
    finally:
        ctx.prec = previous_precision

    return SecondGreenAdjacentConstantGeometricTail(
        target_length=float(a.mid()),
        source_length=float(b.mid()),
        first_degree=first_degree,
        eta_lower=math.nextafter(float(eta.lower()), -math.inf),
        ratio_upper=_float_upper(ratio),
        total_upper=_float_upper(total),
        precision=precision,
    )


def certify_second_green_self_tail(
    degree_count: int = 16,
    first_degree: int = 128,
    explicit_end: int = 4096,
    precision: int = 256,
) -> SecondGreenSelfTail:
    """Certify the self-block tail after removal of both endpoint fluxes."""

    if degree_count < 1 or first_degree <= degree_count:
        raise ValueError("first_degree must exceed the source degree count")
    if explicit_end <= first_degree:
        raise ValueError("explicit_end must exceed first_degree")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        total_square = arb(0)
        for source in range(degree_count):
            source_eigenvalue = source * (source + 1)
            for target in range(first_degree, explicit_end):
                if (target - source) % 2:
                    continue
                target_eigenvalue = target * (target + 1)
                value = (
                    arb((2 * target + 1) * (2 * source + 1)).sqrt()
                    * source_eigenvalue
                    / (target_eigenvalue - source_eigenvalue)
                )
                total_square += value**2
            ratio = arb(source_eigenvalue) / explicit_end**2
            total_square += (
                arb(3)
                * (2 * source + 1)
                * source_eigenvalue**2
                / (1 - ratio) ** 2
                / (2 * (explicit_end - 1) ** 2)
            )
        total = total_square.sqrt()
    finally:
        ctx.prec = previous_precision

    return SecondGreenSelfTail(
        degree_count=degree_count,
        first_degree=first_degree,
        explicit_end=explicit_end,
        total_upper=_float_upper(total),
        precision=precision,
    )


def certify_second_green_adjacent_tail(
    target_length: float,
    source_length: float,
    degree_count: int = 16,
    first_degree: int = 128,
    derivative_order: int = 6,
    explicit_end: int = 4096,
    subdivisions: int = 128,
    precision: int = 256,
    moment_order: int = 8,
    analytic_method: str = "wang",
) -> SecondGreenAdjacentTail:
    """Certify one oriented touching-block tail after the first Green flux."""

    if isinstance(target_length, (int, float)) and target_length <= 0:
        raise ValueError("interval lengths must be positive")
    if isinstance(source_length, (int, float)) and source_length <= 0:
        raise ValueError("interval lengths must be positive")
    if degree_count < 1 or first_degree <= degree_count:
        raise ValueError("first_degree must exceed the source degree count")
    if (
        derivative_order < 1
        or explicit_end <= first_degree
        or subdivisions < 1
        or moment_order < 1
    ):
        raise ValueError("invalid derivative order, explicit end, or subdivisions")
    if analytic_method not in {"wang", "geometric"}:
        raise ValueError("analytic_method must be 'wang' or 'geometric'")
    try:
        from flint import arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = (
            arb(str(target_length))
            if isinstance(target_length, (int, float))
            else arb(target_length)
        )
        b = (
            arb(str(source_length))
            if isinstance(source_length, (int, float))
            else arb(source_length)
        )
        if not a.lower() > 0 or not b.lower() > 0:
            raise ValueError("interval-length balls must be strictly positive")
        source_rows = _local_legendre_coefficients(
            arb, b, degree_count, reversed_=False
        )
        target_rows = _local_legendre_coefficients(
            arb, a, degree_count, reversed_=True
        )

        decompositions = [_source_decomposition(row, b, arb) for row in source_rows]
        singular_polynomials = [
            _singular_polynomial(reflected, a, arb)
            for _, reflected in decompositions
        ]
        singular_map = arb_mat(degree_count, degree_count)
        for target_degree, target in enumerate(target_rows):
            for source_degree, singular in enumerate(singular_polynomials):
                integral = arb(0)
                for left, left_value in enumerate(target):
                    for right, right_value in enumerate(singular):
                        integral += (
                            left_value
                            * right_value
                            * a ** (left + right + 1)
                            / (left + right + 1)
                        )
                singular_map[target_degree, source_degree] = integral

        singular_square = arb(0)
        weighted_singular_square = arb(0)
        maximum_eigenvalue = (degree_count - 1) * degree_count
        for degree in range(first_degree, explicit_end):
            eigenvalue = degree * (degree + 1)
            row = arb_mat(1, degree_count)
            for source in range(degree_count):
                row[0, source] = sum(
                    (
                        -arb((2 * degree + 1) * (2 * low + 1)).sqrt()
                        / (eigenvalue - low * (low + 1))
                        * singular_map[low, source]
                        for low in range(degree_count)
                    ),
                    arb(0),
                )
            row_square = sum(
                (
                    row[0, source].abs_upper() ** 2
                    for source in range(degree_count)
                ),
                arb(0),
            )
            singular_square += row_square
            weighted_singular_square += row_square / eigenvalue**2

        singular_explicit = singular_square.sqrt()
        weighted_singular_explicit = weighted_singular_square.sqrt()

        # Preserve signed endpoint moments in the expansion
        # 1/(lambda_n-lambda_k).  An absolute Frobenius bound on R itself is
        # catastrophically lossy because its large polynomial values at the
        # opposite endpoint cancel from every low moment.
        singular_remainder = arb(0)
        weighted_singular_remainder = arb(0)
        for order in range(moment_order):
            moment_square = arb(0)
            for source in range(degree_count):
                moment = sum(
                    (
                        arb(2 * low + 1).sqrt()
                        * (low * (low + 1)) ** order
                        * singular_map[low, source]
                        for low in range(degree_count)
                    ),
                    arb(0),
                )
                moment_square += moment.abs_upper() ** 2
            exponent = 4 * order + 3
            scalar_tail = (
                arb(1) / explicit_end**exponent
                + arb(1)
                / ((exponent - 1) * explicit_end ** (exponent - 1))
            )
            singular_remainder += (3 * scalar_tail * moment_square).sqrt()
            weighted_exponent = exponent + 4
            weighted_scalar_tail = (
                arb(1) / explicit_end**weighted_exponent
                + arb(1)
                / (
                    (weighted_exponent - 1)
                    * explicit_end ** (weighted_exponent - 1)
                )
            )
            weighted_singular_remainder += (
                3 * weighted_scalar_tail * moment_square
            ).sqrt()

        absolute_moment_square = arb(0)
        for source in range(degree_count):
            absolute_moment = sum(
                (
                    arb(2 * low + 1).sqrt()
                    * (low * (low + 1)) ** moment_order
                    * singular_map[low, source].abs_upper()
                    for low in range(degree_count)
                ),
                arb(0),
            )
            absolute_moment_square += absolute_moment**2
        exponent = 4 * moment_order + 3
        scalar_tail = (
            arb(1) / explicit_end**exponent
            + arb(1) / ((exponent - 1) * explicit_end ** (exponent - 1))
        )
        ratio = arb(maximum_eigenvalue) / (explicit_end * (explicit_end + 1))
        singular_remainder += (
            3 * scalar_tail * absolute_moment_square
        ).sqrt() / (1 - ratio)
        weighted_exponent = exponent + 4
        weighted_scalar_tail = (
            arb(1) / explicit_end**weighted_exponent
            + arb(1)
            / (
                (weighted_exponent - 1)
                * explicit_end ** (weighted_exponent - 1)
            )
        )
        weighted_singular_remainder += (
            3 * weighted_scalar_tail * absolute_moment_square
        ).sqrt() / (1 - ratio)
        singular_upper = singular_explicit + singular_remainder
        weighted_singular_upper = (
            weighted_singular_explicit + weighted_singular_remainder
        )

        if analytic_method == "geometric":
            # Above the source polynomial degree, the regular analytic
            # coefficient is -lambda_n/2 times the coefficient of
            # q(u) log(u+b). Multiplication by a degree-k polynomial is
            # (2k+1)-banded in the Legendre basis. Two banded Cauchy bounds,
            # ||q||_infinity <= sqrt((2k+1)/b), and Heine decay for the
            # coefficients of log(u+b) give the following column envelope.
            eta = (1 + 2 * b / a).acosh()
            if not eta.lower() > 0:
                raise ArithmeticError("the adjacent analytic ellipse was unresolved")
            q_decay = (-2 * eta).exp()
            common = a * arb.pi() * eta.exp() / (8 * b * eta.sinh())
            analytic_square = arb(0)
            for source_degree in range(degree_count):
                first_base = first_degree - source_degree
                if first_base < 2:
                    raise ValueError(
                        "first_degree must exceed the source degree by at least two"
                    )
                m = arb(first_base)
                shifted = m + source_degree
                # The reflected source polynomial is evaluated on the
                # target interval, not on its original source interval.
                # Its normalized supremum therefore contains
                # P_k(1+2a/b); omitting this extrapolation factor is unsound
                # when the source block is short.
                extrapolation = (1 + 2 * a / b).legendre_p(source_degree)
                first_term = (
                    common
                    * (2 * source_degree + 1) ** 3
                    * extrapolation.abs_upper() ** 2
                    * (shifted * (shifted + 1)) ** 2
                    / ((2 * m + 1) * (m - 1))
                    * q_decay**first_base
                )
                ratio = q_decay * (
                    1 + arb(2) / (m + source_degree)
                ) ** 2
                if not ratio.upper() < 1:
                    raise ArithmeticError(
                        "the adjacent analytic Legendre-Q ratio is not below one"
                    )
                analytic_square += first_term / (1 - ratio)
            analytic_upper = analytic_square.sqrt()
            variations = [arb(0)]
        else:
            variations = []
            requested_derivative = derivative_order + 1
            scale = (a / 2) ** requested_derivative * (a / 2).sqrt()
            for polynomial, reflected in decompositions:
                derivative_supremum = arb(0)
                for part in range(subdivisions):
                    lower = a * part / subdivisions
                    upper = a * (part + 1) / subdivisions
                    midpoint = (lower + upper) / 2
                    point = midpoint + arb(0, (upper - lower) / 2)
                    jet = _regular_jet(
                        polynomial,
                        reflected,
                        a,
                        b,
                        point,
                        requested_derivative,
                        arb,
                    )
                    derivative = (
                        math.factorial(requested_derivative)
                        * jet[requested_derivative]
                        * scale
                    )
                    derivative_supremum = max(
                        derivative_supremum, derivative.abs_upper()
                    )
                variations.append(2 * derivative_supremum)

            wang_constant = (
                2 ** (derivative_order + 1)
                / (
                    arb.pi().sqrt()
                    * arb(2 * derivative_order + 1).sqrt()
                    * arb(first_degree - 1) ** (derivative_order + arb("0.5"))
                )
            )
            analytic_upper = sum(
                (
                    (wang_constant * variation).abs_upper() ** 2
                    for variation in variations
                ),
                arb(0),
            ).sqrt()
        total = singular_upper + analytic_upper
        first_eigenvalue = first_degree * (first_degree + 1)
        weighted_analytic_upper = analytic_upper / first_eigenvalue
        weighted_total = weighted_singular_upper + weighted_analytic_upper
    finally:
        ctx.prec = previous_precision

    return SecondGreenAdjacentTail(
        target_length=float(a.mid()),
        source_length=float(b.mid()),
        first_degree=first_degree,
        degree_count=degree_count,
        derivative_order=derivative_order,
        singular_explicit_upper=_float_upper(singular_explicit),
        singular_remainder_upper=_float_upper(singular_remainder),
        singular_frobenius_upper=_float_upper(singular_upper),
        analytic_frobenius_upper=_float_upper(analytic_upper),
        total_upper=_float_upper(total),
        weighted_singular_frobenius_upper=_float_upper(weighted_singular_upper),
        weighted_analytic_frobenius_upper=_float_upper(weighted_analytic_upper),
        weighted_total_upper=_float_upper(weighted_total),
        maximum_variation_upper=_float_upper(max(variations)),
        precision=precision,
        subdivisions=subdivisions,
    )


def certify_first_window_second_green_tails(
    half_width: float,
    degree_count: int = 16,
    first_degree: int = 128,
    derivative_order: int = 12,
    explicit_end: int = 4096,
    subdivisions: int = 192,
    precision: int = 512,
    moment_order: int = 8,
) -> FirstWindowSecondGreenTails:
    """Certify both touching orientations using exact ``log(2)/a`` balls."""

    if not 0.5 <= half_width or not at_most_prime_three_boundary(half_width):
        raise ValueError("require 1/2 <= a <= log(3)/2")
    try:
        from flint import arb, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    previous_precision = ctx.prec
    try:
        ctx.prec = precision
        a = arb(str(half_width))
        displacement = arb.const_log2() / a
        edge = 2 - displacement
        center = 2 * displacement - 2
        edge_to_center = certify_second_green_adjacent_tail(
            edge,
            center,
            degree_count,
            first_degree,
            derivative_order,
            explicit_end,
            subdivisions,
            precision,
            moment_order,
        )
        center_to_edge = certify_second_green_adjacent_tail(
            center,
            edge,
            degree_count,
            first_degree,
            derivative_order,
            explicit_end,
            subdivisions,
            precision,
            moment_order,
        )
    finally:
        ctx.prec = previous_precision

    return FirstWindowSecondGreenTails(
        half_width=half_width,
        edge_to_center=edge_to_center,
        center_to_edge=center_to_edge,
        maximum_adjacent_upper=max(
            edge_to_center.total_upper, center_to_edge.total_upper
        ),
    )
