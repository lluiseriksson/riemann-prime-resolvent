import numpy as np

from experiments.theta_pencil.cut_adapted_prime_basis import (
    build_cut_adapted_prime_matrix,
    first_prime_partition,
)


def test_edge_intervals_are_exact_translates():
    partition = first_prime_partition(0.5)
    assert np.isclose(
        partition.left[0] + partition.displacement, partition.right[0]
    )
    assert np.isclose(
        partition.left[1] + partition.displacement, partition.right[1]
    )
    assert partition.left[1] == partition.center[0]
    assert partition.center[1] == partition.right[0]


def test_prime_block_diagonalizes_without_a_tail():
    result = build_cut_adapted_prime_matrix(0.5, 7, 5)
    transform = result.diagonalizing_transform
    assert np.max(np.abs(transform.T @ transform - np.eye(19))) < 1e-15
    conjugated = transform.T @ result.matrix @ transform
    assert np.max(np.abs(conjugated - np.diag(result.diagonal))) < 1e-15
    assert np.allclose(
        np.linalg.eigvalsh(result.matrix), np.sort(result.diagonal)
    )


def test_first_prime_partition_reaches_point_54():
    partition = first_prime_partition(0.54)
    assert partition.center[1] > partition.center[0]
