"""RF-1 decimal smoke checks, not certificates for an infinite series.

Run this file directly to export the deterministic finite-tail observations.
The universal bound and summability are proved in PrimeTail.lean.
"""
from decimal import Decimal as D, localcontext
import json

import pytest


def mangoldt(n: int) -> D:
    """Independent trial division: log(p) for p^k, zero otherwise."""
    if n < 2:
        return D(0)
    p = 2
    while p * p <= n and n % p:
        p += 1
    if p * p > n:
        return D(n).ln()
    while n % p == 0:
        n //= p
    return D(p).ln() if n == 1 else D(0)


def majorant(delta: D, cutoff: D) -> D:
    return (-delta * cutoff.ln()).exp() * (
        cutoff.ln() / delta + 1 / delta**2
    )


CASES = [(3, '0.01', '1.01'), (3, '0.5', '1.5'),
         (3, '20', '21'), (4, '1', '3'),
         (16, '0.5', '2.5'), (64, '2', '3')]


def observation(n: int, delta: str, sigma: str) -> dict[str, str | int]:
    with localcontext() as ctx:
        ctx.prec = 60
        d, s = D(delta), D(sigma)
        partial = sum((mangoldt(k) / D(k)**s
                       for k in range(n + 1, n + 257)), D(0))
        bound = majorant(d, D(n))
        return dict(N=n, delta=delta, sigma=sigma, terms=256,
                    partial=str(partial), bound=str(bound))


@pytest.mark.parametrize('n,delta,sigma', CASES)
def test_finite_partial_tail(n: int, delta: str, sigma: str) -> None:
    row = observation(n, delta, sigma)
    assert D(0) < D(row['partial']) <= D(row['bound'])


def test_prime_powers_and_first_omitted_integer() -> None:
    with localcontext() as ctx:
        ctx.prec = 60
        assert mangoldt(1) == mangoldt(6) == mangoldt(12) == 0
        assert mangoldt(4) == mangoldt(8) == D(2).ln()
        assert mangoldt(9) == D(3).ln()
        # N=3 starts at 4: filtering to primes would lose this positive term.
        assert mangoldt(3 + 1) / D(4)**21 > 0


def test_noninteger_substitution_is_not_a_tail_bound() -> None:
    with localcontext() as ctx:
        ctx.prec = 60
        x = D(63) / 16
        first_omitted = mangoldt(4) / D(4)**21
        assert int(x) == 3
        assert first_omitted > majorant(D(20), x)
        assert first_omitted < majorant(D(20), D(3))


def test_integer_square_scaling() -> None:
    with localcontext() as ctx:
        ctx.prec = 60
        a, lam, n = D(1), D(2), D(4)
        assert lam**2 == n
        assert majorant(a - D('0.5'), n) / (2*a) == (
            majorant(a - D('0.5'), lam**2) / (2*a))


if __name__ == '__main__':
    print(json.dumps(dict(kind='decimal-smoke-not-certificate', precision=60,
                          cases=[observation(*case) for case in CASES]), indent=2))
