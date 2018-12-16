from common import Test, run_test_cases
from .carts import (
    Turn,
    Direction,
    next_turn,
    parse_map,
    first_crash_location,
    last_cart_location,
)


TEST_STRAIGHT_LINES = ["|", "v", "|", "|", "|", "^", "|"]

TEST_MAP_LINES_PART_1 = [
    "/->-\        ",
    "|   |  /----\\",
    "| /-+--+-\  |",
    "| | |  | v  |",
    "\-+-/  \-+--/",
    "  \------/   ",
]

TEST_MAP_LINES_PART_2 = [
    "/>-<\  ",
    "|   |  ",
    "| /<+-\\",
    "| | | v",
    "\>+</ |",
    "  |   ^",
    "  \<->/",
]

TESTS = [
    Test(next_turn, (Turn.LEFT,), Turn.STRAIGHT),
    Test(next_turn, (Turn.STRAIGHT,), Turn.RIGHT),
    Test(next_turn, (Turn.RIGHT,), Turn.LEFT),
    Test(Direction.UP.apply_turn, (Turn.LEFT,), Direction.LEFT),
    Test(Direction.UP.apply_turn, (Turn.STRAIGHT,), Direction.UP),
    Test(Direction.UP.apply_turn, (Turn.RIGHT,), Direction.RIGHT),
    Test(first_crash_location, parse_map(TEST_STRAIGHT_LINES), (0, 3)),
    Test(first_crash_location, parse_map(TEST_MAP_LINES_PART_1), (7, 3)),
    Test(last_cart_location, parse_map(TEST_MAP_LINES_PART_2), (6, 4)),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
