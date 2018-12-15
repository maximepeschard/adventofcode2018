from common import Test, run_test_cases
from .charge import power_level, power_square


TESTS = [
    Test(power_level, (3, 5, 8), 4),
    Test(power_level, (122, 79, 57), -5),
    Test(power_level, (217, 196, 39), 0),
    Test(power_level, (101, 153, 71), 4),
    Test(power_square, (300, 18, 3), (33, 45, 3)),
    Test(power_square, (300, 42, 3), (21, 61, 3)),
    Test(power_square, (300, 18), (90, 269, 16)),
    Test(power_square, (300, 42), (232, 251, 12)),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
