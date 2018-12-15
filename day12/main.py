from common import root
from .plants import parse_notes, sum_planted_pots


def run() -> None:
    with open(root / "day12" / "input.txt") as fin:
        rules, init = parse_notes(fin.readlines())
    result_part_1 = sum_planted_pots(rules, init, 20)
    print(result_part_1)
    result_part_2 = sum_planted_pots(rules, init, 50000000000)
    print(result_part_2)
