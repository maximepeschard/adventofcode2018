from common import root
from .fabric import parse_claim, overlapping


def run() -> None:
    with open(root / "day03" / "input.txt") as fin:
        claims = [parse_claim(line.strip()) for line in fin]
        result_part_1, result_part_2 = overlapping(claims, 2)
        print(result_part_1)
        print(result_part_2)
