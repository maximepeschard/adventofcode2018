from common import Test, run_test_cases
from .license import make_tree, total_metadata, value


TEST_TREE_DESCRIPTION = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]

TESTS = [
    Test(total_metadata, (make_tree([0, 3, 8, 9, 10]),), 27),
    Test(total_metadata, (make_tree([1, 2, 0, 1, 10, 11, 12]),), 33),
    Test(total_metadata, (make_tree([2, 1, 0, 1, 10, 0, 1, 11, 12]),), 33),
    Test(
        total_metadata,
        (make_tree([2, 3, 1, 1, 0, 1, 99, 2, 0, 3, 10, 11, 12, 1, 1, 2]),),
        138,
    ),
    Test(total_metadata, (make_tree(TEST_TREE_DESCRIPTION),), 138),
    Test(value, (make_tree(TEST_TREE_DESCRIPTION),), 66),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
