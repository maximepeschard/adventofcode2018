from common import root
from .polymer import reduction, best_reduction


def run() -> None:
    with open(root / "day05" / "input.txt") as fin:
        polymer = fin.read().strip()
        result_part_1 = reduction(polymer)
        print(result_part_1)
        result_part_2 = best_reduction(polymer)
        print(result_part_2)
