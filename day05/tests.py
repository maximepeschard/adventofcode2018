from common import Test, run_test_cases
from .polymer import react, reduction, best_reduction


TESTS = [
    Test(react, ("a", "A"), True),
    Test(react, ("A", "a"), True),
    Test(react, ("a", "a"), False),
    Test(react, ("A", "A"), False),
    Test(react, ("a", "b"), False),
    Test(react, ("a", "B"), False),
    Test(reduction, ("aA",), 0),
    Test(reduction, ("abBA",), 0),
    Test(reduction, ("abAB",), 4),
    Test(reduction, ("aabAAB",), 6),
    Test(reduction, ("dabAcCaCBAcCcaDA",), 10),
    Test(reduction, ("dabAcCaCBAcCcaDA", {"a", "A"}), 6),
    Test(reduction, ("dabAcCaCBAcCcaDA", {"b", "B"}), 8),
    Test(reduction, ("dabAcCaCBAcCcaDA", {"c", "C"}), 4),
    Test(reduction, ("dabAcCaCBAcCcaDA", {"d", "D"}), 6),
    Test(best_reduction, ("dabAcCaCBAcCcaDA",), 4)
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
