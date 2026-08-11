"""Exact algebra audit for Proposition 4.1a.1.

This checks the finite-dimensional algebra used by the proof:

* a Fourier evaluation is a rank-one Cauchy--Loewner form;
* symmetric evaluations separate even and odd restrictions;
* the dimension counts in the unbalanced and balanced cases are exact.

It does not test RH or the analytic form-core theorem.  All arithmetic below
uses fractions.
"""

from __future__ import annotations

from fractions import Fraction


def rank(matrix: list[list[Fraction]]) -> int:
    """Return row rank by exact Gaussian elimination."""
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][col]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][col]:
                continue
            factor = work[row][col]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def cauchy_loewner_audit() -> None:
    nodes = [Fraction(n) for n in (-2, -1, 0, 1, 2)]
    for pole in (Fraction(1, 3), Fraction(2, 5)):
        evaluation = [1 / (node - pole) for node in nodes]
        generator = [-1 / (node - pole) for node in nodes]
        for i, left in enumerate(nodes):
            for j, right in enumerate(nodes):
                if i == j:
                    continue
                divided_difference = (
                    generator[i] - generator[j]
                ) / (left - right)
                assert divided_difference == evaluation[i] * evaluation[j]


def parity_rank_audit() -> None:
    # Unbalanced p=3, q=1.  k=p-1 symmetric pairs leave one even line.
    points = [Fraction(1), Fraction(2)]
    even = [[1, point**2, point**4] for point in points]
    odd = [[point] for point in points]
    assert rank(even) == 2
    assert rank(odd) == 1
    assert (3 - rank(even)) + (1 - rank(odd)) == 1

    # The reflected case p=1, q=3 leaves one odd line.
    even_reflected = [[1] for _ in points]
    odd_reflected = [[point, point**3, point**5] for point in points]
    assert rank(even_reflected) == 1
    assert rank(odd_reflected) == 2
    assert (1 - rank(even_reflected)) + (3 - rank(odd_reflected)) == 1

    # Balanced p=q=2.  One symmetric pair leaves one line per sector.
    # Evaluation at zero is independent on the even survivor and vanishes
    # identically on the odd sector, so it leaves one pure odd line.
    point = Fraction(1)
    even_pair = [[1, point**2]]
    odd_pair = [[point, point**3]]
    at_zero_even = [Fraction(1), Fraction(0)]
    at_zero_odd = [Fraction(0), Fraction(0)]
    assert rank(even_pair) == rank(odd_pair) == 1
    assert rank(even_pair + [at_zero_even]) == 2
    assert rank(odd_pair + [at_zero_odd]) == 1
    remaining = (2 - rank(even_pair + [at_zero_even])) + (
        2 - rank(odd_pair + [at_zero_odd])
    )
    assert remaining == 1


def main() -> None:
    cauchy_loewner_audit()
    parity_rank_audit()
    print("SYMMETRIC-EVALUATION-PURIFICATION-AUDIT: PASS")


if __name__ == "__main__":
    main()
