from common import Test, run_test_cases
from .marbles import parse_game_setup, highest_score


TESTS = [
    Test(
        parse_game_setup, ("10 players; last marble is worth 1618 points",), (10, 1618)
    ),
    Test(highest_score, (9, 25), 32),
    Test(highest_score, (10, 1618), 8317),
    Test(highest_score, (13, 7999), 146373),
    Test(highest_score, (17, 1104), 2764),
    Test(highest_score, (21, 6111), 54718),
    Test(highest_score, (30, 5807), 37305),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
