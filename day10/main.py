from common import root
from .stars import parse_point, message


def run() -> None:
    with open(root / "day10" / "input.txt") as fin:
        points = [parse_point(line.strip()) for line in fin]
        # Part 1 result is visual and printed by `message`
        result_part_2 = message(points)
        print(result_part_2)
