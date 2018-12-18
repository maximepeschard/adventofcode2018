from common import Test, run_test_cases
from .chocolate import score_after, recipes_before


TESTS = [
    Test(score_after, (9, 10, (3, 7)), "5158916779"),
    Test(score_after, (5, 10, (3, 7)), "0124515891"),
    Test(score_after, (18, 10, (3, 7)), "9251071085"),
    Test(score_after, (2018, 10, (3, 7)), "5941429882"),
    Test(recipes_before, ("51589", (3, 7)), 9),
    Test(recipes_before, ("01245", (3, 7)), 5),
    Test(recipes_before, ("92510", (3, 7)), 18),
    Test(recipes_before, ("59414", (3, 7)), 2018),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
