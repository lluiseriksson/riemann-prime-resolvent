import math

from experiments.theta_pencil.support_window import (
    at_most_prime_three_boundary,
    in_first_prime_window,
    in_second_prime_window,
    prime_overlap_positive,
)


def test_rounded_log_three_boundary_is_classified_by_its_exact_decimal():
    rounded = math.log(3.0) / 2.0
    below = math.nextafter(rounded, -math.inf)
    assert not at_most_prime_three_boundary(rounded)
    assert not in_first_prime_window(rounded)
    assert in_second_prime_window(rounded)
    assert prime_overlap_positive(rounded, 3)
    assert at_most_prime_three_boundary(below)
    assert in_first_prime_window(below)
    assert not prime_overlap_positive(below, 3)
