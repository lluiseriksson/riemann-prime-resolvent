import numpy as np

from experiments.theta_pencil.cut_adapted_prime_basis import (
    build_cut_adapted_prime_matrix,
    build_second_window_prime_matrix,
    build_third_window_prime_matrix,
    first_prime_partition,
    second_prime_partition,
    third_prime_partition,
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


def test_second_prime_partition_is_closed_under_both_translations():
    for half_width in (
        np.log(3.0) / 2.0 + 1e-6,
        0.56,
        0.65,
        np.log(2.0) - 1e-6,
    ):
        partition = second_prime_partition(half_width)
        for left, right in partition.prime_two_pairs:
            source = partition.intervals[left]
            target = partition.intervals[right]
            assert np.allclose(
                np.asarray(source) + partition.displacement_two, target
            )
        for left, right in partition.prime_three_pairs:
            source = partition.intervals[left]
            target = partition.intervals[right]
            assert np.allclose(
                np.asarray(source) + partition.displacement_three, target
            )
        lengths = np.array(
            [right - left for left, right in partition.intervals]
        )
        assert np.all(lengths > 0)
        assert np.allclose(lengths, lengths[::-1])
        assert np.isclose(lengths[0], lengths[2])
        assert np.isclose(lengths[0], lengths[4])
        assert np.isclose(lengths[0], lengths[6])


def test_second_window_prime_matrix_is_exact_translation_graph():
    result = build_second_window_prime_matrix(0.56, 3, 2, 1)
    assert result.matrix.shape == (17, 17)
    assert np.array_equal(result.matrix, result.matrix.T)
    assert np.max(np.abs(np.linalg.eigvalsh(result.matrix))) > 0

    coefficient_two = np.log(2.0) / np.sqrt(2.0)
    coefficient_three = np.log(3.0) / np.sqrt(3.0)
    offsets = result.offsets
    block_04 = result.matrix[offsets[0] : offsets[1], offsets[4] : offsets[5]]
    block_06 = result.matrix[offsets[0] : offsets[1], offsets[6] : offsets[7]]
    assert np.allclose(block_04, -coefficient_two * np.eye(3))
    assert np.allclose(block_06, -coefficient_three * np.eye(3))


def test_third_prime_partition_closes_all_prime_power_translations():
    partition = third_prime_partition(0.7)
    assert len(partition.intervals) == 13
    for displacement, pairs in (
        (partition.displacement_two, partition.prime_two_pairs),
        (partition.displacement_three, partition.prime_three_pairs),
        (partition.displacement_four, partition.prime_four_pairs),
    ):
        for left, right in pairs:
            assert np.allclose(
                np.asarray(partition.intervals[left]) + displacement,
                partition.intervals[right],
            )
    lengths = np.diff(
        [partition.intervals[0][0]]
        + [interval[1] for interval in partition.intervals]
    )
    assert np.all(lengths > 0)
    assert np.allclose(lengths, lengths[::-1])


def test_third_window_prime_matrix_uses_lambda_four_equals_log_two():
    result = build_third_window_prime_matrix(0.7, 2, 1, 1)
    offsets = result.offsets
    block = result.matrix[offsets[0] : offsets[1], offsets[12] : offsets[13]]
    assert np.allclose(block, -np.log(2.0) / 2.0 * np.eye(2))
