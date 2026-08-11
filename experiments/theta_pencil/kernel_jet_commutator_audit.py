"""Exact lightweight audit of the first-kernel-jet commutator identities.

This checks Proposition 4.1a.4 with rational finite matrices.  It is an
algebra audit, not numerical evidence for the Riemann hypothesis.
"""

from __future__ import annotations

from fractions import Fraction as Q

Matrix = list[list[Q]]
Vector = list[Q]


def mm(left: Matrix, right: Matrix) -> Matrix:
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def madd(left: Matrix, right: Matrix, sign: int = 1) -> Matrix:
    return [
        [x + sign * y for x, y in zip(a, b, strict=True)]
        for a, b in zip(left, right, strict=True)
    ]


def mv(matrix: Matrix, vector: Vector) -> Vector:
    return [sum(x * y for x, y in zip(row, vector, strict=True)) for row in matrix]


def projection_formula() -> None:
    z = Q(0)
    A = [[z, z, z], [z, z, z], [z, z, Q(7)]]
    P = [[Q(1), z, z], [z, Q(1), z], [z, z, z]]
    Qp = [[z, z, z], [z, z, z], [z, z, Q(1)]]
    reduced = [[z, z, z], [z, z, z], [z, z, Q(1, 7)]]
    X = [[Q(2), Q(-3), Q(5)], [Q(-3), Q(11), Q(13)], [Q(5), Q(13), Q(-17)]]
    commutator = madd(mm(X, A), mm(A, X), -1)
    projector_commutator = madd(mm(P, X), mm(X, P), -1)
    source = madd(mm(mm(mm(P, commutator), reduced), Qp), mm(mm(mm(reduced, Qp), commutator), P))
    assert projector_commutator == source

    polynomial = [Q(19), Q(-23), Q(29)]
    w = mv(P, polynomial)
    next_jet = mv(P, mv(X, polynomial))
    correction = mv(projector_commutator, polynomial)
    assert next_jet == [x + y for x, y in zip(mv(X, w), correction, strict=True)]

    # Take p in the complementary space and w=P X p.  This is the finite
    # model of p=x^(k-1), w=P x^k.  It checks (PC9)--(PC11), including every
    # factor two in the double commutator.
    previous = [z, z, Q(1)]
    w = mv(P, mv(X, previous))
    c_w = mv(commutator, w)
    reduced_previous = mv(reduced, previous)
    assert sum(x * y for x, y in zip(reduced_previous, c_w, strict=True)) == -sum(
        x * x for x in w
    )
    a_x = mm(A, X)
    ax_minus_xa = madd(a_x, mm(X, A), -1)
    double = madd(mm(X, ax_minus_xa), mm(ax_minus_xa, X), -1)
    energy = sum(x * y for x, y in zip(w, mv(double, w), strict=True))
    reduced_energy = 2 * sum(
        x * y for x, y in zip(c_w, mv(reduced, c_w), strict=True)
    )
    assert energy == reduced_energy > 0
    left = energy * sum(
        x * y for x, y in zip(previous, reduced_previous, strict=True)
    )
    norm_fourth = 2 * sum(x * x for x in w) ** 2
    assert left >= norm_fourth


def translation_formula() -> None:
    z = Q(0)
    nodes = [Q(-2), Q(-1), z, Q(1), Q(2)]
    size, shift, weight = len(nodes), 2, Q(7, 5)
    X = [[nodes[i] if i == j else z for j in range(size)] for i in range(size)]
    plus = [[z for _ in range(size)] for _ in range(size)]
    minus = [[z for _ in range(size)] for _ in range(size)]
    for i in range(shift, size):
        plus[i][i - shift] = Q(1)
    for i in range(size - shift):
        minus[i][i + shift] = Q(1)
    block = [[-weight * (plus[i][j] + minus[i][j]) for j in range(size)] for i in range(size)]
    direct = madd(mm(X, block), mm(block, X), -1)
    expected = [[-weight * shift * (plus[i][j] - minus[i][j]) for j in range(size)] for i in range(size)]
    assert direct == expected

    # A second commutator turns the oriented difference into the symmetric
    # translation sum with the positive squared displacement in (PC12).
    ax_minus_xa = madd(mm(block, X), mm(X, block), -1)
    double = madd(mm(X, ax_minus_xa), mm(ax_minus_xa, X), -1)
    expected_double = [
        [weight * shift**2 * (plus[i][j] + minus[i][j]) for j in range(size)]
        for i in range(size)
    ]
    assert double == expected_double


def main() -> None:
    projection_formula()
    translation_formula()
    print("KERNEL-JET-COMMUTATOR-AUDIT: PASS (exact rational algebra)")


if __name__ == "__main__":
    main()
