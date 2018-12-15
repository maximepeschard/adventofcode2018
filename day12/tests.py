from common import Test, run_test_cases
from .plants import (
    SpreadRule,
    parse_initial_state,
    parse_rule,
    parse_notes,
    sum_planted_pots,
)


TEST_LINES = [
    "initial state: #..#.#..##......###...###",
    "",
    "...## => #",
    "..#.. => #",
    ".#... => #",
    ".#.#. => #",
    ".#.## => #",
    ".##.. => #",
    ".#### => #",
    "#.#.# => #",
    "#.### => #",
    "##.#. => #",
    "##.## => #",
    "###.. => #",
    "###.# => #",
    "####. => #",
]

TESTS = [
    Test(parse_initial_state, ("initial state: #..##....",), "#..##...."),
    Test(parse_initial_state, ("invalid initial state: #..##....",), None),
    Test(parse_rule, ("..#.. => .",), SpreadRule("..#..", False)),
    Test(parse_rule, (".##.# => #",), SpreadRule(".##.#", True)),
    Test(parse_rule, (".##.# <= #",), None),
    Test(
        parse_notes,
        (TEST_LINES[:4],),
        (
            {SpreadRule("...##", True), SpreadRule("..#..", True)},
            "#..#.#..##......###...###",
        ),
    ),
    Test(sum_planted_pots, parse_notes(TEST_LINES) + (20,), 325),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
