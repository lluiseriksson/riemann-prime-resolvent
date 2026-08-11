"""Exact audit of the parity-free Loewner resolvent identity.

This is a small rational-arithmetic factor check for Proposition 1 and
Lemma 1.1 of ``first-crossing-real-rooted-witness.md``.  It is not numerical
evidence for RH.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


Q = Fraction


def determinant(matrix: list[list[Q]]) -> Q:
    work = [row[:] for row in matrix]
    result = Q(1)
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result *= value
        for entry in range(column, len(work)):
            work[column][entry] /= value
        for row in range(column + 1, len(work)):
            scale = work[row][column]
            for entry in range(column, len(work)):
                work[row][entry] -= scale * work[column][entry]
    return result


def matmul(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def transpose(matrix: list[list[Q]]) -> list[list[Q]]:
    return [list(column) for column in zip(*matrix)]


def subtract(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def outer(left: list[Q], right: list[Q]) -> list[list[Q]]:
    return [[x * y for y in right] for x in left]


def cauchy(vector: list[Q], nodes: list[Q], value: Q) -> Q:
    return sum(coefficient / (value - node) for coefficient, node in zip(vector, nodes))


def main() -> None:
    nodes = list(map(Q, [-2, 0, 1, 4]))
    poles = list(map(Q, [-3, 2, 5]))
    weights = list(map(Q, [1, 2, 3]))

    features = [[Q(1, 1) / (pole - node) for node in nodes] for pole in poles]
    kernel = []
    for removed in range(len(nodes)):
        minor = [[row[column] for column in range(len(nodes)) if column != removed] for row in features]
        kernel.append((-1) ** removed * determinant(minor))

    loewner = [[Q(0) for _ in nodes] for _ in nodes]
    for weight, feature in zip(weights, features):
        for i, j in combinations(range(len(nodes)), 2):
            loewner[i][j] += weight * feature[i] * feature[j]
            loewner[j][i] = loewner[i][j]
        for i in range(len(nodes)):
            loewner[i][i] += weight * feature[i] ** 2

    multiple = [[Q(0) for _ in nodes] for _ in nodes]
    for weight, feature in zip(weights[:2], features[:2]):
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                multiple[i][j] += weight * feature[i] * feature[j]
    assert determinant([row[:2] for row in multiple[:2]]) != 0
    assert all(
        determinant([[multiple[i][j] for j in columns] for i in rows]) == 0
        for rows in combinations(range(len(nodes)), 3)
        for columns in combinations(range(len(nodes)), 3)
    )

    assert all(sum(loewner[i][j] * kernel[j] for j in range(len(nodes))) == 0 for i in range(len(nodes)))
    assert all(sum(multiple[i][j] * kernel[j] for j in range(len(nodes))) == 0 for i in range(len(nodes)))
    assert sum(features[2][j] * kernel[j] for j in range(len(nodes))) == 0
    assert determinant([row[:3] for row in loewner[:3]]) != 0
    assert all(cauchy(kernel, nodes, pole) == 0 for pole in poles)

    values = [sum(weight / (pole - node) for weight, pole in zip(weights, poles)) for node in nodes]
    base = Q(7)
    x = [Q(1) / (node - base) for node in nodes]
    beta = values
    eta = [Q(1) for _ in nodes]
    q = x
    p = [x_i * beta_i for x_i, beta_i in zip(x, beta)]
    c = sum(q_i * xi_i for q_i, xi_i in zip(q, kernel))
    assert c != 0
    x_kernel = [x_i * xi_i for x_i, xi_i in zip(x, kernel)]
    ell = [q_i / c for q_i in q]
    diagonal_x = [[x[i] if i == j else Q(0) for j in range(len(nodes))] for i in range(len(nodes))]
    x_prime = subtract(diagonal_x, outer(x_kernel, ell))
    assert subtract(matmul(loewner, x_prime), matmul(transpose(x_prime), loewner)) == [
        [Q(0) for _ in nodes] for _ in nodes
    ]

    for spectral in [Q(1, 3), Q(2, 3), Q(-1, 2)]:
        left_matrix = [
            [x_prime[i][j] - (spectral if i == j else Q(0)) for j in range(len(nodes))]
            for i in range(len(nodes))
        ]
        right_matrix = [
            [diagonal_x[i][j] - (spectral if i == j else Q(0)) for j in range(len(nodes))]
            for i in range(len(nodes))
        ]
        ratio = determinant(left_matrix) / determinant(right_matrix)
        target = -cauchy(kernel, nodes, base + Q(1) / spectral) / c
        assert ratio == target

    print("exact Loewner kernel: rank 3 with a one-dimensional nullspace")
    print("positive evaluation reduction: nullity 2 -> nullity 1")
    print("exact Cauchy zeros:", ", ".join(str(pole) for pole in poles))
    print("resolvent determinant identity: 3/3 rational points")


if __name__ == "__main__":
    main()
