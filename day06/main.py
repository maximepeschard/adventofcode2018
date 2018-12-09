from common import root
from .coordinates import parse_coordinate, sizes


def run() -> None:
    with open(root / "day06" / "input.txt") as fin:
        coordinates = [parse_coordinate(line.strip()) for line in fin]
        result_part_1, result_part_2 = sizes(coordinates, 10000)
        print(result_part_1)
        print(result_part_2)
