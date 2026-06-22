from fractions import Fraction


def moment(weights, points, n):
    return sum((w * p**n for w, p in zip(weights, points, strict=True)), Fraction(0))


def difference(sequence, k, n):
    work = list(sequence)
    for _ in range(k):
        work = [work[i] - work[i + 1] for i in range(len(work) - 1)]
    return work[n]


def test_resolvent_atoms_are_hausdorff_completely_monotone():
    x0 = Fraction(1)
    spectrum = [Fraction(1), Fraction(4), Fraction(9)]
    weights = [1 / (x0 + lam) for lam in spectrum]
    points = [x0 / (x0 + lam) for lam in spectrum]
    seq = [moment(weights, points, n) for n in range(30)]
    for k in range(8):
        for n in range(8):
            assert difference(seq, k, n) >= 0


def test_exact_difference_identity():
    weights = [Fraction(2, 3), Fraction(3, 5)]
    points = [Fraction(1, 4), Fraction(2, 7)]
    seq = [moment(weights, points, n) for n in range(20)]
    for k in range(6):
        for n in range(6):
            rhs = sum(
                (w * p**n * (1 - p) ** k for w, p in zip(weights, points, strict=True)),
                Fraction(0),
            )
            assert difference(seq, k, n) == rhs
