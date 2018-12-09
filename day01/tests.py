from common import Test, run_test_cases
from .calibration import final_frequency, first_frequency_twice


TESTS = [
    Test(final_frequency, ([+1, -2, +3, +1],), 3),
    Test(final_frequency, ([+1, +1, +1],), 3),
    Test(final_frequency, ([+1, +1, -2],), 0),
    Test(final_frequency, ([-1, -2, -3],), -6),
    Test(first_frequency_twice, ([+1, -2, +3, +1],), 2),
    Test(first_frequency_twice, ([+1, -1],), 0),
    Test(first_frequency_twice, ([+3, +3, +4, -2, -4],), 10),
    Test(first_frequency_twice, ([-6, +3, +8, +5, -6],), 5),
    Test(first_frequency_twice, ([+7, +7, -2, -7, -4],), 14),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
