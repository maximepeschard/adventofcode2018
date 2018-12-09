from common import Test, run_test_cases
from .coordinates import (
    Coordinate,
    Boundaries,
    parse_coordinate,
    manhattan_distance,
    find_boundaries,
    sizes,
)


TEST_COORDINATES = ["1, 1", "1, 6", "8, 3", "3, 4", "5, 5", "8, 9"]

TESTS = [
    Test(parse_coordinate, (TEST_COORDINATES[0],), Coordinate(1, 1)),
    Test(parse_coordinate, (TEST_COORDINATES[1],), Coordinate(1, 6)),
    Test(parse_coordinate, (TEST_COORDINATES[2],), Coordinate(8, 3)),
    Test(manhattan_distance, (Coordinate(0, 0), Coordinate(0, 3)), 3),
    Test(manhattan_distance, (Coordinate(0, 0), Coordinate(3, 0)), 3),
    Test(manhattan_distance, (Coordinate(0, 0), Coordinate(2, 3)), 5),
    Test(
        find_boundaries,
        ([parse_coordinate(c) for c in TEST_COORDINATES],),
        Boundaries(1, 9, 1, 8),
    ),
    Test(sizes, ([parse_coordinate(c) for c in TEST_COORDINATES], 32), (17, 16)),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
