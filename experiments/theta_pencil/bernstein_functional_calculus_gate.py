"""Certified obstruction to a Bernstein-subordination proof of Pick positivity.

For eta > 1/2, put L(eta) = xi'(1/2 + eta) / xi(1/2 + eta), as in
``euler-axis-pick.md``.  A Bernstein function has completely monotone
derivative, hence L'''(eta) >= 0.  This module proves the opposite sign at
eta = 5/2 (equivalently s = 3) by summing the absolutely convergent von
Mangoldt series through a finite cutoff and bounding the omitted tail
elementarily.

The computation is local-light and uses only the Python standard library.
It is an audit of an analytic inequality, not numerical evidence for RH.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, localcontext
import json


PRECISION = 80
CUTOFF = 100_000
PI = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
)


@dataclass(frozen=True)
class BernsteinCertificate:
    """Enclosure data for the exact inequality L'''(5/2) < 0."""

    cutoff: int
    finite_prime_power_sum: str
    elementary_tail_upper_bound: str
    rounding_allowance: str
    threshold: str
    l_third_upper_bound: str


def primes_through(limit: int) -> list[int]:
    """Return all primes at most ``limit`` with an Eratosthenes sieve."""

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, int(limit**0.5) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [value for value in range(2, limit + 1) if sieve[value]]


def finite_von_mangoldt_sum(limit: int) -> Decimal:
    """Compute sum_{n<=limit} Lambda(n) log(n)^3 / n^3.

    For n = p^k the summand is k^3 log(p)^4 / p^(3k).  Enumerating prime
    powers avoids any floating-point factorization or approximation of
    Lambda.
    """

    total = Decimal(0)
    for prime in primes_through(limit):
        log_prime = Decimal(prime).ln()
        prime_power = prime
        exponent = 1
        while prime_power <= limit:
            total += (
                Decimal(exponent**3)
                * log_prime**4
                / Decimal(prime_power**3)
            )
            if prime_power > limit // prime:
                break
            prime_power *= prime
            exponent += 1
    return total


def logarithmic_tail_upper_bound(limit: int) -> Decimal:
    """Bound sum_{n>R} Lambda(n) log(n)^3/n^3 by an integral.

    Since Lambda(n) <= log(n) and log(x)^4/x^3 is decreasing for x >= R,
    the tail is at most

      R^-2 (log(R)^4/2 + log(R)^3 + 3 log(R)^2/2
             + 3 log(R)/2 + 3/4).
    """

    radius = Decimal(limit)
    logarithm = radius.ln()
    polynomial = (
        logarithm**4 / 2
        + logarithm**3
        + Decimal(3) * logarithm**2 / 2
        + Decimal(3) * logarithm / 2
        + Decimal(3) / 4
    )
    return polynomial / radius**2


def bernstein_certificate(limit: int = CUTOFF) -> BernsteinCertificate:
    """Return an enclosure proving centered L'''(5/2) is strictly negative."""

    with localcontext() as context:
        context.prec = PRECISION
        finite_sum = finite_von_mangoldt_sum(limit)
        tail = logarithmic_tail_upper_bound(limit)
        # Decimal.ln is correctly rounded.  This allowance is vastly larger
        # than the accumulated 80-digit rounding error and is still tiny
        # compared with the certified 3e-4 gap.
        rounding_allowance = Decimal("1e-60")
        threshold = (
            Decimal(6) * (Decimal(1) / Decimal(3) ** 4 + Decimal(1) / 2**4)
            - (PI**4 - Decimal(96)) / Decimal(16)
        )
        upper = finite_sum + tail + rounding_allowance - threshold
        assert upper < Decimal("-0.00034")
        return BernsteinCertificate(
            cutoff=limit,
            finite_prime_power_sum=str(finite_sum),
            elementary_tail_upper_bound=str(tail),
            rounding_allowance=str(rounding_allowance),
            threshold=str(threshold),
            l_third_upper_bound=str(upper),
        )


def main() -> None:
    print(json.dumps(asdict(bernstein_certificate()), indent=2))


if __name__ == "__main__":
    main()
